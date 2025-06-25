#!/usr/bin/env python3
"""
💾 SKATECROSS v36.1 - BACKUP PRODUCTION DATA
Backup krytycznych tabel przed cleanup bazy danych
"""

import sys
import os
from datetime import datetime

# Dodaj backend do path
sys.path.append('backend')

try:
    from utils.database import execute_query, get_all
    
    backup_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    print("💾 SKATECROSS v36.1 - BACKUP PRODUCTION DATA")
    print("=" * 60)
    print(f"🕒 Czas: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📅 Backup ID: {backup_timestamp}")
    print()
    
    print("🔄 TWORZENIE BACKUP TABEL...")
    print("-" * 40)
    
    # Lista tabel do backup
    backup_tables = [
        'sectro_sessions',
        'sectro_results', 
        'sectro_measurements',
        'sectro_logs',
        'start_queue',
        'kolejki_startowe',
        'unified_start_queue',
        'aktywna_grupa_settings'
    ]
    
    backup_count = 0
    
    for table in backup_tables:
        try:
            backup_table_name = f"{table}_backup_{backup_timestamp}"
            
            # Sprawdź czy tabela istnieje
            check_query = f"""
                SELECT COUNT(*) as count 
                FROM information_schema.tables 
                WHERE table_name = '{table}'
            """
            result = get_all(check_query)
            
            if result and result[0]['count'] > 0:
                # Sprawdź ile rekordów w oryginalnej tabeli
                count_result = get_all(f"SELECT COUNT(*) as count FROM {table}")
                row_count = count_result[0]['count'] if count_result else 0
                
                # Utwórz backup
                backup_query = f"CREATE TABLE {backup_table_name} AS SELECT * FROM {table}"
                execute_query(backup_query)
                
                print(f"✅ {table} → {backup_table_name} ({row_count} rekordów)")
                backup_count += 1
            else:
                print(f"⚠️  {table} - tabela nie istnieje, pomijam")
                
        except Exception as e:
            print(f"❌ BŁĄD backup {table}: {str(e)[:60]}...")
    
    print(f"\n🎯 BACKUP SUMMARY:")
    print(f"   ✅ Utworzono {backup_count} tabel backup")
    print(f"   📅 Suffix: _backup_{backup_timestamp}")
    
    # Sprawdź utworzone backupy
    print(f"\n🔍 WERYFIKACJA BACKUP:")
    print("-" * 40)
    
    backup_verification_query = f"""
        SELECT table_name, 
               (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = t.table_name) as columns
        FROM information_schema.tables t
        WHERE table_name LIKE '%backup_{backup_timestamp}'
        ORDER BY table_name
    """
    
    backups = get_all(backup_verification_query)
    for backup in backups:
        table_name = backup['table_name']
        columns = backup['columns']
        
        # Policz rekordy w backup
        count_result = get_all(f"SELECT COUNT(*) as count FROM {table_name}")
        row_count = count_result[0]['count'] if count_result else 0
        
        print(f"✅ {table_name}: {row_count} rekordów, {columns} kolumn")
    
    print(f"\n📋 INFORMACJE O RESTORE:")
    print("-" * 40)
    print("W przypadku potrzeby przywrócenia danych:")
    print("1. Usuń aktualne tabele: DROP TABLE nazwa_tabeli;")
    print("2. Przywróć z backup: ALTER TABLE nazwa_tabeli_backup_TIMESTAMP RENAME TO nazwa_tabeli;")
    print(f"3. Timestamp tego backup: {backup_timestamp}")
    
    print(f"\n💾 BACKUP ZAKOŃCZONY: {datetime.now().strftime('%H:%M:%S')}")
    
except Exception as e:
    print(f"❌ BŁĄD podczas backup: {str(e)}")
    sys.exit(1) 