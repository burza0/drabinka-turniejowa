# -*- coding: utf-8 -*-
"""
SKATECROSS QR - Simple Backend v1.0.0
Wersja: 1.0.0 
Prosty serwer dla drabinki turniejowej SKATECROSS
"""

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "<h1>🏁 SKATECROSS QR Dashboard</h1><p>Backend działa na porcie 5001</p>"

@app.route('/api/version')
def get_version():
    return jsonify({
        "success": True,
        "data": {
            "name": "SKATECROSS QR Backend",
            "version": "1.0.0",
            "description": "QR System for skatecross tournaments"
        }
    })

@app.route('/api/status')
def get_status():
    return jsonify({
        "success": True,
        "status": "healthy",
        "message": "SKATECROSS Backend działa poprawnie"
    })

if __name__ == '__main__':
    print("🏁 SKATECROSS QR - Simple Backend v1.0.0")
    print("🚀 Uruchamianie serwera...")
    print("🌐 Dostępny na http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=True) 