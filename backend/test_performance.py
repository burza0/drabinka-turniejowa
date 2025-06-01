#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time
import statistics
import json
from datetime import datetime
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Konfiguracja
API_URL = "http://localhost:5001"  # Port zoptymalizowanego API
ITERATIONS = 10  # Liczba powtórzeń każdego testu

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

def measure_endpoint(endpoint, name, with_cache=True):
    """Mierzy czas odpowiedzi endpointu"""
    times = []
    url = f"{API_URL}{endpoint}"
    
    print(f"\n🔍 Test: {name}")
    print("=" * 50)
    
    # Pierwszy request (cold start / wypełnienie cache)
    start = time.time()
    response = requests.get(url)
    cold_time = (time.time() - start) * 1000
    
    if not response.ok:
        print(f"❌ Błąd: {response.status_code}")
        return None
        
    # Kolejne requesty
    for i in range(ITERATIONS):
        start = time.time()
        response = requests.get(url)
        end = time.time()
        times.append((end - start) * 1000)
        
    # Statystyki
    avg_time = statistics.mean(times)
    min_time = min(times)
    max_time = max(times)
    
    print(f"Cold start: {cold_time:.2f}ms")
    print(f"Średni czas: {avg_time:.2f}ms")
    print(f"Min czas: {min_time:.2f}ms")
    print(f"Max czas: {max_time:.2f}ms")
    
    if with_cache:
        cache_improvement = ((cold_time - min_time) / cold_time) * 100
        print(f"Poprawa dzięki cache: {cache_improvement:.1f}%")
    
    return {
        "endpoint": endpoint,
        "cold_start_ms": cold_time,
        "avg_time_ms": avg_time,
        "min_time_ms": min_time,
        "max_time_ms": max_time,
        "cache_improvement": cache_improvement if with_cache else None
    }

def test_database_performance():
    """Testy wydajności bazy danych"""
    print("\n📊 TESTY WYDAJNOŚCI BAZY DANYCH")
    print("=" * 50)
    
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()
    
    queries = [
        ("Test 1: Podstawowe zawodnicy", """
            SELECT * FROM zawodnicy 
            ORDER BY nr_startowy 
            LIMIT 100
        """),
        ("Test 2: JOIN z wynikami", """
            SELECT z.*, w.czas_przejazdu_s 
            FROM zawodnicy z
            LEFT JOIN wyniki w ON z.nr_startowy = w.nr_startowy
            WHERE z.kategoria = 'Junior A'
        """),
        ("Test 3: Grupowanie po kategoriach", """
            SELECT kategoria, plec, COUNT(*) 
            FROM zawodnicy 
            GROUP BY kategoria, plec
        """),
        ("Test 4: Złożone zapytanie z wieloma JOIN", """
            SELECT z.nr_startowy, z.imie, z.nazwisko,
                   w.czas_przejazdu_s, c.checkpoint_name,
                   k.nazwa as klub_nazwa
            FROM zawodnicy z
            LEFT JOIN wyniki w ON z.nr_startowy = w.nr_startowy
            LEFT JOIN checkpoints c ON z.nr_startowy = c.nr_startowy
            LEFT JOIN kluby k ON z.klub = k.nazwa
            WHERE z.kategoria = 'Junior A'
            AND z.plec = 'M'
            ORDER BY w.czas_przejazdu_s NULLS LAST
            LIMIT 20
        """)
    ]
    
    results = []
    for name, query in queries:
        print(f"\n🔍 {name}")
        times = []
        
        for i in range(ITERATIONS):
            start = time.time()
            cur.execute(query)
            cur.fetchall()
            end = time.time()
            times.append((end - start) * 1000)
            
        avg_time = statistics.mean(times)
        print(f"Średni czas: {avg_time:.2f}ms")
        results.append({"name": name, "avg_time_ms": avg_time})
    
    cur.close()
    conn.close()
    return results

def run_all_tests():
    """Uruchamia wszystkie testy wydajności"""
    print("\n🚀 ROZPOCZYNAM TESTY WYDAJNOŚCI")
    print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "api_version": requests.get(f"{API_URL}/api/version").json()["version"],
        "endpoints": [],
        "database": None
    }
    
    # Testy endpointów API
    endpoints = [
        ("/api/zawodnicy", "Lista zawodników"),
        ("/api/wyniki", "Lista wyników"),
        ("/api/statystyki", "Statystyki"),
        ("/api/kluby", "Lista klubów"),
        ("/api/qr/dashboard", "QR Dashboard"),
        ("/api/version", "Wersja API")
    ]
    
    for endpoint, name in endpoints:
        result = measure_endpoint(endpoint, name)
        if result:
            results["endpoints"].append(result)
    
    # Testy bazy danych
    print("\nUruchamiam testy bazy danych...")
    results["database"] = test_database_performance()
    
    # Zapisz wyniki do pliku
    filename = f"performance_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Testy zakończone. Wyniki zapisano w: {filename}")
    
    return results

if __name__ == "__main__":
    run_all_tests() 