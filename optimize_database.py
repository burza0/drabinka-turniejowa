#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv('DATABASE_URL')

def optimize_database():
    """Optymalizuje bazę danych - dodaje indeksy, usuwa duplikaty"""
    conn = psycopg2.connect(DB_URL)
    conn.autocommit = True  # Wymagane dla CREATE INDEX CONCURRENTLY
    cur = conn.cursor()

    print('🚀 OPTYMALIZACJA BAZY DANYCH')
    print('=' * 50)

    # 1. DODAWANIE INDEKSÓW
    print('\n📈 DODAWANIE INDEKSÓW...')
    
    indexes_to_create = [
        # Zawodnicy - często używane w WHERE i JOIN
        ("idx_zawodnicy_kategoria", "zawodnicy", "kategoria"),
        ("idx_zawodnicy_plec", "zawodnicy", "plec"), 
        ("idx_zawodnicy_klub", "zawodnicy", "klub"),
        ("idx_zawodnicy_checked_in", "zawodnicy", "checked_in"),
        
        # Wyniki - sortowanie i filtrowanie
        ("idx_wyniki_status", "wyniki", "status"),
        ("idx_wyniki_czas", "wyniki", "czas_przejazdu_s"),
        ("idx_wyniki_nr_startowy", "wyniki", "nr_startowy"),
        
        # Checkpoints - JOIN i filtrowanie
        ("idx_checkpoints_nr_startowy", "checkpoints", "nr_startowy"),
        ("idx_checkpoints_checkpoint_name", "checkpoints", "checkpoint_name"),
        ("idx_checkpoints_timestamp", "checkpoints", "timestamp"),
        ("idx_checkpoints_device_id", "checkpoints", "device_id"),
    ]
    
    for index_name, table, column in indexes_to_create:
        try:
            # Sprawdź czy indeks już istnieje
            cur.execute("""
                SELECT 1 FROM pg_indexes 
                WHERE indexname = %s
            """, (index_name,))
            
            if cur.fetchone():
                print(f"  ⏭️  {index_name} już istnieje")
                continue
            
            # Utwórz indeks bez CONCURRENTLY (szybsze dla małych tabel)
            cur.execute(f"CREATE INDEX {index_name} ON {table} ({column})")
            print(f"  ✅ Utworzono indeks: {index_name}")
            
        except Exception as e:
            print(f"  ❌ Błąd tworzenia indeksu {index_name}: {e}")

    # 2. COMPOSITE INDEXES dla często używanych kombinacji
    print('\n🔗 DODAWANIE INDEKSÓW COMPOSITE...')
    
    composite_indexes = [
        ("idx_zawodnicy_kategoria_plec", "zawodnicy", "kategoria, plec"),
        ("idx_wyniki_status_czas", "wyniki", "status, czas_przejazdu_s"),
        ("idx_checkpoints_name_timestamp", "checkpoints", "checkpoint_name, timestamp"),
    ]
    
    for index_name, table, columns in composite_indexes:
        try:
            cur.execute("""
                SELECT 1 FROM pg_indexes 
                WHERE indexname = %s
            """, (index_name,))
            
            if cur.fetchone():
                print(f"  ⏭️  {index_name} już istnieje")
                continue
            
            cur.execute(f"CREATE INDEX {index_name} ON {table} ({columns})")
            print(f"  ✅ Utworzono composite indeks: {index_name}")
            
        except Exception as e:
            print(f"  ❌ Błąd tworzenia composite indeksu {index_name}: {e}")

    # 3. USUWANIE DUPLIKATÓW (osobne połączenie dla transakcji)
    print('\n🧹 USUWANIE DUPLIKATÓW...')
    
    conn2 = psycopg2.connect(DB_URL)
    conn2.autocommit = False
    cur2 = conn2.cursor()
    
    try:
        # Znajdź duplikaty w checkpoints
        cur2.execute("""
            SELECT nr_startowy, checkpoint_name, COUNT(*), array_agg(id ORDER BY timestamp) as ids
            FROM checkpoints
            GROUP BY nr_startowy, checkpoint_name
            HAVING COUNT(*) > 1
        """)
        
        duplicates = cur2.fetchall()
        removed_duplicates = 0
        
        for nr, checkpoint, count, ids in duplicates:
            # Zostaw najnowszy rekord (ostatni), usuń resztę
            ids_to_remove = ids[:-1]  # Wszystkie oprócz ostatniego
            
            for id_to_remove in ids_to_remove:
                cur2.execute("DELETE FROM checkpoints WHERE id = %s", (id_to_remove,))
                removed_duplicates += 1
            
            print(f"  🗑️  Usunięto {len(ids_to_remove)} duplikatów dla Nr {nr}, {checkpoint}")
        
        if removed_duplicates == 0:
            print("  ✅ Brak duplikatów do usunięcia")
        else:
            print(f"  ✅ Usunięto łącznie {removed_duplicates} duplikatów")
            
        conn2.commit()
        
    except Exception as e:
        print(f"  ❌ Błąd usuwania duplikatów: {e}")
        conn2.rollback()
    finally:
        cur2.close()
        conn2.close()

    # 4. VACUUM i ANALYZE
    print('\n🔄 VACUUM i ANALYZE...')
    try:
        cur.execute("VACUUM ANALYZE zawodnicy")
        cur.execute("VACUUM ANALYZE wyniki") 
        cur.execute("VACUUM ANALYZE checkpoints")
        cur.execute("VACUUM ANALYZE kluby")
        print("  ✅ VACUUM ANALYZE wykonane")
    except Exception as e:
        print(f"  ❌ Błąd VACUUM: {e}")

    cur.close()
    conn.close()
    
    print('\n🎉 OPTYMALIZACJA ZAKOŃCZONA POMYŚLNIE!')

