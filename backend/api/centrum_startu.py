# -*- coding: utf-8 -*-
"""
SKATECROSS QR - Centrum Startu API Blueprint
Wersja: 1.0.0
System centrum startu i grup startowych
"""

from flask import Blueprint, jsonify, request
from datetime import datetime
import sys
import os

# Dodaj ścieżkę do utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.database import get_all, get_one, execute_query

centrum_startu_bp = Blueprint('centrum_startu', __name__)

# Cache aktywnej grupy (tymczasowe rozwiązanie)
aktywna_grupa_cache = {
    "numer_grupy": None,
    "kategoria": None,
    "plec": None,
    "nazwa": None
}

@centrum_startu_bp.route('/api/grupy-startowe', methods=['GET'])
def get_grupy_startowe():
    """
    Pobieranie grup startowych z zameldowanymi zawodnikami
    GET /api/grupy-startowe
    """
    try:
        # Pobierz TYLKO zameldowanych zawodników pogrupowanych po kategoriach i płci
        # (to jest właściwa logika - grupy startowe to zameldowani zawodnicy!)
        zawodnicy = get_all("""
            SELECT nr_startowy, imie, nazwisko, kategoria, plec, klub, qr_code,
                   COALESCE(checked_in, false) as checked_in
            FROM zawodnicy 
            WHERE COALESCE(checked_in, false) = true AND kategoria IS NOT NULL
            ORDER BY kategoria, plec, nr_startowy
        """)
        
        # Grupuj zawodników po kategoria + plec
        grupy = {}
        for zawodnik in zawodnicy:
            key = f"{zawodnik['kategoria']} {zawodnik['plec']}"
            if key not in grupy:
                grupy[key] = []
            grupy[key].append(zawodnik)
        
        # Przekształć na format odpowiedzi z dodatkowymi statystykami
        grupy_list = []
        numer_grupy = 1
        
        for grupa_nazwa, zawodnicy_list in sorted(grupy.items()):
            # Wszyscy zawodnicy w tej liście są zameldowani
            zameldowani_count = len(zawodnicy_list)
            
            # Wyodrębnij kategorię i płeć z nazwy grupy
            kategoria = zawodnicy_list[0]['kategoria']
            plec = zawodnicy_list[0]['plec']
            nazwa_grupy = f"Grupa {numer_grupy}: {kategoria} {'Mężczyźni' if plec == 'M' else 'Kobiety'}"
            
            grupy_list.append({
                "numer_grupy": numer_grupy,
                "nazwa": nazwa_grupy,
                "kategoria": kategoria,
                "plec": plec,
                "zawodnicy": zawodnicy_list,
                "liczba_zawodnikow": len(zawodnicy_list),
                "zameldowani": zameldowani_count,
                "niezameldowani": 0,  # Wszyscy są zameldowani
                # Dodaj informacje jak w oryginalnej wersji
                "numery_startowe": ", ".join([str(z["nr_startowy"]) for z in zawodnicy_list]),
                "lista_zawodnikow": ", ".join([f"{z['imie']} {z['nazwisko']}" for z in zawodnicy_list]),
                "estimated_time": len(zawodnicy_list) * 20  # sekundy (20s na zawodnika)
            })
            numer_grupy += 1
        
        return jsonify({
            "success": True,
            "data": {
                "grupy": grupy_list,
                "total_grup": len(grupy_list),
                "total_zawodnikow": len(zawodnicy)
            },
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@centrum_startu_bp.route('/api/grupa-aktywna', methods=['GET'])
def get_grupa_aktywna():
    """Pobieranie aktywnej grupy"""
    try:
        return jsonify({
            "success": True,
            "grupa": aktywna_grupa_cache
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Błąd pobierania aktywnej grupy: {str(e)}"
        }), 500

@centrum_startu_bp.route('/api/grupa-aktywna', methods=['POST'])
def set_grupa_aktywna():
    """Ustawianie/usuwanie aktywnej grupy"""
    try:
        data = request.json
        kategoria = data.get('kategoria')
        plec = data.get('plec')
        nazwa = data.get('nazwa')
        
        # Sprawdź czy grupa już jest aktywna
        if (aktywna_grupa_cache["kategoria"] == kategoria and 
            aktywna_grupa_cache["plec"] == plec):
            # Deaktywuj grupę
            aktywna_grupa_cache.update({
                "numer_grupy": None,
                "kategoria": None,
                "plec": None,
                "nazwa": None
            })
            return jsonify({
                "success": True,
                "action": "removed",
                "message": f"Grupa {nazwa} została deaktywowana"
            })
        else:
            # Aktywuj grupę
            aktywna_grupa_cache.update({
                "numer_grupy": 1,
                "kategoria": kategoria,
                "plec": plec,
                "nazwa": nazwa
            })
            return jsonify({
                "success": True,
                "action": "added",
                "message": f"Grupa {nazwa} została aktywowana"
            })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Błąd toggle grupy aktywnej: {str(e)}"
        }), 500

