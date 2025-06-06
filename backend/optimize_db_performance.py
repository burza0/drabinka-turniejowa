#!/usr/bin/env python3
"""
SKRYPT OPTYMALIZACJI BAZY DANYCH - v30.5.4
Dodaje indeksy PostgreSQL dla poprawy wydajności API
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def optimize_database():
    """Dodaje kluczowe indeksy dla poprawy wydajności"""
    
    DB_URL = os.getenv("DATABASE_URL")
    
    # Indeksy do utworzenia
    indexes = [
        # PRIMARY INDEXES - najważniejsze dla JOIN'ów
        ("idx_zawodnicy_nr_startowy", "CREATE INDEX IF NOT EXISTS idx_zawodnicy_nr_startowy ON zawodnicy(nr_startowy)"),
        ("idx_wyniki_nr_startowy", "CREATE INDEX IF NOT EXISTS idx_wyniki_nr_startowy ON wyniki(nr_startowy)"),
        
        # FILTER INDEXES - dla filtrowania
        ("idx_zawodnicy_kategoria", "CREATE INDEX IF NOT EXISTS idx_zawodnicy_kategoria ON zawodnicy(kategoria)"),
        ("idx_zawodnicy_klub", "CREATE INDEX IF NOT EXISTS idx_zawodnicy_klub ON zawodnicy(klub)"),
        ("idx_zawodnicy_plec", "CREATE INDEX IF NOT EXISTS idx_zawodnicy_plec ON zawodnicy(plec)"),
        ("idx_zawodnicy_qr_code", "CREATE INDEX IF NOT EXISTS idx_zawodnicy_qr_code ON zawodnicy(qr_code) WHERE qr_code IS NOT NULL"),
        
        # SORT INDEXES - dla sortowania
        ("idx_wyniki_czas", "CREATE INDEX IF NOT EXISTS idx_wyniki_czas ON wyniki(czas_przejazdu_s) WHERE czas_przejazdu_s IS NOT NULL"),
        ("idx_wyniki_status", "CREATE INDEX IF NOT EXISTS idx_wyniki_status ON wyniki(status)"),
        
        # COMPOSITE INDEXES - dla złożonych zapytań
        ("idx_zawodnicy_kategoria_plec", "CREATE INDEX IF NOT EXISTS idx_zawodnicy_kategoria_plec ON zawodnicy(kategoria, plec)"),
        ("idx_wyniki_status_czas", "CREATE INDEX IF NOT EXISTS idx_wyniki_status_czas ON wyniki(status, czas_przejazdu_s)"),
    ]
    
    conn = None
    try:
        print("🔧 Łączenie z bazą danych...")
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        print("📊 Sprawdzanie istniejących indeksów...")
        cur.execute("""
            SELECT indexname, tablename 
            FROM pg_indexes 
            WHERE tablename IN ('zawodnicy', 'wyniki')
            ORDER BY tablename, indexname
        """)
        existing_indexes = cur.fetchall()
        
        print(f"✅ Znaleziono {len(existing_indexes)} istniejących indeksów:")
        for idx_name, table_name in existing_indexes:
            print(f"  - {table_name}.{idx_name}")
        
        print("\n🚀 Tworzenie nowych indeksów...")
        
        created_count = 0
        for idx_name, sql in indexes:
            try:
                print(f"📝 Tworzenie indeksu: {idx_name}...")
                cur.execute(sql)
                conn.commit()
                print(f"✅ {idx_name} - OK")
                created_count += 1
            except psycopg2.Error as e:
                if "already exists" in str(e):
                    print(f"ℹ️ {idx_name} - już istnieje")
                else:
                    print(f"❌ {idx_name} - błąd: {e}")
                conn.rollback()
        
        print(f"\n🎉 OPTYMALIZACJA ZAKOŃCZONA!")
        print(f"📈 Utworzono {created_count} nowych indeksów")
        
        # Analiza tabeli po utworzeniu indeksów
        print("\n📊 Uruchamianie ANALYZE dla odświeżenia statystyk...")
        cur.execute("ANALYZE zawodnicy")
        cur.execute("ANALYZE wyniki")
        conn.commit()
        print("✅ ANALYZE zakończone")
        
        # Sprawdzenie końcowej liczby indeksów
        cur.execute("""
            SELECT COUNT(*) 
            FROM pg_indexes 
            WHERE tablename IN ('zawodnicy', 'wyniki')
        """)
        final_count = cur.fetchone()[0]
        print(f"📈 Łączna liczba indeksów: {final_count}")
        
    except Exception as e:
        print(f"❌ BŁĄD OPTYMALIZACJI: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    optimize_database() 