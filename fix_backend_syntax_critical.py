#!/usr/bin/env python3

def fix_backend_syntax():
    """NAPRAWIA KRYTYCZNE BŁĘDY SKŁADNI W backend/api_server.py"""
    
    with open('backend/api_server.py', 'r') as f:
        content = f.read()
    
    print('🔧 NAPRAWIAM KRYTYCZNE BŁĘDY SKŁADNI BACKEND...')
    
    # Problem 1: Całkowicie zepsuta funkcja get_all()
    old_get_all = '''def get_all(query, params=None):
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
            return_db_connection(conn)'''

    new_get_all = '''def get_all(query, params=None):
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
            return_db_connection(conn)'''

    content = content.replace(old_get_all, new_get_all)
    print('✅ Naprawiono funkcję get_all()')

    # Problem 2: Zepsuta funkcja get_one()
    old_get_one = '''def get_one(query, params=None):
    """WERSJA 30.3.6: Pobiera pojedynczy rekord używając connection pool"""
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            return None
            
    cur = conn.cursor()
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
        cur.close()
        return result
    except Exception as e:
        print(f"❌ Błąd w get_one: {str(e)}")
        return None
    finally:
        if conn:
            return_db_connection(conn)'''

    new_get_one = '''def get_one(query, params=None):
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
            return_db_connection(conn)'''

    content = content.replace(old_get_one, new_get_one)
    print('✅ Naprawiono funkcję get_one()')

    # Problem 3: Zepsuta funkcja execute_query()
    old_execute = '''def execute_query(query, params=None):
    """WERSJA 30.3.6: Wykonuje zapytanie używając connection pool"""
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            raise Exception("Nie można uzyskać połączenia z bazą danych")
            
        cur = conn.cursor()
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        conn.commit()
        rowcount = cur.rowcount
        cur.close()
        return rowcount
    except Exception as e:
        if conn:
        conn.rollback()
        raise e
    finally:
        if conn:
            return_db_connection(conn)'''

    new_execute = '''def execute_query(query, params=None):
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
            return_db_connection(conn)'''

    content = content.replace(old_execute, new_execute)
    print('✅ Naprawiono funkcję execute_query()')

    # Zapisz naprawiony plik
    with open('backend/api_server.py', 'w') as f:
        f.write(content)
    
    print('')
    print('✅ WSZYSTKIE KRYTYCZNE BŁĘDY SKŁADNI NAPRAWIONE!')
    print('🎯 Backend powinien się teraz uruchamiać bez błędów Python')

if __name__ == '__main__':
    fix_backend_syntax() 