@centrum_startu_bp.route('/api/start-queue', methods=['GET'])
def get_start_queue():
    """Pobieranie kolejki startowej"""
    try:
        result = []
        
        # Dodaj zawodników z aktywnej grupy
        if aktywna_grupa_cache["kategoria"] and aktywna_grupa_cache["plec"]:
            zawodnicy_w_grupie = get_all("""
                SELECT nr_startowy, imie, nazwisko, kategoria, plec, klub, qr_code,
                       COALESCE(checked_in, false) as checked_in
                FROM zawodnicy 
                WHERE kategoria = %s AND plec = %s AND COALESCE(checked_in, false) = true
                ORDER BY nr_startowy
            """, (aktywna_grupa_cache["kategoria"], aktywna_grupa_cache["plec"]))
            
            for z in zawodnicy_w_grupie:
                zawodnik_info = dict(z)
                zawodnik_info["source_type"] = "AKTYWNA_GRUPA"
                zawodnik_info["ostatni_skan"] = None
                result.append(zawodnik_info)
        
        # Dodaj innych skanowanych zawodników
        pozostali_zawodnicy = get_all("""
            SELECT nr_startowy, imie, nazwisko, kategoria, plec, klub, qr_code,
                   COALESCE(checked_in, false) as checked_in, check_in_time
            FROM zawodnicy 
            WHERE COALESCE(checked_in, false) = true
            ORDER BY check_in_time DESC
        """)
        
        for z in pozostali_zawodnicy:
            # Usuń duplikaty
            if not any(r["nr_startowy"] == z["nr_startowy"] for r in result):
                zawodnik_info = dict(z)
                zawodnik_info["source_type"] = "SKANOWANY"
                zawodnik_info["ostatni_skan"] = z.get("check_in_time")
                result.append(zawodnik_info)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Błąd pobierania kolejki startowej: {str(e)}"}), 500

@centrum_startu_bp.route('/api/start-queue/all-group-statuses', methods=['GET'])
def get_all_group_statuses():
    """Pobieranie statusów wszystkich grup"""
    try:
        # Pobierz wszystkie grupy z zawodnikami
        grupy_stats = get_all("""
            SELECT 
                kategoria,
                plec,
                COUNT(*) as total_zawodnikow,
                COUNT(CASE WHEN COALESCE(checked_in, false) = true THEN 1 END) as zameldowani
            FROM zawodnicy 
            GROUP BY kategoria, plec
            ORDER BY kategoria, plec
        """)
        
        result = {}
        for grupa in grupy_stats:
            key = f"{grupa['kategoria']} {grupa['plec']}"
            result[key] = {
                "total": grupa['total_zawodnikow'],
                "checked_in": grupa['zameldowani'],
                "status": "ACTIVE" if (aktywna_grupa_cache["kategoria"] == grupa['kategoria'] and 
                                    aktywna_grupa_cache["plec"] == grupa['plec']) else "WAITING"
            }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Błąd pobierania statusów grup: {str(e)}"}), 500

