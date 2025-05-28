#!/usr/bin/env python3
import sys
import os

# Dodaj backend do path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Import aplikacji
from api_server import app

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    host = os.getenv("HOST", "0.0.0.0")
    app.run(host=host, port=port, debug=False) 