from queue_manager import QueueManager
import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv

load_dotenv()

print('🔍 DEBUG: Sprawdzanie typu cursor')

qm = QueueManager()

# Test z RealDictCursor
with qm.get_connection() as conn:
    cur = conn.cursor()
    cur.execute("SELECT status FROM start_queue WHERE nr_startowy = 1")
    result = cur.fetchone()
    print(f'RealDictCursor result: {result}')
    print(f'Type: {type(result)}')
    if result:
        print(f'Keys: {result.keys() if hasattr(result, "keys") else "No keys"}')

# Test z normalnym cursor
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()
cur.execute("SELECT status FROM start_queue WHERE nr_startowy = 1")
result = cur.fetchone()
print(f'Normal cursor result: {result}')
print(f'Type: {type(result)}')
cur.close()
conn.close() 