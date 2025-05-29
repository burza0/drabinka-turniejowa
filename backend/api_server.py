from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
import os
from dotenv import load_dotenv
import math
import re

load_dotenv()
app = Flask(__name__)
CORS(app)

DB_URL = os.getenv("DATABASE_URL")

def get_all(query, params=None):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    if params:
        cur.execute(query, params)
    else:
        cur.execute(query)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return [dict(zip(columns, row)) for row in rows]

def execute_query(query, params=None):
    """Wykonuje zapytanie INSERT/UPDATE/DELETE i zwraca liczbę zmienionych wierszy"""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    try:
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        conn.commit()
        rowcount = cur.rowcount
        cur.close()
        conn.close()
        return rowcount
    except Exception as e:
        conn.rollback()
        cur.close()
        conn.close()
        raise e

def validate_time_format(time_str):
    """Waliduje format czasu MM:SS.ms lub SS.ms"""
    if not time_str:
        return None
    
    # Usuń białe znaki
    time_str = time_str.strip()
    
    # Pattern dla MM:SS.ms lub SS.ms
    pattern = r'^(?:(\d{1,2}):)?(\d{1,2})\.(\d{1,3})$'
    match = re.match(pattern, time_str)
    
    if not match:
        raise ValueError(f"Nieprawidłowy format czasu: {time_str}. Użyj MM:SS.ms lub SS.ms")
    
    minutes = int(match.group(1)) if match.group(1) else 0
    seconds = int(match.group(2))
    milliseconds = match.group(3).ljust(3, '0')[:3]  # Uzupełnij do 3 cyfr
    
    # Konwertuj na sekundy z częściami dziesiętnymi
    total_seconds = minutes * 60 + seconds + int(milliseconds) / 1000
    
    return total_seconds

@app.route("/")
def home():
    return "Backend działa!"

@app.route("/api/wyniki")
def wyniki():
    rows = get_all("""
        SELECT w.nr_startowy, w.czas_przejazdu_s, w.status, 
               z.imie, z.nazwisko, z.kategoria, z.plec
        FROM wyniki w
        LEFT JOIN zawodnicy z ON w.nr_startowy = z.nr_startowy
        ORDER BY w.nr_startowy
    """)
    return jsonify(rows)

@app.route("/api/zawodnicy")
def zawodnicy():
    rows = get_all("""
        SELECT z.nr_startowy, z.imie, z.nazwisko, z.kategoria, z.plec, z.klub,
               w.czas_przejazdu_s, w.status
        FROM zawodnicy z
        LEFT JOIN wyniki w ON z.nr_startowy = w.nr_startowy
        ORDER BY z.nr_startowy
    """)
    return jsonify(rows)

@app.route("/api/kategorie")
def kategorie():
    # Pobierz kategorie
    kategorie_rows = get_all("SELECT DISTINCT kategoria FROM zawodnicy WHERE kategoria IS NOT NULL ORDER BY kategoria")
    kategorie_list = [row["kategoria"] for row in kategorie_rows]
    
    # Pobierz łączną liczbę zawodników
    total_rows = get_all("SELECT COUNT(*) as total FROM zawodnicy WHERE kategoria IS NOT NULL")
    total_zawodnikow = total_rows[0]["total"] if total_rows else 0
    
    return jsonify({
        "kategorie": kategorie_list,
        "total_zawodnikow": total_zawodnikow
    })

