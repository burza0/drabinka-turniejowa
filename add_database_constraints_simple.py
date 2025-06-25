#!/usr/bin/env python3
"""
🔒 SKATECROSS v36.1 - ADD DATABASE CONSTRAINTS (Simple Version)
Dodaje constraints bez CONCURRENTLY
"""

import sys
import os
from datetime import datetime

# Dodaj backend do path
sys.path.append('backend')

try:
    from utils.database import execute_query, get_all
    
    print("🔒 SKATECROSS v36.1 - DODAWANIE DATABASE CONSTRAINTS (SIMPLE)")
    print("=" * 60)
    print(f"🕒 Czas: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    constraints_added = 0
    
    # CONSTRAINT 1: Tylko jedna sesja 'active' jednocześnie
    print("1️⃣ Dodaję UNIQUE INDEX dla statusu 'active'...")
    try:
        execute_query("""
            CREATE UNIQUE INDEX idx_one_active_session 
            ON sectro_sessions (status) 
            WHERE status = 'active'
        """)
        print("   ✅ Index idx_one_active_session dodany")
        constraints_added += 1
    except Exception as e:
        if "already exists" in str(e).lower():
            print("   ℹ️ Index idx_one_active_session już istnieje")
        else:
            print(f"   ⚠️ Błąd: {str(e)}")
    
    # CONSTRAINT 2: Tylko jedna sesja 'timing' jednocześnie  
    print("2️⃣ Dodaję UNIQUE INDEX dla statusu 'timing'...")
    try:
        execute_query("""
            CREATE UNIQUE INDEX idx_one_timing_session 
            ON sectro_sessions (status) 
            WHERE status = 'timing'
        """)
        print("   ✅ Index idx_one_timing_session dodany")
        constraints_added += 1
    except Exception as e:
        if "already exists" in str(e).lower():
            print("   ℹ️ Index idx_one_timing_session już istnieje")
        else:
            print(f"   ⚠️ Błąd: {str(e)}")
    
    # CONSTRAINT 3: Unikalne pary (kategoria, plec) dla aktywnych sesji
    print("3️⃣ Dodaję UNIQUE INDEX dla aktywnych grup...")
    try:
        execute_query("""
            CREATE UNIQUE INDEX idx_unique_active_group 
            ON sectro_sessions (kategoria, plec) 
            WHERE status IN ('active', 'timing')
        """)
        print("   ✅ Index idx_unique_active_group dodany")
        constraints_added += 1
    except Exception as e:
        if "already exists" in str(e).lower():
            print("   ℹ️ Index idx_unique_active_group już istnieje")
        else:
            print(f"   ⚠️ Błąd: {str(e)}")
    
    print(f"\n📈 DODANO {constraints_added} nowych constraints/indexes")
    
    # Sprawdź wszystkie indeksy związane z naszą tabelą
    print("\n🔍 WERYFIKACJA INDEXES:")
    print("-" * 40)
    
    indexes = get_all("""
        SELECT 
            indexname,
            indexdef
        FROM pg_indexes 
        WHERE tablename = 'sectro_sessions'
        AND (indexname LIKE '%active%' OR indexname LIKE '%timing%' OR indexname LIKE '%group%')
        ORDER BY indexname
    """)
    
    if indexes:
        print("📋 Aktywne indeksy zabezpieczające:")
        for idx in indexes:
            print(f"   🔗 {idx['indexname']}")
    else:
        print("⚠️ Brak indeksów zabezpieczających")
    
    print(f"\n✅ Zakończono: {datetime.now().strftime('%H:%M:%S')}")
    
except Exception as e:
    print(f"❌ BŁĄD podczas dodawania constraints: {str(e)}")
    sys.exit(1) 