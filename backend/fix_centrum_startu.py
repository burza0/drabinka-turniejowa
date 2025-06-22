#!/usr/bin/env python3
"""
Skrypt naprawczy dla centrum startu
Sprawdza strukturę tabeli start_queue i ją poprawia
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

def fix_centrum_startu():
    """Naprawia strukturę centrum startu"""
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        print("🔧 Naprawa centrum startu...")
        
        # 1. Sprawdzenie struktury tabeli start_queue
        print("🔍 Sprawdzanie struktury tabeli start_queue...")
        try:
            cur.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'start_queue'
                ORDER BY ordinal_position
            """)
            columns = cur.fetchall()
            
            if columns:
                print("📋 Obecna struktura tabeli start_queue:")
                for col_name, col_type in columns:
                    print(f"  - {col_name}: {col_type}")
            else:
                print("❌ Tabela start_queue nie istnieje")
                
        except Exception as e:
            print(f"❌ Błąd sprawdzania struktury: {e}")
        
        # 2. Usunięcie starej tabeli i utworzenie nowej
        print("🗑️ Usuwanie starej tabeli start_queue...")
        cur.execute("DROP TABLE IF EXISTS start_queue CASCADE")
        
        print("📊 Tworzenie nowej tabeli start_queue...")
        cur.execute("""
            CREATE TABLE start_queue (
                id SERIAL PRIMARY KEY,
                kategoria VARCHAR(50) NOT NULL,
                plec CHAR(1) NOT NULL CHECK (plec IN ('M', 'K')),
                numer_grupy INTEGER NOT NULL,
                nazwa VARCHAR(100) NOT NULL,
                status VARCHAR(20) DEFAULT 'WAITING' CHECK (status IN ('WAITING', 'ACTIVE', 'FINISHED')),
                estimated_time TIMESTAMP NULL,
                created_at TIMESTAMP DEFAULT NOW(),
                UNIQUE(kategoria, plec)
            )
        """)
        
        # 3. Pobieranie kategorii zawodników z bazy
        print("🔍 Pobieranie kategorii zawodników...")
        cur.execute("""
            SELECT DISTINCT kategoria, plec, COUNT(*) as liczba
            FROM zawodnicy 
            WHERE kategoria IS NOT NULL AND plec IS NOT NULL
            GROUP BY kategoria, plec
            ORDER BY kategoria, plec
        """)
        
        kategorie = cur.fetchall()
        print(f"✅ Znaleziono {len(kategorie)} grup kategoriowych")
        
        # 4. Tworzenie grup startowych
        print("🏁 Tworzenie grup startowych...")
        numer_grupy = 1
        
        for kategoria, plec, liczba in kategorie:
            plec_nazwa = "Mężczyźni" if plec == "M" else "Kobiety"
            nazwa_grupy = f"{kategoria} {plec_nazwa}"
            
            cur.execute("""
                INSERT INTO start_queue (kategoria, plec, numer_grupy, nazwa, status)
                VALUES (%s, %s, %s, %s, 'WAITING')
            """, (kategoria, plec, numer_grupy, nazwa_grupy))
            
            print(f"  ✅ Grupa {numer_grupy}: {nazwa_grupy} ({liczba} zawodników)")
            numer_grupy += 1
        
        # 5. Aktualizacja tabeli zawodnicy
        print("👥 Aktualizacja tabeli zawodnicy...")
        try:
            cur.execute("""
                ALTER TABLE zawodnicy 
                ADD COLUMN IF NOT EXISTS checked_in BOOLEAN DEFAULT FALSE
            """)
            cur.execute("""
                ALTER TABLE zawodnicy 
                ADD COLUMN IF NOT EXISTS check_in_time TIMESTAMP NULL
            """)
            cur.execute("""
                ALTER TABLE zawodnicy 
                ADD COLUMN IF NOT EXISTS ostatni_skan TIMESTAMP NULL
            """)
            print("  ✅ Kolumny centrum startu dodane")
        except Exception as e:
            print(f"  ℹ️ Kolumny już istnieją: {e}")
        
        # 6. Zatwierdzenie zmian
        conn.commit()
        
        # 7. Sprawdzenie wyników
        cur.execute("SELECT COUNT(*) FROM start_queue")
        liczba_grup = cur.fetchone()[0]
        
        print(f"\n🎉 SUKCES!")
        print(f"✅ Utworzono {liczba_grup} grup startowych")
        print(f"✅ Tabela start_queue naprawiona")
        print(f"✅ Centrum startu gotowe")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Błąd naprawy: {e}")
        if 'conn' in locals():
            conn.rollback()

if __name__ == "__main__":
    fix_centrum_startu() 