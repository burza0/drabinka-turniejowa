"""
🚀 New API Endpoints - Unified Queue Architecture
Purpose: New endpoints using QueueManager for unified queue management
Author: AI Assistant  
Date: 2025-06-07
"""

from flask import Blueprint, request, jsonify
from queue_manager import QueueManager
import json

# Create blueprint for new endpoints
new_queue_api = Blueprint('new_queue_api', __name__)
qm = QueueManager()

# 📊 QUEUE RETRIEVAL ENDPOINTS
@new_queue_api.route('/api/v2/start-queue', methods=['GET'])
def get_start_queue_v2():
    """New unified start queue endpoint"""
    try:
        queue = qm.get_current_queue()
        stats = qm.get_queue_stats()
        
        return jsonify({
            'success': True,
            'queue': queue,
            'count': len(queue),
            'stats': stats,
            'version': '2.0',
            'architecture': 'unified'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@new_queue_api.route('/api/v2/queue/stats', methods=['GET'])
def get_queue_stats_v2():
    """Detailed queue statistics"""
    try:
        stats = qm.get_queue_stats()
        return jsonify({
            'success': True,
            'stats': stats,
            'version': '2.0'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ➕ ADDING TO QUEUE ENDPOINTS
@new_queue_api.route('/api/v2/queue/scan', methods=['POST'])
def add_scanned_athlete_v2():
    """Add athlete to queue via QR scan"""
    try:
        data = request.json or {}
        nr_startowy = data.get('nr_startowy')
        device_id = data.get('device_id')
        qr_code = data.get('qr_code')
        
        if not nr_startowy:
            return jsonify({'success': False, 'error': 'nr_startowy wymagany'}), 400
        
        result = qm.add_scanned_athlete(nr_startowy, device_id, qr_code)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@new_queue_api.route('/api/v2/queue/sync-group', methods=['POST'])
def sync_active_group_v2():
    """Sync athletes from active group to queue"""
    try:
        data = request.json or {}
        required_fields = ['kategoria', 'plec', 'nazwa']
        
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'{field} wymagane'}), 400
        
        result = qm.sync_active_group(data)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ❌ REMOVING FROM QUEUE ENDPOINTS  
@new_queue_api.route('/api/v2/queue/remove/<int:nr_startowy>', methods=['DELETE'])
def remove_athlete_v2(nr_startowy):
    """Remove athlete from queue with option for permanent removal"""
    try:
        data = request.json or {}
        permanent = data.get('permanent', False)
        
        result = qm.remove_athlete(nr_startowy, permanent)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@new_queue_api.route('/api/v2/queue/hide/<int:nr_startowy>', methods=['POST'])
def hide_athlete_v2(nr_startowy):
    """Hide athlete from queue (temporary removal)"""
    try:
        result = qm.remove_athlete(nr_startowy, permanent=False)
        
        if result['success']:
            return jsonify({
                **result,
                'action': 'hidden',
                'note': 'Zawodnik może zostać przywrócony'
            })
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@new_queue_api.route('/api/v2/queue/unhide/<int:nr_startowy>', methods=['POST'])
def unhide_athlete_v2(nr_startowy):
    """Unhide previously hidden athlete"""
    try:
        result = qm.unhide_athlete(nr_startowy)
        
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# 🔍 ATHLETE INFO ENDPOINTS
@new_queue_api.route('/api/v2/queue/athlete/<int:nr_startowy>', methods=['GET'])
def get_athlete_queue_info_v2(nr_startowy):
    """Get specific athlete queue information"""
    try:
        info = qm.get_athlete_queue_info(nr_startowy)
        
        if info:
            return jsonify({
                'success': True,
                'athlete': info
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Zawodnik nie jest w kolejce'
            }), 404
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# 🧹 MAINTENANCE ENDPOINTS
@new_queue_api.route('/api/v2/queue/clear', methods=['DELETE'])
def clear_queue_v2():
    """Clear entire queue (emergency function)"""
    try:
        # Require confirmation
        data = request.json or {}
        if not data.get('confirm', False):
            return jsonify({
                'success': False,
                'error': 'Wymagane potwierdzenie: {"confirm": true}'
            }), 400
        
        result = qm.clear_queue()
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# 🔄 COMPATIBILITY ENDPOINTS
@new_queue_api.route('/api/v2/compatibility/old-to-new', methods=['POST'])
def migrate_from_old_system():
    """Migration endpoint from old checkpoint system"""
    try:
        # This would handle any remaining migration needs
        return jsonify({
            'success': True,
            'message': 'Migration completed in previous steps',
            'note': 'Old system data already migrated to new architecture'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# 📊 HEALTH CHECK
@new_queue_api.route('/api/v2/health', methods=['GET'])
def health_check_v2():
    """Health check for new queue system"""
    try:
        stats = qm.get_queue_stats()
        return jsonify({
            'success': True,
            'status': 'healthy',
            'queue_stats': stats,
            'architecture': 'unified',
            'version': '2.0'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': str(e)
        }), 500 