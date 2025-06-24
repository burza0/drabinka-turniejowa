# -*- coding: utf-8 -*-
"""
SKATECROSS QR - Centrum Startu API Blueprint
Wersja: 2.0.0 - v36.1 Legacy Endpoints DISABLED
System centrum startu - tylko nowoczesne unified API
"""

from flask import Blueprint, jsonify, request
from datetime import datetime
import sys
import os

# Dodaj ścieżkę do utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.database import get_all, get_one, execute_query

centrum_startu_bp = Blueprint('centrum_startu', __name__)

# ==========================================
# 🚫 LEGACY ENDPOINTS DISABLED v36.1
# ==========================================
# Następujące endpoints zostały wyłączone w v36.1:
# - /api/grupy-startowe → zastąpione przez /api/unified/groups
# - /api/grupa-aktywna → zastąpione przez /api/unified/activate-group, /api/unified/deactivate-group  
# - /api/start-queue → zastąpione przez /api/unified/queue
# - /api/scan-qr → zastąpione przez /api/unified/checkin

@centrum_startu_bp.route('/api/grupy-startowe', methods=['GET'])
def get_grupy_startowe_disabled():
    """LEGACY ENDPOINT DISABLED - używaj /api/unified/groups"""
    return jsonify({
        "success": False,
        "error": "Legacy endpoint disabled in v36.1",
        "migration": {
            "old_endpoint": "/api/grupy-startowe",
            "new_endpoint": "/api/unified/groups",
            "message": "Użyj nowego unified API dla lepszej wydajności i funkcjonalności"
        }
    }), 410  # 410 Gone

@centrum_startu_bp.route('/api/grupa-aktywna', methods=['GET', 'POST'])
def grupa_aktywna_disabled():
    """LEGACY ENDPOINT DISABLED - używaj unified API"""
    return jsonify({
        "success": False,
        "error": "Legacy endpoint disabled in v36.1",
        "migration": {
            "old_endpoint": "/api/grupa-aktywna",
            "new_endpoints": {
                "GET": "/api/unified/groups (sprawdź status grup)",
                "POST activate": "/api/unified/activate-group",
                "POST deactivate": "/api/unified/deactivate-group"
            },
            "message": "Unified API zapewnia lepszą kontrolę nad grupami i sesje SECTRO"
        }
    }), 410  # 410 Gone

@centrum_startu_bp.route('/api/start-queue', methods=['GET'])
def start_queue_disabled():
    """LEGACY ENDPOINT DISABLED - używaj /api/unified/queue"""
    return jsonify({
        "success": False,
        "error": "Legacy endpoint disabled in v36.1", 
        "migration": {
            "old_endpoint": "/api/start-queue",
            "new_endpoint": "/api/unified/queue",
            "message": "Nowa kolejka unified zawiera priorytety SECTRO i lepsze sortowanie"
        }
    }), 410  # 410 Gone

@centrum_startu_bp.route('/api/scan-qr', methods=['POST'])
def scan_qr_disabled():
    """LEGACY ENDPOINT DISABLED - używaj /api/unified/checkin"""
    return jsonify({
        "success": False,
        "error": "Legacy endpoint disabled in v36.1",
        "migration": {
            "old_endpoint": "/api/scan-qr",
            "new_endpoint": "/api/unified/checkin", 
            "message": "Unified checkin automatycznie dodaje do aktywnych sesji SECTRO"
        }
    }), 410  # 410 Gone

# ==========================================
# ✅ ZACHOWANE NOWOCZESNE ENDPOINTS
# ==========================================

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

# ==========================================
# 🚫 LEGACY ENDPOINTS CLEANUP (remove from start-queue)
# ==========================================

@centrum_startu_bp.route('/api/start-queue/remove/<int:nr_startowy>', methods=['DELETE'])
def remove_from_queue_disabled(nr_startowy):
    """LEGACY ENDPOINT DISABLED - używaj unified API"""
    return jsonify({
        "success": False,
        "error": "Legacy endpoint disabled in v36.1",
        "migration": {
            "old_endpoint": f"/api/start-queue/remove/{nr_startowy}",
            "new_endpoint": "/api/unified/checkin (z action: checkout)",
            "message": "Użyj unified checkin/checkout API"
        }
    }), 410  # 410 Gone

@centrum_startu_bp.route('/api/start-queue/clear', methods=['POST'])
def clear_queue_disabled():
    """LEGACY ENDPOINT DISABLED - używaj unified API"""
    return jsonify({
        "success": False,
        "error": "Legacy endpoint disabled in v36.1",
        "migration": {
            "old_endpoint": "/api/start-queue/clear",
            "new_endpoint": "/api/unified/clear-all (when implemented)",
            "message": "Bulk operacje dostępne w unified API"
        }
    }), 410  # 410 Gone

@centrum_startu_bp.route('/api/start-queue/all-group-statuses', methods=['GET'])
def get_all_group_statuses_disabled():
    """LEGACY ENDPOINT DISABLED - używaj /api/unified/groups"""
    return jsonify({
        "success": False,
        "error": "Legacy endpoint disabled in v36.1",
        "migration": {
            "old_endpoint": "/api/start-queue/all-group-statuses",
            "new_endpoint": "/api/unified/groups",
            "message": "Unified groups API zawiera wszystkie statusy grup z SECTRO"
        }
    }), 410  # 410 Gone

print("🏁 SKATECROSS QR - Moduł Centrum Startu załadowany z Supabase PostgreSQL")
print("🚫 v36.1: Legacy endpoints DISABLED - używaj /api/unified/*") 