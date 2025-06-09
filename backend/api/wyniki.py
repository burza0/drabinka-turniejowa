from utils.database import get_all, execute_query
from utils.validators import validate_time_format
from flask import Blueprint, jsonify, request

wyniki_bp = Blueprint('wyniki', __name__)

@wyniki_bp.route("/api/wyniki")
def get_wyniki():
    """Pobiera listę wszystkich wyników"""
    rows = get_all("""
        SELECT w.nr_startowy, w.czas_przejazdu_s, w.status, 
               z.imie, z.nazwisko, z.kategoria, z.plec
        FROM wyniki w
        LEFT JOIN zawodnicy z ON w.nr_startowy = z.nr_startowy
        ORDER BY w.nr_startowy
    """)
    return jsonify(rows)

@wyniki_bp.route("/api/wyniki", methods=['PUT'])
def update_wynik():
    """Aktualizuje wynik zawodnika"""
    data = request.json
    nr_startowy = data.get('nr_startowy')
    czas = data.get('czas')
    status = data.get('status')
    
    if not nr_startowy:
        return jsonify({"error": "Brak numeru startowego"}), 400
        
    if czas:
        try:
            czas_s = validate_time_format(czas)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
    else:
        czas_s = None
        
    query = """
        UPDATE wyniki 
        SET czas_przejazdu_s = %s, status = %s
        WHERE nr_startowy = %s
    """
    execute_query(query, (czas_s, status, nr_startowy))
    
    return jsonify({"success": True, "message": "Wynik zaktualizowany"}) 