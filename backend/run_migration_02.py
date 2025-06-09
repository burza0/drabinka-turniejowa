import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv('DATABASE_URL')

print('🔄 Uruchamiam migrację 02: migracja istniejących danych...')

# Wczytaj plik SQL
with open('migrations/02_migrate_existing_data.sql', 'r') as f:
    migration_sql = f.read()

# Wykonaj migrację
conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

try:
    cur.execute(migration_sql)
    conn.commit()
    print('✅ Migracja 02 zakończona sukcesem!')
    
    # Pokaż podsumowanie migracji
    cur.execute("""
    SELECT 
        source_type,
        status,
        COUNT(*) as count
    FROM start_queue
    GROUP BY source_type, status
    ORDER BY source_type, status
    """)
    
    print('\n📊 PODSUMOWANIE MIGRACJI:')
    total = 0
    for row in cur.fetchall():
        print(f'  {row[0]} + {row[1]}: {row[2]} zawodników')
        total += row[2]
    print(f'  TOTAL: {total} zawodników w nowej kolejce')
    
    # Sprawdź widok
    cur.execute("SELECT COUNT(*) FROM v_current_queue")
    visible_count = cur.fetchone()[0]
    print(f'  WIDOCZNI W KOLEJCE: {visible_count} zawodników')
    
    # Pokaż przykład danych
    cur.execute("""
    SELECT nr_startowy, source_type, status, queue_position, 
           group_info->>'kategoria' as kategoria
    FROM start_queue 
    ORDER BY queue_position, added_at 
    LIMIT 5
    """)
    print('\n📋 PRZYKŁAD DANYCH:')
    for row in cur.fetchall():
        print(f'  #{row[0]}: {row[1]} | {row[2]} | pos:{row[3]} | {row[4]}')
        
except Exception as e:
    conn.rollback()
    print(f'❌ Błąd migracji: {e}')
    
finally:
    cur.close()
    conn.close() 