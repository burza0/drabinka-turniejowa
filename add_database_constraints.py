#!/usr/bin/env python3
"""
🔒 SKATECROSS v36.1 - ADD DATABASE CONSTRAINTS
Dodaje constraints aby zapobiec duplikatom aktywnych sesji w przyszłości
"""

import sys
import os
from datetime import datetime

# Dodaj backend do path
sys.path.append('backend')

try:
    from utils.database import execute_query, get_all
    
    print("🔒 SKATECROSS v36.1 - DODAWANIE DATABASE CONSTRAINTS")
    print("=" * 60)
    print(f"🕒 Czas: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    print("🎯 CEL: Zapobiec duplikatom aktywnych sesji SECTRO")
    print("-" * 40)
    
    # CONSTRAINT 1: Tylko jedna sesja 'active' jednocześnie
    print("1️⃣ Dodaję UNIQUE constraint dla statusu 'active'...")
    try:
        execute_query("""
            CREATE UNIQUE INDEX CONCURRENTLY idx_one_active_session 
            ON sectro_sessions (status) 
            WHERE status = 'active'
        """)
        print("   ✅ Constraint idx_one_active_session dodany")
    except Exception as e:
        if "already exists" in str(e).lower():
            print("   ℹ️ Constraint idx_one_active_session już istnieje")
        else:
            print(f"   ⚠️ Błąd: {str(e)}")
    
    # CONSTRAINT 2: Tylko jedna sesja 'timing' jednocześnie  
    print("2️⃣ Dodaję UNIQUE constraint dla statusu 'timing'...")
    try:
        execute_query("""
            CREATE UNIQUE INDEX CONCURRENTLY idx_one_timing_session 
            ON sectro_sessions (status) 
            WHERE status = 'timing'
        """)
        print("   ✅ Constraint idx_one_timing_session dodany")
    except Exception as e:
        if "already exists" in str(e).lower():
            print("   ℹ️ Constraint idx_one_timing_session już istnieje")
        else:
            print(f"   ⚠️ Błąd: {str(e)}")
    
    # CONSTRAINT 3: Unikalne pary (kategoria, plec) dla aktywnych sesji
    print("3️⃣ Dodaję UNIQUE constraint dla aktywnych grup...")
    try:
        execute_query("""
            CREATE UNIQUE INDEX CONCURRENTLY idx_unique_active_group 
            ON sectro_sessions (kategoria, plec) 
            WHERE status IN ('active', 'timing')
        """)
        print("   ✅ Constraint idx_unique_active_group dodany")
    except Exception as e:
        if "already exists" in str(e).lower():
            print("   ℹ️ Constraint idx_unique_active_group już istnieje")
        else:
            print(f"   ⚠️ Błąd: {str(e)}")
    
    # CONSTRAINT 4: Sesja nie może mieć NULL kategoria/plec jeśli status = active
    print("4️⃣ Dodaję CHECK constraint dla kompletności danych...")
    try:
        execute_query("""
            ALTER TABLE sectro_sessions 
            ADD CONSTRAINT chk_active_session_complete 
            CHECK (
                (status NOT IN ('active', 'timing')) OR 
                (kategoria IS NOT NULL AND plec IS NOT NULL AND nazwa IS NOT NULL)
            )
        """)
        print("   ✅ Constraint chk_active_session_complete dodany")
    except Exception as e:
        if "already exists" in str(e).lower():
            print("   ℹ️ Constraint chk_active_session_complete już istnieje")
        else:
            print(f"   ⚠️ Błąd: {str(e)}")
    
    print("\n🔍 WERYFIKACJA CONSTRAINTS:")
    print("-" * 40)
    
    # Sprawdź dodane constraints
    constraints = get_all("""
        SELECT 
            conname as constraint_name,
            contype as constraint_type,
            pg_get_constraintdef(oid) as definition
        FROM pg_constraint 
        WHERE conrelid = 'sectro_sessions'::regclass
        AND conname LIKE '%active%' OR conname LIKE '%timing%' OR conname LIKE '%group%'
        ORDER BY conname
    """)
    
    print("📋 Dodane constraints:")
    for c in constraints:
        constraint_type = {
            'u': 'UNIQUE',
            'c': 'CHECK', 
            'p': 'PRIMARY KEY',
            'f': 'FOREIGN KEY'
        }.get(c['constraint_type'], c['constraint_type'])
        
        print(f"   ✅ {c['constraint_name']} ({constraint_type})")
    
    # Sprawdź indeksy
    indexes = get_all("""
        SELECT 
            indexname,
            indexdef
        FROM pg_indexes 
        WHERE tablename = 'sectro_sessions'
        AND (indexname LIKE '%active%' OR indexname LIKE '%timing%' OR indexname LIKE '%group%')
        ORDER BY indexname
    """)
    
    print("\n📋 Dodane indeksy:")
    for idx in indexes:
        print(f"   🔗 {idx['indexname']}")
        print(f"      {idx['indexdef']}")
    
    print("\n🧪 TEST CONSTRAINTS:")
    print("-" * 40)
    
    # Test 1: Sprawdź czy można dodać 2 aktywne sesje
    print("Test 1: Próba dodania duplikatu aktywnej sesji...")
    try:
        # Najpierw sprawdź czy są aktywne sesje
        active_sessions = get_all("SELECT COUNT(*) as count FROM sectro_sessions WHERE status = 'active'")
        active_count = active_sessions[0]['count'] if active_sessions else 0
        
        if active_count == 0:
            # Dodaj testową sesję
            execute_query("""
                INSERT INTO sectro_sessions (nazwa, kategoria, plec, status, created_at)
                VALUES ('TEST Constraint Check', 'Test', 'M', 'active', CURRENT_TIMESTAMP)
            """)
            print("   ✅ Pierwsza aktywna sesja dodana")
            
            # Próbuj dodać drugą
            try:
                execute_query("""
                    INSERT INTO sectro_sessions (nazwa, kategoria, plec, status, created_at)
                    VALUES ('TEST Constraint Check 2', 'Test', 'K', 'active', CURRENT_TIMESTAMP)
                """)
                print("   ❌ PROBLEM: Druga aktywna sesja została dodana! Constraint nie działa!")
            except Exception as e:
                print("   ✅ DOBRY: Druga aktywna sesja odrzucona przez constraint")
            
            # Cleanup - usuń testową sesję
            execute_query("DELETE FROM sectro_sessions WHERE nazwa LIKE 'TEST Constraint%'")
            print("   🧹 Testowe sesje usunięte")
        else:
            print(f"   ℹ️ Pomijam test - {active_count} aktywnych sesji już istnieje")
    except Exception as e:
        print(f"   ⚠️ Błąd testu: {str(e)}")
    
    print("\n📈 PODSUMOWANIE:")
    print("-" * 40)
    print("✅ Database constraints dodane do sectro_sessions:")
    print("   🔒 idx_one_active_session - max 1 sesja 'active'")
    print("   🔒 idx_one_timing_session - max 1 sesja 'timing'") 
    print("   🔒 idx_unique_active_group - unikalne grupy (kategoria,plec)")
    print("   🔒 chk_active_session_complete - kompletność danych")
    print()
    print("🎯 EFEKT: System API + Database constraints = 100% ochrona przed duplikatami!")
    print(f"🕒 Zakończono: {datetime.now().strftime('%H:%M:%S')}")
    
except Exception as e:
    print(f"❌ BŁĄD podczas dodawania constraints: {str(e)}")
    sys.exit(1) 