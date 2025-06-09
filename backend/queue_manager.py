"""
🚀 Queue Manager - Unified Queue Architecture
Purpose: Replace checkpoint-based system with dedicated queue management
Author: AI Assistant
Date: 2025-06-07
"""

import os
import psycopg2
import psycopg2.extras
from datetime import datetime
import json
from typing import List, Dict, Optional, Tuple
from dotenv import load_dotenv

load_dotenv()

class QueueManager:
    """🎯 Unified queue management system"""
    
    def __init__(self):
        self.db_url = os.getenv('DATABASE_URL')
        
    def get_connection(self):
        """Get database connection"""
        return psycopg2.connect(self.db_url, cursor_factory=psycopg2.extras.RealDictCursor)
    
    # 📊 QUEUE RETRIEVAL
    def get_current_queue(self) -> List[Dict]:
        """Get current queue (visible athletes only)"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT * FROM v_current_queue 
                ORDER BY queue_position, added_at
            """)
            return [dict(row) for row in cur.fetchall()]
    
    def get_queue_stats(self) -> Dict:
        """Get queue statistics"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            
            # Count by status
            cur.execute("""
                SELECT status, COUNT(*) as count 
                FROM start_queue 
                GROUP BY status
            """)
            status_counts = {row['status']: row['count'] for row in cur.fetchall()}
            
            # Count by source
            cur.execute("""
                SELECT source_type, COUNT(*) as count 
                FROM start_queue 
                WHERE status IN ('waiting', 'called')
                GROUP BY source_type
            """)
            source_counts = {row['source_type']: row['count'] for row in cur.fetchall()}
            
            return {
                'total_in_queue': status_counts.get('waiting', 0) + status_counts.get('called', 0),
                'waiting': status_counts.get('waiting', 0),
                'called': status_counts.get('called', 0),
                'hidden': status_counts.get('hidden', 0),
                'removed': status_counts.get('removed', 0),
                'scanned': source_counts.get('scanned', 0),
                'active_group': source_counts.get('active_group', 0)
            }
    
    # ➕ ADDING TO QUEUE
    def add_scanned_athlete(self, nr_startowy: int, device_id: str = None, qr_code: str = None) -> Dict:
        """Add athlete to queue via QR scan"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            
            # Get athlete info
            cur.execute("SELECT * FROM zawodnicy WHERE nr_startowy = %s", (nr_startowy,))
            athlete = cur.fetchone()
            if not athlete:
                return {'success': False, 'error': 'Zawodnik nie istnieje'}
            
            # Check if already in queue
            cur.execute("SELECT status FROM start_queue WHERE nr_startowy = %s", (nr_startowy,))
            existing = cur.fetchone()
            if existing:
                if existing['status'] in ['waiting', 'called']:
                    return {'success': False, 'error': 'Zawodnik już jest w kolejce'}
                elif existing['status'] == 'hidden':
                    # Unhide athlete
                    return self.unhide_athlete(nr_startowy)
            
            # Get next position
            cur.execute("SELECT COALESCE(MAX(queue_position), 0) + 1 as next_position FROM start_queue WHERE status = 'waiting'")
            next_position_result = cur.fetchone()
            next_position = next_position_result['next_position'] if next_position_result else 1
            
            # Add to queue
            try:
                cur.execute("""
                    INSERT INTO start_queue (
                        nr_startowy, source_type, source_metadata, 
                        added_at, scanned_at, status, group_info, queue_position
                    ) VALUES (
                        %s, 'scanned', %s, NOW(), NOW(), 'waiting', %s, %s
                    )
                """, (
                    nr_startowy,
                    json.dumps({
                        'device_id': device_id,
                        'qr_code': qr_code,
                        'scan_timestamp': datetime.now().isoformat()
                    }),
                    json.dumps({
                        'kategoria': athlete['kategoria'],
                        'plec': athlete['plec'],
                        'klub': athlete['klub']
                    }),
                    next_position
                ))
                conn.commit()
                
                return {
                    'success': True,
                    'message': f'Dodano zawodnika #{nr_startowy} do kolejki',
                    'type': 'scanned',
                    'position': next_position
                }
                
            except Exception as e:
                conn.rollback()
                return {'success': False, 'error': str(e)}
    
    def sync_active_group(self, group_data: Dict) -> Dict:
        """Sync athletes from active group"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            
            try:
                # Get checked-in athletes from active group
                cur.execute("""
                    SELECT nr_startowy, imie, nazwisko, kategoria, plec, klub
                    FROM zawodnicy 
                    WHERE kategoria = %s AND plec = %s AND checked_in = TRUE
                """, (group_data['kategoria'], group_data['plec']))
                
                group_athletes = cur.fetchall()
                added_count = 0
                skipped_count = 0
                
                for athlete in group_athletes:
                    # Check if already in queue (any status)
                    cur.execute("SELECT status FROM start_queue WHERE nr_startowy = %s", (athlete['nr_startowy'],))
                    existing = cur.fetchone()
                    
                    if existing:
                        skipped_count += 1
                        continue
                    
                    # Get next position
                    cur.execute("SELECT COALESCE(MAX(queue_position), 0) + 1 as next_position FROM start_queue WHERE status = 'waiting'")
                    next_position_result = cur.fetchone()
                    next_position = next_position_result['next_position'] if next_position_result else 1
                    
                    # Add to queue
                    cur.execute("""
                        INSERT INTO start_queue (
                            nr_startowy, source_type, source_metadata,
                            added_at, status, group_info, queue_position
                        ) VALUES (
                            %s, 'active_group', %s, NOW(), 'waiting', %s, %s
                        )
                    """, (
                        athlete['nr_startowy'],
                        json.dumps({
                            'grupa_numer': group_data.get('numer_grupy'),
                            'grupa_nazwa': group_data.get('nazwa'),
                            'auto_sync': True,
                            'sync_timestamp': datetime.now().isoformat()
                        }),
                        json.dumps({
                            'kategoria': athlete['kategoria'],
                            'plec': athlete['plec'],
                            'klub': athlete['klub']
                        }),
                        next_position
                    ))
                    added_count += 1
                
                conn.commit()
                
                return {
                    'success': True,
                    'message': f'Zsynchronizowano grupę: {added_count} dodanych, {skipped_count} pominiętych',
                    'added_count': added_count,
                    'skipped_count': skipped_count,
                    'total_athletes': len(group_athletes)
                }
                
            except Exception as e:
                conn.rollback()
                return {'success': False, 'error': str(e)}
    
    # ❌ REMOVING FROM QUEUE
    def remove_athlete(self, nr_startowy: int, permanent: bool = False) -> Dict:
        """Remove athlete from queue (hide or permanent)"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            
            # Check if athlete is in queue
            cur.execute("SELECT * FROM start_queue WHERE nr_startowy = %s", (nr_startowy,))
            athlete_queue = cur.fetchone()
            if not athlete_queue:
                return {'success': False, 'error': 'Zawodnik nie jest w kolejce'}
            
            try:
                if permanent:
                    # Permanent removal
                    cur.execute("DELETE FROM start_queue WHERE nr_startowy = %s", (nr_startowy,))
                    # Reorder positions
                    self._reorder_queue_positions(cur)
                    action = 'usunięto'
                    type_action = 'removed'
                else:
                    # Hide athlete
                    cur.execute("""
                        UPDATE start_queue 
                        SET status = 'hidden', queue_position = 0 
                        WHERE nr_startowy = %s
                    """, (nr_startowy,))
                    # Reorder positions for remaining athletes
                    self._reorder_queue_positions(cur)
                    action = 'ukryto'
                    type_action = 'hidden'
                
                conn.commit()
                
                return {
                    'success': True,
                    'message': f'Zawodnik #{nr_startowy} został {action} z kolejki',
                    'type': type_action,
                    'permanent': permanent
                }
                
            except Exception as e:
                conn.rollback()
                return {'success': False, 'error': str(e)}
    
    def unhide_athlete(self, nr_startowy: int) -> Dict:
        """Unhide previously hidden athlete"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            
            # Check if athlete is hidden
            cur.execute("SELECT status FROM start_queue WHERE nr_startowy = %s", (nr_startowy,))
            result = cur.fetchone()
            if not result or result['status'] != 'hidden':
                return {'success': False, 'error': 'Zawodnik nie jest ukryty lub nie istnieje w kolejce'}
            
            try:
                # Get next position
                cur.execute("SELECT COALESCE(MAX(queue_position), 0) + 1 as next_position FROM start_queue WHERE status = 'waiting'")
                next_position_result = cur.fetchone()
                next_position = next_position_result['next_position'] if next_position_result else 1
                
                # Unhide
                cur.execute("""
                    UPDATE start_queue 
                    SET status = 'waiting', queue_position = %s 
                    WHERE nr_startowy = %s
                """, (next_position, nr_startowy))
                
                conn.commit()
                
                return {
                    'success': True,
                    'message': f'Przywrócono zawodnika #{nr_startowy} do kolejki',
                    'type': 'unhidden',
                    'position': next_position
                }
                
            except Exception as e:
                conn.rollback()
                return {'success': False, 'error': str(e)}
    
    # 🔧 UTILITY METHODS
    def _reorder_queue_positions(self, cursor):
        """Reorder queue positions for waiting athletes"""
        cursor.execute("""
            WITH ordered_queue AS (
                SELECT nr_startowy, ROW_NUMBER() OVER (ORDER BY added_at) as new_position
                FROM start_queue 
                WHERE status = 'waiting'
            )
            UPDATE start_queue 
            SET queue_position = oq.new_position
            FROM ordered_queue oq
            WHERE start_queue.nr_startowy = oq.nr_startowy
        """)
    
    def clear_queue(self) -> Dict:
        """Clear entire queue (emergency function)"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            
            try:
                cur.execute("DELETE FROM start_queue")
                count = cur.rowcount
                conn.commit()
                
                return {
                    'success': True,
                    'message': f'Wyczyszczono kolejkę ({count} zawodników)',
                    'removed_count': count
                }
                
            except Exception as e:
                conn.rollback()
                return {'success': False, 'error': str(e)}
    
    def get_athlete_queue_info(self, nr_startowy: int) -> Optional[Dict]:
        """Get specific athlete queue information"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM start_queue WHERE nr_startowy = %s", (nr_startowy,))
            result = cur.fetchone()
            return dict(result) if result else None 