@app.route("/api/statystyki")
def statystyki():
    """Endpoint zwracający statystyki zawodników według kategorii i płci"""
    rows = get_all("""
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
def kluby():
    """Endpoint zwracający listę klubów z liczbą zawodników"""
    # Pobierz kluby z liczbą zawodników
    rows = get_all("""
        SELECT k.id, k.nazwa, k.miasto, k.utworzony_date,
               COUNT(z.nr_startowy) as liczba_zawodnikow,
               SUM(CASE WHEN z.plec = 'M' THEN 1 ELSE 0 END) as mezczyzni,
               SUM(CASE WHEN z.plec = 'K' THEN 1 ELSE 0 END) as kobiety
        FROM kluby k
        LEFT JOIN zawodnicy z ON k.nazwa = z.klub
        GROUP BY k.id, k.nazwa, k.miasto, k.utworzony_date
        ORDER BY liczba_zawodnikow DESC, k.nazwa
    """)
    
    # Dodaj też podstawową listę nazw klubów
    kluby_nazwy = get_all("SELECT DISTINCT nazwa FROM kluby ORDER BY nazwa")
    nazwy_list = [row["nazwa"] for row in kluby_nazwy]
    
    return jsonify({
        'kluby_szczegoly': rows,
        'nazwy_klubow': nazwy_list,
        'total_klubow': len(rows)
    })

def create_tournament_bracket(zawodnicy_list):
    """
    Tworzy drabinkę turniejową z grupami 4-osobowymi
    Do ćwierćfinałów wchodzi maksymalnie 16 najlepszych zawodników
    Pozostali odpadają z turnieju
    """
    # Sortuj wszystkich zawodników według czasu (najlepsi pierwsi)
    zawodnicy_sorted = sorted(zawodnicy_list, 
        key=lambda x: float(x['czas_przejazdu_s']) if x['czas_przejazdu_s'] else 999999)
    
    # Weź maksymalnie 16 najlepszych do ćwierćfinałów
    max_zawodnikow_cwierćfinaly = 16
    zawodnicy_cwierćfinaly = zawodnicy_sorted[:max_zawodnikow_cwierćfinaly]
    odpadli_zawodnicy = zawodnicy_sorted[max_zawodnikow_cwierćfinaly:]
    
    liczba_zawodnikow_cwierćfinaly = len(zawodnicy_cwierćfinaly)
    
    # Jeśli mniej niż 4 zawodników, wszyscy przechodzą do półfinału
    if liczba_zawodnikow_cwierćfinaly < 4:
        return {
            "ćwierćfinały": [],
            "półfinały": [{"grupa": 1, "zawodnicy": zawodnicy_cwierćfinaly, "awansują": min(2, len(zawodnicy_cwierćfinaly))}],
            "finał": [],
            "odpadli": odpadli_zawodnicy,
            "info": f"Za mało zawodników na ćwierćfinały ({liczba_zawodnikow_cwierćfinaly}/4)",
            "statystyki": {
                "łącznie_zawodników": len(zawodnicy_list),
                "w_ćwierćfinałach": liczba_zawodnikow_cwierćfinaly,
                "odpadło": len(odpadli_zawodnicy),
                "grup_ćwierćfinały": 0,
                "grup_półfinały": 1,
                "grup_finał": 0
            }
        }
    
    # Oblicz liczbę grup w ćwierćfinałach (maksymalnie 4 grupy po 4 zawodników)
    liczba_grup_cwierćfinaly = math.ceil(liczba_zawodnikow_cwierćfinaly / 4)
    
    # Podziel zawodników na grupy 4-osobowe dla ćwierćfinałów
    cwierćfinały = []
    awansujący_do_półfinałów = []
    
    for i in range(liczba_grup_cwierćfinaly):
        start_idx = i * 4
        end_idx = min(start_idx + 4, liczba_zawodnikow_cwierćfinaly)
        grupa_zawodnicy = zawodnicy_cwierćfinaly[start_idx:end_idx]
        
        cwierćfinały.append({
            "grupa": i + 1,
            "zawodnicy": grupa_zawodnicy,
            "awansują": min(2, len(grupa_zawodnicy))
        })
        
        # Dodaj 2 najlepszych z grupy do półfinałów
        liczba_awansujących = min(2, len(grupa_zawodnicy))
        awansujący_do_półfinałów.extend(grupa_zawodnicy[:liczba_awansujących])
    
    # Utwórz grupy półfinałowe z faktycznymi zawodnikami
    liczba_grup_półfinały = math.ceil(len(awansujący_do_półfinałów) / 4)
    półfinały = []
    awansujący_do_finału = []
    
    for i in range(liczba_grup_półfinały):
        start_idx = i * 4
        end_idx = min(start_idx + 4, len(awansujący_do_półfinałów))
        grupa_zawodnicy = awansujący_do_półfinałów[start_idx:end_idx]
        
        # Sortuj zawodników w grupie według czasu
        grupa_zawodnicy_sorted = sorted(grupa_zawodnicy, 
            key=lambda x: float(x['czas_przejazdu_s']) if x['czas_przejazdu_s'] else 999999)
        
        półfinały.append({
            "grupa": i + 1,
            "zawodnicy": grupa_zawodnicy_sorted,
            "awansują": min(2, len(grupa_zawodnicy_sorted))
        })
        
        # Dodaj 2 najlepszych z grupy do finału
        liczba_awansujących = min(2, len(grupa_zawodnicy_sorted))
        awansujący_do_finału.extend(grupa_zawodnicy_sorted[:liczba_awansujących])
    
    # Utwórz finał z faktycznymi zawodnikami
    finał = []
    if len(awansujący_do_finału) >= 2:
        # Sortuj finalistów według czasu
        finaliści_sorted = sorted(awansujący_do_finału, 
            key=lambda x: float(x['czas_przejazdu_s']) if x['czas_przejazdu_s'] else 999999)
        
        finał.append({
            "grupa": 1,
            "zawodnicy": finaliści_sorted,
            "awansują": 1
        })
    
    return {
        "ćwierćfinały": cwierćfinały,
        "półfinały": półfinały,
        "finał": finał,
        "odpadli": odpadli_zawodnicy,
        "statystyki": {
            "łącznie_zawodników": len(zawodnicy_list),
            "w_ćwierćfinałach": liczba_zawodnikow_cwierćfinaly,
            "odpadło": len(odpadli_zawodnicy),
            "grup_ćwierćfinały": len(cwierćfinały),
            "grup_półfinały": len(półfinały),
            "grup_finał": len(finał)
        }
    }

@app.route("/api/drabinka")
def drabinka():
    """Endpoint zwracający drabinkę turniejową z grupami 4-osobowymi"""
    # Pobierz wszystkich zawodników z wynikami (tylko ukończonych)
    zawodnicy = get_all("""
        SELECT z.nr_startowy, z.imie, z.nazwisko, z.kategoria, z.plec, 
               w.czas_przejazdu_s, w.status
        FROM zawodnicy z
        LEFT JOIN wyniki w ON z.nr_startowy = w.nr_startowy
        WHERE z.kategoria IS NOT NULL AND z.plec IS NOT NULL
        AND (w.status = 'FINISHED' OR w.status IS NULL)
        ORDER BY z.kategoria, z.plec, 
                 CASE WHEN w.czas_przejazdu_s IS NOT NULL 
                      THEN CAST(w.czas_przejazdu_s AS FLOAT) 
                      ELSE 999999 END
    """)
    
    # Pogrupuj zawodników według kategorii i płci
    grupy = {}
    
    for zawodnik in zawodnicy:
        kategoria = zawodnik['kategoria']
        plec = zawodnik['plec']
        
        if kategoria not in grupy:
            grupy[kategoria] = {'M': [], 'K': []}
        
        grupy[kategoria][plec].append(zawodnik)
    
    # Utwórz drabinki dla każdej kategorii i płci
    result = {}
    
    for kategoria in grupy:
        result[kategoria] = {}
        
        for plec in ['M', 'K']:
            zawodnicy_plec = grupy[kategoria][plec]
            plec_nazwa = "Mężczyźni" if plec == 'M' else "Kobiety"
            
            # Utwórz drabinkę dla tej grupy
            drabinka_grupa = create_tournament_bracket(zawodnicy_plec)
            result[kategoria][plec_nazwa] = drabinka_grupa
    
    # Dodaj podsumowanie wszystkich kategorii
    result["podsumowanie"] = {
        "wszystkie_kategorie": list(grupy.keys()),
        "łączna_liczba_zawodników": len(zawodnicy),
        "podział_płeć": {
            "mężczyźni": len([z for z in zawodnicy if z['plec'] == 'M']),
            "kobiety": len([z for z in zawodnicy if z['plec'] == 'K'])
        }
    }
    
    return jsonify(result)

@app.route("/api/zawodnicy", methods=['POST'])
def add_zawodnik():
    data = request.get_json()
    nr_startowy = data['nr_startowy']
    imie = data['imie']
    nazwisko = data['nazwisko']
    kategoria = data['kategoria']
    plec = data['plec']
    klub = data['klub']
    
    rowcount = execute_query("""
        INSERT INTO zawodnicy (nr_startowy, imie, nazwisko, kategoria, plec, klub)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (nr_startowy, imie, nazwisko, kategoria, plec, klub))
    
    return jsonify({"message": f"Zawodnik o nr_startowym {nr_startowy} został dodany"}), 201

