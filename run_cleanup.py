#!/usr/bin/env python3
"""
🧹 SKATECROSS v36.1 - RUN DATABASE CLEANUP
Bezpieczne uruchomienie cleanup SQL w środowisku Python
"""

import sys
import os
from datetime import datetime

# Dodaj backend do path
sys.path.append('backend')

try:
    from utils.database import execute_query, get_all
    
    print("🧹 SKATECROSS v36.1 - DATABASE CLEANUP")
    print("=" * 60)
    print(f"🕒 Czas: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # FAZA 1: STAN PRZED CLEANUP
    print("📊 STAN PRZED CLEANUP:")
    print("-" * 40)
    
    result = get_all("SELECT COUNT(*) as count FROM sectro_sessions WHERE status = 'active'")
    active_before = result[0]['count'] if result else 0
    print(f"🔴 Aktywne sesje PRZED: {active_before}")
    
    result = get_all("SELECT COUNT(*) as count FROM sectro_sessions WHERE nazwa IN ('a', 'e', 't', 'y')")
    smieciowe_before = result[0]['count'] if result else 0
    print(f"🗑️ Sesje śmieciowe PRZED: {smieciowe_before}")
    
    print("\n🔄 ROZPOCZYNAM CLEANUP...")
    print("-" * 40)
    
    # FAZA 2: CLEANUP SECTRO_SESSIONS
    print("1️⃣ Anulowanie sesji bez kategoria/plec...")
    rows_affected = execute_query("""
        UPDATE sectro_sessions 
        SET status = 'cancelled', end_time = CURRENT_TIMESTAMP
        WHERE (kategoria IS NULL OR kategoria = '' OR plec IS NULL OR plec = '')
        AND status = 'active'
    """)
    print(f"   ✅ Anulowano {rows_affected} sesji śmieciowych")
    
    print("2️⃣ Anulowanie starych sesji aktywnych (>7 dni)...")
    rows_affected = execute_query("""
        UPDATE sectro_sessions 
        SET status = 'cancelled', end_time = CURRENT_TIMESTAMP
        WHERE status = 'active' 
        AND created_at < CURRENT_TIMESTAMP - INTERVAL '7 days'
    """)
    print(f"   ✅ Anulowano {rows_affected} starych sesji")
    
    print("3️⃣ Zachowywanie tylko najnowszych sesji dla grup...")
    # Najpierw znajdź duplikaty
    duplicates = get_all("""
        SELECT kategoria, plec, COUNT(*) as count
        FROM sectro_sessions 
        WHERE status = 'active' 
        AND kategoria IS NOT NULL 
        AND plec IS NOT NULL
        GROUP BY kategoria, plec
        HAVING COUNT(*) > 1
    """)
    
    if duplicates:
        print(f"   🔍 Znaleziono {len(duplicates)} grup z duplikatami:")
        for dup in duplicates:
            print(f"      - {dup['kategoria']}-{dup['plec']}: {dup['count']} sesji")
        
        # Anuluj starsze duplikaty
        rows_affected = execute_query("""
            WITH latest_sessions AS (
                SELECT kategoria, plec, MAX(created_at) as latest_date
                FROM sectro_sessions 
                WHERE status = 'active' 
                AND kategoria IS NOT NULL 
                AND plec IS NOT NULL
                GROUP BY kategoria, plec
            )
            UPDATE sectro_sessions 
            SET status = 'cancelled', end_time = CURRENT_TIMESTAMP
            WHERE status = 'active' 
            AND kategoria IS NOT NULL 
            AND plec IS NOT NULL
            AND NOT EXISTS (
                SELECT 1 FROM latest_sessions ls 
                WHERE ls.kategoria = sectro_sessions.kategoria 
                AND ls.plec = sectro_sessions.plec 
                AND ls.latest_date = sectro_sessions.created_at
            )
        """)
        print(f"   ✅ Anulowano {rows_affected} starszych duplikatów")
    else:
        print("   ✅ Brak duplikatów do usunięcia")
    
    # FAZA 3: LEGACY TABELE
    print("\n4️⃣ Czyszczenie legacy tabel...")
    
    legacy_tables = ['start_queue', 'unified_start_queue', 'kolejki_startowe', 'aktywna_grupa_settings']
    for table in legacy_tables:
        try:
            rows_affected = execute_query(f"TRUNCATE TABLE {table}")
            print(f"   ✅ Wyczyszczono {table}")
        except Exception as e:
            print(f"   ⚠️ {table}: {str(e)[:50]}...")
    
    # FAZA 4: SECTRO_RESULTS CLEANUP
    print("\n5️⃣ Usuwanie wyników z anulowanych sesji...")
    
    # Sectro results
    rows_affected = execute_query("""
        DELETE FROM sectro_results 
        WHERE session_id IN (
            SELECT id FROM sectro_sessions WHERE status = 'cancelled'
        )
    """)
    print(f"   ✅ Usunięto {rows_affected} wyników z anulowanych sesji")
    
    # Sectro measurements
    rows_affected = execute_query("""
        DELETE FROM sectro_measurements 
        WHERE session_id IN (
            SELECT id FROM sectro_sessions WHERE status = 'cancelled'
        )
    """)
    print(f"   ✅ Usunięto {rows_affected} pomiarów z anulowanych sesji")
    
    # Sectro logs
    rows_affected = execute_query("""
        DELETE FROM sectro_logs 
        WHERE session_id IN (
            SELECT id FROM sectro_sessions WHERE status = 'cancelled'
        )
    """)
    print(f"   ✅ Usunięto {rows_affected} logów z anulowanych sesji")
    
    # FAZA 5: WERYFIKACJA PO CLEANUP
    print("\n📊 STAN PO CLEANUP:")
    print("-" * 40)
    
    result = get_all("SELECT COUNT(*) as count FROM sectro_sessions WHERE status = 'active'")
    active_after = result[0]['count'] if result else 0
    print(f"🟢 Aktywne sesje PO: {active_after}")
    
    result = get_all("SELECT COUNT(*) as count FROM sectro_sessions WHERE nazwa IN ('a', 'e', 't', 'y') AND status = 'active'")
    smieciowe_after = result[0]['count'] if result else 0
    print(f"🗑️ Sesje śmieciowe aktywne PO: {smieciowe_after}")
    
    # Sprawdź pozostałe aktywne sesje
    active_sessions = get_all("""
        SELECT id, nazwa, kategoria, plec, status, created_at 
        FROM sectro_sessions 
        WHERE status IN ('active', 'timing')
        ORDER BY created_at DESC
    """)
    
    print(f"\n🎯 POZOSTAŁE AKTYWNE SESJE ({len(active_sessions)}):")
    for session in active_sessions:
        print(f"   - ID:{session['id']} | '{session['nazwa']}' | {session['kategoria']}-{session['plec']} | {session['status']}")
    
    # Statystyki końcowe
    print(f"\n📈 PODSUMOWANIE CLEANUP:")
    print(f"   🔴 Aktywne sesje: {active_before} → {active_after}")
    print(f"   🗑️ Sesje śmieciowe aktywne: {smieciowe_before} → {smieciowe_after}")
    
    if active_after <= 1 and smieciowe_after == 0:
        print("   ✅ CLEANUP SUKCES - baza oczyszczona!")
    else:
        print("   ⚠️ CLEANUP CZĘŚCIOWY - sprawdź pozostałe problemy")
    
    print(f"\n🧹 CLEANUP ZAKOŃCZONY: {datetime.now().strftime('%H:%M:%S')}")
    
except Exception as e:
    print(f"❌ BŁĄD podczas cleanup: {str(e)}")
    print("\n🔄 W razie problemów przywróć backup:")
    print("   ALTER TABLE sectro_sessions_backup_20250624_165845 RENAME TO sectro_sessions;")
    sys.exit(1) 