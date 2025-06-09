from queue_manager import QueueManager
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

print('🐛 DEBUG: Problem z przywracaniem zawodnika')

qm = QueueManager()

# Sprawdź bezpośrednio w bazie
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

# Sprawdź zawodnika #1
cur.execute("SELECT nr_startowy, status, queue_position FROM start_queue WHERE nr_startowy = 1")
result = cur.fetchone()
print(f'Zawodnik #1 w bazie: {result}')

# Sprawdź wszystkich ukrytych
cur.execute("SELECT nr_startowy, status FROM start_queue WHERE status = 'hidden'")
hidden = cur.fetchall()
print(f'Ukryci zawodnicy: {hidden}')

# Sprawdź maksymalną pozycję
cur.execute("SELECT COALESCE(MAX(queue_position), 0) FROM start_queue WHERE status = 'waiting'")
max_pos = cur.fetchone()[0]
print(f'Maksymalna pozycja: {max_pos}')

cur.close()
conn.close()

# Test przywracania z debugowaniem
print('\n🔄 Test przywracania zawodnika #1:')
result = qm.unhide_athlete(1)
print(f'Rezultat: {result}')

if result['success']:
    # Sprawdź po przywróceniu
    info = qm.get_athlete_queue_info(1)
    print(f'Status po przywróceniu: {info["status"]}')
    print(f'Pozycja po przywróceniu: {info["queue_position"]}') 