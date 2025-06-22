"""
SKATECROSS QR System - API Module
Inicjalizacja i rejestracja wszystkich blueprintów
"""

from flask import Flask
from .zawodnicy import zawodnicy_bp
from .qr_generation import qr_generation_bp
from .centrum_startu import centrum_startu_bp

def init_app(app: Flask):
    """Inicjalizuje wszystkie blueprinty API"""
    app.register_blueprint(zawodnicy_bp)
    app.register_blueprint(qr_generation_bp)
    app.register_blueprint(centrum_startu_bp) 