@centrum_startu_bp.route('/api/start-queue/remove/<int:nr_startowy>', methods=['DELETE'])
def remove_from_queue(nr_startowy):
    """Usuwanie zawodnika z kolejki startowej"""
    try:
        rows_affected = execute_query("""
            UPDATE zawodnicy 
            SET checked_in = false,
                check_in_time = NULL
            WHERE nr_startowy = %s
        """, (nr_startowy,))
        
        if rows_affected > 0:
            return jsonify({
                "success": True,
                "message": f"Zawodnik {nr_startowy} usunięty z kolejki"
            })
        else:
            return jsonify({
                "success": False,
                "error": "Zawodnik nie znaleziony"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@centrum_startu_bp.route('/api/start-queue/clear', methods=['POST'])
def clear_queue():
    """Czyszczenie całej kolejki startowej"""
    try:
        rows_affected = execute_query("""
            UPDATE zawodnicy 
            SET checked_in = false,
                check_in_time = NULL
            WHERE COALESCE(checked_in, false) = true
        """)
        
        return jsonify({
            "success": True,
            "message": f"Kolejka wyczyszczona. Usunięto {rows_affected} zawodników."
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@centrum_startu_bp.route('/api/scan-qr', methods=['POST'])
def scan_qr_code():
    """
    Endpoint do skanowania kodu QR i meldowania zawodnika
    POST /api/scan-qr
    Body: {"qr_code": "QR102", "action": "checkin"}
    """
    try:
        data = request.get_json()
        
        if not data or 'qr_code' not in data:
            return jsonify({
                "success": False,
                "error": "Brak kodu QR w żądaniu"
            }), 400
        
        qr_code = data['qr_code']
        action = data.get('action', 'checkin')  # checkin lub checkout
        
        # Znajdź zawodnika po kodzie QR
        zawodnik = get_one("""
            SELECT nr_startowy, imie, nazwisko, kategoria, plec, klub, qr_code,
                   COALESCE(checked_in, false) as checked_in
            FROM zawodnicy 
            WHERE qr_code = %s
        """, (qr_code,))
        
        if not zawodnik:
            return jsonify({
                "success": False,
                "error": f"Nie znaleziono zawodnika z kodem QR: {qr_code}"
            }), 404
        
        # Aktualizuj status meldowania
        new_status = True if action == 'checkin' else False
        
        rows_affected = execute_query("""
            UPDATE zawodnicy 
            SET checked_in = %s, 
                check_in_time = CASE WHEN %s = true THEN CURRENT_TIMESTAMP ELSE check_in_time END
            WHERE qr_code = %s
        """, (new_status, new_status, qr_code))
        
        if rows_affected > 0:
            # Pobierz zaktualizowane dane zawodnika
            updated_zawodnik = get_one("""
                SELECT nr_startowy, imie, nazwisko, kategoria, plec, klub, qr_code,
                       COALESCE(checked_in, false) as checked_in
                FROM zawodnicy 
                WHERE qr_code = %s
            """, (qr_code,))
            
            return jsonify({
                "success": True,
                "data": {
                    "zawodnik": updated_zawodnik,
                    "action": action,
                    "message": f"Zawodnik {action}ed pomyślnie"
                },
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "success": False,
                "error": "Błąd podczas aktualizacji statusu zawodnika"
            }), 500
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@centrum_startu_bp.route('/api/centrum-startu/manual-checkin', methods=['POST'])
def manual_checkin():
    """
    Ręczne meldowanie zawodnika po numerze startowym
    POST /api/centrum-startu/manual-checkin
    Body: {"nr_startowy": 102, "action": "checkin"}
    """
    try:
        data = request.get_json()
        
        if not data or 'nr_startowy' not in data:
            return jsonify({
                "success": False,
                "error": "Brak numeru startowego w żądaniu"
            }), 400
        
        nr_startowy = data['nr_startowy']
        action = data.get('action', 'checkin')
        
        # Znajdź zawodnika po numerze startowym
        zawodnik = get_one("""
            SELECT nr_startowy, imie, nazwisko, kategoria, plec, klub, qr_code,
                   COALESCE(checked_in, false) as checked_in
            FROM zawodnicy 
            WHERE nr_startowy = %s
        """, (nr_startowy,))
        
        if not zawodnik:
            return jsonify({
                "success": False,
                "error": f"Nie znaleziono zawodnika o numerze startowym: {nr_startowy}"
            }), 404
        
        # Aktualizuj status
        new_status = True if action == 'checkin' else False
        
        rows_affected = execute_query("""
            UPDATE zawodnicy 
            SET checked_in = %s,
                check_in_time = CASE WHEN %s = true THEN CURRENT_TIMESTAMP ELSE check_in_time END
            WHERE nr_startowy = %s
        """, (new_status, new_status, nr_startowy))
        
        if rows_affected > 0:
            # Pobierz zaktualizowane dane
            updated_zawodnik = get_one("""
                SELECT nr_startowy, imie, nazwisko, kategoria, plec, klub, qr_code,
                       COALESCE(checked_in, false) as checked_in
                FROM zawodnicy 
                WHERE nr_startowy = %s
            """, (nr_startowy,))
            
            return jsonify({
                "success": True,
                "data": {
                    "zawodnik": updated_zawodnik,
                    "action": action,
                    "message": f"Zawodnik ręcznie {action}ed"
                },
                "timestamp": datetime.now().isoformat()
            })
        else:
            return jsonify({
                "success": False,
                "error": "Błąd podczas aktualizacji statusu zawodnika"
            }), 500
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@centrum_startu_bp.route('/api/centrum-startu/stats', methods=['GET'])
def centrum_stats():
    """
    Statystyki centrum startu
    GET /api/centrum-startu/stats
    """
    try:
        # Pobierz statystyki z bazy
        stats_result = get_one("""
            SELECT 
                COUNT(*) as total_zawodnicy,
                COUNT(CASE WHEN COALESCE(checked_in, false) = true THEN 1 END) as zameldowani,
                COUNT(CASE WHEN COALESCE(checked_in, false) = false THEN 1 END) as niezameldowani,
                COUNT(DISTINCT kategoria) as liczba_kategorii,
                COUNT(DISTINCT klub) as liczba_klubow
            FROM zawodnicy
        """)
        
        # Pobierz grupy startowe (zameldowani zawodnicy)
        grupy_stats = get_all("""
            SELECT 
                kategoria,
                plec,
                COUNT(*) as liczba_zawodnikow
            FROM zawodnicy 
            WHERE COALESCE(checked_in, false) = true
            GROUP BY kategoria, plec
            ORDER BY kategoria, plec
        """)
        
        # Przekształć grupy na format odpowiedzi
        grupy_formatted = {}
        for grupa in grupy_stats:
            key = f"{grupa['kategoria']} {grupa['plec']}"
            grupy_formatted[key] = grupa['liczba_zawodnikow']
        
        stats = {
            "total_zawodnicy": stats_result['total_zawodnicy'] if stats_result else 0,
            "zameldowani": stats_result['zameldowani'] if stats_result else 0,
            "niezameldowani": stats_result['niezameldowani'] if stats_result else 0,
            "liczba_kategorii": stats_result['liczba_kategorii'] if stats_result else 0,
            "liczba_klubow": stats_result['liczba_klubow'] if stats_result else 0,
            "grupy_startowe": grupy_formatted
        }
        
        return jsonify({
            "success": True,
            "data": stats,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

print("🏁 SKATECROSS QR - Moduł Centrum Startu załadowany z Supabase PostgreSQL") 