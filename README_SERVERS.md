# 🚀 SKATECROSS - Zarządzanie serwerami

Automatyczne skrypty do uruchamiania i zatrzymywania serwerów deweloperskich.

## 📋 Dostępne skrypty

### `./start_servers.sh` - Uruchomienie serwerów
Uruchamia jednocześnie backend API i frontend Vite w tle.

**Funkcje:**
- ✅ Sprawdza i zatrzymuje istniejące procesy na portach 5000 i 5173
- ✅ Weryfikuje środowisko (venv, pliki projektu)
- ✅ Uruchamia backend API z bazą danych Supabase
- ✅ Uruchamia frontend Vite z Hot Module Replacement
- ✅ Monitoruje uruchomienie i wyświetla status
- ✅ Zapisuje PID procesów do plików `.backend_pid` i `.frontend_pid`

### `./stop_servers.sh` - Zatrzymanie serwerów
Zatrzymuje wszystkie procesy związane z aplikacją.

**Funkcje:**
- ✅ Czyta PID z plików i zatrzymuje procesy
- ✅ Sprawdza procesy na portach 5000 i 5173
- ✅ Czyści wszystkie pozostałe procesy (python, npm, vite)
- ✅ Weryfikuje czy porty są wolne
- ✅ Opcjonalnie czyści logi (`--clean-logs`)

## 🎯 Szybkie użycie

```bash
# Uruchom serwery
./start_servers.sh

# Zatrzymaj serwery
./stop_servers.sh

# Zatrzymaj serwery i wyczyść logi
./stop_servers.sh --clean-logs
```

## 🌐 Adresy po uruchomieniu

- **Główna aplikacja**: http://localhost:5173/
- **Backend API**: http://localhost:5000/
- **Wersja API**: http://localhost:5000/api/version

## 📊 Monitoring

### Sprawdzenie procesów
```bash
ps aux | grep -E '(api_server|npm.*dev|vite)'
```

### Przegląd logów
```bash
# Backend
tail -f backend.log

# Frontend
tail -f frontend.log

# Oba na raz
tail -f backend.log frontend.log
```

### Sprawdzenie portów
```bash
lsof -i:5000  # Backend
lsof -i:5173  # Frontend
```

## 🔧 Wymagania

- **Python 3** z aktywnym `venv`
- **Node.js** z npm
- **curl** (do testowania)
- **lsof** (do sprawdzania portów)

## 📂 Struktura plików

```
drabinka-turniejowa/
├── start_servers.sh      # Uruchamianie serwerów
├── stop_servers.sh       # Zatrzymywanie serwerów
├── backend.log           # Logi backend (generowane)
├── frontend.log          # Logi frontend (generowane)
├── .backend_pid          # PID backend (generowane)
├── .frontend_pid         # PID frontend (generowane)
├── backend/
│   └── api_server.py
├── frontend/
│   └── package.json
└── venv/
```

## 🐛 Rozwiązywanie problemów

### Problem: Port zajęty
```bash
# Sprawdź co zajmuje port
lsof -i:5000
lsof -i:5173

# Wymuś zatrzymanie
./stop_servers.sh
```

### Problem: Backend nie startuje
```bash
# Sprawdź logi
tail -f backend.log

# Sprawdź czy venv jest aktywny
source venv/bin/activate
pip list | grep Flask
```

### Problem: Frontend nie startuje
```bash
# Sprawdź logi
tail -f frontend.log

# Sprawdź czy node_modules istnieje
cd frontend && npm install
```

### Problem: Baza danych
Backend używa **Supabase** z URL-em skonfigurowanym w skrypcie.

## 🎨 Kolory w output

Skrypty używają kolorów dla lepszej czytelności:
- 🟣 **Fioletowy**: Nagłówki
- 🔵 **Niebieski**: Informacje
- 🟡 **Żółty**: Ostrzeżenia
- 🟢 **Zielony**: Sukces
- 🔴 **Czerwony**: Błędy

## 📝 Wersja

**Wersja skryptów**: 31.0  
**Wersja API**: 30.5.0 