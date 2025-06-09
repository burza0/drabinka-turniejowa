import os
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv('DATABASE_URL')
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

print(f'🔍 Analizuję obecną strukturę bazy danych...')
print(f'📅 Timestamp: {timestamp}')
print(f'🗄️  Database URL: {DB_URL[:50]}...')

# Sprawdź obecne tabele
conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

print('\n📊 OBECNA STRUKTURA BAZY:')
cur.execute("""
SELECT table_name, column_name, data_type 
FROM information_schema.columns 
WHERE table_schema = 'public' 
AND table_name IN ('zawodnicy', 'checkpoints', 'aktywna_grupa_settings', 'wyniki')
ORDER BY table_name, ordinal_position
""")

for row in cur.fetchall():
    print(f'  {row[0]}.{row[1]}: {row[2]}')

# Sprawdź dane w checkpoints
print('\n📈 DANE W CHECKPOINTS:')
cur.execute('SELECT checkpoint_name, COUNT(*) FROM checkpoints GROUP BY checkpoint_name')
for row in cur.fetchall():
    print(f'  {row[0]}: {row[1]} rekordów')

# Sprawdź aktywną grupę
print('\n🎯 AKTYWNA GRUPA:')
cur.execute('SELECT * FROM aktywna_grupa_settings LIMIT 1')
active_group = cur.fetchone()
if active_group:
    print(f'  {active_group}')
else:
    print('  ⚠️ BRAK AKTYWNEJ GRUPY')

# Sprawdź aktualną kolejkę
print('\n🚶 AKTUALNA KOLEJKA (symulacja):')
cur.execute("""
SELECT COUNT(*) as skanowani FROM checkpoints 
WHERE checkpoint_name = 'start-line-verify'
""")
skanowani = cur.fetchone()[0]

cur.execute("""
SELECT COUNT(*) as ukryci FROM checkpoints 
WHERE checkpoint_name = 'hidden-from-queue'
""")
ukryci = cur.fetchone()[0]

print(f'  Skanowani: {skanowani}')
print(f'  Ukryci: {ukryci}')

cur.close()
conn.close()
print('\n✅ Analiza zakończona') 