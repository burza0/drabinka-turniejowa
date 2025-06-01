#!/usr/bin/env python3
"""
Sprawdzenie gotowości WERSJI 30.2 do deployment-ciu na produkcję
"""

import os
import sys
import json

def check_version():
    """Sprawdź czy VERSION to 30.2"""
    try:
        with open('VERSION', 'r') as f:
            version = f.read().strip()
        if version == '30.2':
            print(f"✅ VERSION: {version}")
            return True
        else:
            print(f"❌ VERSION: {version} (oczekiwane: 30.2)")
            return False
    except FileNotFoundError:
        print("❌ Brak pliku VERSION")
        return False

def check_requirements():
    """Sprawdź czy requirements.txt nie zawiera problemowych zależności"""
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read()
        
        # Problemowe zależności z wersji 31
        problematic = ['Flask-Caching', 'psycopg2-pool', 'uuid']
        issues = []
        
        for package in problematic:
            if package in requirements:
                issues.append(package)
        
        if not issues:
            print("✅ requirements.txt: Czyste (bez problematycznych zależności)")
            return True
        else:
            print(f"❌ requirements.txt: Zawiera problemowe zależności: {', '.join(issues)}")
            return False
    except FileNotFoundError:
        print("❌ Brak pliku requirements.txt")
        return False

def check_api_server():
    """Sprawdź czy api_server.py zawiera komentarze wersji 30.1/30.2"""
    try:
        with open('backend/api_server.py', 'r') as f:
            content = f.read()
        
        checks = [
            ("WERSJA 30.1: Wyłączony cache", "Cache wyłączony"),
            ("WERSJA 30.2: Uproszczone połączenia", "Connection pooling wyłączony"),
            ("get_simple_connection", "Funkcja prostych połączeń"),
            ("# from cache import app_cache", "Import cache zakomentowany")
        ]
        
        all_good = True
        for check, description in checks:
            if check in content:
                print(f"✅ api_server.py: {description}")
            else:
                print(f"❌ api_server.py: Brak - {description}")
                all_good = False
        
        return all_good
    except FileNotFoundError:
        print("❌ Brak pliku backend/api_server.py")
        return False

def check_gunicorn_config():
    """Sprawdź czy istnieje konfiguracja gunicorn"""
    if os.path.exists('backend/gunicorn_config.py'):
        print("✅ gunicorn_config.py: Istnieje")
        return True
    else:
        print("❌ gunicorn_config.py: Brak")
        return False

def check_procfile():
    """Sprawdź czy Procfile używa gunicorn"""
    try:
        with open('Procfile', 'r') as f:
            content = f.read()
        
        if 'gunicorn -c gunicorn_config.py' in content:
            print("✅ Procfile: Używa gunicorn z custom config")
            return True
        else:
            print("❌ Procfile: Nie używa gunicorn lub brak custom config")
            return False
    except FileNotFoundError:
        print("❌ Brak pliku Procfile")
        return False

def check_frontend_build():
    """Sprawdź czy frontend został zbudowany"""
    if os.path.exists('frontend/dist/index.html'):
        print("✅ Frontend: Zbudowany (dist/index.html istnieje)")
        return True
    else:
        print("❌ Frontend: Nie zbudowany (brak dist/index.html)")
        return False

def check_deployment_docs():
    """Sprawdź czy istnieje dokumentacja deployment"""
    if os.path.exists('DEPLOYMENT_V30.2.md'):
        print("✅ Dokumentacja: DEPLOYMENT_V30.2.md istnieje")
        return True
    else:
        print("❌ Dokumentacja: Brak DEPLOYMENT_V30.2.md")
        return False

def main():
    """Główna funkcja sprawdzająca"""
    print("🔍 SPRAWDZENIE GOTOWOŚCI WERSJI 30.2 DO PRODUKCJI")
    print("=" * 55)
    
    checks = [
        check_version,
        check_requirements,
        check_api_server,
        check_gunicorn_config,
        check_procfile,
        check_frontend_build,
        check_deployment_docs
    ]
    
    results = []
    for check in checks:
        result = check()
        results.append(result)
        print()
    
    passed = sum(results)
    total = len(results)
    
    print("=" * 55)
    print(f"📊 WYNIK: {passed}/{total} sprawdzeń przeszło pomyślnie")
    
    if passed == total:
        print("🎉 WERSJA 30.2 GOTOWA DO DEPLOYMENT-U! 🚀")
        print()
        print("Następne kroki:")
        print("1. 🌐 Deploy backend na Railway")
        print("2. 🎨 Deploy frontend na Vercel") 
        print("3. 🗄️ Inicjalizacja bazy danych")
        print("4. 🧪 Testowanie produkcji")
        print()
        print("📚 Szczegóły w: DEPLOYMENT_V30.2.md")
        return 0
    else:
        print("❌ WYMAGANE POPRAWKI PRZED DEPLOYMENT-EM")
        print("📚 Sprawdź: DEPLOYMENT_V30.2.md")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 