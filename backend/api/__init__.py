# -*- coding: utf-8 -*-
"""
SKATECROSS QR - API Module Initialization
Wersja: 2.0.0
Główny moduł inicjalizacji wszystkich endpointów API
"""

from flask import Flask
from flask_cors import CORS

# Importy wszystkich blueprintów
from .zawodnicy import zawodnicy_bp
from .qr_generation import qr_generation_bp
from .centrum_startu import centrum_startu_bp
from .centrum_startu_v2 import centrum_startu_v2_bp
from .unified_start_api import unified_bp
from .rankingi import rankingi_bp
from .drabinka import drabinka_bp
from .statystyki import statystyki_bp
from .wyniki import wyniki_bp
# from .import_export_api import import_export_bp  # Tymczasowo wyłączone - brak pandas

def init_app(app: Flask) -> None:
    """
    Inicjalizuje wszystkie blueprinty API w aplikacji Flask
    
    Args:
        app: Instancja aplikacji Flask
    """
    
    # ✅ POPRAWIONA KONFIGURACJA CORS - WSPARCIE DLA PORTÓW 5173 I 5175
    CORS(app, 
         origins=["http://localhost:5173", "http://localhost:5175", "http://127.0.0.1:5173", "http://127.0.0.1:5175"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization", "X-User-ID"])
    
    print("🔗 Rejestruję blueprinty SKATECROSS...")
    
    # Rejestracja blueprintów
    app.register_blueprint(zawodnicy_bp)
    app.register_blueprint(qr_generation_bp)
    app.register_blueprint(centrum_startu_bp)
    app.register_blueprint(centrum_startu_v2_bp)
    app.register_blueprint(unified_bp)
    app.register_blueprint(rankingi_bp)
    app.register_blueprint(drabinka_bp)
    app.register_blueprint(statystyki_bp)
    app.register_blueprint(wyniki_bp)
    # app.register_blueprint(import_export_bp)  # Tymczasowo wyłączone
    
    print("✅ Blueprinty SKATECROSS zarejestrowane:")
    print("   👤 zawodnicy_bp - /api/zawodnicy/*")
    print("   🔲 qr_generation_bp - /api/qr/*")
    print("   🚫 centrum_startu_bp - LEGACY ENDPOINTS DISABLED (używaj /api/unified/*)")
    print("   🏁 centrum_startu_v2_bp - /api/v2/* (NOWA WERSJA Z SECTRO)")
    print("   🚀 unified_bp - /api/unified/* (UNIFIED START CONTROL)")
    print("   📊 rankingi_bp - /api/rankings/*")
    print("   🏆 drabinka_bp - /api/drabinka")
    print("   📈 statystyki_bp - /api/kluby, /api/statystyki, /api/kategorie")
    print("   🏅 wyniki_bp - /api/wyniki")
    print("   ℹ️ version endpoint - /api/version")

print("📦 SKATECROSS QR - API Module Init loaded") 