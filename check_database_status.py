#!/usr/bin/env python3
"""
🔍 SKATECROSS v36.1 - DATABASE STATUS CHECK
Sprawdzenie stanu bazy danych przed rozpoczęciem cleanup
"""

import sys
import os
from datetime import datetime

# Dodaj backend do path
sys.path.append('backend')

try:
    from utils.database import get_all, execute_query
    
    print("🔍 SKATECROSS v36.1 - ANALIZA BAZY DANYCH")
    print("=" * 60)
    print(f"🕒 Czas: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    print("📊 SEKCJA 1: SECTRO SESSIONS")
    print("-" * 40)
    
    # Sprawdź aktywne sesje
    result = get_all("SELECT COUNT(*) as count FROM sectro_sessions WHERE status = 'active'")
    active_count = result[0]['count'] if result else 0
    print(f"🚨 Aktywne sesje SECTRO: {active_count}")
    
    if active_count > 1:
        print("   ⚠️  PROBLEM: Więcej niż 1 aktywna sesja!")
    elif active_count == 1:
        print("   ✅ OK: Dokładnie 1 aktywna sesja")
    else:
        print("   ℹ️  INFO: Brak aktywnych sesji")
    
    # Sprawdź wszystkie sesje
    result = get_all("""
        SELECT status, COUNT(*) as count 
        FROM sectro_sessions 
        GROUP BY status 
        ORDER BY count DESC
    """)
    print("\n📈 Sesje wg statusu:")
    for row in result:
        print(f"   - {row['status']}: {row['count']} sesji")
    
    # Sprawdź śmieciowe sesje
    result = get_all("""
        SELECT id, nazwa, status, kategoria, plec, created_at 
        FROM sectro_sessions 
        WHERE nazwa IN ('a', 'e', 't', 'y') OR kategoria IS NULL OR plec IS NULL
        ORDER BY created_at DESC
    """)
    print(f"\n🗑️ Sesje śmieciowe/niepełne: {len(result)}")
    for row in result:
        print(f"   - ID:{row['id']} | '{row['nazwa']}' | {row['status']} | {row['kategoria']}-{row['plec']} | {row['created_at']}")
    
    print("\n📊 SEKCJA 2: LEGACY TABELE")
    print("-" * 40)
    
    legacy_tables = ['start_queue', 'kolejki_startowe', 'unified_start_queue', 'aktywna_grupa_settings']
    for table in legacy_tables:
        try:
            result = get_all(f"SELECT COUNT(*) as count FROM {table}")
            count = result[0]['count'] if result else 0
            print(f"🗑️ {table}: {count} rekordów")
        except Exception as e:
            print(f"❌ {table}: BŁĄD - {str(e)[:50]}...")
    
    print("\n📊 SEKCJA 3: STATYSTYKI OGÓLNE")
    print("-" * 40)
    
    # Zawodnicy
    result = get_all("SELECT COUNT(*) as count FROM zawodnicy")
    zawodnicy_count = result[0]['count'] if result else 0
    print(f"👥 Zawodnicy: {zawodnicy_count}")
    
    # Checked in
    result = get_all("SELECT COUNT(*) as count FROM zawodnicy WHERE checked_in = true")
    checked_in_count = result[0]['count'] if result else 0
    print(f"✅ Zameldowani: {checked_in_count}")
    
    # Wyniki
    result = get_all("SELECT COUNT(*) as count FROM wyniki")
    wyniki_count = result[0]['count'] if result else 0
    print(f"🏁 Wyniki: {wyniki_count}")
    
    # SECTRO results
    result = get_all("SELECT COUNT(*) as count FROM sectro_results")
    sectro_results_count = result[0]['count'] if result else 0
    print(f"⏱️ SECTRO results: {sectro_results_count}")
    
    print("\n🎯 REKOMENDACJE:")
    print("-" * 40)
    
    if active_count > 1:
        print("🚨 KRYTYCZNE: Wymagany cleanup aktywnych sesji!")
        print("   Uruchom: CLEANUP_DATABASE_SCRIPT.sql")
    
    # Sprawdź czy istnieją śmieciowe sesje
    result = get_all("""
        SELECT COUNT(*) as count FROM sectro_sessions 
        WHERE nazwa IN ('a', 'e', 't', 'y') OR kategoria IS NULL OR plec IS NULL
    """)
    smieciowe_count = result[0]['count'] if result else 0
    
    if smieciowe_count > 0:
        print("🗑️ WYMAGANE: Cleanup śmieciowych sesji")
    
    # Sprawdź legacy tabele
    legacy_total = 0
    for table in legacy_tables:
        try:
            result = get_all(f"SELECT COUNT(*) as count FROM {table}")
            legacy_total += result[0]['count'] if result else 0
        except:
            pass
    
    if legacy_total > 0:
        print("📋 ZALECANE: Usunięcie legacy tabel")
    
    if active_count <= 1 and smieciowe_count == 0 and legacy_total == 0:
        print("✅ BAZA W DOBREJ KONDYCJI - można pominąć cleanup")
    
    print(f"\n✅ Analiza zakończona: {datetime.now().strftime('%H:%M:%S')}")
    
except Exception as e:
    print(f"❌ BŁĄD podczas analizy: {str(e)}")
    sys.exit(1) 