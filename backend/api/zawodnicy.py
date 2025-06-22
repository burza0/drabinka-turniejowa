# -*- coding: utf-8 -*-
"""
SKATECROSS QR - Zawodnicy API Blueprint
Wersja: 2.0.0
Endpointy zarządzania zawodnikami - z Supabase PostgreSQL
"""

from flask import Blueprint, jsonify, request
import sys
import os

# Dodaj ścieżkę do utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.database import get_all, get_one, execute_query
from utils.api_response import APIResponse, handle_api_errors, validate_pagination

zawodnicy_bp = Blueprint('zawodnicy', __name__)

@zawodnicy_bp.route('/api/zawodnicy', methods=['GET'])
@handle_api_errors
def get_zawodnicy():
    """
    Endpoint zwracający listę wszystkich zawodników z Supabase PostgreSQL
    GET /api/zawodnicy?page=1&limit=50
    """
    # Obsługa paginacji
    page, limit = validate_pagination(
        request.args.get('page'),
        request.args.get('limit')
    )
    
    # Policz wszystkich zawodników
    count_result = get_one("SELECT COUNT(*) as total FROM zawodnicy")
    total = count_result['total'] if count_result else 0
    
    # Pobierz paginowane dane
    offset = (page - 1) * limit
    zawodnicy = get_all("""
        SELECT nr_startowy, imie, nazwisko, kategoria, plec, klub, qr_code, 
               COALESCE(checked_in, false) as checked_in
        FROM zawodnicy 
        ORDER BY nr_startowy 
        LIMIT %s OFFSET %s
    """, (limit, offset))
    
    return APIResponse.paginated(
        data=zawodnicy,
        page=page,
        limit=limit,
        total=total,
        message="Zawodnicy pobrani pomyślnie z Supabase"
    )

@zawodnicy_bp.route('/api/zawodnicy/<int:nr_startowy>', methods=['GET'])
@handle_api_errors
def get_zawodnik(nr_startowy):
    """
    Endpoint zwracający pojedynczego zawodnika po numerze startowym
    GET /api/zawodnicy/{nr_startowy}
    """
    zawodnik = get_one("""
        SELECT nr_startowy, imie, nazwisko, kategoria, plec, klub, qr_code,
               COALESCE(checked_in, false) as checked_in
        FROM zawodnicy 
        WHERE nr_startowy = %s
    """, (nr_startowy,))
    
    if not zawodnik:
        return APIResponse.not_found("Zawodnik", nr_startowy)
    
    return APIResponse.success(
        data=zawodnik,
        message=f"Zawodnik nr {nr_startowy} pobrany pomyślnie"
    )

@zawodnicy_bp.route('/api/zawodnicy/kategoria/<kategoria>', methods=['GET'])
@handle_api_errors
def get_zawodnicy_kategoria(kategoria):
    """
    Endpoint zwracający zawodników z danej kategorii
    GET /api/zawodnicy/kategoria/{kategoria}?plec=M/K&page=1&limit=50
    """
    plec = request.args.get('plec')
    page, limit = validate_pagination(
        request.args.get('page'),
        request.args.get('limit')
    )
    
    # Buduj zapytanie SQL w zależności od parametrów
    if plec:
        count_query = "SELECT COUNT(*) as total FROM zawodnicy WHERE kategoria = %s AND plec = %s"
        data_query = """
            SELECT nr_startowy, imie, nazwisko, kategoria, plec, klub, qr_code,
                   COALESCE(checked_in, false) as checked_in
            FROM zawodnicy 
            WHERE kategoria = %s AND plec = %s
            ORDER BY nr_startowy 
            LIMIT %s OFFSET %s
        """
        count_params = (kategoria, plec)
        data_params = (kategoria, plec, limit, (page - 1) * limit)
    else:
        count_query = "SELECT COUNT(*) as total FROM zawodnicy WHERE kategoria = %s"
        data_query = """
            SELECT nr_startowy, imie, nazwisko, kategoria, plec, klub, qr_code,
                   COALESCE(checked_in, false) as checked_in
            FROM zawodnicy 
            WHERE kategoria = %s
            ORDER BY nr_startowy 
            LIMIT %s OFFSET %s
        """
        count_params = (kategoria,)
        data_params = (kategoria, limit, (page - 1) * limit)
    
    # Policz wyniki
    count_result = get_one(count_query, count_params)
    total = count_result['total'] if count_result else 0
    
    # Pobierz dane
    zawodnicy = get_all(data_query, data_params)
    
    # Dodatkowe metadane
    extra_meta = {
        "kategoria": kategoria,
        "plec": plec,
        "filters_applied": {
            "kategoria": kategoria,
            "plec": plec if plec else "wszystkie"
        }
    }
    
    response_data = APIResponse.paginated(
        data=zawodnicy,
        page=page,
        limit=limit,
        total=total,
        message=f"Zawodnicy z kategorii {kategoria} pobrani pomyślnie"
    )
    
    # Dodaj dodatkowe metadane
    response_data.json["meta"].update(extra_meta)
    
    return response_data

print("👤 SKATECROSS QR - Moduł Zawodników załadowany z Supabase PostgreSQL") 