# -*- coding: utf-8 -*-
"""
SKATECROSS QR - Unified Start Manager
Wersja: 1.0.0
Unified system łączący Centrum Startu z SECTRO Live Timing
"""

from flask import Blueprint, jsonify, request
from datetime import datetime
import sys
import os
import json

# Dodaj ścieżkę do utils
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
from utils.database import get_all, get_one, execute_query

class UnifiedStartManager:
    """
    Centralny manager dla wszystkich operacji startowych
    Łączy funkcjonalności Centrum Startu z SECTRO Live Timing
    """
    
    def __init__(self):
        self.active_session_cache = None
    
    def register_athlete_unified(self, identifier, action='checkin'):
        """
        Unified rejestracja zawodnika z auto-dodaniem do aktywnej sesji
        
        Args:
            identifier: nr_startowy (int) lub qr_code (str)
            action: 'checkin' lub 'checkout'
        """
        try:
            # Znajdź zawodnika
            athlete = self._find_athlete(identifier)
            if not athlete:
                return {'success': False, 'error': 'Zawodnik nie znaleziony'}
            
            # Sprawdź czy ma kategorię i płeć
            if not athlete['kategoria'] or not athlete['plec']:
                return {'success': False, 'error': 'Zawodnik nie ma przypisanej kategorii/płci'}
            
            nr_startowy = athlete['nr_startowy']
            new_status = True if action == 'checkin' else False
            
            # Aktualizuj status meldowania
            execute_query("""
                UPDATE zawodnicy 
                SET checked_in = %s, 
                    check_in_time = CASE WHEN %s = true THEN CURRENT_TIMESTAMP ELSE NULL END
                WHERE nr_startowy = %s
            """, (new_status, new_status, nr_startowy))
            
            # Jeśli checkin - sprawdź aktywną sesję i dodaj automatycznie
            if new_status:
                active_session = self._get_active_session_for_athlete(athlete)
                if active_session:
                    self._add_athlete_to_session(active_session['id'], nr_startowy)
            
            # Odśwież dane zawodnika
            updated_athlete = self._find_athlete(nr_startowy)
            
            return {
                'success': True,
                'action': action,
                'athlete': updated_athlete,
                'auto_added_to_session': bool(active_session) if new_status else False,
                'message': f'Zawodnik #{nr_startowy} {action}ed'
            }
            
        except Exception as e:
            return {'success': False, 'error': f'Błąd rejestracji: {str(e)}'}
    
    def activate_group_unified(self, kategoria, plec, nazwa=None):
        """
        Unified aktywacja grupy z automatycznym tworzeniem sesji SECTRO
        
        Args:
            kategoria: kategoria zawodników
            plec: płeć zawodników  
            nazwa: opcjonalna nazwa sesji
        """
        try:
            # Sprawdź zawodników w grupie (zarówno zameldowanych jak i niezameldowanych)
            all_athletes = get_all("""
                SELECT nr_startowy, imie, nazwisko, kategoria, plec, klub, COALESCE(checked_in, false) as checked_in
                FROM zawodnicy 
                WHERE kategoria = %s AND plec = %s
                ORDER BY nr_startowy
            """, (kategoria, plec))
            
            checked_in_athletes = [a for a in all_athletes if a['checked_in']]
            
            if not all_athletes:
                return {'success': False, 'error': 'Brak zawodników w kategorii/płci'}
            
            # Pozwól na aktywację nawet bez zameldowanych - administrator może chcieć przygotować sesję
            athletes = checked_in_athletes if checked_in_athletes else all_athletes
            
            # Sprawdź czy już istnieje aktywna sesja dla tej grupy
            existing_session = get_one("""
                SELECT id, nazwa, status FROM sectro_sessions 
                WHERE kategoria = %s AND plec = %s 
                AND status IN ('active', 'timing')
                ORDER BY created_at DESC LIMIT 1
            """, (kategoria, plec))
            
            if existing_session:
                # Dodaj zameldowanych zawodników do istniejącej sesji (na wypadek gdyby ich brakowało)
                session_id = existing_session['id']
                athletes_added = 0
                for athlete in athletes:
                    execute_query("""
                        INSERT INTO sectro_results (session_id, nr_startowy, status, created_at)
                        VALUES (%s, %s, 'dns', CURRENT_TIMESTAMP)
                        ON CONFLICT (session_id, nr_startowy) DO NOTHING
                    """, (session_id, athlete['nr_startowy']))
                    athletes_added += 1
                
                return {
                    'success': True,
                    'action': 'already_active',
                    'session': existing_session,
                    'athletes_count': len(athletes),
                    'athletes_added': athletes_added,
                    'message': f'Grupa już ma aktywną sesję SECTRO #{existing_session["id"]} (dodano {athletes_added} zawodników)'
                }
            
            # Utwórz nową sesję SECTRO automatycznie
            if not nazwa:
                plec_nazwa = 'Mężczyźni' if plec == 'M' else 'Kobiety'
                nazwa = f'Auto: {kategoria} {plec_nazwa}'
            
            # Najpierw wstaw sesję
            execute_query("""
                INSERT INTO sectro_sessions (nazwa, kategoria, plec, status, config, created_at)
                VALUES (%s, %s, %s, 'active', %s, CURRENT_TIMESTAMP)
            """, (
                nazwa,
                kategoria, 
                plec,
                json.dumps({
                    'wejscie_start': 1,
                    'wejscie_finish': 4,
                    'auto_created': True,
                    'created_from_group': f'{kategoria}_{plec}',
                    'athletes_count': len(athletes)
                })
            ))
            
            # Potem pobierz ID najnowszej sesji
            session_data = get_one("""
                SELECT id FROM sectro_sessions 
                WHERE kategoria = %s AND plec = %s AND status = 'active'
                ORDER BY created_at DESC LIMIT 1
            """, (kategoria, plec))
            
            if not session_data:
                return {'success': False, 'error': 'Nie udało się utworzyć sesji'}
            
            session_id = session_data['id']
            
            # Dodaj wszystkich zawodników do sesji (z logowaniem)
            athletes_added = 0
            for athlete in athletes:
                execute_query("""
                    INSERT INTO sectro_results (session_id, nr_startowy, status, created_at)
                    VALUES (%s, %s, 'dns', CURRENT_TIMESTAMP)
                    ON CONFLICT (session_id, nr_startowy) DO NOTHING
                """, (session_id, athlete['nr_startowy']))
                athletes_added += 1
            
            # Zaloguj utworzenie sesji
            execute_query("""
                INSERT INTO sectro_logs (session_id, log_type, message, created_at)
                VALUES (%s, 'INFO', %s, CURRENT_TIMESTAMP)
            """, (session_id, f'Auto-created unified session for {nazwa} with {len(athletes)} athletes'))
            
            # Pobierz utworzoną sesję
            session = get_one("""
                SELECT id, nazwa, kategoria, plec, status, config, created_at
                FROM sectro_sessions WHERE id = %s
            """, (session_id,))
            
            # Ustaw jako aktywną w cache
            self.active_session_cache = session
            
            return {
                'success': True,
                'action': 'activated',
                'session': session,
                'athletes_added': len(athletes),
                'group': f'{kategoria} {plec}',
                'message': f'Grupa {nazwa} aktywowana z sesją SECTRO #{session_id}'
            }
            
        except Exception as e:
            return {'success': False, 'error': f'Błąd aktywacji grupy: {str(e)}'}
    
    def deactivate_group_unified(self, kategoria, plec):
        """Deaktywuje grupę i kończy sesję SECTRO"""
        try:
            # Znajdź aktywną sesję
            session = get_one("""
                SELECT id, nazwa FROM sectro_sessions 
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
                INSERT INTO sectro_logs (session_id, log_type, message, created_at)
                VALUES (%s, 'INFO', %s, CURRENT_TIMESTAMP)
            """, (session['id'], 'Session manually deactivated via unified system'))
            
            # Wyczyść cache
            self.active_session_cache = None
            
            return {
                'success': True,
                'action': 'deactivated',
                'session_id': session['id'],
                'message': f'Grupa deaktywowana, sesja {session["nazwa"]} zakończona'
            }
            
        except Exception as e:
            return {'success': False, 'error': f'Błąd deaktywacji: {str(e)}'}
    
    def get_unified_queue(self):
        """
        Pobiera unified kolejkę startową z priorytetami SECTRO - BEZ DUPLIKATÓW
        """
        try:
            # NAPRAWIONE zapytanie - dla każdego zawodnika tylko jedna najlepsza sesja
            queue = get_all("""
                WITH best_sessions AS (
                    SELECT DISTINCT ON (z.nr_startowy)
                        z.nr_startowy,
                        z.imie,
                        z.nazwisko, 
                        z.kategoria,
                        z.plec,
                        z.klub,
                        z.checked_in,
                        z.check_in_time,
                        
                        -- SECTRO data (najlepsza sesja)
                        s.id as session_id,
                        s.nazwa as session_name,
                        s.status as session_status,
                        r.status as sectro_status,
                        r.start_time,
                        r.finish_time,
                        r.total_time,
                        
                        -- Session priority (niższe = lepsze)
                        CASE 
                            WHEN s.status = 'active' THEN 1
                            WHEN s.status = 'timing' THEN 2  
                            WHEN s.status = 'completed' THEN 3
                            WHEN s.status = 'cancelled' THEN 4
                            ELSE 5
                        END as session_priority
                        
                    FROM zawodnicy z
                    LEFT JOIN sectro_results r ON z.nr_startowy = r.nr_startowy
                    LEFT JOIN sectro_sessions s ON r.session_id = s.id
                    WHERE z.checked_in = true 
                    AND s.status IN ('active', 'timing')
                    ORDER BY z.nr_startowy, session_priority ASC, s.created_at DESC
                )
                SELECT 
                    nr_startowy,
                    imie,
                    nazwisko, 
                    kategoria,
                    plec,
                    klub,
                    checked_in,
                    check_in_time,
                    session_id,
                    session_name,
                    session_status,
                    sectro_status,
                    start_time,
                    finish_time,
                    total_time,
                    
                    -- Unified status calculation
                    CASE 
                        WHEN total_time IS NOT NULL THEN 'FINISHED'
                        WHEN start_time IS NOT NULL THEN 'TIMING' 
                        WHEN session_id IS NOT NULL THEN 'READY'
                        WHEN checked_in = true THEN 'REGISTERED'
                        ELSE 'WAITING'
                    END as unified_status,
                    
                    -- Source type
                    CASE
                        WHEN session_status IN ('active', 'timing') THEN 'SECTRO_ACTIVE'
                        WHEN checked_in = true THEN 'CHECKED_IN'
                        ELSE 'MANUAL'
                    END as source_type,
                    
                    -- Priority for sorting (niższe = wyższy priorytet)
                    CASE 
                        WHEN start_time IS NOT NULL AND finish_time IS NULL THEN 1  -- Currently timing
                        WHEN session_status = 'active' AND session_id IS NOT NULL THEN 2   -- Ready in active session
                        WHEN checked_in = true THEN 3                                -- Checked in
                        ELSE 4                                                          -- Others
                    END as priority
                    
                FROM best_sessions
                ORDER BY priority ASC, check_in_time DESC, nr_startowy ASC
            """)
            
            return queue
            
        except Exception as e:
            print(f"❌ Błąd get_unified_queue: {e}")
            return []
    
    def get_groups_with_status(self):
        """Pobiera grupy startowe z unified statusami"""
        try:
            # Pobierz zameldowanych zawodników pogrupowanych
            zawodnicy = get_all("""
                SELECT nr_startowy, imie, nazwisko, kategoria, plec, klub, 
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
            
            # Przekształć na format odpowiedzi z statusami SECTRO
            grupy_list = []
            for i, (key, grupa) in enumerate(sorted(grupy.items()), 1):
                plec_nazwa = 'Mężczyźni' if grupa['plec'] == 'M' else 'Kobiety'
                nazwa_grupy = f"Grupa {i}: {grupa['kategoria']} {plec_nazwa}"
                
                # Sprawdź status SECTRO dla grupy
                sectro_info = self._get_sectro_info_for_group(grupa['kategoria'], grupa['plec'])
                
                grupy_list.append({
                    'numer_grupy': i,
                    'key': key,
                    'nazwa': nazwa_grupy,
                    'kategoria': grupa['kategoria'],
                    'plec': grupa['plec'],
                    'zawodnicy': grupa['zawodnicy'],
                    'liczba_zawodnikow': len(grupa['zawodnicy']),
                    'status': sectro_info['status'],
                    'sectro_session_id': sectro_info['session_id'],
                    'session_name': sectro_info['session_name'],
                    'estimated_time': len(grupa['zawodnicy']) * 20,  # 20s na zawodnika
                    'unified_ready': sectro_info['status'] in ['ACTIVE', 'TIMING']
                })
            
            return grupy_list
            
        except Exception as e:
            print(f"❌ Błąd get_groups_with_status: {e}")
            return []
    
    def get_dashboard_data(self):
        """Single endpoint dla wszystkich danych dashboard"""
        try:
            groups = self.get_groups_with_status()
            queue = self.get_unified_queue()
            active_session = self._get_current_active_session()
            active_sessions = self._get_all_active_sessions()  # NEW: wszystkie aktywne sesje
            stats = self._get_unified_stats()
            
            return {
                'success': True,
                'groups': groups,
                'queue': queue,
                'activeSession': active_session,  # backward compatibility
                'activeSessions': active_sessions,  # NEW: lista wszystkich aktywnych
                'stats': stats,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'success': False, 'error': f'Błąd dashboard data: {str(e)}'}
    
    # ===== HELPER METHODS =====
    
    def _find_athlete(self, identifier):
        """Znajdź zawodnika po nr_startowy lub qr_code"""
        if isinstance(identifier, int) or (isinstance(identifier, str) and identifier.isdigit()):
            # Search by nr_startowy
            return get_one("""
                SELECT nr_startowy, imie, nazwisko, kategoria, plec, klub, qr_code,
                       COALESCE(checked_in, false) as checked_in
                FROM zawodnicy WHERE nr_startowy = %s
            """, (int(identifier),))
        else:
            # Search by qr_code
            return get_one("""
                SELECT nr_startowy, imie, nazwisko, kategoria, plec, klub, qr_code,
                       COALESCE(checked_in, false) as checked_in
                FROM zawodnicy WHERE qr_code = %s
            """, (str(identifier),))
    
    def _get_active_session_for_athlete(self, athlete):
        """Znajdź aktywną sesję SECTRO dla zawodnika"""
        return get_one("""
            SELECT id, nazwa, status FROM sectro_sessions 
            WHERE kategoria = %s AND plec = %s 
            AND status IN ('active', 'timing')
            ORDER BY created_at DESC LIMIT 1
        """, (athlete['kategoria'], athlete['plec']))
    
    def _add_athlete_to_session(self, session_id, nr_startowy):
        """Dodaj zawodnika do sesji SECTRO"""
        execute_query("""
            INSERT INTO sectro_results (session_id, nr_startowy, status, created_at)
            VALUES (%s, %s, 'waiting', CURRENT_TIMESTAMP)
            ON CONFLICT (session_id, nr_startowy) DO NOTHING
        """, (session_id, nr_startowy))
    
    def _get_sectro_info_for_group(self, kategoria, plec):
        """Pobierz informacje SECTRO dla grupy"""
        session = get_one("""
            SELECT id, nazwa, status FROM sectro_sessions 
            WHERE kategoria = %s AND plec = %s 
            AND status IN ('active', 'timing', 'completed')
            ORDER BY created_at DESC LIMIT 1
        """, (kategoria, plec))
        
        if session:
            status_map = {
                'active': 'ACTIVE',
                'timing': 'TIMING', 
                'completed': 'COMPLETED'
            }
            return {
                'session_id': session['id'],
                'session_name': session['nazwa'],
                'status': status_map.get(session['status'], 'WAITING')
            }
        else:
            return {
                'session_id': None,
                'session_name': None,
                'status': 'WAITING'
            }
    
    def _get_current_active_session(self):
        """Pobierz aktualnie aktywną sesję"""
        return get_one("""
            SELECT id, nazwa, kategoria, plec, status, config, created_at, start_time
            FROM sectro_sessions 
            WHERE status IN ('active', 'timing')
            ORDER BY created_at DESC LIMIT 1
        """)
    
    def _get_all_active_sessions(self):
        """Pobierz wszystkie aktywne sesje SECTRO"""
        return get_all("""
            SELECT id, nazwa, kategoria, plec, status, config, created_at, start_time
            FROM sectro_sessions 
            WHERE status IN ('active', 'timing')
            ORDER BY created_at DESC
        """)
    
    def _get_unified_stats(self):
        """Pobierz unified statystyki"""
        try:
            basic_stats = get_one("""
                SELECT 
                    COUNT(*) as total_zawodnicy,
                    COUNT(CASE WHEN COALESCE(checked_in, false) = true THEN 1 END) as zameldowani,
                    COUNT(CASE WHEN COALESCE(checked_in, false) = false THEN 1 END) as niezameldowani,
                    COUNT(DISTINCT kategoria) as liczba_kategorii
                FROM zawodnicy
            """)
            
            sectro_stats = get_one("""
                SELECT 
                    COUNT(*) as total_sessions,
                    COUNT(CASE WHEN status = 'active' THEN 1 END) as active_sessions,
                    COUNT(CASE WHEN status = 'timing' THEN 1 END) as timing_sessions,
                    COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_sessions
                FROM sectro_sessions
            """)
            
            queue_stats = get_one("""
                SELECT COUNT(*) as queue_length FROM zawodnicy WHERE checked_in = true
            """)
            
            return {
                'zawodnicy': dict(basic_stats) if basic_stats else {},
                'sectro': dict(sectro_stats) if sectro_stats else {},
                'queue': dict(queue_stats) if queue_stats else {},
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Błąd _get_unified_stats: {e}")
            return {}
    
    def get_group_details(self, kategoria, plec):
        """Pobierz szczegóły grupy z listą wszystkich zawodników"""
        try:
            # Pobierz wszystkich zawodników w kategorii/płci
            all_athletes = get_all("""
                SELECT nr_startowy, imie, nazwisko, kategoria, plec, klub, 
                       COALESCE(checked_in, false) as checked_in, check_in_time
                FROM zawodnicy 
                WHERE kategoria = %s AND plec = %s
                ORDER BY nr_startowy
            """, (kategoria, plec))
            
            # Sprawdź status SECTRO dla grupy
            sectro_info = self._get_sectro_info_for_group(kategoria, plec)
            
            # Pobierz szczegóły sesji SECTRO jeśli istnieje
            session_details = None
            if sectro_info['session_id']:
                session_details = get_one("""
                    SELECT id, nazwa, status, config, created_at, start_time, end_time
                    FROM sectro_sessions WHERE id = %s
                """, (sectro_info['session_id'],))
                
                # Pobierz wyniki SECTRO dla zawodników
                sectro_results = get_all("""
                    SELECT nr_startowy, status, start_time, finish_time, total_time
                    FROM sectro_results WHERE session_id = %s
                """, (sectro_info['session_id'],))
                
                # Dodaj wyniki SECTRO do zawodników
                sectro_dict = {r['nr_startowy']: r for r in sectro_results}
                for athlete in all_athletes:
                    athlete['sectro_result'] = sectro_dict.get(athlete['nr_startowy'])
            
            # Podziel na zameldowanych i niezameldowanych
            checked_in_athletes = [a for a in all_athletes if a['checked_in']]
            not_checked_in_athletes = [a for a in all_athletes if not a['checked_in']]
            
            plec_nazwa = 'Mężczyźni' if plec == 'M' else 'Kobiety'
            
            return {
                'success': True,
                'data': {
                    'kategoria': kategoria,
                    'plec': plec,
                    'nazwa_grupy': f'{kategoria} {plec_nazwa}',
                    'status': sectro_info['status'],
                    'session': session_details,
                    'group': {
                        'kategoria': kategoria,
                        'plec': plec,
                        'athletes_count': len(checked_in_athletes),
                        'total_athletes': len(all_athletes),
                        'is_active': sectro_info['status'] in ['ACTIVE', 'TIMING']
                    },
                    'athletes': checked_in_athletes,  # Frontend oczekuje bezpośrednio zameldowanych
                    'all_athletes': all_athletes,     # Wszystkich na wszelki wypadek
                    'counts': {
                        'total': len(all_athletes),
                        'checked_in': len(checked_in_athletes),
                        'not_checked_in': len(not_checked_in_athletes)
                    },
                    'estimated_time': len(checked_in_athletes) * 20,  # 20s per athlete
                    'unified_ready': sectro_info['status'] in ['ACTIVE', 'TIMING']
                },
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'success': False, 'error': f'Błąd pobierania szczegółów grupy: {str(e)}'}
    
    def remove_athlete_from_group(self, nr_startowy, kategoria=None, plec=None):
        """Usuń zawodnika z grupy (check-out)"""
        try:
            # Check-out zawodnika
            result = self.register_athlete_unified(nr_startowy, 'checkout')
            
            if result['success']:
                return {
                    'success': True,
                    'action': 'removed',
                    'athlete': result['athlete'],
                    'message': f'Zawodnik #{nr_startowy} usunięty z grupy'
                }
            else:
                return result
                
        except Exception as e:
            return {'success': False, 'error': f'Błąd usuwania zawodnika: {str(e)}'}
    
    def delete_group(self, kategoria, plec, force=False):
        """Usuń całą grupę (check-out wszystkich zawodników)"""
        try:
            # Sprawdź czy grupa ma aktywną sesję
            sectro_info = self._get_sectro_info_for_group(kategoria, plec)
            
            if sectro_info['status'] == 'ACTIVE' and not force:
                return {
                    'success': False, 
                    'error': 'Grupa ma aktywną sesję SECTRO. Użyj force=true aby wymusić usunięcie.'
                }
            
            # Pobierz wszystkich zameldowanych zawodników
            athletes = get_all("""
                SELECT nr_startowy FROM zawodnicy 
                WHERE kategoria = %s AND plec = %s AND COALESCE(checked_in, false) = true
            """, (kategoria, plec))
            
            if not athletes:
                return {'success': False, 'error': 'Brak zameldowanych zawodników w grupie'}
            
            # Check-out wszystkich zawodników
            removed_count = 0
            for athlete in athletes:
                result = self.register_athlete_unified(athlete['nr_startowy'], 'checkout')
                if result['success']:
                    removed_count += 1
            
            # Jeśli force i jest aktywna sesja - dezaktywuj ją
            if force and sectro_info['status'] == 'ACTIVE':
                self.deactivate_group_unified(kategoria, plec)
            
            return {
                'success': True,
                'action': 'deleted',
                'removed_athletes': removed_count,
                'total_athletes': len(athletes),
                'force_used': force,
                'message': f'Grupa {kategoria} {plec} usunięta ({removed_count} zawodników)'
            }
            
        except Exception as e:
            return {'success': False, 'error': f'Błąd usuwania grupy: {str(e)}'}

print("🔄 SKATECROSS QR - Unified Start Manager załadowany") 