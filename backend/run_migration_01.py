import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv('DATABASE_URL')

print('🏗️ Uruchamiam migrację 01: tworzenie tabeli start_queue...')

# Wczytaj plik SQL
with open('migrations/01_create_start_queue.sql', 'r') as f:
    migration_sql = f.read()

# Wykonaj migrację
conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

try:
    cur.execute(migration_sql)
    conn.commit()
    print('✅ Migracja 01 zakończona sukcesem!')
    
    # Sprawdź czy tabela została utworzona
    cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'start_queue'")
    if cur.fetchone()[0] > 0:
        print('✅ Tabela start_queue została utworzona')
    
    # Sprawdź widok
    cur.execute("SELECT COUNT(*) FROM information_schema.views WHERE table_name = 'v_current_queue'")
    if cur.fetchone()[0] > 0:
        print('✅ Widok v_current_queue został utworzony')
        
    # Pokaż strukturę tabeli
    cur.execute("""
    SELECT column_name, data_type, is_nullable 
    FROM information_schema.columns 
    WHERE table_name = 'start_queue' 
    ORDER BY ordinal_position
    """)
    print('\n📊 STRUKTURA TABELI start_queue:')
    for row in cur.fetchall():
        print(f'  {row[0]}: {row[1]} (nullable: {row[2]})')
        
except Exception as e:
    conn.rollback()
    print(f'❌ Błąd migracji: {e}')
    
finally:
    cur.close()
    conn.close() 