@app.route("/api/zawodnicy/<int:nr_startowy>", methods=['DELETE'])
def delete_zawodnik(nr_startowy):
    rowcount = execute_query("""
        DELETE FROM zawodnicy WHERE nr_startowy = %s
    """, (nr_startowy,))
    
    return jsonify({"message": f"Zawodnik o nr_startowym {nr_startowy} został usunięty"}), 200

@app.route("/api/zawodnicy/<int:nr_startowy>", methods=['PUT'])
def update_zawodnik(nr_startowy):
    """Aktualizuje dane zawodnika i jego wynik"""
    try:
        data = request.get_json()
        
        # Pobierz dane zawodnika
        new_nr_startowy = data.get('nr_startowy', nr_startowy)
        imie = data.get('imie')
        nazwisko = data.get('nazwisko')
        kategoria = data.get('kategoria')
        plec = data.get('plec')
        klub = data.get('klub')
        
        # Pobierz dane wyniku
        czas_str = data.get('czas_przejazdu')
        status = data.get('status')
        
        # Walidacja formatu czasu
        czas_przejazdu_s = None
        if czas_str:
            try:
                czas_przejazdu_s = validate_time_format(czas_str)
            except ValueError as e:
                return jsonify({"error": str(e)}), 400
        
        # Sprawdź czy nowy nr_startowy nie jest już zajęty (jeśli zmieniony)
        if new_nr_startowy != nr_startowy:
            existing = get_all("SELECT nr_startowy FROM zawodnicy WHERE nr_startowy = %s", (new_nr_startowy,))
            if existing:
                return jsonify({"error": f"Nr startowy {new_nr_startowy} jest już zajęty"}), 400
        
        # Aktualizuj dane zawodnika
        execute_query("""
            UPDATE zawodnicy 
            SET nr_startowy = %s, imie = %s, nazwisko = %s, kategoria = %s, plec = %s, klub = %s
            WHERE nr_startowy = %s
        """, (new_nr_startowy, imie, nazwisko, kategoria, plec, klub, nr_startowy))
        
        # Aktualizuj wynik jeśli podano
        if czas_przejazdu_s is not None or status:
            # Sprawdź czy wynik istnieje
            existing_wynik = get_all("SELECT nr_startowy FROM wyniki WHERE nr_startowy = %s", (new_nr_startowy,))
            
            if existing_wynik:
                # Aktualizuj istniejący wynik
                if czas_przejazdu_s is not None and status:
                    execute_query("""
                        UPDATE wyniki SET czas_przejazdu_s = %s, status = %s WHERE nr_startowy = %s
                    """, (czas_przejazdu_s, status, new_nr_startowy))
                elif czas_przejazdu_s is not None:
                    execute_query("""
                        UPDATE wyniki SET czas_przejazdu_s = %s WHERE nr_startowy = %s
                    """, (czas_przejazdu_s, new_nr_startowy))
                elif status:
                    execute_query("""
                        UPDATE wyniki SET status = %s WHERE nr_startowy = %s
                    """, (status, new_nr_startowy))
            else:
                # Utwórz nowy wynik
                execute_query("""
                    INSERT INTO wyniki (nr_startowy, czas_przejazdu_s, status)
                    VALUES (%s, %s, %s)
                """, (new_nr_startowy, czas_przejazdu_s, status or 'DNF'))
        
        return jsonify({
            "message": f"Zawodnik nr {nr_startowy} został zaktualizowany",
            "new_nr_startowy": new_nr_startowy
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Błąd podczas aktualizacji: {str(e)}"}), 500

@app.route("/api/wyniki", methods=['PUT'])
def update_wynik():
    data = request.get_json()
    nr_startowy = data['nr_startowy']
    czas_przejazdu_s = data['czas_przejazdu_s']
    status = data['status']
    
    rowcount = execute_query("""
        UPDATE wyniki SET czas_przejazdu_s = %s, status = %s WHERE nr_startowy = %s
    """, (czas_przejazdu_s, status, nr_startowy))
    
    return jsonify({"message": f"Wynik o nr_startowym {nr_startowy} został zaktualizowany"}), 200

if __name__ == "__main__":
    # Konfiguracja dla produkcji (Railway, Heroku)
    port = int(os.getenv("PORT", 5000))
    host = os.getenv("HOST", "0.0.0.0")
    debug = os.getenv("FLASK_ENV", "production") == "development"
    
    app.run(host=host, port=port, debug=debug)

