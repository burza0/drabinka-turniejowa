"""
SKATECROSS QR System - Zawodnicy Module
Blueprint dla endpointów związanych z zawodnikami
"""

from flask import Blueprint, jsonify
from utils.database import zawodnicy_data

zawodnicy_bp = Blueprint('zawodnicy', __name__)

@zawodnicy_bp.route("/api/zawodnicy")
def get_zawodnicy():
    """Endpoint zwracający listę zawodników z QR kodami"""
    try:
        return jsonify(zawodnicy_data)
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Błąd pobierania zawodników: {str(e)}"
        }), 500 