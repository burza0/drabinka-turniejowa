"""
SECTRO Live Timing API Blueprint
System pomiarów czasu dla zawodów SKATECROSS z urządzeniem SECTRO

Autor: Claude AI
Data: 2024
Wersja: 1.0

Obsługuje ramki SECTRO w formacie CZL1123456789:
- CZL = Prefix
- 1 = Input number (1=START, 4=FINISH) 
- 123456789 = Timestamp (HHMMSSMMM)
"""

from flask import Blueprint, request, jsonify
from database_utils import get_all, get_one, execute_query
from .sectro_parser import SectroParser
import datetime
import logging
import subprocess
import os
from typing import Dict, List, Optional

# Import SECTRO modules
from .sectro_parser import SectroParser, SectroFrame

# Create blueprint for SECTRO endpoints
sectro_bp = Blueprint('sectro', __name__, url_prefix='/api/sectro')

# Global parser instance (will be configured per session)
parser = SectroParser()

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ====== SESSION MANAGEMENT ======

@sectro_bp.route('/sessions', methods=['GET'])
def get_sessions():
    """Get list of all SECTRO sessions"""
    try:
        sessions = get_all("""
            SELECT s.id, s.nazwa, s.kategoria, s.plec, s.start_time, s.end_time, s.status, s.config,
                   COUNT(r.id) as results_count,
                   COUNT(CASE WHEN r.status = 'completed' THEN 1 END) as completed_count
            FROM sectro_sessions s
            LEFT JOIN sectro_results r ON s.id = r.session_id
            GROUP BY s.id, s.nazwa, s.kategoria, s.plec, s.start_time, s.end_time, s.status
            ORDER BY s.created_at DESC
        """)
        
        return jsonify({
            'success': True,
            'sessions': sessions,
            'count': len(sessions)
        })
        
    except Exception as e:
        logger.error(f"Error getting sessions: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@sectro_bp.route('/sessions', methods=['POST'])
def create_session():
    """Create new SECTRO session"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['nazwa']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing field: {field}'}), 400
        
        # Map frontend values to database values
        kategoria = data.get('kategoria', '')
        if kategoria == 'Wszystkie':
            kategoria = ''
            
        plec = data.get('plec', '')
        if plec == 'Wszystkie':
            plec = ''
        elif plec == 'Mężczyźni':
            plec = 'M'
        elif plec == 'Kobiety':
            plec = 'K'
        else:
            # Jeśli przyszło 'M' lub 'K' bezpośrednio, zostaw jak jest
            if plec not in ['M', 'K']:
                plec = ''
        
        # Insert session with proper status
        session_id = execute_query("""
            INSERT INTO sectro_sessions (nazwa, kategoria, plec, wejscie_start, wejscie_finish, config, status)
            VALUES (%s, %s, %s, %s, %s, %s, 'active')
            RETURNING id
        """, (
            data['nazwa'],
            kategoria,
            plec,
            data.get('wejscie_start', 1),
            data.get('wejscie_finish', 4),
            data.get('config', '{}')
        ))
        
        # Get created session
        session = get_one("""
            SELECT * FROM sectro_sessions WHERE id = %s
        """, (session_id,))
        
        # Log creation
        _log_session_event(session_id, 'INFO', f"Session created: {data['nazwa']}")
        
        return jsonify({
            'success': True,
            'session': session
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating session: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@sectro_bp.route('/sessions/<int:session_id>', methods=['GET'])
def get_session(session_id):
    """Get single session with details"""
    try:
        session = get_one("""
            SELECT * FROM sectro_sessions WHERE id = %s
        """, (session_id,))
        
        if not session:
            return jsonify({'success': False, 'error': 'Session not found'}), 404
        
        # Get session statistics
        stats = get_one("""
            SELECT 
                COUNT(DISTINCT m.nr_startowy) as athletes_measured,
                COUNT(r.id) as results_count,
                COUNT(CASE WHEN r.status = 'completed' THEN 1 END) as completed_count,
                MIN(r.total_time) as best_time,
                AVG(r.total_time) as avg_time
            FROM sectro_sessions s
            LEFT JOIN sectro_measurements m ON s.id = m.session_id AND m.measurement_type IN ('START', 'FINISH')
            LEFT JOIN sectro_results r ON s.id = r.session_id
            WHERE s.id = %s
            GROUP BY s.id
        """, (session_id,))
        
        return jsonify({
            'success': True,
            'session': session,
            'statistics': stats
        })
        
    except Exception as e:
        logger.error(f"Error getting session {session_id}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@sectro_bp.route('/sessions/<int:session_id>/start', methods=['POST'])
def start_session(session_id):
    """Start timing session"""
    try:
        # Update session status
        execute_query("""
            UPDATE sectro_sessions 
            SET status = 'active', start_time = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (session_id,))
        
        # Log event
        _log_session_event(session_id, 'INFO', "Session started")
        
        # Uruchom skrypt sectro_manual.py w tle
        script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sectro_manual.py')
        subprocess.Popen(['python3', script_path], 
                        env=dict(os.environ, SESSION_ID=str(session_id)))
        
        return jsonify({
            'success': True,
            'message': 'Session started and manual timing script launched',
            'session_id': session_id
        })
        
    except Exception as e:
        logger.error(f"Error starting session {session_id}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@sectro_bp.route('/sessions/<int:session_id>/stop', methods=['POST'])
def stop_session(session_id):
    """Stop timing session"""
    try:
        # Update session status
        execute_query("""
            UPDATE sectro_sessions 
            SET status = 'completed', end_time = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (session_id,))
        
        # Log event
        _log_session_event(session_id, 'INFO', "Session stopped")
        
        return jsonify({
            'success': True,
            'message': 'Session stopped',
            'session_id': session_id
        })
        
    except Exception as e:
        logger.error(f"Error stopping session {session_id}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ====== MEASUREMENTS ======

@sectro_bp.route('/measurements', methods=['POST'])
def record_measurement():
    """Record new measurement from SECTRO device"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['session_id', 'raw_frame']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'Missing field: {field}'}), 400
        
        session_id = data['session_id']
        raw_frame = data['raw_frame']
        nr_startowy = data.get('nr_startowy')
        
        # Parse frame
        frame = parser.parse_frame(raw_frame)
        
        if not frame.is_valid:
            _log_session_event(session_id, 'ERROR', f"Invalid frame: {raw_frame}")
            return jsonify({'success': False, 'error': 'Invalid frame format'}), 400
        
        # Skip sync frames for measurements
        if frame.is_sync:
            _log_session_event(session_id, 'FRAME', f"Sync frame ignored: {raw_frame}")
            return jsonify({'success': True, 'message': 'Sync frame ignored'})
        
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
        
        # Process measurement (create/update result)
        result = _process_measurement(session_id, nr_startowy, frame)
        
        # Log event
        _log_session_event(session_id, 'INFO', 
                          f"{frame.measurement_type} recorded for athlete {nr_startowy}: {parser.format_time(frame.timestamp)}")
        
        return jsonify({
            'success': True,
            'measurement_id': measurement_id,
            'frame': {
                'type': frame.measurement_type,
                'input': frame.input_number,
                'timestamp': frame.timestamp,
                'formatted_time': parser.format_time(frame.timestamp)
            },
            'result': result
        })
        
    except Exception as e:
        logger.error(f"Error recording measurement: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@sectro_bp.route('/sessions/<int:session_id>/results', methods=['GET'])
def get_session_results(session_id):
    """Get results for session"""
    try:
        results = get_all("""
            SELECT r.*, z.imie, z.nazwisko, z.kategoria, z.plec, z.klub
            FROM sectro_results r
            LEFT JOIN zawodnicy z ON r.nr_startowy = z.nr_startowy
            WHERE r.session_id = %s
            ORDER BY r.total_time ASC
        """, (session_id,))
        
        # Add positions
        for i, result in enumerate(results):
            result['position'] = i + 1
        
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })
        
    except Exception as e:
        logger.error(f"Error getting results for session {session_id}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ====== HARDWARE STATUS ======

@sectro_bp.route('/hardware/status', methods=['GET'])
def get_hardware_status():
    """Get SECTRO hardware connection status"""
    try:
        # This would be implemented with actual hardware monitoring
        # For now, return mock status
        status = {
            'connected': False,
            'port': '/dev/ttyUSB0',
            'baudrate': 115200,
            'last_frame': None,
            'frame_count': 0,
            'error_count': 0
        }
        
        return jsonify({
            'success': True,
            'hardware': status
        })
        
    except Exception as e:
        logger.error(f"Error getting hardware status: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ====== LOGS ======

@sectro_bp.route('/logs', methods=['GET'])
def get_logs():
    """Get SECTRO logs"""
    try:
        session_id = request.args.get('session_id')
        limit = int(request.args.get('limit', 100))
        
        query = """
            SELECT * FROM sectro_logs
        """
        params = []
        
        if session_id:
            query += " WHERE session_id = %s"
            params.append(session_id)
        
        query += " ORDER BY created_at DESC LIMIT %s"
        params.append(limit)
        
        logs = get_all(query, params)
        
        return jsonify({
            'success': True,
            'logs': logs,
            'count': len(logs)
        })
        
    except Exception as e:
        logger.error(f"Error getting logs: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


# ====== HELPER FUNCTIONS ======

def _process_measurement(session_id: int, nr_startowy: int, frame: SectroFrame) -> Optional[Dict]:
    """Process measurement and create/update result"""
    try:
        if frame.measurement_type == 'START':
            # Record start time
            execute_query("""
                INSERT INTO sectro_results (session_id, nr_startowy, start_time, status)
                VALUES (%s, %s, %s, 'in_progress')
                ON CONFLICT (session_id, nr_startowy) 
                DO UPDATE SET start_time = EXCLUDED.start_time, status = 'in_progress'
            """, (session_id, nr_startowy, frame.timestamp))
            
            return {'status': 'started', 'start_time': frame.timestamp}
            
        elif frame.measurement_type == 'FINISH':
            # Get start time and calculate total time
            logger.info(f"🔍 Processing FINISH for athlete {nr_startowy}, session {session_id}")
            start_result = get_one("""
                SELECT start_time FROM sectro_results 
                WHERE session_id = %s AND nr_startowy = %s
            """, (session_id, nr_startowy))
            
            logger.info(f"🔍 Start result for athlete {nr_startowy}: {start_result}")
            
            if start_result and start_result['start_time']:
                # Convert Decimal to float for calculation
                start_time = float(start_result['start_time'])
                total_time = frame.timestamp - start_time
                logger.info(f"🔍 Calculated total_time: {total_time} (finish: {frame.timestamp}, start: {start_time})")
                
                # Handle day rollover
                if total_time < 0:
                    total_time += 24 * 3600
                    logger.info(f"🔍 Adjusted for day rollover: {total_time}")
                
                # Update result
                logger.info(f"🔍 Updating result for athlete {nr_startowy}")
                rows_updated = execute_query("""
                    UPDATE sectro_results 
                    SET finish_time = %s, total_time = %s, status = 'completed'
                    WHERE session_id = %s AND nr_startowy = %s
                """, (frame.timestamp, total_time, session_id, nr_startowy))
                
                logger.info(f"🔍 UPDATE affected {rows_updated} rows")
                
                return {
                    'status': 'completed',
                    'start_time': start_time,
                    'finish_time': frame.timestamp,
                    'total_time': total_time,
                    'formatted_time': parser.format_time(total_time)
                }
            else:
                # Finish without start - record as error
                logger.warning(f"❌ FINISH without START for athlete {nr_startowy}, start_result: {start_result}")
                _log_session_event(session_id, 'WARNING', 
                                 f"FINISH without START for athlete {nr_startowy}")
                return {'status': 'error', 'message': 'Finish without start'}
        
        return None
        
    except Exception as e:
        logger.error(f"Error processing measurement: {e}")
        return {'status': 'error', 'message': str(e)}


def _log_session_event(session_id: int, log_type: str, message: str, raw_data: str = None):
    """Log session event"""
    try:
        execute_query("""
            INSERT INTO sectro_logs (session_id, log_type, message, raw_data)
            VALUES (%s, %s, %s, %s)
        """, (session_id, log_type, message, raw_data))
    except Exception as e:
        logger.error(f"Error logging event: {e}")


# Initialize init file for module
def create_init_file():
    """Create __init__.py for sectro module"""
    init_content = '''"""SECTRO Live Timing Module"""

from .sectro_parser import SectroParser, SectroFrame
from .sectro_api import sectro_bp

__all__ = ['SectroParser', 'SectroFrame', 'sectro_bp']
'''
    
    with open(os.path.join(os.path.dirname(__file__), '__init__.py'), 'w') as f:
        f.write(init_content)


if __name__ == "__main__":
    # Create init file when run directly
    create_init_file()
    print("SECTRO API module initialized!") 