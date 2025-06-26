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
CORS(app)

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
    port = int(os.getenv("PORT", 5003)); app.run(debug=True, port=port, host="0.0.0.0") 