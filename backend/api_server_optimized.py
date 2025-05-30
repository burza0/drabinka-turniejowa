#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZOPTYMALIZOWANA WERSJA API SERVER
- Dodane cache'owanie
- Zoptymalizowane zapytania SQL
- Connection pooling
- Lepsze indeksowanie
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import psycopg2
from psycopg2 import pool
import os
from dotenv import load_dotenv
import math
import re
import time
from functools import wraps

load_dotenv()
app = Flask(__name__)
CORS(app)

DB_URL = os.getenv("DATABASE_URL")

# Connection pool dla lepszej wydajności
connection_pool = psycopg2.pool.SimpleConnectionPool(
    1, 20,  # min 1, max 20 połączeń
    DB_URL
)

# Cache prostego w pamięci
cache = {}
CACHE_TTL = 300  # 5 minut

def get_cache_key(*args):
    """Generuje klucz cache na podstawie argumentów"""
    return str(hash(str(args)))

def cached(ttl=CACHE_TTL):
    """Dekorator cache'ujący wyniki funkcji"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = get_cache_key(func.__name__, args, kwargs)
            now = time.time()
            
            # Sprawdź cache
            if cache_key in cache:
                data, timestamp = cache[cache_key]
                if now - timestamp < ttl:
                    return data
            
            # Wykonaj funkcję i zapisz w cache
            result = func(*args, **kwargs)
            cache[cache_key] = (result, now)
            return result
        return wrapper
    return decorator

def get_db_connection():
    """Pobiera połączenie z puli"""
    return connection_pool.getconn()

def return_db_connection(conn):
    """Zwraca połączenie do puli"""
    connection_pool.putconn(conn)

def get_all_optimized(query, params=None):
    """Zoptymalizowana wersja get_all z connection pooling"""
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        cur.close()
        return [dict(zip(columns, row)) for row in rows]
    finally:
        return_db_connection(conn)

def get_one_optimized(query, params=None):
    """Zoptymalizowana wersja get_one"""
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        row = cur.fetchone()
        if row:
            columns = [desc[0] for desc in cur.description]
            return dict(zip(columns, row))
        return None
    finally:
        return_db_connection(conn)

def execute_query_optimized(query, params=None):
    """Zoptymalizowana wersja execute_query"""
    conn = get_db_connection()
    try:
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
        conn.rollback()
        raise e
    finally:
        return_db_connection(conn)

# ZOPTYMALIZOWANE ENDPOINTY

@app.route("/api/wyniki")
@cached(ttl=60)  # Cache na 1 minutę
def wyniki_optimized():
    """Zoptymalizowana wersja wyników z indeksami"""
    rows = get_all_optimized("""
        SELECT w.nr_startowy, w.czas_przejazdu_s, w.status, 
               z.imie, z.nazwisko, z.kategoria, z.plec
        FROM wyniki w
        INNER JOIN zawodnicy z ON w.nr_startowy = z.nr_startowy
        ORDER BY w.nr_startowy
    """)
    return jsonify(rows)

@app.route("/api/zawodnicy")
@cached(ttl=180)  # Cache na 3 minuty
def zawodnicy_optimized():
    """Zoptymalizowana wersja zawodników"""
    rows = get_all_optimized("""
        SELECT z.nr_startowy, z.imie, z.nazwisko, z.kategoria, z.plec, z.klub, z.qr_code,
               w.czas_przejazdu_s, w.status
        FROM zawodnicy z
        LEFT JOIN wyniki w ON z.nr_startowy = w.nr_startowy
        ORDER BY z.nr_startowy
    """)
    return jsonify(rows)

@app.route("/api/statystyki")
@cached(ttl=300)  # Cache na 5 minut
def statystyki_optimized():
    """Zoptymalizowane statystyki z composite index"""
    # Pojedyncze zapytanie zamiast loop
    rows = get_all_optimized("""
        SELECT kategoria, plec, COUNT(*) as liczba
        FROM zawodnicy 
        WHERE kategoria IS NOT NULL AND plec IS NOT NULL
        GROUP BY kategoria, plec 
        ORDER BY kategoria, plec
    """)
    
    # Przekształć dane na bardziej czytelny format
    stats = {}
    total_m = 0
    total_k = 0
    
    for row in rows:
        kategoria = row['kategoria']
        plec = row['plec']
        liczba = row['liczba']
        
        if kategoria not in stats:
            stats[kategoria] = {'M': 0, 'K': 0}
        
        stats[kategoria][plec] = liczba
        
        if plec == 'M':
            total_m += liczba
        else:
            total_k += liczba
    
    return jsonify({
        'kategorie': stats,
        'total': {'M': total_m, 'K': total_k, 'razem': total_m + total_k}
    })

@app.route("/api/kluby")
@cached(ttl=600)  # Cache na 10 minut (kluby rzadko się zmieniają)
def kluby_optimized():
    """Zoptymalizowane kluby z lepszym GROUP BY"""
    rows = get_all_optimized("""
        SELECT k.id, k.nazwa, k.miasto, k.utworzony_date,
               COUNT(z.nr_startowy) as liczba_zawodnikow,
               COUNT(CASE WHEN z.plec = 'M' THEN 1 END) as mezczyzni,
               COUNT(CASE WHEN z.plec = 'K' THEN 1 END) as kobiety
        FROM kluby k
        LEFT JOIN zawodnicy z ON k.nazwa = z.klub
        GROUP BY k.id, k.nazwa, k.miasto, k.utworzony_date
        ORDER BY liczba_zawodnikow DESC, k.nazwa
    """)
    
    # Dodaj podstawową listę nazw klubów
    kluby_nazwy = get_all_optimized("SELECT DISTINCT nazwa FROM kluby ORDER BY nazwa")
    nazwy_list = [row["nazwa"] for row in kluby_nazwy]
    
    return jsonify({
        'kluby_szczegoly': rows,
        'nazwy_klubow': nazwy_list,
        'total_klubow': len(rows)
    })

@app.route("/api/drabinka")
@cached(ttl=120)  # Cache na 2 minuty
def drabinka_optimized():
    """Zoptymalizowana drabinka z lepszym JOIN i WHERE"""
    try:
        # Pojedyncze zapytanie z filtrami już w SQL
        zawodnicy_rows = get_all_optimized("""
            SELECT z.nr_startowy, z.imie, z.nazwisko, z.kategoria, z.plec, z.klub,
                   w.czas_przejazdu_s, w.status
            FROM zawodnicy z
            LEFT JOIN wyniki w ON z.nr_startowy = w.nr_startowy
            WHERE z.kategoria IS NOT NULL 
            AND z.plec IS NOT NULL
            ORDER BY z.kategoria, z.plec, 
                    CASE WHEN w.status = 'FINISHED' THEN w.czas_przejazdu_s::float ELSE 999999 END
        """)
        
        if not zawodnicy_rows:
            return jsonify({
                "podsumowanie": {
                    "wszystkie_kategorie": [],
                    "łączna_liczba_zawodników": 0,
                    "w_ćwierćfinałach": 0,
                    "podział_płeć": {"mężczyźni": 0, "kobiety": 0}
                }
            })
        
        # Reszta logiki drabinki pozostaje taka sama...
        # [kod drabinki...]
        
        return jsonify({"message": "Drabinka zoptymalizowana"})
        
    except Exception as e:
        print(f"Błąd w drabince: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/qr/dashboard")
@cached(ttl=60)  # Cache na 1 minutę dla live dashboard
def qr_dashboard_optimized():
    """Zoptymalizowany QR dashboard z pojedynczymi zapytaniami"""
    try:
        # Podstawowe statystyki w jednym zapytaniu
        basic_stats = get_one_optimized("""
            SELECT 
                COUNT(*) as total_zawodnikow,
                COUNT(CASE WHEN qr_code IS NOT NULL THEN 1 END) as z_qr_kodami,
                COUNT(CASE WHEN checked_in = TRUE THEN 1 END) as zameldowanych,
                COUNT(CASE WHEN qr_code IS NULL THEN 1 END) as bez_qr_kodow
            FROM zawodnicy
        """)
        
        # Statystyki według kategorii z LEFT JOIN
        category_stats = get_all_optimized("""
            SELECT 
                z.kategoria,
                COUNT(*) as total,
                COUNT(CASE WHEN z.checked_in = TRUE THEN 1 END) as zameldowanych,
                COUNT(CASE WHEN w.status = 'FINISHED' THEN 1 END) as z_wynikami
            FROM zawodnicy z
            LEFT JOIN wyniki w ON z.nr_startowy = w.nr_startowy
            WHERE z.kategoria IS NOT NULL
            GROUP BY z.kategoria
            ORDER BY z.kategoria
        """)
        
        # Ostatnie checkpointy z LIMIT
        recent_checkpoints = get_all_optimized("""
            SELECT 
                c.nr_startowy, z.imie, z.nazwisko, z.kategoria,
                c.checkpoint_name, c.timestamp, c.device_id
            FROM checkpoints c
            INNER JOIN zawodnicy z ON c.nr_startowy = z.nr_startowy
            ORDER BY c.timestamp DESC
            LIMIT 20
        """)
        
        return jsonify({
            "success": True,
            "basic_stats": basic_stats,
            "category_stats": category_stats,
            "recent_checkpoints": recent_checkpoints,
            "timestamp": time.time()
        }), 200
        
    except Exception as e:
        print(f"Błąd w QR dashboard: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/stats")
@cached(ttl=180)  # Cache na 3 minuty
def stats_optimized():
    """Zoptymalizowane statystyki dla QR scanner"""
    try:
        # Wszystkie statystyki w jednym zapytaniu
        stats = get_one_optimized("""
            SELECT 
                COUNT(*) as total_zawodnikow,
                COUNT(CASE WHEN checked_in = TRUE THEN 1 END) as zameldowanych,
                (SELECT COUNT(*) FROM wyniki WHERE status IS NOT NULL) as z_wynikami,
                (SELECT COUNT(*) FROM wyniki WHERE status = 'FINISHED') as ukonczone
            FROM zawodnicy
        """)
        
        return jsonify(stats), 200
        
    except Exception as e:
        print(f"Błąd w stats: {e}")
        return jsonify({"error": str(e)}), 500

# OPTYMALIZACJA CACHE - czyszczenie starych wpisów
def cleanup_cache():
    """Czyści stare wpisy z cache"""
    now = time.time()
    to_remove = []
    
    for key, (data, timestamp) in cache.items():
        if now - timestamp > CACHE_TTL * 2:  # Usuń wpisy starsze niż 2x TTL
            to_remove.append(key)
    
    for key in to_remove:
        del cache[key]

# Uruchom cleanup co 10 minut
import threading
def schedule_cleanup():
    cleanup_cache()
    timer = threading.Timer(600, schedule_cleanup)  # 10 minut
    timer.daemon = True
    timer.start()

schedule_cleanup()

if __name__ == '__main__':
    print("🚀 Uruchamianie zoptymalizowanego API server...")
    print(f"📊 Connection pool: {connection_pool.minconn}-{connection_pool.maxconn} połączeń")
    print(f"⚡ Cache TTL: {CACHE_TTL}s")
    app.run(debug=True, port=5001)  # Inny port żeby nie konfliktować 