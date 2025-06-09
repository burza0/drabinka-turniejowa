from flask import Flask
from .zawodnicy import zawodnicy_bp
from .wyniki import wyniki_bp
from .statystyki import statystyki_bp
from .rankingi import rankingi_bp
from .drabinka import drabinka_bp
from .centrum_startu import centrum_startu_bp

def init_app(app: Flask):
    """Inicjalizuje wszystkie blueprinty API"""
    app.register_blueprint(zawodnicy_bp)
    app.register_blueprint(wyniki_bp)
    app.register_blueprint(statystyki_bp)
    app.register_blueprint(rankingi_bp)
    app.register_blueprint(drabinka_bp)
    app.register_blueprint(centrum_startu_bp) 