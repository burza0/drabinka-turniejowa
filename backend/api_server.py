from flask import Flask, jsonify, request, send_from_directory
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
    """Serwuje frontend Vue 3"""
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'dist')
    return send_from_directory(frontend_path, 'index.html')

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
        SELECT z.nr_startowy, z.imie, z.nazwisko, z.kategoria, z.plec, z.klub, z.qr_code,
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

@app.route("/api/zawodnicy/<int:nr_startowy>", methods=['GET'])
def get_zawodnik(nr_startowy):
    """Endpoint do pobierania pojedynczego zawodnika dla podglądu"""
    try:
        rows = get_all("""
            SELECT z.nr_startowy, z.imie, z.nazwisko, z.kategoria, z.plec, z.klub, 
                   z.qr_code, z.checked_in, z.check_in_time,
                   CASE WHEN w.czas_przejazdu_s IS NOT NULL THEN true ELSE false END as ma_wynik
            FROM zawodnicy z
            LEFT JOIN wyniki w ON z.nr_startowy = w.nr_startowy
            WHERE z.nr_startowy = %s
        """, (nr_startowy,))
        
        if not rows:
            return jsonify({
                "success": False,
                "message": f"Nie znaleziono zawodnika z numerem startowym {nr_startowy}"
            }), 404
        
        zawodnik = rows[0]
        
        return jsonify({
            "success": True,
            "zawodnik": {
                "nr_startowy": zawodnik["nr_startowy"],
                "imie": zawodnik["imie"],
                "nazwisko": zawodnik["nazwisko"],
                "kategoria": zawodnik["kategoria"],
                "plec": zawodnik["plec"],
                "klub": zawodnik["klub"],
                "qr_code": bool(zawodnik["qr_code"]),
                "checked_in": bool(zawodnik["checked_in"]),
                "check_in_time": zawodnik["check_in_time"],
                "ma_wynik": zawodnik["ma_wynik"]
            }
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Błąd podczas pobierania zawodnika: {str(e)}"
        }), 500

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

@app.route("/api/qr/check-in", methods=['POST'])
def qr_check_in():
    """Endpoint do zameldowania zawodnika poprzez QR kod lub ręcznie"""
    try:
        data = request.json
        qr_code = data.get('qr_code')
        nr_startowy = data.get('nr_startowy')
        manual = data.get('manual', False)
        reason = data.get('reason')  # powód ręcznego zameldowania
        description = data.get('description')  # opis szczegółowy
        device_id = data.get('device_id', 'unknown')
        
        if not qr_code and not nr_startowy:
            return jsonify({"error": "Brak QR kodu lub numeru startowego"}), 400
        
        # Znajdź zawodnika po QR kodzie lub numerze startowym
        if qr_code:
            zawodnik = get_all("""
                SELECT nr_startowy, imie, nazwisko, kategoria, plec, klub, checked_in
                FROM zawodnicy 
                WHERE qr_code = %s
            """, (qr_code,))
        else:
            zawodnik = get_all("""
                SELECT nr_startowy, imie, nazwisko, kategoria, plec, klub, checked_in
                FROM zawodnicy 
                WHERE nr_startowy = %s
            """, (nr_startowy,))
        
        if not zawodnik:
            if qr_code:
                return jsonify({"error": "Nie znaleziono zawodnika o tym QR kodzie"}), 404
            else:
                return jsonify({
                    "success": False,
                    "message": f"Nie znaleziono zawodnika z numerem startowym {nr_startowy}"
                }), 404
        
        zawodnik = zawodnik[0]
        
        if zawodnik['checked_in']:
            return jsonify({
                "success": False, 
                "message": "Zawodnik już zameldowany",
                "zawodnik": zawodnik
            }), 200
        
        # Zamelduj zawodnika
        execute_query("""
            UPDATE zawodnicy 
            SET checked_in = TRUE, check_in_time = CURRENT_TIMESTAMP 
            WHERE nr_startowy = %s
        """, (zawodnik['nr_startowy'],))
        
        # Przygotuj checkpoint_name z dodatkowym oznaczeniem ręcznego zameldowania
        checkpoint_name = 'check-in'
        if manual:
            checkpoint_name = 'manual-check-in'
        
        # Zapisz checkpoint z dodatkowymi danymi dla ręcznego zameldowania
        checkpoint_qr = qr_code if qr_code else f"MANUAL_{zawodnik['nr_startowy']}"
        
        execute_query("""
            INSERT INTO checkpoints (nr_startowy, checkpoint_name, qr_code, device_id)
            VALUES (%s, %s, %s, %s)
        """, (zawodnik['nr_startowy'], checkpoint_name, checkpoint_qr, device_id))
        
        # Jeśli to ręczne zameldowanie, zapisz dodatkowe informacje w logach
        if manual and reason:
            try:
                log_entry = f"MANUAL CHECK-IN: {zawodnik['imie']} {zawodnik['nazwisko']} (#{zawodnik['nr_startowy']}) - Reason: {reason}"
                if description:
                    log_entry += f" - Description: {description}"
                print(f"[MANUAL CHECK-IN] {log_entry}")
                
                # Możesz dodać zapis do osobnej tabeli logów jeśli masz
                # execute_query("""
                #     INSERT INTO manual_logs (nr_startowy, action, reason, description, timestamp)
                #     VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
                # """, (zawodnik['nr_startowy'], 'manual-check-in', reason, description))
                
            except Exception as log_error:
                print(f"Warning: Could not log manual check-in: {log_error}")
        
        zawodnik['checked_in'] = True
        
        message = f"Zawodnik {zawodnik['imie']} {zawodnik['nazwisko']} zameldowany pomyślnie"
        if manual:
            message += " (ręcznie)"
        
        return jsonify({
            "success": True,
            "message": message,
            "zawodnik": zawodnik,
            "manual": manual,
            "reason": reason if manual else None
        }), 200
        
    except Exception as e:
        print(f"Błąd w check-in: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/qr/scan-result", methods=['POST'])
