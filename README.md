# 🏁 Drabinka Turniejowa - SECTRO Timing

System do zarządzania wynikami i drabinką turniejową.

## 🚀 Uruchamianie lokalnie

### 1. Przygotowanie bazy danych
```bash
# Stwórz bazę PostgreSQL
createdb drabinka_db

# Załaduj strukturę tabel
psql drabinka_db < backend/setup.sql
```

### 2. Konfiguracja backendu
```bash
# Skopiuj przykładową konfigurację
cp backend/env_example backend/.env

# Edytuj backend/.env i ustaw DATABASE_URL
nano backend/.env
```

### 3. Uruchomienie aplikacji
```bash
# Uruchom oba serwisy (backend + frontend)
chmod +x run_local.sh
./run_local.sh
```

### 4. Dostęp do aplikacji
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000

## 🔧 API Endpointy

- `GET /api/zawodnicy` - Lista zawodników
- `GET /api/kategorie` - Lista kategorii  
- `GET /api/wyniki` - Wyniki zawodników
- `GET /api/drabinka` - Drabinka turniejowa

## 📁 Struktura projektu

```
drabinka-turniejowa/
├── backend/           # Flask API
│   ├── api_server.py  # Główny serwer API
│   ├── setup.sql      # Struktura bazy danych
│   └── requirements.txt
├── frontend/          # Vue.js frontend  
│   ├── src/
│   │   ├── components/
│   │   └── api.js
│   └── package.json
└── run_local.sh       # Skrypt uruchamiający
```

## 🐛 Rozwiązywanie problemów

### Problemy z połączeniem frontend -> backend:
1. ✅ **Konfiguracja proxy w Vite** - dodano proxy `/api` -> `localhost:5000`
2. ✅ **CORS w Flask** - dodano `flask-cors`
3. ✅ **Błąd SQL** - usunięto nieistniejącą kolumnę `id` z zapytania

### Jeśli frontend nie wyświetla danych:
1. Sprawdź czy backend działa: `curl http://localhost:5000/api/zawodnicy`
2. Sprawdź konsole przeglądarki (F12) pod kątem błędów
3. Sprawdź czy baza danych zawiera dane testowe
