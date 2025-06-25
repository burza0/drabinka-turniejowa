#!/usr/bin/env python3
"""
Skrypt inicjalizacji danych centrum startu
Tworzy tabele start_queue i wypełnia ją grupami startowymi na podstawie kategorii zawodników
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

def init_centrum_startu():
    """Inicjalizuje dane centrum startu"""
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        print("🚀 Inicjalizacja centrum startu...")
        
        # 1. Tworzenie tabeli start_queue jeśli nie istnieje
        print("📊 Tworzenie tabeli start_queue...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS start_queue (
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
        
        # 2. Czyszczenie istniejących danych
        print("🧹 Czyszczenie starych danych...")
        cur.execute("DELETE FROM start_queue")
        
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
        
        # 5. Dodanie kolumn do tabeli zawodnicy jeśli nie istnieją
        print("👥 Aktualizacja tabeli zawodnicy...")
        try:
            cur.execute("""
                ALTER TABLE zawodnicy 
                ADD COLUMN IF NOT EXISTS checked_in BOOLEAN DEFAULT FALSE,
                ADD COLUMN IF NOT EXISTS check_in_time TIMESTAMP NULL,
                ADD COLUMN IF NOT EXISTS ostatni_skan TIMESTAMP NULL
            """)
            print("  ✅ Kolumny centrum startu dodane do tabeli zawodnicy")
        except Exception as e:
            print(f"  ℹ️ Kolumny już istnieją lub błąd: {e}")
        
        # 6. Zatwierdzenie zmian
        conn.commit()
        
        # 7. Sprawdzenie wyników
        cur.execute("SELECT COUNT(*) FROM start_queue")
        liczba_grup = cur.fetchone()[0]
        
        print(f"\n🎉 SUKCES!")
        print(f"✅ Utworzono {liczba_grup} grup startowych")
        print(f"✅ Tabela start_queue gotowa")
        print(f"✅ Centrum startu skonfigurowane")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Błąd inicjalizacji: {e}")
        if 'conn' in locals():
            conn.rollback()

if __name__ == "__main__":
    init_centrum_startu() 