#!/usr/bin/env python3
"""
SKATECROSS QR Backend Server
Uruchamianie: python start_server.py
"""

import os
import sys
from dotenv import load_dotenv

# Załaduj zmienne środowiskowe
load_dotenv()

# Sprawdź czy baza danych jest skonfigurowana
if not os.getenv('DATABASE_URL'):
    print("❌ BŁĄD: Nie znaleziono DATABASE_URL w pliku .env")
    print("📋 Utwórz plik .env na podstawie env_example")
    print("📖 Zobacz SETUP.md dla instrukcji")
    sys.exit(1)

try:
    # Importuj aplikację Flask
    from api_server import app
    
    print("🚀 Uruchamianie SKATECROSS QR Backend...")
    print(f"🌐 Dostępny na: http://localhost:5001")
    print(f"📊 API endpoints: http://localhost:5001/api/version")
    print("🔗 Frontend proxy: Vite automatycznie przekieruje /api/* na ten serwer")
    print("⏹️  Zatrzymanie: Ctrl+C")
    print("-" * 60)
    
    # Uruchom serwer
    app.run(
        host='0.0.0.0',  # Dostępny z innych urządzeń w sieci
        port=5001,
        debug=True,
        threaded=True
    )
    
except ImportError as e:
    print(f"❌ BŁĄD IMPORTU: {e}")
    print("📦 Sprawdź czy zainstalowane są dependencies: pip install -r requirements.txt")
    sys.exit(1)
    
except Exception as e:
    print(f"❌ BŁĄD SERWERA: {e}")
    print("🔧 Sprawdź konfigurację bazy danych i pliku .env")
    sys.exit(1) 