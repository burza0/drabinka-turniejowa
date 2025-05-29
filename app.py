#!/usr/bin/env python3
import os
import sys
from flask import Flask, send_from_directory, send_file
from flask_cors import CORS

# Dodaj backend do path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Import aplikacji backendu
from api_server import app as api_app

# Utwórz główną aplikację
app = Flask(__name__, static_folder='frontend/dist')
CORS(app)

# Zarejestruj wszystkie endpointy API z backend aplikacji
for rule in api_app.url_map.iter_rules():
    endpoint = api_app.view_functions[rule.endpoint]
    app.add_url_rule(rule.rule, rule.endpoint, endpoint, methods=rule.methods)

# Serwuj frontend (statyczne pliki Vue)
@app.route('/')
def serve_frontend():
    """Serwuj główną stronę frontendu"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    """Serwuj statyczne pliki frontendu (CSS, JS, itp.)"""
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        # Dla Vue Router - zwróć index.html dla wszystkich ścieżek
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    # Konfiguracja dla Heroku
    port = int(os.getenv("PORT", 5000))
    host = os.getenv("HOST", "0.0.0.0")
    debug = os.getenv("FLASK_ENV", "production") == "development"
    
    app.run(host=host, port=port, debug=debug) 