"""
SKATECROSS QR System - Centrum Startu Module
Blueprint dla endpointów grup startowych i skanowania QR
"""

from flask import Blueprint, jsonify, request
from datetime import datetime
from utils.database import (
    grupy_startowe_data, zawodnicy_data,
    find_grupa_by_kategoria_plec, get_zawodnicy_w_grupie,
    get_aktywna_grupa, set_grupa_aktywna,
    find_zawodnik_by_nr, checkin_zawodnik
)

centrum_startu_bp = Blueprint('centrum_startu', __name__)

@centrum_startu_bp.route("/api/grupy-startowe")
def get_grupy_startowe():
    """Endpoint zwracający grupy startowe"""
    try:
        result = []
        for grupa in grupy_startowe_data:
            # Znajdź zawodników w tej grupie
            zawodnicy_w_grupie = get_zawodnicy_w_grupie(grupa["kategoria"], grupa["plec"])
            
            grupa_info = grupa.copy()
            grupa_info["liczba_zawodnikow"] = len(zawodnicy_w_grupie)
            grupa_info["numery_startowe"] = ", ".join([str(z["nr_startowy"]) for z in zawodnicy_w_grupie])
            grupa_info["lista_zawodnikow"] = ", ".join([f"{z['imie']} {z['nazwisko']}" for z in zawodnicy_w_grupie])
            grupa_info["estimated_time"] = None
            
            result.append(grupa_info)
        
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ Błąd w grupy-startowe: {str(e)}")
        return jsonify({"error": f"Błąd pobierania grup startowych: {str(e)}"}), 500

@centrum_startu_bp.route("/api/grupa-aktywna", methods=['GET'])
def get_grupa_aktywna():
    """Pobieranie aktywnej grupy"""
    try:
        aktywna_grupa = get_aktywna_grupa()
        
        return jsonify({
            "success": True,
            "grupa": aktywna_grupa
        })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Błąd pobierania aktywnej grupy: {str(e)}"
        }), 500

@centrum_startu_bp.route("/api/grupa-aktywna", methods=['POST'])
def set_grupa_aktywna_endpoint():
    """Ustawianie/usuwanie aktywnej grupy"""
    try:
        data = request.json
        kategoria = data.get('kategoria')
        plec = data.get('plec')
        nazwa = data.get('nazwa')
        
        # Znajdź grupę
        grupa = find_grupa_by_kategoria_plec(kategoria, plec)
        
        if not grupa:
            return jsonify({
                "success": False,
                "error": "Grupa nie istnieje"
            }), 404
        
        # Sprawdź czy grupa już jest aktywna
        if grupa["status"] == "ACTIVE":
            # Deaktywuj grupę
            set_grupa_aktywna(kategoria, plec, False)
            return jsonify({
                "success": True,
                "action": "removed",
                "message": f"Grupa {nazwa} została deaktywowana"
            })
        else:
            # Aktywuj grupę
            set_grupa_aktywna(kategoria, plec, True)
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

@centrum_startu_bp.route("/api/start-queue", methods=['GET'])
def get_start_queue():
    """Pobieranie kolejki startowej"""
    try:
        result = []
        
        # Dodaj zawodników z aktywnej grupy
        aktywna_grupa = get_aktywna_grupa()
        if aktywna_grupa:
            zawodnicy_w_grupie = get_zawodnicy_w_grupie(aktywna_grupa["kategoria"], aktywna_grupa["plec"])
            for z in zawodnicy_w_grupie:
                zawodnik_info = z.copy()
                zawodnik_info["source_type"] = "AKTYWNA_GRUPA"
                zawodnik_info["ostatni_skan"] = None
                result.append(zawodnik_info)
        
        # Dodaj skanowanych zawodników
        for z in zawodnicy_data:
            if z.get("checked_in"):
                zawodnik_info = z.copy()
                zawodnik_info["source_type"] = "SKANOWANY"
                zawodnik_info["ostatni_skan"] = z.get("check_in_time")
                # Usuń duplikaty
                if not any(r["nr_startowy"] == z["nr_startowy"] for r in result):
                    result.append(zawodnik_info)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"Błąd pobierania kolejki startowej: {str(e)}"}), 500

@centrum_startu_bp.route("/api/qr/scan-result", methods=['POST'])
def qr_scan_result():
    """Endpoint dla skanowania QR kodów w centrum startu"""
    try:
        data = request.json
        qr_code = data.get('qr_code', '').strip()
        
        if not qr_code:
            return jsonify({
                "success": False,
                "action": "ODRZUC",
                "message": "Pusty kod QR"
            }), 400
        
        # Spróbuj wyciągnąć numer startowy z QR kodu
        if qr_code.startswith('SKATECROSS_QR_'):
            nr_startowy_str = qr_code.replace('SKATECROSS_QR_', '')
        else:
            nr_startowy_str = qr_code
        
        try:
            nr_startowy = int(nr_startowy_str)
        except ValueError:
            return jsonify({
                "success": False,
                "action": "ODRZUC",
                "message": f"Nieprawidłowy format kodu QR: {qr_code}"
            }), 400
        
        # Znajdź zawodnika
        zawodnik = find_zawodnik_by_nr(nr_startowy)
        
        if not zawodnik:
            return jsonify({
                "success": False,
                "action": "ODRZUC",
                "message": f"Zawodnik z numerem {nr_startowy} nie istnieje"
            }), 404
        
        # Sprawdź czy już jest w kolejce
        if zawodnik.get('checked_in'):
            return jsonify({
                "success": True,
                "action": "OSTRZEZENIE",
                "message": f"Zawodnik {zawodnik['imie']} {zawodnik['nazwisko']} jest już w kolejce",
                "zawodnik": zawodnik
            })
        
        # Dodaj zawodnika do kolejki
        checkin_zawodnik(nr_startowy)
        
        return jsonify({
            "success": True,
            "action": "AKCEPTUJ",
            "message": f"Zawodnik {zawodnik['imie']} {zawodnik['nazwisko']} dodany do kolejki",
            "zawodnik": zawodnik
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "action": "ODRZUC",
            "message": f"Błąd skanowania: {str(e)}"
        }), 500 