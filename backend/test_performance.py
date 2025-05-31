import time
from api_server import get_all, get_one, get_db_connection, release_db_connection

def analyze_query(query, params=None):
    """Analizuje plan wykonania zapytania"""
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        explain_query = f"EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) {query}"
        if params:
            cur.execute(explain_query, params)
        else:
            cur.execute(explain_query)
        plan = cur.fetchone()[0]
        cur.close()
        return plan
    finally:
        release_db_connection(conn)

def measure_query_time(query, params=None):
    start_time = time.time()
    result = get_all(query, params) if params else get_all(query)
    end_time = time.time()
    return end_time - start_time, result

def print_query_analysis(name, query, params=None):
    """Wykonuje i analizuje zapytanie"""
    print(f"\n=== {name} ===")
    
    # Zmierz czas wykonania
    execution_time, result = measure_query_time(query, params)
    print(f"Czas wykonania: {execution_time:.3f}s")
    print(f"Liczba wyników: {len(result)}")
    
    try:
        # Pobierz i przeanalizuj plan wykonania
        plan = analyze_query(query, params)
        
        # Wyciągnij najważniejsze informacje z planu
        planning_time = plan[0]['Planning Time']
        execution_time = plan[0]['Execution Time']
        total_cost = plan[0]['Plan']['Total Cost']
        
        print(f"Czas planowania: {planning_time:.3f}ms")
        print(f"Czas wykonania (EXPLAIN): {execution_time:.3f}ms")
        print(f"Całkowity koszt: {total_cost:.2f}")
        
        # Sprawdź użycie indeksów
        plan_str = str(plan)
        if 'Index Scan' in plan_str:
            print("✅ Zapytanie używa indeksów")
            # Wyświetl użyte indeksy
            if 'Index Name' in plan_str:
                print("   Użyte indeksy:", plan_str.count('Index Name'))
        elif 'Seq Scan' in plan_str:
            print("⚠️ Zapytanie używa skanowania sekwencyjnego!")
        else:
            print("ℹ️ Zapytanie nie używa indeksów ani skanowania sekwencyjnego")
        
    except Exception as e:
        print(f"⚠️ Błąd podczas analizy planu wykonania: {str(e)}")
    
    return execution_time

def run_performance_tests():
    print("Rozpoczynam szczegółowe testy wydajności...")
    
    times = []
    
    # Test 1: Wyszukiwanie po kategorii
    query1 = """
        SELECT z.*, w.czas_przejazdu_s 
        FROM zawodnicy z 
        LEFT JOIN wyniki w ON z.nr_startowy = w.nr_startowy 
        WHERE z.kategoria = 'OPEN'
    """
    times.append(print_query_analysis("Test 1 - Wyszukiwanie po kategorii", query1))
    
    # Test 2: Wyszukiwanie wyników
    query2 = """
        SELECT * FROM wyniki 
        WHERE status = 'FINISHED'
    """
    times.append(print_query_analysis("Test 2 - Wyszukiwanie wyników po statusie", query2))
    
    # Test 3: Złożone zapytanie z grupowaniem
    query3 = """
        SELECT kategoria, plec, COUNT(*) as liczba
        FROM zawodnicy 
        WHERE checked_in = TRUE
        GROUP BY kategoria, plec
    """
    times.append(print_query_analysis("Test 3 - Grupowanie z filtrowaniem", query3))
    
    # Test 4: Wyszukiwanie zawodników z wynikami
    query4 = """
        SELECT z.imie, z.nazwisko, z.kategoria, w.czas_przejazdu_s
        FROM zawodnicy z
        JOIN wyniki w ON z.nr_startowy = w.nr_startowy
        WHERE z.plec = 'M' AND w.status = 'FINISHED'
    """
    times.append(print_query_analysis("Test 4 - Złożone join z filtrowaniem", query4))
    
    # Test 5: Wyszukiwanie checkpointów
    query5 = """
        SELECT c.*, z.imie, z.nazwisko
        FROM checkpoints c
        JOIN zawodnicy z ON c.nr_startowy = z.nr_startowy
        WHERE c.checkpoint_name = 'check-in'
        ORDER BY c.timestamp DESC
        LIMIT 10
    """
    times.append(print_query_analysis("Test 5 - Wyszukiwanie checkpointów z join", query5))
    
    # Test 6: Złożone zapytanie dla drabinki
    query6 = """
        WITH kwalifikacje AS (
            SELECT 
                z.nr_startowy,
                z.imie,
                z.nazwisko,
                z.kategoria,
                z.plec,
                w.czas_przejazdu_s,
                ROW_NUMBER() OVER (PARTITION BY z.kategoria, z.plec ORDER BY w.czas_przejazdu_s) as pozycja
            FROM zawodnicy z
            JOIN wyniki w ON z.nr_startowy = w.nr_startowy
            WHERE w.status = 'FINISHED'
        )
        SELECT *
        FROM kwalifikacje
        WHERE pozycja <= 16
        ORDER BY kategoria, plec, pozycja;
    """
    times.append(print_query_analysis("Test 6 - Złożone zapytanie kwalifikacyjne", query6))
    
    print("\n=== Podsumowanie ===")
    print(f"Średni czas wykonania: {sum(times)/len(times):.3f}ms")
    print(f"Najszybsze zapytanie: {min(times):.3f}ms")
    print(f"Najwolniejsze zapytanie: {max(times):.3f}ms")

if __name__ == "__main__":
    run_performance_tests() 