def show_optimization_results():
    """Pokazuje wyniki optymalizacji"""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    print('\n📊 WYNIKI OPTYMALIZACJI:')
    print('=' * 30)
    
    # Sprawdź liczbę indeksów
    cur.execute("""
        SELECT COUNT(*) FROM pg_indexes 
        WHERE schemaname = 'public'
    """)
    index_count = cur.fetchone()[0]
    print(f"Łączna liczba indeksów: {index_count}")
    
    # Sprawdź duplikaty po optymalizacji
    cur.execute("""
        SELECT COUNT(*) FROM (
            SELECT nr_startowy, checkpoint_name, COUNT(*)
            FROM checkpoints
            GROUP BY nr_startowy, checkpoint_name
            HAVING COUNT(*) > 1
        ) duplicates
    """)
    duplicate_count = cur.fetchone()[0]
    print(f"Pozostałe duplikaty: {duplicate_count}")
    
    # Test wydajności prostego zapytania
    import time
    start_time = time.time()
    
    cur.execute("""
        SELECT z.nr_startowy, z.imie, z.nazwisko, z.kategoria, z.plec, 
               w.czas_przejazdu_s, w.status
        FROM zawodnicy z
        LEFT JOIN wyniki w ON z.nr_startowy = w.nr_startowy
        WHERE z.kategoria = 'Junior A' AND z.plec = 'M'
        ORDER BY w.czas_przejazdu_s
        LIMIT 10
    """)
    
    end_time = time.time()
    query_time = (end_time - start_time) * 1000
    
    results = cur.fetchall()
    print(f"Test query (Junior A, M): {len(results)} wyników w {query_time:.2f}ms")
    
    # Sprawdź nowe indeksy
    cur.execute("""
        SELECT indexname FROM pg_indexes 
        WHERE schemaname = 'public' 
        AND indexname LIKE 'idx_%'
        ORDER BY indexname
    """)
    
    new_indexes = cur.fetchall()
    print(f"\nNowe indeksy ({len(new_indexes)}):")
    for idx in new_indexes:
        print(f"  • {idx[0]}")
    
    cur.close()
    conn.close()

if __name__ == '__main__':
    optimize_database()
    show_optimization_results() 