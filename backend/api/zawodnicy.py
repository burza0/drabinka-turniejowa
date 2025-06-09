from utils.database import get_all, get_one, execute_query
from flask import Blueprint, jsonify, request

zawodnicy_bp = Blueprint('zawodnicy', __name__)

@zawodnicy_bp.route("/api/zawodnicy")
def get_zawodnicy():
    """Pobiera listę wszystkich zawodników"""
    rows = get_all("""
        SELECT z.nr_startowy, z.imie, z.nazwisko, z.kategoria, z.plec, z.klub, z.qr_code,
               w.czas_przejazdu_s, w.status
        FROM zawodnicy z
        LEFT JOIN wyniki w ON z.nr_startowy = w.nr_startowy
        ORDER BY z.nr_startowy
    """)
    return jsonify(rows)

@zawodnicy_bp.route("/api/zawodnicy", methods=['POST'])
def add_zawodnik():
    """Dodaje nowego zawodnika"""
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
    execute_query(query_wyniki, (data['nr_startowy'], 'oczekuje'))
    
    return jsonify({"success": True, "message": "Zawodnik dodany"})

@zawodnicy_bp.route("/api/zawodnicy/<int:nr_startowy>", methods=['DELETE'])
def delete_zawodnik(nr_startowy):
    """Usuwa zawodnika"""
    execute_query("DELETE FROM zawodnicy WHERE nr_startowy = %s", (nr_startowy,))
    execute_query("DELETE FROM wyniki WHERE nr_startowy = %s", (nr_startowy,))
    return jsonify({"success": True, "message": "Zawodnik usunięty"})

@zawodnicy_bp.route("/api/zawodnicy/<int:nr_startowy>", methods=['GET'])
def get_zawodnik(nr_startowy):
    """Pobiera szczegóły zawodnika"""
    zawodnik = get_one("""
        SELECT z.*, w.czas_przejazdu_s, w.status
        FROM zawodnicy z
        LEFT JOIN wyniki w ON z.nr_startowy = w.nr_startowy
        WHERE z.nr_startowy = %s
    """, (nr_startowy,))
    
    if not zawodnik:
        return jsonify({"error": "Zawodnik nie znaleziony"}), 404
        
    return jsonify(zawodnik)

@zawodnicy_bp.route("/api/zawodnicy/<int:nr_startowy>", methods=['PUT'])
def update_zawodnik(nr_startowy):
    """Aktualizuje dane zawodnika"""
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
        data.get('klub'),
        nr_startowy
    )
    execute_query(query, params)
    return jsonify({"success": True, "message": "Zawodnik zaktualizowany"}) 