from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
import os
from dotenv import load_dotenv
import math

load_dotenv()
app = Flask(__name__)
CORS(app)

DB_URL = os.getenv("DATABASE_URL")

def get_all(query):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return [dict(zip(columns, row)) for row in rows]

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
    rows = get_all("SELECT * FROM zawodnicy ORDER BY nr_startowy")
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

if __name__ == "__main__":
    app.run(port=5000, debug=True)

