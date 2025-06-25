"""
SKATECROSS QR System - Main Server (Modular Architecture v32.0)
Główny serwer z modułową strukturą blueprintów
"""

from flask import Flask, jsonify
from flask_cors import CORS
import os

# Import API modules  
from api import init_app

app = Flask(__name__)
CORS(app)

# Initialize API modules
init_app(app)

# System version
SYSTEM_VERSION = "1.0.0"
SYSTEM_NAME = "SKATECROSS QR System (Modular Demo)"
SYSTEM_FEATURES = ["QR Generation", "QR Printing", "Start Queue", "Scanner", "Modular Architecture"]

@app.route("/api/version")
def get_version():
    """Endpoint zwracający wersję systemu"""
    try:
        return jsonify({
            "version": SYSTEM_VERSION,
            "name": SYSTEM_NAME,
            "features": SYSTEM_FEATURES,
            "status": "demo",
            "environment": "standalone",
            "database": "in-memory",
            "architecture": "modular_v32.0"
        })
    except Exception as e:
        return jsonify({"version": "unknown", "error": str(e)}), 500

@app.route("/")
def home():
    """Home endpoint"""
    return jsonify({
        "message": "🚀 SKATECROSS QR System - Modular Architecture",
        "version": SYSTEM_VERSION,
        "status": "running",
        "endpoints": [
            "/api/version",
            "/api/zawodnicy", 
            "/api/qr/generate/<nr>",
            "/api/qr/generate-bulk",
            "/api/qr/stats",
            "/api/grupy-startowe",
            "/api/grupa-aktywna",
            "/api/start-queue",
            "/api/qr/scan-result"
        ]
    })

if __name__ == "__main__":
    print("🚀 Uruchamiam SKATECROSS QR Backend (Modular Architecture v32.0)")
    print("📊 Modułowa struktura: api/zawodnicy.py, api/qr_generation.py, api/centrum_startu.py")
    print("💾 Dane przechowywane w pamięci (utils/database.py)")
    print("🌐 Serwer dostępny na http://localhost:5001")
    print("🏗️ Architektura: Blueprinty + Utils")
    print("-" * 60)
    app.run(debug=True, port=5001) 