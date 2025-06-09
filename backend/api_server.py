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
SYSTEM_VERSION = "32.0"
SYSTEM_NAME = "SKATECROSS Drabinka Turniejowa"
SYSTEM_FEATURES = ["SECTRO Live Timing", "QR System", "Start Queue", "Rankings", "Toggle Buttons", "Queue Management"]

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

@app.route("/api/version")
def get_version():
    """Endpoint zwracający wersję systemu"""
    try:
        return jsonify({
            "version": SYSTEM_VERSION,
            "name": SYSTEM_NAME,
            "features": SYSTEM_FEATURES,
            "status": "production",
            "sectro": "integrated",
            "environment": "production" if os.getenv("PRODUCTION") else "development"
        })
    except Exception as e:
        print(f"Błąd przy endpoincie wersji: {e}")
        return jsonify({"version": "unknown", "error": str(e)}), 500

# ... reszta endpointów, które jeszcze nie zostały przeniesione ...

if __name__ == "__main__":
    app.run(debug=True) 