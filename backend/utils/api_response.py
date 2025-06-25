# -*- coding: utf-8 -*-
"""
SKATECROSS QR - Standardized API Response Format
Wersja: 1.0.0
Ujednolicone formaty odpowiedzi dla wszystkich endpointów API
"""

from flask import jsonify
from datetime import datetime
from typing import Any, Optional, Dict, List, Union
import traceback

class APIResponse:
    """
    Klasa do tworzenia standardowych odpowiedzi API
    
    Ujednolicony format:
    {
        "success": bool,
        "data": any | null,
        "meta": {
            "timestamp": str,
            "count": int | null,
            "total": int | null,
            "page": int | null,
            "limit": int | null
        },
        "error": {
            "message": str | null,
            "code": str | null,
            "details": any | null
        } | null
    }
    """
    
    @staticmethod
    def success(
        data: Any = None,
        count: Optional[int] = None,
        total: Optional[int] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        message: Optional[str] = None
    ):
        """
        Zwraca standardową odpowiedź sukcesu
        
        Args:
            data: Dane do zwrócenia
            count: Liczba elementów w bieżącej odpowiedzi
            total: Całkowita liczba elementów (dla paginacji)
            page: Numer strony (dla paginacji)
            limit: Limit elementów na stronę
            message: Opcjonalny komunikat
        """
        # Auto-count jeśli data to lista
        if count is None and isinstance(data, (list, tuple)):
            count = len(data)
            
        response = {
            "success": True,
            "data": data,
            "meta": {
                "timestamp": datetime.now().isoformat(),
                "count": count,
                "total": total,
                "page": page,
                "limit": limit
            },
            "error": None
        }
        
        if message:
            response["message"] = message
            
        return jsonify(response)
    
    @staticmethod
    def error(
        message: str,
        code: Optional[str] = None,
        details: Any = None,
        status_code: int = 400,
        data: Any = None
    ):
        """
        Zwraca standardową odpowiedź błędu
        
        Args:
            message: Komunikat błędu
            code: Kod błędu (np. 'VALIDATION_ERROR', 'NOT_FOUND')
            details: Szczegółowe informacje o błędzie
            status_code: Kod statusu HTTP
            data: Opcjonalne dane (np. dla błędów walidacji)
        """
        response = {
            "success": False,
            "data": data,
            "meta": {
                "timestamp": datetime.now().isoformat(),
                "count": None,
                "total": None,
                "page": None,
                "limit": None
            },
            "error": {
                "message": message,
                "code": code,
                "details": details
            }
        }
        
        return jsonify(response), status_code
    
    @staticmethod
    def not_found(resource: str, identifier: Any = None):
        """Standardowa odpowiedź 404"""
        message = f"{resource} nie znaleziony"
        if identifier:
            message += f" (ID: {identifier})"
            
        return APIResponse.error(
            message=message,
            code="NOT_FOUND",
            status_code=404
        )
    
    @staticmethod
    def validation_error(message: str, details: Dict = None):
        """Standardowa odpowiedź błędu walidacji"""
        return APIResponse.error(
            message=message,
            code="VALIDATION_ERROR",
            details=details,
            status_code=400
        )
    
    @staticmethod
    def internal_error(exception: Exception, debug: bool = False):
        """Standardowa odpowiedź błędu serwera"""
        message = "Wystąpił błąd wewnętrzny serwera"
        details = None
        
        if debug:
            details = {
                "exception": str(exception),
                "traceback": traceback.format_exc()
            }
            
        return APIResponse.error(
            message=message,
            code="INTERNAL_ERROR",
            details=details,
            status_code=500
        )
    
    @staticmethod
    def paginated(
        data: List[Any],
        page: int,
        limit: int,
        total: int,
        message: Optional[str] = None
    ):
        """Standardowa odpowiedź z paginacją"""
        return APIResponse.success(
            data=data,
            count=len(data),
            total=total,
            page=page,
            limit=limit,
            message=message
        )


class ErrorCodes:
    """Standardowe kody błędów"""
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    CONFLICT = "CONFLICT"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    BAD_REQUEST = "BAD_REQUEST"
    
    # Błędy specyficzne dla SKATECROSS
    ZAWODNIK_NOT_FOUND = "ZAWODNIK_NOT_FOUND"
    INVALID_QR_CODE = "INVALID_QR_CODE"
    RACE_TIME_INVALID = "RACE_TIME_INVALID"
    TOURNAMENT_PHASE_ERROR = "TOURNAMENT_PHASE_ERROR"


# Dekoratory do automatycznej standardizacji odpowiedzi
def handle_api_errors(func):
    """
    Dekorator do automatycznego przechwytywania błędów
    i zwracania standardowych odpowiedzi
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return APIResponse.validation_error(str(e))
        except KeyError as e:
            return APIResponse.validation_error(f"Brakuje wymaganego pola: {e}")
        except Exception as e:
            return APIResponse.internal_error(e, debug=True)
    
    wrapper.__name__ = func.__name__
    return wrapper


def validate_pagination(page: Optional[str] = None, limit: Optional[str] = None):
    """
    Walidacja parametrów paginacji
    
    Returns:
        tuple: (page, limit) jako integery
    """
    try:
        page = int(page) if page else 1
        limit = int(limit) if limit else 50
        
        if page < 1:
            raise ValueError("Numer strony musi być większy od 0")
        if limit < 1 or limit > 1000:
            raise ValueError("Limit musi być między 1 a 1000")
            
        return page, limit
    except ValueError as e:
        if "invalid literal" in str(e):
            raise ValueError("Parametry paginacji muszą być liczbami")
        raise


def validate_season(season: Optional[str] = None):
    """
    Walidacja parametru sezonu
    
    Returns:
        int | None: Sezon jako integer lub None dla wszystkich sezonów
    """
    if not season:
        return None
        
    try:
        season_int = int(season)
        current_year = datetime.now().year
        
        if season_int < 2020 or season_int > current_year + 2:
            raise ValueError(f"Sezon musi być między 2020 a {current_year + 2}")
            
        return season_int
    except ValueError as e:
        if "invalid literal" in str(e):
            raise ValueError("Sezon musi być liczbą")
        raise


# Przykłady użycia:
if __name__ == "__main__":
    # Sukces z danymi
    response1 = APIResponse.success(
        data=[{"id": 1, "name": "Anna"}],
        message="Zawodnicy pobrani pomyślnie"
    )
    
    # Błąd walidacji
    response2 = APIResponse.validation_error(
        "Nieprawidłowy format numeru startowego",
        details={"field": "nr_startowy", "value": "abc"}
    )
    
    # Nie znaleziono
    response3 = APIResponse.not_found("Zawodnik", 123)
    
    print("Standardowe odpowiedzi API utworzone!") 