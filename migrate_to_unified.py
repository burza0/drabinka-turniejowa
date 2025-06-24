#!/usr/bin/env python3
"""
SKATECROSS UNIFIED START CONTROL - Data Migration
Migracja danych z centrum_startu + sectro do unified system
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from utils.database import get_db_connection
import json
from datetime import datetime

def backup_existing_data():
    """Backup istniejących danych przed migracją"""
    print("📦 Tworzenie backup danych...")
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Backup aktywnej grupy settings
    cur.execute("SELECT * FROM aktywna_grupa_settings")
    aktywna_grupa = cur.fetchall()
    
    # Backup sesji SECTRO
    cur.execute("SELECT * FROM sectro_sessions ORDER BY created_at DESC LIMIT 10")
    sectro_sessions = cur.fetchall()
    
    # Backup wyników SECTRO  
    cur.execute("SELECT * FROM sectro_results ORDER BY created_at DESC LIMIT 50")
    sectro_results = cur.fetchall()
    
    backup_data = {
        "timestamp": datetime.now().isoformat(),
        "aktywna_grupa": aktywna_grupa,
        "sectro_sessions": sectro_sessions,
        "sectro_results": sectro_results
    }
    
    with open('backup_pre_unified.json', 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, indent=2, ensure_ascii=False, default=str)
    
    conn.close()
    print("✅ Backup zapisany do backup_pre_unified.json")

def create_unified_tables():
    """Stwórz tabele dla unified system"""
    print("🗃️ Tworzenie tabel unified...")
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Tabela unified queue
    cur.execute("""
        CREATE TABLE IF NOT EXISTS unified_start_queue (
            id SERIAL PRIMARY KEY,
            zawodnik_nr_startowy INTEGER REFERENCES zawodnicy(nr_startowy),
            kategoria VARCHAR(50),
            plec VARCHAR(1),
            status VARCHAR(20) DEFAULT 'checked_in',
            group_active BOOLEAN DEFAULT FALSE,
            session_id INTEGER,
            queue_position INTEGER,
            checked_in_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            activated_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tabela unified sessions (rozszerzenie sectro_sessions)
    cur.execute("""
        ALTER TABLE sectro_sessions 
        ADD COLUMN IF NOT EXISTS unified_group_id VARCHAR(100),
        ADD COLUMN IF NOT EXISTS auto_created BOOLEAN DEFAULT FALSE,
        ADD COLUMN IF NOT EXISTS kategoria VARCHAR(50),
        ADD COLUMN IF NOT EXISTS plec VARCHAR(1)
    """)
    
    # Index dla wydajności
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_unified_queue_group 
        ON unified_start_queue(kategoria, plec, status)
    """)
    
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_sectro_sessions_unified 
        ON sectro_sessions(unified_group_id, kategoria, plec)
    """)
    
    conn.commit()
    conn.close()
    print("✅ Tabele unified utworzone")

def migrate_existing_checkins():
    """Migruj istniejące meldowania z aktywnej grupy"""
    print("🔄 Migracja istniejących meldowań...")
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Pobierz zameldowanych zawodników
    cur.execute("""
        SELECT z.nr_startowy, z.kategoria, z.plec 
        FROM zawodnicy z 
        WHERE z.checked_in = true
    """)
    
    checked_in = cur.fetchall()
    migrated_count = 0
    
    for nr_startowy, kategoria, plec in checked_in:
        # Sprawdź czy już nie ma w unified queue
        cur.execute("""
            SELECT id FROM unified_start_queue 
            WHERE zawodnik_nr_startowy = %s
        """, (nr_startowy,))
        
        if not cur.fetchone():
            # Dodaj do unified queue
            cur.execute("""
                INSERT INTO unified_start_queue 
                (zawodnik_nr_startowy, kategoria, plec, status, queue_position)
                VALUES (%s, %s, %s, 'checked_in', %s)
            """, (nr_startowy, kategoria, plec, migrated_count + 1))
            migrated_count += 1
    
    conn.commit()
    conn.close()
    print(f"✅ Zmigrowano {migrated_count} meldowań")

