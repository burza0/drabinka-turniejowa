from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Import SECTRO module
from sectro.sectro_api import sectro_bp
# Import API modules
from api import init_app

load_dotenv()
app = Flask(__name__)

# ✅ POPRAWIONA KONFIGURACJA CORS - WSPARCIE DLA PORTÓW 5173 I 5175
CORS(app, 
     origins=["http://localhost:5173", "http://localhost:5175", "http://127.0.0.1:5173", "http://127.0.0.1:5175"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization", "X-User-ID"])

# Register SECTRO blueprint
app.register_blueprint(sectro_bp)

# Initialize API modules
init_app(app)

# System version
SYSTEM_VERSION = "37.0"
SYSTEM_NAME = "SKATECROSS Drabinka Turniejowa"
SYSTEM_FEATURES = ["Unified Start Control", "SECTRO Live Timing", "Database Cleanup", "QR System", "Start Queue", "Rankings", "Time Rankings"]

# Cache aktywnej grupy
aktywna_grupa_cache = {
    "numer_grupy": None,
    "kategoria": None,
    "plec": None,
    "nazwa": None
}

@app.route("/")
def home():
    """Serwuje frontend Vue 3"""
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'dist')
    return send_from_directory(frontend_path, 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    """Serwuje pliki statyczne frontendu"""
    frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'dist')
    return send_from_directory(frontend_path, path)

@app.route("/api/version")
def version():
    """Zwraca informacje o wersji systemu"""
    return jsonify({
        "name": SYSTEM_NAME,
        "version": SYSTEM_VERSION,
        "features": SYSTEM_FEATURES,
        "api_status": "operational",
        "environment": "production" if os.getenv("HEROKU_APP_NAME") else "development"
    })

# ... reszta endpointów, które jeszcze nie zostały przeniesione ...

if __name__ == "__main__":
    # ✅ NAPRAWIONE: POPRAWNY PORT 5001 I WYŁĄCZONY DEBUG MODE
    port = int(os.getenv("PORT", 5001))
    debug_mode = os.getenv("FLASK_DEBUG", "0") == "1"
    
    print(f"🚀 Uruchamiam SKATECROSS v{SYSTEM_VERSION} na porcie {port}")
    print(f"🔧 Debug mode: {'ON' if debug_mode else 'OFF'}")
    
    app.run(debug=debug_mode, port=port, host="0.0.0.0") 