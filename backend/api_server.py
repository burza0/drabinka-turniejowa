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

@app.route("/api/zawodnicy", methods=['POST'])
def add_zawodnik():
    data = request.json
    query = """
        INSERT INTO zawodnicy (nr_startowy, imie, nazwisko, kategoria, plec, klub)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (
        data['nr_startowy'],
        data['imie'],
        data['nazwisko'],
        data['kategoria'],
        data['plec'],
        data.get('klub')  # klub jest opcjonalny
    )
    execute_query(query, params)
    
    # Dodaj rekord do tabeli wyniki
    query_wyniki = """
        INSERT INTO wyniki (nr_startowy, status)
        VALUES (%s, %s)
    """
    execute_query(query_wyniki, (data['nr_startowy'], 'NOT_STARTED'))
    
    return jsonify({"message": "Zawodnik dodany"}), 201

@app.route("/api/zawodnicy/<int:nr_startowy>", methods=['DELETE'])
def delete_zawodnik(nr_startowy):
    query = "DELETE FROM zawodnicy WHERE nr_startowy = %s"
    execute_query(query, (nr_startowy,))
    return jsonify({"message": "Zawodnik usunięty"}), 200

@app.route("/api/zawodnicy/<int:nr_startowy>", methods=['PUT'])
def update_zawodnik(nr_startowy):
    data = request.json
    query = """
        UPDATE zawodnicy 
        SET imie = %s, nazwisko = %s, kategoria = %s, plec = %s, klub = %s
        WHERE nr_startowy = %s
    """
    params = (
        data['imie'],
        data['nazwisko'],
        data['kategoria'],
        data['plec'],
        data.get('klub'),  # klub jest opcjonalny
        nr_startowy
    )
    execute_query(query, params)
    return jsonify({"message": "Zawodnik zaktualizowany"}), 200

@app.route("/api/wyniki", methods=['PUT'])
def update_wynik():
    data = request.json
    nr_startowy = data['nr_startowy']
    czas = data.get('czas_przejazdu_s')
    status = data.get('status')
    
    if czas is not None:
        czas = validate_time_format(czas)
    
    query = """
        UPDATE wyniki 
        SET czas_przejazdu_s = %s, status = %s
        WHERE nr_startowy = %s
    """
    params = (czas, status, nr_startowy)
    execute_query(query, params)
    return jsonify({"message": "Wynik zaktualizowany"}), 200

@app.route("/api/drabinka")
def drabinka():
    """Endpoint zwracający drabinkę turniejową"""
    try:
        # Pobierz wszystkich zawodników z czasami
        zawodnicy_rows = get_all("""
            SELECT z.nr_startowy, z.imie, z.nazwisko, z.kategoria, z.plec, z.klub,
                   w.czas_przejazdu_s, w.status
            FROM zawodnicy z
            LEFT JOIN wyniki w ON z.nr_startowy = w.nr_startowy
            WHERE z.kategoria IS NOT NULL AND z.plec IS NOT NULL
            ORDER BY z.kategoria, z.plec, w.czas_przejazdu_s ASC NULLS LAST
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
        
        # Organizuj zawodników według kategorii i płci
        kategorie_dict = {}
        for zawodnik in zawodnicy_rows:
            kategoria = zawodnik['kategoria']
            plec = "Mężczyźni" if zawodnik['plec'] == 'M' else "Kobiety"
            
            if kategoria not in kategorie_dict:
                kategorie_dict[kategoria] = {}
            if plec not in kategorie_dict[kategoria]:
                kategorie_dict[kategoria][plec] = []
            
            kategorie_dict[kategoria][plec].append(zawodnik)
        
        # Generuj drabinkę dla każdej kategorii/płci
        drabinka_data = {}
        total_w_cwierćfinałach = 0
        total_mezczyzni = 0
        total_kobiety = 0
        
        for kategoria, plcie in kategorie_dict.items():
            drabinka_data[kategoria] = {}
            
            for plec, zawodnicy_list in plcie.items():
                if plec == "Mężczyźni":
                    total_mezczyzni += len(zawodnicy_list)
                else:
                    total_kobiety += len(zawodnicy_list)
                
                # Filtruj zawodników z czasami (FINISHED)
                zawodnicy_z_czasami = [z for z in zawodnicy_list if z['czas_przejazdu_s'] is not None and z['status'] == 'FINISHED']
                
                if len(zawodnicy_z_czasami) < 4:
                    # Za mało zawodników do drabinki
                    drabinka_data[kategoria][plec] = {
                        "info": f"Za mało zawodników z czasami ({len(zawodnicy_z_czasami)}/4) do utworzenia drabinki",
                        "statystyki": {
                            "łącznie_zawodników": len(zawodnicy_list),
                            "z_czasami": len(zawodnicy_z_czasami),
                            "w_ćwierćfinałach": 0,
                            "grup_ćwierćfinały": 0,
                            "grup_półfinały": 0,
                            "grup_finał": 0
                        }
                    }
                    continue
                
                # Weź maksymalnie 16 najlepszych (najszybszych)
                najlepsi = zawodnicy_z_czasami[:16]
                w_cwierćfinałach = len(najlepsi)
                total_w_cwierćfinałach += w_cwierćfinałach
                
                # Podziel na grupy po 4
                grupy_ćwierćfinały = []
                for i in range(0, len(najlepsi), 4):
                    grupa = najlepsi[i:i+4]
                    if len(grupa) >= 4:  # Tylko pełne grupy
                        grupy_ćwierćfinały.append({
                            "grupa": f"Ć{len(grupy_ćwierćfinały) + 1}",
                            "awansują": 2,
                            "zawodnicy": grupa
                        })
                
                # Wygeneruj półfinały (zwycięzcy + drudzy z ćwierćfinałów)
                półfinałowcy = []
                for grupa in grupy_ćwierćfinały:
                    # Awansują 2 najlepszych z każdej grupy
                    półfinałowcy.extend(grupa["zawodnicy"][:2])
                
                grupy_półfinały = []
                for i in range(0, len(półfinałowcy), 4):
                    grupa = półfinałowcy[i:i+4]
                    if len(grupa) >= 4:
                        grupy_półfinały.append({
                            "grupa": f"P{len(grupy_półfinały) + 1}",
                            "awansują": 2,
                            "zawodnicy": grupa
                        })
                    elif len(grupa) > 0:
                        # Niepełna grupa w półfinałach
                        grupy_półfinały.append({
                            "grupa": f"P{len(grupy_półfinały) + 1}",
                            "awansują": min(2, len(grupa)),
                            "zawodnicy": grupa
                        })
                
                # Wygeneruj finał
                finałowcy = []
                for grupa in grupy_półfinały:
                    awansuje = grupa["awansują"]
                    finałowcy.extend(grupa["zawodnicy"][:awansuje])
                
                grupy_finał = []
                if len(finałowcy) >= 4:
                    grupy_finał.append({
                        "grupa": "F1",
                        "awansują": 4,  # Wszyscy w finale mają miejsca 1-4
                        "zawodnicy": finałowcy[:4]
                    })
                elif len(finałowcy) > 0:
                    grupy_finał.append({
                        "grupa": "F1",
                        "awansują": len(finałowcy),
                        "zawodnicy": finałowcy
                    })
                
                drabinka_data[kategoria][plec] = {
                    "statystyki": {
                        "łącznie_zawodników": len(zawodnicy_list),
                        "z_czasami": len(zawodnicy_z_czasami),
                        "w_ćwierćfinałach": w_cwierćfinałach,
                        "grup_ćwierćfinały": len(grupy_ćwierćfinały),
                        "grup_półfinały": len(grupy_półfinały),
                        "grup_finał": len(grupy_finał)
                    },
                    "ćwierćfinały": grupy_ćwierćfinały,
                    "półfinały": grupy_półfinały,
                    "finał": grupy_finał
                }
        
        # Dodaj podsumowanie
        wszystkie_kategorie = list(kategorie_dict.keys())
        łączna_liczba = sum(len(plcie) for kategoria in kategorie_dict.values() for plcie in kategoria.values())
        
        result = {
            "podsumowanie": {
                "wszystkie_kategorie": sorted(wszystkie_kategorie),
                "łączna_liczba_zawodników": łączna_liczba,
                "w_ćwierćfinałach": total_w_cwierćfinałach,
                "podział_płeć": {
                    "mężczyźni": total_mezczyzni,
                    "kobiety": total_kobiety
                }
            }
        }
        
        # Dodaj dane kategorii
        result.update(drabinka_data)
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Błąd w endpoincie drabinki: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 