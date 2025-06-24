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
        NAPRAWIONE v36.1: Sprawdza duplikaty i blokuje wiele aktywnych sesji
        
        Args:
            kategoria: kategoria zawodników
            plec: płeć zawodników  
            nazwa: opcjonalna nazwa sesji
        """
        try:
            # 🔥 PUNKT 2.1.1: Sprawdź czy istnieją inne aktywne sesje
            other_active_sessions = get_all("""
                SELECT id, nazwa, kategoria, plec, status 
                FROM sectro_sessions 
                WHERE status IN ('active', 'timing')
                AND NOT (kategoria = %s AND plec = %s)
            """, (kategoria, plec))
            
            if other_active_sessions:
                session_list = [f"#{s['id']} {s['kategoria']}-{s['plec']} ({s['nazwa']})" for s in other_active_sessions]
                return {
                    'success': False, 
                    'error': f'Tylko jedna grupa może być aktywna jednocześnie. Aktywne sesje: {", ".join(session_list)}',
                    'active_sessions': other_active_sessions,
                    'action': 'blocked_by_other_active'
                }
            
            # Sprawdź zameldowanych zawodników w grupie
            athletes = get_all("""
                SELECT nr_startowy, imie, nazwisko, kategoria, plec, klub
                FROM zawodnicy 
                WHERE kategoria = %s AND plec = %s AND COALESCE(checked_in, false) = true
                ORDER BY nr_startowy
            """, (kategoria, plec))
            
            if not athletes:
                return {'success': False, 'error': 'Brak zameldowanych zawodników w grupie'}
            
            # 🔥 PUNKT 2.1.2: Sprawdź czy już istnieje aktywna sesja dla tej grupy (powinno być tylko 1)
            existing_sessions = get_all("""
                SELECT id, nazwa, status, created_at FROM sectro_sessions 
                WHERE kategoria = %s AND plec = %s 
                AND status IN ('active', 'timing')
                ORDER BY created_at DESC
            """, (kategoria, plec))
            
            if existing_sessions:
                if len(existing_sessions) > 1:
                    # DUPLIKATY! Anuluj starsze
                    latest_session = existing_sessions[0]
                    older_sessions = existing_sessions[1:]
                    
                    for old_session in older_sessions:
                        execute_query("""
                            UPDATE sectro_sessions 
                            SET status = 'cancelled', end_time = CURRENT_TIMESTAMP
                            WHERE id = %s
                        """, (old_session['id'],))
                        
                        execute_query("""
                            INSERT INTO sectro_logs (session_id, log_type, message, created_at)
                            VALUES (%s, 'WARNING', %s, CURRENT_TIMESTAMP)
                        """, (old_session['id'], f'AUTO-CANCELLED duplicate session for {kategoria}-{plec}'))
                    
                    # Zwróć najnowszą sesję
                    return {
                        'success': True,
                        'action': 'cleaned_duplicates',
                        'session': latest_session,
                        'athletes_count': len(athletes),
                        'cancelled_duplicates': len(older_sessions),
                        'message': f'Grupa już aktywna w sesji #{latest_session["id"]}. Wyczyszczono {len(older_sessions)} duplikatów.'
                    }
                else:
                    # Tylko 1 sesja - OK
                    session = existing_sessions[0]
                    return {
                        'success': True,
                        'action': 'already_active',
                        'session': session,
                        'athletes_count': len(athletes),
                        'message': f'Grupa już ma aktywną sesję SECTRO #{session["id"]}'
                    }
            
            # 🔥 PUNKT 2.1.3: Utwórz nową sesję SECTRO automatycznie
            if not nazwa:
                plec_nazwa = 'Mężczyźni' if plec == 'M' else 'Kobiety'
                nazwa = f'Auto: {kategoria} {plec_nazwa}'
            
            session_id = execute_query("""
                INSERT INTO sectro_sessions (nazwa, kategoria, plec, status, config, created_at)
                VALUES (%s, %s, %s, 'active', %s, CURRENT_TIMESTAMP)
                RETURNING id
            """, (
                nazwa,
                kategoria, 
                plec,
                json.dumps({
                    'wejscie_start': 1,
                    'wejscie_finish': 4,
                    'auto_created': True,
                    'created_from_group': f'{kategoria}_{plec}',
                    'athletes_count': len(athletes),
                    'created_by': 'unified_start_manager_v36.1'
                })
            ))
            
            # Dodaj wszystkich zawodników do sesji
            for athlete in athletes:
                execute_query("""
                    INSERT INTO sectro_results (session_id, nr_startowy, status, created_at)
                    VALUES (%s, %s, 'in_progress', CURRENT_TIMESTAMP)
                    ON CONFLICT (session_id, nr_startowy) DO NOTHING
                """, (session_id, athlete['nr_startowy']))
            
            # Zaloguj utworzenie sesji
            execute_query("""
                INSERT INTO sectro_logs (session_id, log_type, message, created_at)
                VALUES (%s, 'INFO', %s, CURRENT_TIMESTAMP)
            """, (session_id, f'v36.1 Auto-created unified session for {nazwa} with {len(athletes)} athletes'))
            
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
        """
        Deaktywuje grupę i kończy sesję SECTRO
        NAPRAWIONE v36.1: Cleanup duplikatów i proper resource cleanup
        """
        try:
            # 🔥 PUNKT 2.1.5: Znajdź WSZYSTKIE aktywne sesje dla grupy
            sessions = get_all("""
                SELECT id, nazwa, status FROM sectro_sessions 
                WHERE kategoria = %s AND plec = %s 
                AND status IN ('active', 'timing')
                ORDER BY created_at DESC
            """, (kategoria, plec))
            
            if not sessions:
                return {'success': False, 'error': 'Brak aktywnej sesji do deaktywacji'}
            
            deactivated_count = 0
            session_names = []
            
            # Zakończ WSZYSTKIE aktywne sesje dla grupy
            for session in sessions:
                # Zakończ sesję
                execute_query("""
                    UPDATE sectro_sessions 
                    SET status = 'completed', end_time = CURRENT_TIMESTAMP
                    WHERE id = %s
                """, (session['id'],))
                
                # 🔥 PUNKT 2.1.6: Cleanup powiązanych danych
                # Ustaw wyniki jako completed jeśli mają start_time ale nie finish_time
                execute_query("""
                    UPDATE sectro_results 
                    SET status = 'completed', finish_time = CURRENT_TIMESTAMP
                    WHERE session_id = %s 
                    AND start_time IS NOT NULL 
                    AND finish_time IS NULL
                """, (session['id'],))
                
                # Zaloguj
                execute_query("""
                    INSERT INTO sectro_logs (session_id, log_type, message, created_at)
                    VALUES (%s, 'INFO', %s, CURRENT_TIMESTAMP)
                """, (session['id'], f'v36.1 Session manually deactivated via unified system (#{session["id"]} of {len(sessions)} sessions)'))
                
                deactivated_count += 1
                session_names.append(f'#{session["id"]} {session["nazwa"]}')
            
            # Wyczyść cache
            self.active_session_cache = None
            
            message = f'Grupa deaktywowana: {deactivated_count} sesji zakończonych'
            if deactivated_count > 1:
                message += f' (CLEANUP DUPLIKATÓW!)'
            
            return {
                'success': True,
                'action': 'deactivated',
                'sessions_deactivated': deactivated_count,
                'session_names': session_names,
                'cleanup_duplicates': deactivated_count > 1,
                'message': message
            }
            
        except Exception as e:
            return {'success': False, 'error': f'Błąd deaktywacji: {str(e)}'}
    
    def get_unified_queue(self):
        """
        Pobiera unified kolejkę startową z priorytetami SECTRO
        """
        try:
            # Główne zapytanie unified queue
            queue = get_all("""
                SELECT 
                    z.nr_startowy,
                    z.imie,
                    z.nazwisko, 
                    z.kategoria,
                    z.plec,
                    z.klub,
                    z.checked_in,
                    z.check_in_time,
                    
                    -- SECTRO data
                    s.id as session_id,
                    s.nazwa as session_name,
                    s.status as session_status,
                    r.status as sectro_status,
                    r.start_time,
                    r.finish_time,
                    r.total_time,
                    
                    -- Unified status calculation
                    CASE 
                        WHEN r.total_time IS NOT NULL THEN 'FINISHED'
                        WHEN r.start_time IS NOT NULL THEN 'TIMING' 
                        WHEN r.session_id IS NOT NULL THEN 'READY'
                        WHEN z.checked_in = true THEN 'REGISTERED'
                        ELSE 'WAITING'
                    END as unified_status,
                    
                    -- Source type
                    CASE
                        WHEN s.status IN ('active', 'timing') THEN 'SECTRO_ACTIVE'
                        WHEN z.checked_in = true THEN 'CHECKED_IN'
                        ELSE 'MANUAL'
                    END as source_type,
                    
                    -- Priority for sorting
                    CASE 
                        WHEN r.start_time IS NOT NULL AND r.finish_time IS NULL THEN 1  -- Currently timing
                        WHEN s.status = 'active' AND r.session_id IS NOT NULL THEN 2   -- Ready in active session
                        WHEN z.checked_in = true THEN 3                                -- Checked in
                        ELSE 4                                                          -- Others
                    END as priority
                    
                FROM zawodnicy z
                LEFT JOIN sectro_results r ON z.nr_startowy = r.nr_startowy
                LEFT JOIN sectro_sessions s ON r.session_id = s.id
                WHERE z.checked_in = true OR r.session_id IS NOT NULL
                ORDER BY priority ASC, s.created_at DESC, r.start_time DESC, z.check_in_time DESC, z.nr_startowy ASC
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
            stats = self._get_unified_stats()
            
            return {
                'success': True,
                'groups': groups,
                'queue': queue,
                'activeSession': active_session,
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
            VALUES (%s, %s, 'in_progress', CURRENT_TIMESTAMP)
            ON CONFLICT (session_id, nr_startowy) DO NOTHING
        """, (session_id, nr_startowy))
    
    def _get_sectro_info_for_group(self, kategoria, plec):
        """
        Pobierz informacje SECTRO dla grupy
        NAPRAWIONE v36.1: Sprawdza duplikaty i auto-cleanup
        """
        sessions = get_all("""
            SELECT id, nazwa, status, created_at FROM sectro_sessions 
            WHERE kategoria = %s AND plec = %s 
            AND status IN ('active', 'timing')
            ORDER BY created_at DESC
        """, (kategoria, plec))
        
        if not sessions:
            return {
                'session_id': None,
                'session_name': None,
                'status': 'WAITING'
            }
        
        # 🔥 PUNKT 2.1.4: Auto-cleanup duplikatów w locie
        if len(sessions) > 1:
            latest_session = sessions[0]
            older_sessions = sessions[1:]
            
            # Anuluj starsze duplikaty
            for old_session in older_sessions:
                try:
                    execute_query("""
                        UPDATE sectro_sessions 
                        SET status = 'cancelled', end_time = CURRENT_TIMESTAMP
                        WHERE id = %s
                    """, (old_session['id'],))
                    
                    execute_query("""
                        INSERT INTO sectro_logs (session_id, log_type, message, created_at)
                        VALUES (%s, 'WARNING', %s, CURRENT_TIMESTAMP)
                    """, (old_session['id'], f'AUTO-CLEANUP duplicate session for {kategoria}-{plec} via _get_sectro_info_for_group'))
                except Exception as e:
                    print(f"⚠️ Błąd auto-cleanup sesji #{old_session['id']}: {e}")
            
            print(f"🧹 Auto-cleaned {len(older_sessions)} duplicate sessions for {kategoria}-{plec}")
            session = latest_session
        else:
            session = sessions[0]
        
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
    
    def _get_current_active_session(self):
        """Pobierz aktualnie aktywną sesję"""
        return get_one("""
            SELECT id, nazwa, kategoria, plec, status, config, created_at, start_time
            FROM sectro_sessions 
            WHERE status IN ('active', 'timing')
            ORDER BY created_at DESC LIMIT 1
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
        """
        Pobiera szczegóły grupy z listą zawodników
        
        Args:
            kategoria: kategoria zawodników
            plec: płeć zawodników
        """
        try:
            # Pobierz zameldowanych zawodników w grupie
            athletes = get_all("""
                SELECT nr_startowy, imie, nazwisko, kategoria, plec, klub,
                       COALESCE(checked_in, false) as checked_in, check_in_time
                FROM zawodnicy 
                WHERE kategoria = %s AND plec = %s AND COALESCE(checked_in, false) = true
                ORDER BY nr_startowy
            """, (kategoria, plec))
            
            # Sprawdź sesję SECTRO
            session = get_one("""
                SELECT id, nazwa, status, created_at, end_time
                FROM sectro_sessions 
                WHERE kategoria = %s AND plec = %s 
                ORDER BY created_at DESC LIMIT 1
            """, (kategoria, plec))
            
            # Sprawdź wyniki SECTRO dla zawodników w grupie
            if session:
                results = get_all("""
                    SELECT r.nr_startowy, r.status, r.start_time, r.finish_time, r.total_time
                    FROM sectro_results r
                    WHERE r.session_id = %s
                    ORDER BY r.nr_startowy
                """, (session['id'],))
            else:
                results = []
            
            return {
                'success': True,
                'data': {
                    'group': {
                        'kategoria': kategoria,
                        'plec': plec,
                        'athletes_count': len(athletes),
                        'is_active': session and session['status'] in ['active', 'timing'] if session else False
                    },
                    'athletes': athletes,
                    'session': session,
                    'results': results
                }
            }
            
        except Exception as e:
            return {'success': False, 'error': f'Błąd pobierania szczegółów grupy: {str(e)}'}

    def remove_athlete_from_group(self, nr_startowy, kategoria=None, plec=None):
        """
        Usuwa zawodnika z grupy (check-out)
        
        Args:
            nr_startowy: numer startowy zawodnika
            kategoria: opcjonalna kategoria (do walidacji)
            plec: opcjonalna płeć (do walidacji)
        """
        try:
            # Znajdź zawodnika
            athlete = get_one("""
                SELECT nr_startowy, imie, nazwisko, kategoria, plec, 
                       COALESCE(checked_in, false) as checked_in
                FROM zawodnicy 
                WHERE nr_startowy = %s
            """, (nr_startowy,))
            
            if not athlete:
                return {'success': False, 'error': 'Zawodnik nie znaleziony'}
            
            if not athlete['checked_in']:
                return {'success': False, 'error': 'Zawodnik nie jest zameldowany'}
            
            # Walidacja kategorii/płci jeśli podane
            if kategoria and athlete['kategoria'] != kategoria:
                return {'success': False, 'error': 'Nieprawidłowa kategoria zawodnika'}
            
            if plec and athlete['plec'] != plec:
                return {'success': False, 'error': 'Nieprawidłowa płeć zawodnika'}
            
            # Sprawdź czy zawodnik jest w aktywnej sesji SECTRO
            active_result = get_one("""
                SELECT r.id, s.nazwa as session_name, r.status, r.start_time, r.finish_time
                FROM sectro_results r
                JOIN sectro_sessions s ON r.session_id = s.id
                WHERE r.nr_startowy = %s AND s.status IN ('active', 'timing')
                AND r.start_time IS NOT NULL AND r.finish_time IS NULL
            """, (nr_startowy,))
            
            if active_result:
                return {
                    'success': False, 
                    'error': f'Zawodnik jest obecnie w trakcie pomiaru w sesji "{active_result["session_name"]}". Nie można usunąć z grupy.'
                }
            
            # Usuń z meldowania
            execute_query("""
                UPDATE zawodnicy 
                SET checked_in = false, check_in_time = NULL
                WHERE nr_startowy = %s
            """, (nr_startowy,))
            
            # Usuń z sesji SECTRO jeśli nie ma pomiarów
            execute_query("""
                DELETE FROM sectro_results 
                WHERE nr_startowy = %s 
                AND start_time IS NULL AND finish_time IS NULL
            """, (nr_startowy,))
            
            return {
                'success': True,
                'athlete': athlete,
                'message': f'Zawodnik #{nr_startowy} {athlete["imie"]} {athlete["nazwisko"]} usunięty z grupy'
            }
            
        except Exception as e:
            return {'success': False, 'error': f'Błąd usuwania zawodnika z grupy: {str(e)}'}

    def delete_group(self, kategoria, plec, force=False):
        """
        Usuwa całą grupę (check-out wszystkich zawodników)
        
        Args:
            kategoria: kategoria grupy
            plec: płeć grupy
            force: czy wymusić usunięcie aktywnej grupy
        """
        try:
            # Znajdź zawodników w grupie
            athletes = get_all("""
                SELECT nr_startowy, imie, nazwisko, COALESCE(checked_in, false) as checked_in
                FROM zawodnicy 
                WHERE kategoria = %s AND plec = %s AND COALESCE(checked_in, false) = true
                ORDER BY nr_startowy
            """, (kategoria, plec))
            
            if not athletes:
                return {'success': False, 'error': 'Brak zameldowanych zawodników w grupie'}
            
            # Sprawdź aktywną sesję
            active_session = get_one("""
                SELECT id, nazwa, status FROM sectro_sessions 
                WHERE kategoria = %s AND plec = %s 
                AND status IN ('active', 'timing')
                ORDER BY created_at DESC LIMIT 1
            """, (kategoria, plec))
            
            if active_session and not force:
                return {
                    'success': False, 
                    'error': f'Grupa ma aktywną sesję SECTRO "{active_session["nazwa"]}". Użyj force=true aby wymusić usunięcie.'
                }
            
            # Sprawdź czy ktoś jest w trakcie pomiaru
            athletes_timing = get_all("""
                SELECT r.nr_startowy, z.imie, z.nazwisko, s.nazwa as session_name
                FROM sectro_results r
                JOIN sectro_sessions s ON r.session_id = s.id
                JOIN zawodnicy z ON r.nr_startowy = z.nr_startowy
                WHERE z.kategoria = %s AND z.plec = %s
                AND s.status IN ('active', 'timing')
                AND r.start_time IS NOT NULL AND r.finish_time IS NULL
            """, (kategoria, plec))
            
            if athletes_timing and not force:
                names = [f"#{a['nr_startowy']} {a['imie']} {a['nazwisko']}" for a in athletes_timing]
                return {
                    'success': False,
                    'error': f'Zawodnicy w trakcie pomiaru: {", ".join(names)}. Użyj force=true aby wymusić usunięcie.'
                }
            
            removed_count = 0
            errors = []
            
            # Usuń każdego zawodnika z grupy
            for athlete in athletes:
                result = self.remove_athlete_from_group(athlete['nr_startowy'], kategoria, plec)
                if result['success']:
                    removed_count += 1
                else:
                    errors.append(f"#{athlete['nr_startowy']}: {result['error']}")
            
            # Jeśli force i aktywna sesja, zakończ ją
            if force and active_session:
                execute_query("""
                    UPDATE sectro_sessions 
                    SET status = 'cancelled', end_time = CURRENT_TIMESTAMP
                    WHERE id = %s
                """, (active_session['id'],))
                
                execute_query("""
                    INSERT INTO sectro_logs (session_id, log_type, message, created_at)
                    VALUES (%s, 'WARNING', %s, CURRENT_TIMESTAMP)
                """, (active_session['id'], 'Session force-cancelled due to group deletion'))
            
            return {
                'success': True,
                'removed_athletes': removed_count,
                'total_athletes': len(athletes),
                'errors': errors,
                'session_cancelled': bool(force and active_session),
                'message': f'Grupa {kategoria} {plec} usunięta: {removed_count}/{len(athletes)} zawodników'
            }
            
        except Exception as e:
            return {'success': False, 'error': f'Błąd usuwania grupy: {str(e)}'}

print("🔄 SKATECROSS QR - Unified Start Manager załadowany") 