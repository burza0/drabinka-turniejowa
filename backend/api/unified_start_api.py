# -*- coding: utf-8 -*-
"""
SKATECROSS QR - Unified Start API Blueprint
Wersja: 1.0.0
API endpoints dla zintegrowanego systemu Centrum Startu + SECTRO Live Timing
"""

from flask import Blueprint, jsonify, request
from datetime import datetime
import sys
import os

# Dodaj ścieżkę do unified manager
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from unified_start_manager import UnifiedStartManager

# Utwórz blueprint
unified_bp = Blueprint('unified_start', __name__)

# Globalna instancja managera
manager = UnifiedStartManager()

# ===============================================
# UNIFIED API ENDPOINTS
# ===============================================

@unified_bp.route('/api/unified/health', methods=['GET'])
def health_check():
    """Health check endpoint dla unified system"""
    try:
        return jsonify({
            'success': True,
            'status': 'healthy',
            'manager': 'ready',
            'timestamp': datetime.now().isoformat(),
            'message': 'Unified Start Control działa poprawnie'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'status': 'error',
            'error': str(e)
        }), 500

@unified_bp.route('/api/unified/dashboard-data', methods=['GET'])
def get_dashboard_data():
    """
    Single endpoint dla wszystkich danych dashboard
    GET /api/unified/dashboard-data
    
    Zwraca:
    - groups: grupy startowe z statusami SECTRO
    - queue: unified kolejka startowa
    - activeSession: aktywna sesja SECTRO
    - stats: unified statystyki
    """
    try:
        result = manager.get_dashboard_data()
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Błąd dashboard data: {str(e)}'
        }), 500

@unified_bp.route('/api/unified/register-athlete', methods=['POST'])
def register_athlete():
    """
    Unified rejestracja zawodnika z auto-dodaniem do aktywnej sesji
    POST /api/unified/register-athlete
    
    Body:
    {
        "identifier": 123 | "QR123",  // nr_startowy lub qr_code
        "action": "checkin" | "checkout"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'identifier' not in data:
            return jsonify({
                'success': False,
                'error': 'Brak identifier w żądaniu'
            }), 400
        
        identifier = data['identifier']
        action = data.get('action', 'checkin')
        
        result = manager.register_athlete_unified(identifier, action)
        
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Błąd rejestracji: {str(e)}'
        }), 500

@unified_bp.route('/api/unified/activate-group', methods=['POST'])
def activate_group():
    """
    Unified aktywacja grupy z automatycznym tworzeniem sesji SECTRO
    POST /api/unified/activate-group
    
    Body:
    {
        "kategoria": "Junior A",
        "plec": "M",
        "nazwa": "Custom Session Name"  // opcjonalne
    }
    """
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['kategoria', 'plec']):
            return jsonify({
                'success': False,
                'error': 'Brak kategoria lub plec w żądaniu'
            }), 400
        
        kategoria = data['kategoria']
        plec = data['plec']
        nazwa = data.get('nazwa')
        
        result = manager.activate_group_unified(kategoria, plec, nazwa)
        
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Błąd aktywacji grupy: {str(e)}'
        }), 500

@unified_bp.route('/api/unified/deactivate-group', methods=['POST'])
def deactivate_group():
    """
    Unified deaktywacja grupy i zakończenie sesji SECTRO
    POST /api/unified/deactivate-group
    
    Body:
    {
        "kategoria": "Junior A",
        "plec": "M"
    }
    """
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['kategoria', 'plec']):
            return jsonify({
                'success': False,
                'error': 'Brak kategoria lub plec w żądaniu'
            }), 400
        
        kategoria = data['kategoria']
        plec = data['plec']
        
        result = manager.deactivate_group_unified(kategoria, plec)
        
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Błąd deaktywacji grupy: {str(e)}'
        }), 500

@unified_bp.route('/api/unified/group-details/<kategoria>/<plec>', methods=['GET'])
def get_group_details(kategoria, plec):
    """
    Pobieranie szczegółów grupy z listą zawodników
    GET /api/unified/group-details/{kategoria}/{plec}
    """
    try:
        result = manager.get_group_details(kategoria, plec)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Błąd pobierania szczegółów grupy: {str(e)}'
        }), 500

@unified_bp.route('/api/unified/remove-athlete-from-group', methods=['POST'])
def remove_athlete_from_group():
    """
    Usuwanie zawodnika z grupy (check-out)
    POST /api/unified/remove-athlete-from-group
    
    Body:
    {
        "nr_startowy": 123,
        "kategoria": "Junior A",
        "plec": "M"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'nr_startowy' not in data:
            return jsonify({
                'success': False,
                'error': 'Brak nr_startowy w żądaniu'
            }), 400
        
        nr_startowy = data['nr_startowy']
        kategoria = data.get('kategoria')
        plec = data.get('plec')
        
        result = manager.remove_athlete_from_group(nr_startowy, kategoria, plec)
        
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Błąd usuwania zawodnika z grupy: {str(e)}'
        }), 500