def qr_scan_result():
    """Endpoint do zapisania wyniku zawodnika poprzez QR kod"""
    try:
        data = request.json
        qr_code = data.get('qr_code')
        czas = data.get('czas')  # może być timestamp lub MM:SS.ms
        status = data.get('status', 'FINISHED')
        checkpoint = data.get('checkpoint', 'finish')
        
        if not qr_code:
            return jsonify({"error": "Brak QR kodu"}), 400
        
        # Znajdź zawodnika po QR kodzie
        zawodnik = get_all("""
            SELECT nr_startowy, imie, nazwisko, kategoria, plec, klub
            FROM zawodnicy 
            WHERE qr_code = %s
        """, (qr_code,))
        
        if not zawodnik:
            return jsonify({"error": "Nie znaleziono zawodnika o tym QR kodzie"}), 404
        
        zawodnik = zawodnik[0]
        
        # Przetwórz czas
        if czas:
            try:
                # Jeśli to timestamp, konwertuj na sekundy
                if isinstance(czas, (int, float)):
                    # Assume timestamp in milliseconds
                    czas_s = float(czas) / 1000 if czas > 1000000 else float(czas)
                else:
                    # Jeśli to string, użyj validate_time_format
                    czas_s = validate_time_format(str(czas))
            except Exception as e:
                return jsonify({"error": f"Nieprawidłowy format czasu: {e}"}), 400
        else:
            czas_s = None
        
        # Zapisz wynik
        execute_query("""
            UPDATE wyniki 
            SET czas_przejazdu_s = %s, status = %s
            WHERE nr_startowy = %s
        """, (czas_s, status, zawodnik['nr_startowy']))
        
        # Zapisz checkpoint
        execute_query("""
            INSERT INTO checkpoints (nr_startowy, checkpoint_name, qr_code, device_id)
            VALUES (%s, %s, %s, %s)
        """, (zawodnik['nr_startowy'], checkpoint, qr_code, data.get('device_id', 'unknown')))
        
        return jsonify({
            "success": True,
            "message": f"Wynik dla {zawodnik['imie']} {zawodnik['nazwisko']} zapisany",
            "zawodnik": zawodnik,
            "czas": czas_s,
            "status": status
        }), 200
        
    except Exception as e:
        print(f"Błąd w scan-result: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/qr/verify-result", methods=['POST'])