def link_sectro_sessions():
    """Połącz istniejące sesje SECTRO z unified system"""
    print("🔗 Łączenie sesji SECTRO z unified...")
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Pobierz aktywne sesje SECTRO
    cur.execute("""
        SELECT id, nazwa, created_at 
        FROM sectro_sessions 
        WHERE status = 'active' 
        ORDER BY created_at DESC
    """)
    
    active_sessions = cur.fetchall()
    
    for session_id, session_name, created_at in active_sessions:
        # Spróbuj wyodrębnić kategorię i płeć z nazwy sesji
        kategoria = None
        plec = None
        
        if "JUNIOR" in session_name.upper():
            kategoria = "JUNIOR"
        elif "SENIOR" in session_name.upper():
            kategoria = "SENIOR"
        elif "OPEN" in session_name.upper():
            kategoria = "OPEN"
            
        if "KOBIET" in session_name.upper() or "_F" in session_name.upper():
            plec = "F"
        elif "MEZCZYZN" in session_name.upper() or "_M" in session_name.upper():
            plec = "M"
        
        if kategoria and plec:
            # Aktualizuj sesję
            unified_group_id = f"{kategoria}_{plec}"
            cur.execute("""
                UPDATE sectro_sessions 
                SET unified_group_id = %s, kategoria = %s, plec = %s, auto_created = false
                WHERE id = %s
            """, (unified_group_id, kategoria, plec, session_id))
            
            print(f"   Sesja {session_id}: {session_name} → {unified_group_id}")
    
    conn.commit()
    conn.close()
    print("✅ Sesje SECTRO połączone")

def validate_migration():
    """Sprawdź poprawność migracji"""
    print("✅ Walidacja migracji...")
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Sprawdź unified queue
    cur.execute("SELECT COUNT(*) FROM unified_start_queue")
    queue_count = cur.fetchone()[0]
    
    # Sprawdź połączone sesje
    cur.execute("SELECT COUNT(*) FROM sectro_sessions WHERE unified_group_id IS NOT NULL")
    linked_sessions = cur.fetchone()[0]
    
    # Sprawdź zameldowanych
    cur.execute("SELECT COUNT(*) FROM zawodnicy WHERE checked_in = true")
    checked_in_count = cur.fetchone()[0]
    
    print(f"📊 Statystyki migracji:")
    print(f"   • Unified queue: {queue_count} zawodników")
    print(f"   • Połączonych sesji SECTRO: {linked_sessions}")
    print(f"   • Zameldowanych zawodników: {checked_in_count}")
    
    # Sprawdź spójność
    if queue_count >= checked_in_count * 0.8:  # 80% tolerance
        print("✅ Migracja wygląda poprawnie")
    else:
        print("⚠️ Możliwe problemy z migracją - sprawdź dane")
    
    conn.close()

def main():
    """Główny proces migracji"""
    print("=" * 60)
    print("🔄 SKATECROSS UNIFIED START CONTROL - MIGRACJA DANYCH")
    print("=" * 60)
    
    try:
        # Krok 1: Backup
        backup_existing_data()
        
        # Krok 2: Stwórz tabele
        create_unified_tables()
        
        # Krok 3: Migruj meldowania
        migrate_existing_checkins()
        
        # Krok 4: Połącz sesje SECTRO
        link_sectro_sessions()
        
        # Krok 5: Walidacja
        validate_migration()
        
        print("\n" + "=" * 60)
        print("🎉 MIGRACJA ZAKOŃCZONA POMYŚLNIE!")
        print("📋 Następne kroki:")
        print("   1. Uruchom test_unified_integration.py")
        print("   2. Sprawdź frontend /unified")
        print("   3. Jeśli wszystko OK - wykonaj cleanup (faza 4)")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ BŁĄD MIGRACJI: {e}")
        print("🔧 Sprawdź backup_pre_unified.json i przywróć dane")

if __name__ == "__main__":
    main() 