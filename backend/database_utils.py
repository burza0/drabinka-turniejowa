import psycopg2
import os
from dotenv import load_dotenv
from psycopg2 import pool
import atexit

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

# WERSJA 30.3.6: CONNECTION POOLING dla wydajności na Heroku
connection_pool = None

def init_db_pool():
    """Inicjalizuje pulę połączeń z optymalizacją dla Heroku"""
    global connection_pool
    if connection_pool is None:
        try:
            connection_pool = psycopg2.pool.SimpleConnectionPool(
                1, 15,  # min 1, max 15 połączeń (Heroku hobby-dev limit = 20)
                DB_URL,
                connect_timeout=10  # 10 sekund timeout
            )
            print("✅ Connection pool zainicjalizowany (1-15 połączeń)")
        except Exception as e:
            print(f"❌ Błąd inicjalizacji connection pool: {e}")
            connection_pool = None

def get_db_connection():
    """Pobiera połączenie z puli z timeout handling"""
    global connection_pool
    if connection_pool is None:
        init_db_pool()
    
    try:
        if connection_pool:
            return connection_pool.getconn()
        else:
            # Fallback do prostego połączenia
            return psycopg2.connect(DB_URL, connect_timeout=10)
    except Exception as e:
        print(f"❌ Błąd pobierania połączenia: {e}")
        return None

def return_db_connection(conn):
    """Zwraca połączenie do puli"""
    global connection_pool
    if connection_pool is not None and conn is not None:
        try:
            connection_pool.putconn(conn)
        except Exception as e:
            print(f"⚠️ Błąd zwracania połączenia do puli: {e}")
            # Spróbuj zamknąć połączenie bezpośrednio
            try:
                conn.close()
            except:
                pass

def get_all(query, params=None):
    """WERSJA 30.3.6: Pobiera wszystkie rekordy używając connection pool"""
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            print("❌ Błąd: Nie udało się uzyskać połączenia z bazą danych")
            return []
            
        cur = conn.cursor()
        try:
            if params:
                print(f"🔍 Wykonuję zapytanie: {query} z parametrami: {params}")
                cur.execute(query, params)
            else:
                print(f"🔍 Wykonuję zapytanie: {query}")
                cur.execute(query)
                        
            rows = cur.fetchall()
            if not rows:
                print("ℹ️ Zapytanie nie zwróciło żadnych wyników")
                return []
                        
            columns = [desc[0] for desc in cur.description]
            result = [dict(zip(columns, row)) for row in rows]
            print(f"✅ Znaleziono {len(result)} wyników")
            return result
                    
        except Exception as e:
            print(f"❌ Błąd podczas wykonywania zapytania: {str(e)}")
            return []
        finally:
            cur.close()
    except Exception as e:
        print(f"❌ Błąd w get_all: {str(e)}")
        return []
    finally:
        if conn:
            return_db_connection(conn)

def get_one(query, params=None):
    """WERSJA 30.3.6: Pobiera pojedynczy rekord używając connection pool"""
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            return None
            
        cur = conn.cursor()
        try:
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
            row = cur.fetchone()
            if row:
                columns = [desc[0] for desc in cur.description]
                result = dict(zip(columns, row))
            else:
                result = None
            return result
        finally:
            cur.close()
    except Exception as e:
        print(f"❌ Błąd w get_one: {str(e)}")
        return None
    finally:
        if conn:
            return_db_connection(conn)

def execute_query(query, params=None):
    """WERSJA 30.3.6: Wykonuje zapytanie używając connection pool"""
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            raise Exception("Nie można uzyskać połączenia z bazą danych")
            
        cur = conn.cursor()
        try:
            if params:
                cur.execute(query, params)
            else:
                cur.execute(query)
            conn.commit()
            rowcount = cur.rowcount
            return rowcount
        finally:
            cur.close()
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            return_db_connection(conn)

def cleanup_db_pool():
    """Czyści connection pool przy wyłączaniu aplikacji"""
    global connection_pool
    if connection_pool is not None:
        try:
            connection_pool.closeall()
            print("🧹 Connection pool zamknięty przy shutdown")
        except Exception as e:
            print(f"⚠️ Błąd zamykania connection pool: {e}")
        connection_pool = None

# Inicjalizacja puli przy starcie modułu
init_db_pool()

# Zarejestruj cleanup funkcję przy shutdown aplikacji
atexit.register(cleanup_db_pool) 