def qr_verify_result():
    """Endpoint do weryfikacji wyniku zawodnika poprzez QR kod"""
    try:
        data = request.json
        qr_code = data.get('qr_code')
        
        if not qr_code:
            return jsonify({"error": "Brak QR kodu"}), 400
        
        # Znajdź zawodnika z wynikiem
        zawodnik_data = get_all("""
            SELECT z.nr_startowy, z.imie, z.nazwisko, z.kategoria, z.plec, z.klub,
                   z.checked_in, z.check_in_time,
               w.czas_przejazdu_s, w.status
        FROM zawodnicy z
        LEFT JOIN wyniki w ON z.nr_startowy = w.nr_startowy
            WHERE z.qr_code = %s
        """, (qr_code,))
        
        if not zawodnik_data:
            return jsonify({"error": "Nie znaleziono zawodnika o tym QR kodzie"}), 404
        
        zawodnik = zawodnik_data[0]
        
        # Sprawdź pozycję w kategorii
        if zawodnik['czas_przejazdu_s'] and zawodnik['status'] == 'FINISHED':
            pozycja_data = get_all("""
                SELECT COUNT(*) + 1 as pozycja
                FROM zawodnicy z
                JOIN wyniki w ON z.nr_startowy = w.nr_startowy
                WHERE z.kategoria = %s AND z.plec = %s 
                AND w.status = 'FINISHED' 
                AND w.czas_przejazdu_s < %s
            """, (zawodnik['kategoria'], zawodnik['plec'], zawodnik['czas_przejazdu_s']))
            
            pozycja = pozycja_data[0]['pozycja'] if pozycja_data else None
        else:
            pozycja = None
        
        # Sprawdź awans do drabinki (top 16 w kategorii/płci)
        awans_data = get_all("""
            SELECT COUNT(*) as lepszych
            FROM zawodnicy z
            JOIN wyniki w ON z.nr_startowy = w.nr_startowy
            WHERE z.kategoria = %s AND z.plec = %s 
            AND w.status = 'FINISHED' 
            AND w.czas_przejazdu_s < %s
        """, (zawodnik['kategoria'], zawodnik['plec'], zawodnik['czas_przejazdu_s'])) if zawodnik['czas_przejazdu_s'] else []
        
        awans_do_drabinki = (awans_data[0]['lepszych'] < 16) if awans_data and zawodnik['czas_przejazdu_s'] else False
        
        return jsonify({
            "success": True,
            "zawodnik": {
                "nr_startowy": zawodnik['nr_startowy'],
                "imie": zawodnik['imie'],
                "nazwisko": zawodnik['nazwisko'],
                "kategoria": zawodnik['kategoria'],
                "plec": zawodnik['plec'],
                "klub": zawodnik['klub'],
                "checked_in": zawodnik['checked_in'],
                "check_in_time": zawodnik['check_in_time'].isoformat() if zawodnik['check_in_time'] else None
            },
            "wynik": {
                "czas_przejazdu_s": zawodnik['czas_przejazdu_s'],
                "status": zawodnik['status'],
                "pozycja_w_kategorii": pozycja,
                "awans_do_drabinki": awans_do_drabinki
            }
        }), 200
        
    except Exception as e:
        print(f"Błąd w verify-result: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/qr/generate/<int:nr_startowy>", methods=['POST'])
def qr_generate_for_zawodnik(nr_startowy):
    """Endpoint do generowania QR kodu dla konkretnego zawodnika"""
    try:
        import qrcode
        import uuid
        import base64
        from io import BytesIO
        
        # Znajdź zawodnika
        zawodnik_data = get_all("""
            SELECT nr_startowy, imie, nazwisko, qr_code
            FROM zawodnicy 
            WHERE nr_startowy = %s
        """, (nr_startowy,))
        
        if not zawodnik_data:
            return jsonify({"error": "Nie znaleziono zawodnika"}), 404
        
        zawodnik = zawodnik_data[0]
        
        # Jeśli już ma QR kod, zwróć istniejący
        if zawodnik['qr_code']:
            qr_data = zawodnik['qr_code']
        else:
            # Wygeneruj nowy QR kod
            unique_hash = uuid.uuid4().hex[:8].upper()
            qr_data = f"SKATECROSS_{nr_startowy}_{unique_hash}"
            
            # Zapisz do bazy
            execute_query("""
                UPDATE zawodnicy SET qr_code = %s WHERE nr_startowy = %s
            """, (qr_data, nr_startowy))
        
        # Wygeneruj obraz QR kodu
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Konwertuj do base64
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        
        return jsonify({
            "success": True,
            "zawodnik": zawodnik,
            "qr_code": qr_data,
            "qr_image": f"data:image/png;base64,{img_base64}"
        }), 200
        
    except Exception as e:
        print(f"Błąd w generate QR: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/qr/stats")