@unified_bp.route('/api/unified/delete-group', methods=['POST'])
def delete_group():
    """
    Usuwanie całej grupy (check-out wszystkich zawodników)
    POST /api/unified/delete-group
    
    Body:
    {
        "kategoria": "Junior A",
        "plec": "M",
        "force": false  // true = wymusza usunięcie aktywnej grupy
    }
    """
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['kategoria', 'plec']):
            return jsonify({
                'success': False,
                'error': 'Brak kategoria lub plec w żądaniu'
            }), 400
        
        kategoria = data['kategoria']
        plec = data['plec']
        force = data.get('force', False)
        
        result = manager.delete_group(kategoria, plec, force)
        
        status_code = 200 if result['success'] else 400
        return jsonify(result), status_code
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Błąd usuwania grupy: {str(e)}'
        }), 500

@unified_bp.route('/api/unified/queue', methods=['GET'])
def get_unified_queue():
    """
    Pobieranie unified kolejki startowej z priorytetami SECTRO
    GET /api/unified/queue
    """
    try:
        queue = manager.get_unified_queue()
        
        return jsonify({
            'success': True,
            'data': queue,
            'count': len(queue),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Błąd pobierania kolejki: {str(e)}'
        }), 500

@unified_bp.route('/api/unified/groups', methods=['GET'])
def get_unified_groups():
    """
    Pobieranie grup startowych z unified statusami
    GET /api/unified/groups
    """
    try:
        groups = manager.get_groups_with_status()
        
        return jsonify({
            'success': True,
            'data': groups,
            'count': len(groups),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Błąd pobierania grup: {str(e)}'
        }), 500

@unified_bp.route('/api/unified/stats', methods=['GET'])
def get_unified_stats():
    """
    Pobieranie unified statystyk
    GET /api/unified/stats
    """
    try:
        stats = manager._get_unified_stats()
        
        return jsonify({
            'success': True,
            'data': stats,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Błąd pobierania statystyk: {str(e)}'
        }), 500

