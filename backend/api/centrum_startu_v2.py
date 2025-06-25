# -*- coding: utf-8 -*-
"""
SKATECROSS v37.0 - Centrum Startu v2.0
Zrefaktoryzowana wersja z integracją SECTRO Live Timing
"""

from flask import Blueprint, jsonify, request
from datetime import datetime
import sys
import os
import json

# Dodaj ścieżkę do utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.database import get_all, get_one, execute_query

centrum_startu_v2_bp = Blueprint('centrum_startu_v2', __name__)

# ===============================================
# CORE FUNCTIONS - Single Source of Truth
# ===============================================

class CentrumStartuManager:
    """Centralny manager dla wszystkich operacji centrum startu"""
    
    def __init__(self):
        self.active_sessions = {}  # Cache aktywnych sesji SECTRO
    
    def get_grupy_startowe(self):
        """Pobiera grupy startowe z TYLKO zameldowanymi zawodnikami"""
        zawodnicy = get_all("""
            SELECT nr_startowy, imie, nazwisko, kategoria, plec, klub, qr_code,
                   COALESCE(checked_in, false) as checked_in, check_in_time
            FROM zawodnicy 
            WHERE COALESCE(checked_in, false) = true 
            AND kategoria IS NOT NULL 
            AND plec IS NOT NULL
            ORDER BY kategoria, plec, nr_startowy
        """)
        
        # Grupuj po kategoria + płeć
        grupy = {}
        for zawodnik in zawodnicy:
            key = f"{zawodnik['kategoria']}_{zawodnik['plec']}"
            if key not in grupy:
                grupy[key] = {
                    'kategoria': zawodnik['kategoria'],
                    'plec': zawodnik['plec'],
                    'zawodnicy': []
                }
            grupy[key]['zawodnicy'].append(zawodnik)
        
        # Przekształć na format odpowiedzi
        grupy_list = []
        for i, (key, grupa) in enumerate(sorted(grupy.items()), 1):
            plec_nazwa = 'Mężczyźni' if grupa['plec'] == 'M' else 'Kobiety'
            nazwa_grupy = f"Grupa {i}: {grupa['kategoria']} {plec_nazwa}"
            
            grupy_list.append({
                'numer_grupy': i,
                'key': key,
                'nazwa': nazwa_grupy,
                'kategoria': grupa['kategoria'],
                'plec': grupa['plec'],
                'zawodnicy': grupa['zawodnicy'],
                'liczba_zawodnikow': len(grupa['zawodnicy']),
                'status': self._get_grupa_status(grupa['kategoria'], grupa['plec']),
                'sectro_session_id': self._get_sectro_session_id(grupa['kategoria'], grupa['plec']),
                'estimated_time': len(grupa['zawodnicy']) * 20  # 20s na zawodnika
            })
        
        return grupy_list
    
    def _get_grupa_status(self, kategoria, plec):
        """Sprawdza status grupy (WAITING, ACTIVE, TIMING, COMPLETED)"""
        # Sprawdź czy istnieje aktywna sesja SECTRO dla tej grupy
        session = get_one("""
            SELECT id, status FROM sectro_sessions 
            WHERE kategoria = %s AND plec = %s 
            AND status IN ('active', 'timing')
            ORDER BY created_at DESC LIMIT 1
        """, (kategoria, plec))
        
        if session:
            return 'TIMING' if session['status'] == 'timing' else 'ACTIVE'
        
        # Sprawdź czy grupa ma jakichś zawodników zameldowanych
        count = get_one("""
            SELECT COUNT(*) as count FROM zawodnicy 
            WHERE kategoria = %s AND plec = %s AND COALESCE(checked_in, false) = true
        """, (kategoria, plec))
        
        return 'WAITING' if count and count['count'] > 0 else 'EMPTY'
    
    def _get_sectro_session_id(self, kategoria, plec):
        """Pobiera ID aktywnej sesji SECTRO dla grupy"""
        session = get_one("""
            SELECT id FROM sectro_sessions 
            WHERE kategoria = %s AND plec = %s 
            AND status IN ('active', 'timing')
            ORDER BY created_at DESC LIMIT 1
        """, (kategoria, plec))
        
        return session['id'] if session else None
    
    def activate_grupa(self, kategoria, plec, nazwa):
        """Aktywuje grupę i automatycznie tworzy sesję SECTRO"""
        try:
            # 1. Sprawdź czy grupa ma zameldowanych zawodników
            zawodnicy = get_all("""
                SELECT nr_startowy, imie, nazwisko FROM zawodnicy 
                WHERE kategoria = %s AND plec = %s AND COALESCE(checked_in, false) = true
            """, (kategoria, plec))
            
            if not zawodnicy:
                return {'success': False, 'error': 'Grupa nie ma zameldowanych zawodników'}
            
            # 2. Sprawdź czy już istnieje aktywna sesja
            existing_session = get_one("""
                SELECT id, status FROM sectro_sessions 
                WHERE kategoria = %s AND plec = %s 
                AND status IN ('active', 'timing')
            """, (kategoria, plec))
            
            if existing_session:
                return {
                    'success': True, 
                    'action': 'already_active',
                    'sectro_session_id': existing_session['id'],
                    'message': f'Grupa {nazwa} już ma aktywną sesję SECTRO'
                }
            
            # 3. Utwórz nową sesję SECTRO
            session_id = execute_query("""
                INSERT INTO sectro_sessions (nazwa, kategoria, plec, status, config)
                VALUES (%s, %s, %s, 'active', %s)
                RETURNING id
            """, (
                nazwa, 
                kategoria, 
                plec, 
                json.dumps({
                    'wejscie_start': 1,
                    'wejscie_finish': 4,
                    'auto_created': True,
                    'zawodnicy_count': len(zawodnicy)
                })
            ))
            
            # 4. Dodaj zawodników do sesji (puste STARTy)
            for zawodnik in zawodnicy:
                execute_query("""
                    INSERT INTO sectro_results (session_id, nr_startowy, status)
                    VALUES (%s, %s, 'in_progress')
                """, (session_id, zawodnik['nr_startowy']))
            
            # 5. Zaloguj wydarzenie
            execute_query("""
                INSERT INTO sectro_logs (session_id, log_type, message)
                VALUES (%s, 'INFO', %s)
            """, (session_id, f'Auto-created session for {nazwa} with {len(zawodnicy)} athletes'))
            
            return {
                'success': True,
                'action': 'activated',
                'sectro_session_id': session_id,
                'zawodnicy_count': len(zawodnicy),
                'message': f'Grupa {nazwa} aktywowana z sesją SECTRO #{session_id}'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def deactivate_grupa(self, kategoria, plec):
        """Deaktywuje grupę i kończy sesję SECTRO"""
        try:
            # Znajdź aktywną sesję
            session = get_one("""
                SELECT id FROM sectro_sessions 
                WHERE kategoria = %s AND plec = %s 
                AND status IN ('active', 'timing')
                ORDER BY created_at DESC LIMIT 1
            """, (kategoria, plec))
            
            if not session:
                return {'success': False, 'error': 'Brak aktywnej sesji do deaktywacji'}
            
            # Zakończ sesję
            execute_query("""
                UPDATE sectro_sessions 
                SET status = 'completed', end_time = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (session['id'],))
            
            # Zaloguj
            execute_query("""
                INSERT INTO sectro_logs (session_id, log_type, message)
                VALUES (%s, 'INFO', %s)
            """, (session['id'], f'Session manually deactivated'))
            
            return {
                'success': True,
                'action': 'deactivated',
                'sectro_session_id': session['id'],
                'message': 'Grupa deaktywowana, sesja SECTRO zakończona'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def meluj_zawodnika(self, nr_startowy, action='checkin'):
        """Melduje/wymeldowuje zawodnika z walidacją"""
        try:
            # Pobierz dane zawodnika
            zawodnik = get_one("""
                SELECT nr_startowy, imie, nazwisko, kategoria, plec, klub,
                       COALESCE(checked_in, false) as checked_in
                FROM zawodnicy WHERE nr_startowy = %s
            """, (nr_startowy,))
            
            if not zawodnik:
                return {'success': False, 'error': f'Zawodnik #{nr_startowy} nie istnieje'}
            
            if not zawodnik['kategoria'] or not zawodnik['plec']:
                return {'success': False, 'error': 'Zawodnik nie ma przypisanej kategorii/płci'}
            
            new_status = True if action == 'checkin' else False
            
            # Aktualizuj status
            execute_query("""
                UPDATE zawodnicy 
                SET checked_in = %s, 
                    check_in_time = CASE WHEN %s = true THEN CURRENT_TIMESTAMP ELSE NULL END
                WHERE nr_startowy = %s
            """, (new_status, new_status, nr_startowy))
            
            # Jeśli meldowanie - sprawdź czy trzeba dodać do aktywnej sesji SECTRO
            if new_status:
                session = get_one("""
                    SELECT id FROM sectro_sessions 
                    WHERE kategoria = %s AND plec = %s 
                    AND status IN ('active', 'timing')
                    ORDER BY created_at DESC LIMIT 1
                """, (zawodnik['kategoria'], zawodnik['plec']))
                
                if session:
                    # Dodaj do sesji SECTRO
                    execute_query("""
                        INSERT INTO sectro_results (session_id, nr_startowy, status)
                        VALUES (%s, %s, 'in_progress')
                        ON CONFLICT (session_id, nr_startowy) DO NOTHING
                    """, (session['id'], nr_startowy))
            
            return {
                'success': True,
                'action': action,
                'zawodnik': zawodnik,
                'message': f'Zawodnik #{nr_startowy} {action}ed'
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_live_queue(self):
        """Pobiera aktualną kolejkę startową z priorytetami"""
        # Najpierw sprawdź czy są aktywne sesje SECTRO
        active_sessions = get_all("""
            SELECT id, nazwa, kategoria, plec, status 
            FROM sectro_sessions 
            WHERE status IN ('active', 'timing')
            ORDER BY created_at DESC
        """)
        
        if active_sessions:
            # Pobierz zawodników z aktywnych sesji SECTRO
            sectro_queue = get_all("""
                SELECT z.nr_startowy, z.imie, z.nazwisko, z.kategoria, z.plec, z.klub,
                       r.status as sectro_status, s.id as session_id, s.nazwa as session_name,
                       z.check_in_time, 'SECTRO_ACTIVE' as source_type
                FROM sectro_results r
                JOIN sectro_sessions s ON r.session_id = s.id
                JOIN zawodnicy z ON r.nr_startowy = z.nr_startowy
                WHERE s.status IN ('active', 'timing')
                AND z.checked_in = true
                ORDER BY s.created_at, z.nr_startowy
            """)
            
            if sectro_queue:
                return sectro_queue
        
        # Fallback: pokaż zameldowanych zawodników
        sectro_queue = get_all("""
            SELECT nr_startowy, imie, nazwisko, kategoria, plec, klub,
                   'in_progress' as sectro_status, NULL as session_id, NULL as session_name,
                   check_in_time, 'CHECKED_IN' as source_type
            FROM zawodnicy 
            WHERE checked_in = true
            ORDER BY check_in_time
        """)
        
        return sectro_queue

# Instancja managera
manager = CentrumStartuManager()

# ===============================================
# API ENDPOINTS - v2.0
# ===============================================

@centrum_startu_v2_bp.route('/api/v2/grupy-startowe', methods=['GET'])
def get_grupy_startowe_v2():
    """Pobieranie grup startowych v2.0 z integracją SECTRO"""
    try:
        grupy = manager.get_grupy_startowe()
        
        return jsonify({
            'success': True,
            'data': {
                'grupy': grupy,
                'total_grup': len(grupy),
                'total_zawodnikow': sum(g['liczba_zawodnikow'] for g in grupy)
            },
            'version': '2.0',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@centrum_startu_v2_bp.route('/api/v2/grupa/activate', methods=['POST'])
def activate_grupa_v2():
    """Aktywacja grupy z automatycznym tworzeniem sesji SECTRO"""
    try:
        data = request.get_json()
        kategoria = data.get('kategoria')
        plec = data.get('plec')
        nazwa = data.get('nazwa')
        
        if not all([kategoria, plec, nazwa]):
            return jsonify({'success': False, 'error': 'Brak wymaganych danych'}), 400
        
        result = manager.activate_grupa(kategoria, plec, nazwa)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@centrum_startu_v2_bp.route('/api/v2/grupa/deactivate', methods=['POST'])
def deactivate_grupa_v2():
    """Deaktywacja grupy i zakończenie sesji SECTRO"""
    try:
        data = request.get_json()
        kategoria = data.get('kategoria')
        plec = data.get('plec')
        
        if not all([kategoria, plec]):
            return jsonify({'success': False, 'error': 'Brak wymaganych danych'}), 400
        
        result = manager.deactivate_grupa(kategoria, plec)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@centrum_startu_v2_bp.route('/api/v2/checkin', methods=['POST'])
def checkin_v2():
    """Meldowanie zawodnika v2.0 z walidacją i integracją SECTRO"""
    try:
        data = request.get_json()
        
        # Obsługa różnych formatów danych
        if 'nr_startowy' in data:
            nr_startowy = data['nr_startowy']
        elif 'qr_code' in data:
            # Znajdź zawodnika po QR
            zawodnik = get_one("""
                SELECT nr_startowy FROM zawodnicy WHERE qr_code = %s
            """, (data['qr_code'],))
            if not zawodnik:
                return jsonify({'success': False, 'error': 'Nie znaleziono zawodnika o podanym QR'}), 404
            nr_startowy = zawodnik['nr_startowy']
        else:
            return jsonify({'success': False, 'error': 'Brak nr_startowy lub qr_code'}), 400
        
        action = data.get('action', 'checkin')
        
        result = manager.meluj_zawodnika(nr_startowy, action)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@centrum_startu_v2_bp.route('/api/v2/queue', methods=['GET'])
def get_queue_v2():
    """Pobieranie kolejki startowej v2.0 z priorytetami SECTRO"""
    try:
        queue = manager.get_live_queue()
        
        return jsonify({
            'success': True,
            'data': queue,
            'count': len(queue),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@centrum_startu_v2_bp.route('/api/v2/stats', methods=['GET'])
def get_stats_v2():
    """Statystyki centrum startu v2.0"""
    try:
        stats = get_one("""
            SELECT 
                COUNT(*) as total_zawodnicy,
                COUNT(CASE WHEN COALESCE(checked_in, false) = true THEN 1 END) as zameldowani,
                COUNT(CASE WHEN COALESCE(checked_in, false) = false THEN 1 END) as niezameldowani,
                COUNT(DISTINCT kategoria) as liczba_kategorii
            FROM zawodnicy
        """)
        
        # Statystyki sesji SECTRO
        sectro_stats = get_one("""
            SELECT 
                COUNT(*) as total_sessions,
                COUNT(CASE WHEN status = 'active' THEN 1 END) as active_sessions,
                COUNT(CASE WHEN status = 'timing' THEN 1 END) as timing_sessions,
                COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_sessions
            FROM sectro_sessions
        """)
        
        return jsonify({
            'success': True,
            'data': {
                'zawodnicy': dict(stats) if stats else {},
                'sectro': dict(sectro_stats) if sectro_stats else {},
                'grupy_startowe': len(manager.get_grupy_startowe())
            },
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@centrum_startu_v2_bp.route('/api/v2/cleanup', methods=['POST'])
def cleanup_v2():
    """Czyszczenie starych sesji SECTRO"""
    try:
        data = request.get_json() or {}
        cleanup_type = data.get('type', 'old_sessions')
        
        if cleanup_type == 'old_sessions':
            # Zakończ wszystkie stare sesje bez przypisanych zawodników
            rows_affected = execute_query("""
                UPDATE sectro_sessions 
                SET status = 'cancelled', end_time = CURRENT_TIMESTAMP
                WHERE status = 'active' 
                AND id NOT IN (
                    SELECT DISTINCT session_id 
                    FROM sectro_results 
                    WHERE session_id IS NOT NULL
                )
            """)
            
            return jsonify({
                'success': True,
                'message': f'Wyczyszczono {rows_affected} starych sesji',
                'type': cleanup_type
            })
        
        elif cleanup_type == 'empty_sessions':
            # Usuń sesje bez wyników
            rows_affected = execute_query("""
                DELETE FROM sectro_sessions 
                WHERE id NOT IN (
                    SELECT DISTINCT session_id 
                    FROM sectro_results 
                    WHERE session_id IS NOT NULL
                )
                AND status != 'completed'
            """)
            
            return jsonify({
                'success': True,
                'message': f'Usunięto {rows_affected} pustych sesji',
                'type': cleanup_type
            })
        
        else:
            return jsonify({'success': False, 'error': 'Nieznany typ czyszczenia'}), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

print("🏁 SKATECROSS v37.0 - Centrum Startu v2.0 z integracją SECTRO załadowany!")