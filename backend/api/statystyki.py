from utils.database import get_all
from flask import Blueprint, jsonify
from utils.api_response import APIResponse, handle_api_errors

statystyki_bp = Blueprint('statystyki', __name__)

@statystyki_bp.route("/api/kategorie")
@handle_api_errors
def get_kategorie():
    """Pobiera listę kategorii z liczbą zawodników"""
    # Pobierz kategorie
    kategorie_rows = get_all("SELECT DISTINCT kategoria FROM zawodnicy WHERE kategoria IS NOT NULL ORDER BY kategoria")
    kategorie_list = [row["kategoria"] for row in kategorie_rows]
    
    # Pobierz łączną liczbę zawodników
    total_rows = get_all("SELECT COUNT(*) as total FROM zawodnicy WHERE kategoria IS NOT NULL")
    total_zawodnikow = total_rows[0]["total"] if total_rows else 0
    
    data = {
        "kategorie": kategorie_list,
        "total_zawodnikow": total_zawodnikow
    }
    
    return APIResponse.success(
        data=data,
        count=len(kategorie_list),
        message="Kategorie pobrane pomyślnie"
    )

@statystyki_bp.route("/api/statystyki")
@handle_api_errors
def get_statystyki():
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
    
    data = {
        'kategorie': stats,
        'total': {'M': total_m, 'K': total_k, 'razem': total_m + total_k}
    }
    
    return APIResponse.success(
        data=data,
        count=total_m + total_k,
        message="Statystyki zawodników pobrane pomyślnie"
    )

@statystyki_bp.route("/api/kluby")
@handle_api_errors
def get_kluby():
    """Endpoint zwracający listę klubów z liczbą zawodników"""
    # Pobierz podstawową listę nazw klubów
    nazwy_rows = get_all("SELECT DISTINCT klub FROM zawodnicy WHERE klub IS NOT NULL ORDER BY klub")
    nazwy_list = [row["klub"] for row in nazwy_rows]
    
    data = {
        'nazwy_klubow': nazwy_list,
        'total_klubow': len(nazwy_list)
    }
    
    return APIResponse.success(
        data=data,
        count=len(nazwy_list),
        message="Lista klubów pobrana pomyślnie"
    ) 