@unified_bp.route('/api/unified/record-measurement', methods=['POST'])
def record_measurement():
    """
    Unified zapis pomiaru SECTRO z auto-update kolejki
    POST /api/unified/record-measurement
    
    Body:
    {
        "raw_frame": "CZL1123456789",
        "nr_startowy": 123,          // opcjonalne
        "session_id": 1              // opcjonalne
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'raw_frame' not in data:
            return jsonify({
                'success': False,
                'error': 'Brak raw_frame w żądaniu'
            }), 400
        
        raw_frame = data['raw_frame']
        nr_startowy = data.get('nr_startowy')
        session_id = data.get('session_id')
        
        # Import SECTRO parser
        from sectro.sectro_parser import SectroParser
        
        # Parse frame
        parser = SectroParser()
        frame = parser.parse_frame(raw_frame)
        
        if not frame.is_valid:
            return jsonify({
                'success': False,
                'error': 'Nieprawidłowa ramka SECTRO'
            }), 400
        
        # Get active session if not provided
        if not session_id:
            active_session = manager._get_current_active_session()
            if not active_session:
                return jsonify({
                    'success': False,
                    'error': 'Brak aktywnej sesji SECTRO'
                }), 400
            session_id = active_session['id']
        
        # Record measurement using existing SECTRO API
        from sectro.sectro_api import sectro_bp
        from utils.database import execute_query
        
        # Import helper function
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'sectro'))
        
        # Record measurement
        measurement_id = execute_query("""
            INSERT INTO sectro_measurements 
            (session_id, nr_startowy, measurement_type, wejscie, timestamp_sectro, raw_frame)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            session_id,
            nr_startowy,
            frame.measurement_type,
            frame.input_number,
            frame.timestamp,
            raw_frame
        ))
        
        # Process measurement (similar to sectro_api._process_measurement)
        result_info = None
        if frame.measurement_type == 'START':
            # Record start time
            execute_query("""
                INSERT INTO sectro_results (session_id, nr_startowy, start_time, status)
                VALUES (%s, %s, %s, 'in_progress')
                ON CONFLICT (session_id, nr_startowy) 
                DO UPDATE SET start_time = EXCLUDED.start_time, status = 'in_progress'
            """, (session_id, nr_startowy, frame.timestamp))
            
            result_info = {'status': 'started', 'start_time': frame.timestamp}
            
        elif frame.measurement_type == 'FINISH':
            # Get start time and calculate total time
            from utils.database import get_one
            start_result = get_one("""
                SELECT start_time FROM sectro_results 
                WHERE session_id = %s AND nr_startowy = %s
            """, (session_id, nr_startowy))
            
            if start_result and start_result['start_time']:
                start_time = float(start_result['start_time'])
                total_time = frame.timestamp - start_time
                
                # Handle day rollover
                if total_time < 0:
                    total_time += 24 * 3600
                
                # Update result
                execute_query("""
                    UPDATE sectro_results 
                    SET finish_time = %s, total_time = %s, status = 'completed'
                    WHERE session_id = %s AND nr_startowy = %s
                """, (frame.timestamp, total_time, session_id, nr_startowy))
                
                result_info = {
                    'status': 'completed',
                    'start_time': start_time,
                    'finish_time': frame.timestamp,
                    'total_time': total_time
                }
        
        return jsonify({
            'success': True,
            'measurement_id': measurement_id,
            'frame': {
                'type': frame.measurement_type,
                'input': frame.input_number,
                'timestamp': frame.timestamp,
                'formatted_time': parser.format_time(frame.timestamp)
            },
            'result': result_info,
            'message': f'{frame.measurement_type} recorded for athlete {nr_startowy}'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Błąd zapisu pomiaru: {str(e)}'
        }), 500

# ===============================================
# COMPATIBILITY ENDPOINTS (backward compatibility)
# ===============================================

@unified_bp.route('/api/unified/scan-qr', methods=['POST'])
def scan_qr_compatibility():
    """
    Compatibility endpoint dla QR skanowania
    POST /api/unified/scan-qr
    
    Body:
    {
        "qr_code": "QR123",
        "action": "checkin"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'qr_code' not in data:
            return jsonify({
                'success': False,
                'error': 'Brak qr_code w żądaniu'
            }), 400
        
        qr_code = data['qr_code']
        action = data.get('action', 'checkin')
        
        # Use unified registration
        result = manager.register_athlete_unified(qr_code, action)
        
        # Format response for compatibility
        if result['success']:
            return jsonify({
                'success': True,
                'data': {
                    'zawodnik': result['athlete'],
                    'action': result['action'],
                    'message': result['message'],
                    'auto_added_to_session': result.get('auto_added_to_session', False)
                },
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify(result), 400
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Błąd skanowania QR: {str(e)}'
        }), 500

print("🔄 SKATECROSS QR - Unified Start API Blueprint załadowany") 