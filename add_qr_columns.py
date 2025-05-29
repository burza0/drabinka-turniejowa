#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

def add_qr_columns():
    """Dodaje kolumny QR code do tabeli zawodnicy"""
    
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        print("🔧 Dodawanie kolumn QR code do tabeli zawodnicy...")
        
        # Sprawdź czy kolumny już istnieją
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'zawodnicy' 
            AND column_name IN ('qr_code', 'checked_in', 'check_in_time')
        """)
        existing_columns = [row[0] for row in cur.fetchall()]
        
        # Dodaj kolumny jeśli nie istnieją
        if 'qr_code' not in existing_columns:
            cur.execute("ALTER TABLE zawodnicy ADD COLUMN qr_code VARCHAR(255) UNIQUE")
            print("✅ Dodano kolumnę qr_code")
        else:
            print("ℹ️  Kolumna qr_code już istnieje")
            
        if 'checked_in' not in existing_columns:
            cur.execute("ALTER TABLE zawodnicy ADD COLUMN checked_in BOOLEAN DEFAULT FALSE")
            print("✅ Dodano kolumnę checked_in")
        else:
            print("ℹ️  Kolumna checked_in już istnieje")
            
        if 'check_in_time' not in existing_columns:
            cur.execute("ALTER TABLE zawodnicy ADD COLUMN check_in_time TIMESTAMP")
            print("✅ Dodano kolumnę check_in_time")
        else:
            print("ℹ️  Kolumna check_in_time już istnieje")
        
        # Dodaj tabelę checkpointów
        cur.execute("""
            CREATE TABLE IF NOT EXISTS checkpoints (
                id SERIAL PRIMARY KEY,
                nr_startowy INTEGER REFERENCES zawodnicy(nr_startowy),
                checkpoint_name VARCHAR(50) NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                device_id VARCHAR(100),
                qr_code VARCHAR(255)
            )
        """)
        print("✅ Utworzono tabelę checkpoints")
        
        conn.commit()
        cur.close()
        conn.close()
        
        print("\n🎉 Migracja bazy danych zakończona pomyślnie!")
        
    except Exception as e:
        print(f"❌ Błąd podczas migracji: {e}")
        if conn:
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    add_qr_columns() 