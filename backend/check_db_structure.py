import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv('DATABASE_URL')

def check_db_structure():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    # Sprawdź strukture tabeli checkpoints
    cur.execute("""
        SELECT column_name, data_type, is_nullable 
        FROM information_schema.columns 
        WHERE table_name = 'checkpoints' 
        ORDER BY ordinal_position;
    """)
    columns = cur.fetchall()
    
    print('=== KOLUMNY W TABELI checkpoints ===')
    for col in columns:
        print(f'{col[0]} - {col[1]} - nullable: {col[2]}')
    
    # Sprawdź czy tabela ma jakieś dane
    cur.execute('SELECT COUNT(*) FROM checkpoints;')
    count = cur.fetchone()[0]
    print(f'\nLiczba rekordów w checkpoints: {count}')
    
    # Sprawdź pierwsze 3 rekordy
    if count > 0:
        cur.execute('SELECT * FROM checkpoints LIMIT 3;')
        rows = cur.fetchall()
        print('\n=== PRZYKŁADOWE DANE ===')
        for row in rows:
            print(row)
    
    cur.close()
    conn.close()

if __name__ == '__main__':
    check_db_structure() 