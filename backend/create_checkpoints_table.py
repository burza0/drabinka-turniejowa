import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv('DATABASE_URL')

def create_checkpoints_table():
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    # Tworzenie tabeli checkpoints
    cur.execute('''
        CREATE TABLE IF NOT EXISTS checkpoints (
            id SERIAL PRIMARY KEY,
            nr_startowy INTEGER NOT NULL,
            checkpoint_name VARCHAR(50) NOT NULL,
            qr_code VARCHAR(100),
            device_id VARCHAR(100),
            scan_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    
    # Dodanie przykładowych danych testowych
    cur.execute('''
        INSERT INTO checkpoints (nr_startowy, checkpoint_name, qr_code, device_id)
        SELECT z.nr_startowy, 'check-in', z.qr_code, 'admin-device'
        FROM zawodnicy z
        WHERE z.checked_in = TRUE
        ON CONFLICT DO NOTHING;
    ''')
    
    cur.execute('''
        INSERT INTO checkpoints (nr_startowy, checkpoint_name, qr_code, device_id)
        SELECT z.nr_startowy, 'finish', z.qr_code, 'admin-device'
        FROM zawodnicy z
        JOIN wyniki w ON z.nr_startowy = w.nr_startowy
        WHERE w.status = 'FINISHED'
        ON CONFLICT DO NOTHING;
    ''')
    
    conn.commit()
    cur.close()
    conn.close()
    print('✅ Tabela checkpoints utworzona i wypełniona danymi testowymi!')

if __name__ == '__main__':
    create_checkpoints_table() 