def qr_stats():
    """Endpoint zwracający statystyki QR kodów"""
    try:
        # Podstawowe statystyki
        total_data = get_all("SELECT COUNT(*) as total FROM zawodnicy")
        total = total_data[0]['total'] if total_data else 0
        
        with_qr_data = get_all("SELECT COUNT(*) as with_qr FROM zawodnicy WHERE qr_code IS NOT NULL")
        with_qr = with_qr_data[0]['with_qr'] if with_qr_data else 0
        
        checked_in_data = get_all("SELECT COUNT(*) as checked_in FROM zawodnicy WHERE checked_in = TRUE")
        checked_in = checked_in_data[0]['checked_in'] if checked_in_data else 0
        
        # Statystyki checkpointów
        checkpoint_stats = get_all("""
            SELECT checkpoint_name, COUNT(*) as count
            FROM checkpoints
            GROUP BY checkpoint_name
            ORDER BY count DESC
        """)
        
        return jsonify({
            "total_zawodnikow": total,
            "z_qr_kodami": with_qr,
            "zameldowanych": checked_in,
            "bez_qr_kodow": total - with_qr,
            "procent_zameldowanych": round((checked_in / total * 100), 1) if total > 0 else 0,
            "checkpoints": checkpoint_stats
        }), 200
        
    except Exception as e:
        print(f"Błąd w QR stats: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/qr-scanner")
@app.route("/qr-scanner/")
def qr_scanner():
    """Serwuje QR Scanner aplikację"""
    qr_scanner_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'qr-scanner')
    return send_from_directory(qr_scanner_path, 'index.html')

@app.route("/qr-scanner/<path:filename>")
def qr_scanner_static(filename):
    """Serwuje statyczne pliki QR Scanner"""
    qr_scanner_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'qr-scanner')
    return send_from_directory(qr_scanner_path, filename)

@app.route("/<path:filename>")
def frontend_static(filename):
    """Serwuje statyczne pliki frontendu"""
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'dist')
    try:
        return send_from_directory(frontend_path, filename)
    except FileNotFoundError:
        # Dla Vue Router - zwróć index.html dla nieznanych ścieżek
        return send_from_directory(frontend_path, 'index.html')

