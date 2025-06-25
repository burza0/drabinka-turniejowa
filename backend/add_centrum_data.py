#!/usr/bin/env python3
"""
Prosty skrypt dodający dane centrum startu do istniejącej tabeli
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

def add_centrum_data():
    """Dodaje przykładowe dane centrum startu"""
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        print("🏁 Dodawanie danych centrum startu...")
        
        # Usuń stare dane
        cur.execute("DELETE FROM start_queue")
        
        # Dodaj przykładowe grupy używając prostej struktury
        grupy = [
            (1, "Senior Mężczyźni", "Senior", "M"),
            (2, "Senior Kobiety", "Senior", "K"), 
            (3, "Masters Mężczyźni", "Masters", "M"),
            (4, "Masters Kobiety", "Masters", "K"),
            (5, "Junior A Mężczyźni", "Junior A", "M"),
            (6, "Junior A Kobiety", "Junior A", "K"),
        ]
        
        for nr, nazwa, kategoria, plec in grupy:
            # Znajdź zawodnika z tej kategorii jako przykład
            cur.execute("""
                SELECT nr_startowy FROM zawodnicy 
                WHERE kategoria = %s AND plec = %s 
                LIMIT 1
            """, (kategoria, plec))
            
            result = cur.fetchone()
            if result:
                nr_startowy = result[0]
                
                # Dodaj do start_queue używając obecnej struktury
                cur.execute("""
                    INSERT INTO start_queue (nr_startowy, source_type, status, group_info, queue_position)
                    VALUES (%s, 'GROUP', 'WAITING', %s, %s)
                """, (nr_startowy, f'{{"nazwa":"{nazwa}","kategoria":"{kategoria}","plec":"{plec}"}}', nr))
                
                print(f"✅ Dodano grupę {nr}: {nazwa}")
        
        conn.commit()
        print(f"🎉 Dodano {len(grupy)} grup do centrum startu!")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Błąd: {e}")

if __name__ == "__main__":
    add_centrum_data() 