@app.route("/api/qr/dashboard")
def qr_dashboard():
    """Endpoint dla QR Admin Dashboard - kompleksowe statystyki"""
    try:
        # Podstawowe statystyki
        basic_stats = get_all("""
            SELECT 
                COUNT(*) as total_zawodnikow,
                COUNT(CASE WHEN qr_code IS NOT NULL THEN 1 END) as z_qr_kodami,
                COUNT(CASE WHEN checked_in = TRUE THEN 1 END) as zameldowanych,
                COUNT(CASE WHEN qr_code IS NULL THEN 1 END) as bez_qr_kodow
            FROM zawodnicy
        """)[0]
        
        # Statystyki według kategorii
        category_stats = get_all("""
            SELECT 
                kategoria,
                COUNT(*) as total,
                COUNT(CASE WHEN checked_in = TRUE THEN 1 END) as zameldowanych,
                COUNT(CASE WHEN w.status = 'FINISHED' THEN 1 END) as z_wynikami
            FROM zawodnicy z
            LEFT JOIN wyniki w ON z.nr_startowy = w.nr_startowy
            GROUP BY kategoria
            ORDER BY kategoria
        """)
        
        # Ostatnie checkpointy
        recent_checkpoints = get_all("""
            SELECT 
                c.nr_startowy,
                z.imie,
                z.nazwisko,
                z.kategoria,
                c.checkpoint_name,
                c.timestamp,
                c.device_id
            FROM checkpoints c
            JOIN zawodnicy z ON c.nr_startowy = z.nr_startowy
            ORDER BY c.timestamp DESC
            LIMIT 20
        """)
        
        # Aktywność urządzeń (ostatnie 24h)
        device_activity = get_all("""
            SELECT 
                device_id,
                COUNT(*) as total_scans,
                MAX(timestamp) as last_activity,
                COUNT(CASE WHEN checkpoint_name = 'check-in' THEN 1 END) as check_ins,
                COUNT(CASE WHEN checkpoint_name = 'finish' THEN 1 END) as results
            FROM checkpoints
            WHERE timestamp >= NOW() - INTERVAL '24 hours'
            GROUP BY device_id
            ORDER BY last_activity DESC
        """)
        
        # Postęp zawodów według godzin (dzisiaj)
        hourly_progress = get_all("""
            SELECT 
                DATE_TRUNC('hour', timestamp) as hour,
                COUNT(*) as scans,
                COUNT(CASE WHEN checkpoint_name = 'check-in' THEN 1 END) as check_ins,
                COUNT(CASE WHEN checkpoint_name = 'finish' THEN 1 END) as results
            FROM checkpoints
            WHERE timestamp >= CURRENT_DATE
            GROUP BY DATE_TRUNC('hour', timestamp)
            ORDER BY hour
        """)
        
        # Problematyczne sytuacje
        issues = []
        
        # Zawodnicy zameldowani ale bez wyników (po 2h od check-in)
        no_results = get_all("""
            SELECT 
                z.nr_startowy,
                z.imie,
                z.nazwisko,
                z.kategoria,
                z.check_in_time
            FROM zawodnicy z
            LEFT JOIN wyniki w ON z.nr_startowy = w.nr_startowy
            WHERE z.checked_in = TRUE 
            AND w.status IS NULL
            AND z.check_in_time < NOW() - INTERVAL '2 hours'
            LIMIT 10
        """)
        
        if no_results:
            issues.append({
                "type": "no_results",
                "title": "Zawodnicy bez wyników (>2h od check-in)",
                "count": len(no_results),
                "details": no_results
            })
        
        # Duplikaty QR kodów
        duplicate_qr = get_all("""
            SELECT qr_code, COUNT(*) as count
            FROM zawodnicy
            WHERE qr_code IS NOT NULL
            GROUP BY qr_code
            HAVING COUNT(*) > 1
        """)
        
        if duplicate_qr:
            issues.append({
                "type": "duplicate_qr",
                "title": "Duplikaty QR kodów",
                "count": len(duplicate_qr),
                "details": duplicate_qr
            })
        
        return jsonify({
            "success": True,
            "basic_stats": basic_stats,
            "category_stats": category_stats,
            "recent_checkpoints": recent_checkpoints,
            "device_activity": device_activity,
            "hourly_progress": hourly_progress,
            "issues": issues,
            "timestamp": __import__('datetime').datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        print(f"Błąd w QR dashboard: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/qr/live-feed")
def qr_live_feed():
    """Endpoint dla live feed ostatnich aktywności QR"""
    try:
        # Ostatnie 50 skanów
        live_feed = get_all("""
            SELECT 
                c.nr_startowy,
                z.imie,
                z.nazwisko,
                z.kategoria,
                z.plec,
                c.checkpoint_name,
                c.timestamp,
                c.device_id,
                w.czas_przejazdu_s,
                w.status
            FROM checkpoints c
            JOIN zawodnicy z ON c.nr_startowy = z.nr_startowy
            LEFT JOIN wyniki w ON z.nr_startowy = w.nr_startowy
            ORDER BY c.timestamp DESC
            LIMIT 50
        """)
        
        return jsonify({
            "success": True,
            "feed": live_feed,
            "timestamp": __import__('datetime').datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        print(f"Błąd w live feed: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/qr/devices")
def qr_devices():
    """Endpoint listujący aktywne urządzenia skanujące"""
    try:
        devices = get_all("""
            SELECT 
                device_id,
                COUNT(*) as total_scans,
                MIN(timestamp) as first_scan,
                MAX(timestamp) as last_scan,
                COUNT(DISTINCT nr_startowy) as unique_zawodnicy,
                COUNT(CASE WHEN checkpoint_name = 'check-in' THEN 1 END) as check_ins,
                COUNT(CASE WHEN checkpoint_name = 'finish' THEN 1 END) as results,
                COUNT(CASE WHEN checkpoint_name = 'verify' THEN 1 END) as verifications
            FROM checkpoints
            GROUP BY device_id
            ORDER BY last_scan DESC
        """)
        
        return jsonify({
            "success": True,
            "devices": devices,
            "timestamp": __import__('datetime').datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        print(f"Błąd w devices: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/qr/export")
def qr_export():
    """Endpoint do eksportu danych QR do CSV"""
    try:
        import csv
        import io
        
        # Eksport wszystkich checkpointów
        checkpoints = get_all("""
            SELECT 
                c.nr_startowy,
                z.imie,
                z.nazwisko,
                z.kategoria,
                z.plec,
                z.klub,
                c.checkpoint_name,
                c.timestamp,
                c.device_id,
                c.qr_code
            FROM checkpoints c
            JOIN zawodnicy z ON c.nr_startowy = z.nr_startowy
            ORDER BY c.timestamp DESC
        """)
        
        # Tworzenie CSV
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Nagłówki
        writer.writerow([
            'Nr', 'Imię', 'Nazwisko', 'Kategoria', 'Płeć', 'Klub',
            'Checkpoint', 'Czas skanu', 'Urządzenie', 'QR Kod'
        ])
        
        # Dane
        for checkpoint in checkpoints:
            writer.writerow([
                checkpoint['nr_startowy'],
                checkpoint['imie'],
                checkpoint['nazwisko'],
                checkpoint['kategoria'],
                checkpoint['plec'],
                checkpoint['klub'] or '',
                checkpoint['checkpoint_name'],
                checkpoint['timestamp'].isoformat() if checkpoint['timestamp'] else '',
                checkpoint['device_id'] or '',
                checkpoint['qr_code'] or ''
            ])
        
        # Zwróć jako plik CSV
        output.seek(0)
        
        from flask import Response
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={
                'Content-Disposition': f'attachment; filename=qr_checkpoints_{__import__("datetime").datetime.now().strftime("%Y%m%d_%H%M")}.csv'
            }
        )
        
    except Exception as e:
        print(f"Błąd w export: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/qr/generate-bulk", methods=['POST'])
def qr_generate_bulk():
    """Endpoint do grupowego generowania QR kodów dla wybranych zawodników"""
    try:
        import qrcode
        import uuid
        import base64
        from io import BytesIO
        
        data = request.json
        zawodnicy_ids = data.get('zawodnicy_ids', [])
        
        if not zawodnicy_ids:
            return jsonify({"error": "Brak wybranych zawodników"}), 400
        
        # Znajdź zawodników
        placeholders = ','.join(['%s'] * len(zawodnicy_ids))
        zawodnicy_data = get_all(f"""
            SELECT nr_startowy, imie, nazwisko, kategoria, plec, klub, qr_code
            FROM zawodnicy 
            WHERE nr_startowy IN ({placeholders})
            ORDER BY nr_startowy
        """, zawodnicy_ids)
        
        if not zawodnicy_data:
            return jsonify({"error": "Nie znaleziono zawodników"}), 404
        
        results = []
        
        for zawodnik in zawodnicy_data:
            nr_startowy = zawodnik['nr_startowy']
            
            # Sprawdź czy już ma QR kod
            if zawodnik['qr_code']:
                qr_data = zawodnik['qr_code']
            else:
                # Wygeneruj nowy QR kod
                unique_hash = uuid.uuid4().hex[:8].upper()
                qr_data = f"SKATECROSS_{nr_startowy}_{unique_hash}"
                
                # Zapisz do bazy
                execute_query("""
                    UPDATE zawodnicy SET qr_code = %s WHERE nr_startowy = %s
                """, (qr_data, nr_startowy))
                zawodnik['qr_code'] = qr_data
            
            # Wygeneruj obraz QR kodu
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=8,
                border=2,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Konwertuj do base64
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            img_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            results.append({
                "zawodnik": zawodnik,
                "qr_code": qr_data,
                "qr_image": f"data:image/png;base64,{img_base64}"
            })
        
        return jsonify({
            "success": True,
            "count": len(results),
            "qr_codes": results
        }), 200
        
    except Exception as e:
        print(f"Błąd w bulk generate QR: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/grupy-startowe")
def grupy_startowe():
    """Endpoint zwracający grupy startowe na podstawie zameldowanych zawodników"""
    try:
        # Pobierz zameldowanych zawodników pogrupowanych
        grupy_data = get_all("""
            SELECT 
                kategoria,
                plec,
                COUNT(*) as liczba_zameldowanych,
                STRING_AGG(
                    CONCAT(nr_startowy, ': ', imie, ' ', nazwisko, ' (', klub, ')'), 
                    E'\n' ORDER BY nr_startowy
                ) as lista_zawodnikow,
                STRING_AGG(nr_startowy::text, ',' ORDER BY nr_startowy) as numery_startowe
            FROM zawodnicy 
            WHERE checked_in = TRUE AND kategoria IS NOT NULL
            GROUP BY kategoria, plec 
            ORDER BY kategoria, plec
        """)
        
        # Organizuj w grupy startowe
        grupy_startowe = []
        numer_grupy = 1
        
        for grupa in grupy_data:
            nazwa_grupy = f"Grupa {numer_grupy}: {grupa['kategoria']} {'Mężczyźni' if grupa['plec'] == 'M' else 'Kobiety'}"
            
            grupy_startowe.append({
                "numer_grupy": numer_grupy,
                "nazwa": nazwa_grupy,
                "kategoria": grupa['kategoria'],
                "plec": grupa['plec'],
                "liczba_zawodnikow": grupa['liczba_zameldowanych'],
                "lista_zawodnikow": grupa['lista_zawodnikow'],
                "numery_startowe": grupa['numery_startowe'],
                "estimated_time": grupa['liczba_zameldowanych'] * 20, # sekundy (20s na zawodnika)
                "status": "OCZEKUJE" # OCZEKUJE, AKTYWNA, UKONCZONA
            })
            numer_grupy += 1
        
        return jsonify({
            "success": True,
            "total_grup": len(grupy_startowe),
            "total_zawodnikow": sum(g['liczba_zawodnikow'] for g in grupy_startowe),
            "grupy": grupy_startowe,
            "estimated_total_time_min": sum(g['estimated_time'] for g in grupy_startowe) / 60
        }), 200
        
    except Exception as e:
        print(f"Błąd w grupy-startowe: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/grupa-aktywna", methods=['POST'])
def set_grupa_aktywna():
    """Ustawienie aktywnej grupy startowej"""
    try:
        data = request.json
        numer_grupy = data.get('numer_grupy')
        kategoria = data.get('kategoria')
        plec = data.get('plec')
        
        if not all([numer_grupy, kategoria, plec]):
            return jsonify({"error": "Brak wymaganych danych"}), 400
        
        # Tu można dodać logikę zapisywania aktywnej grupy do cache/bazy
        # Na razie zwracamy potwierdzenie
        
        return jsonify({
            "success": True,
            "message": f"Grupa {numer_grupy} ({kategoria} {plec}) ustawiona jako aktywna",
            "aktywna_grupa": {
                "numer": numer_grupy,
                "kategoria": kategoria,
                "plec": plec
            }
        }), 200
        
    except Exception as e:
        print(f"Błąd w set-grupa-aktywna: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/start-line-verify", methods=['POST'])
def start_line_verify():
    """Weryfikacja zawodnika na linii startu poprzez QR kod"""
    try:
        data = request.json
        qr_code = data.get('qr_code')
        expected_kategoria = data.get('kategoria')  # opcjonalne - aktywna grupa
        expected_plec = data.get('plec')  # opcjonalne - aktywna grupa
        
        if not qr_code:
            return jsonify({"error": "Brak QR kodu"}), 400
        
        # Znajdź zawodnika
        zawodnik_data = get_all("""
            SELECT z.nr_startowy, z.imie, z.nazwisko, z.kategoria, z.plec, z.klub,
                   z.checked_in, z.check_in_time,
                   w.czas_przejazdu_s, w.status
            FROM zawodnicy z
            LEFT JOIN wyniki w ON z.nr_startowy = w.nr_startowy
            WHERE z.qr_code = %s
        """, (qr_code,))
        
        if not zawodnik_data:
            return jsonify({
                "success": False,
                "error": "Nie znaleziono zawodnika o tym QR kodzie",
                "action": "ODRZUC"
            }), 404
        
        zawodnik = zawodnik_data[0]
        
        # Sprawdzenia weryfikacyjne
        issues = []
        action = "AKCEPTUJ"
        
        # 1. Czy zameldowany?
        if not zawodnik['checked_in']:
            issues.append("❌ Zawodnik nie jest zameldowany")
            action = "ODRZUC"
        
        # 2. Czy już ma wynik?
        if zawodnik['czas_przejazdu_s'] is not None:
            issues.append("⚠️ Zawodnik już ma zapisany wynik")
            action = "OSTRZEZENIE"
        
        # 3. Czy pasuje do aktywnej grupy?
        if expected_kategoria and zawodnik['kategoria'] != expected_kategoria:
            issues.append(f"⚠️ Zawodnik z kategorii {zawodnik['kategoria']}, oczekiwano {expected_kategoria}")
            action = "OSTRZEZENIE"
            
        if expected_plec and zawodnik['plec'] != expected_plec:
            issues.append(f"⚠️ Zawodnik płci {zawodnik['plec']}, oczekiwano {expected_plec}")
            action = "OSTRZEZENIE"
        
        # Zapisz checkpoint 'start-line' 
        execute_query("""
            INSERT INTO checkpoints (nr_startowy, checkpoint_name, qr_code, device_id)
            VALUES (%s, %s, %s, %s)
        """, (zawodnik['nr_startowy'], 'start-line-verify', qr_code, data.get('device_id', 'start-device')))
        
        return jsonify({
            "success": True,
            "action": action,  # AKCEPTUJ, OSTRZEZENIE, ODRZUC
            "issues": issues,
            "zawodnik": {
                "nr_startowy": zawodnik['nr_startowy'],
                "imie": zawodnik['imie'],
                "nazwisko": zawodnik['nazwisko'],
                "kategoria": zawodnik['kategoria'],
                "plec": zawodnik['plec'],
                "klub": zawodnik['klub'],
                "checked_in": zawodnik['checked_in'],
                "ma_wynik": zawodnik['czas_przejazdu_s'] is not None,
                "status": zawodnik['status']
            },
            "komunikat": {
                "AKCEPTUJ": f"✅ {zawodnik['imie']} {zawodnik['nazwisko']} - GOTOWY DO STARTU",
                "OSTRZEZENIE": f"⚠️ {zawodnik['imie']} {zawodnik['nazwisko']} - SPRAWDŹ SZCZEGÓŁY",
                "ODRZUC": f"❌ {zawodnik['imie']} {zawodnik['nazwisko']} - NIE MOŻE STARTOWAĆ"
            }[action]
        }), 200
        
    except Exception as e:
        print(f"Błąd w start-line-verify: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/start-queue", methods=['GET'])
def get_start_queue():
    """Pobierz kolejkę zawodników oczekujących na starcie"""
    try:
        # Pobierz kolejkę startową (zawodnicy którzy byli skanowani na start line)
        queue_data = get_all("""
            SELECT DISTINCT
                z.nr_startowy, z.imie, z.nazwisko, z.kategoria, z.plec, z.klub,
                c.timestamp as ostatni_skan,
                w.czas_przejazdu_s,
                w.status
            FROM zawodnicy z
            LEFT JOIN checkpoints c ON z.nr_startowy = c.nr_startowy 
                AND c.checkpoint_name = 'start-line-verify'
            LEFT JOIN wyniki w ON z.nr_startowy = w.nr_startowy
            WHERE c.nr_startowy IS NOT NULL
            ORDER BY c.timestamp DESC
            LIMIT 20
        """)
        
        return jsonify({
            "success": True,
            "queue": queue_data,
            "count": len(queue_data)
        }), 200
        
    except Exception as e:
        print(f"Błąd w start-queue: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/qr/manual-checkins", methods=['GET'])
def get_manual_checkins():
    """Endpoint do pobierania historii ręcznych zameldowań"""
    try:
        # Pobierz ręczne zameldowania z checkpoints
        manual_checkins = get_all("""
            SELECT c.nr_startowy, c.timestamp, c.device_id,
                   z.imie, z.nazwisko, z.kategoria, z.plec, z.klub,
                   z.checked_in, z.check_in_time
            FROM checkpoints c
            JOIN zawodnicy z ON c.nr_startowy = z.nr_startowy
            WHERE c.checkpoint_name = 'manual-check-in'
            ORDER BY c.timestamp DESC
            LIMIT 50
        """)
        
        # Formatuj dane dla frontend
        formatted_checkins = []
        for checkin in manual_checkins:
            formatted_checkins.append({
                "nr_startowy": checkin["nr_startowy"],
                "imie": checkin["imie"],
                "nazwisko": checkin["nazwisko"],
                "kategoria": checkin["kategoria"],
                "plec": checkin["plec"],
                "klub": checkin["klub"],
                "checked_in": checkin["checked_in"],
                "check_in_time": checkin["check_in_time"].isoformat() if checkin["check_in_time"] else None,
                "timestamp": checkin["timestamp"].isoformat() if checkin["timestamp"] else None,
                "device_id": checkin["device_id"],
                "powod": "manual",  # Podstawowy powód - można rozszerzyć jeśli będzie tabela logów
                "ma_wynik": False  # Można dodać sprawdzenie wyników jeśli potrzebne
            })
        
        return jsonify({
            "success": True,
            "manual_checkins": formatted_checkins,
            "total": len(formatted_checkins)
        }), 200
        
    except Exception as e:
        print(f"Błąd w manual-checkins: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 