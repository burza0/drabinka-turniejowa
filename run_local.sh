#!/bin/bash
# Skrypt do uruchamiania lokalnie

echo "🚀 Uruchamianie Drabinka Turniejowa..."

# Sprawdź czy istnieje plik .env w backendzie
if [ ! -f "backend/.env" ]; then
    echo "❌ Brak pliku backend/.env - utwórz go z DATABASE_URL"
    echo "Przykład: DATABASE_URL=postgresql://user:password@localhost/dbname"
    exit 1
fi

# Uruchom backend
echo "📊 Uruchamianie backend (Flask)..."
cd backend
python3 -m venv venv 2>/dev/null || true
source venv/bin/activate
pip install -r ../requirements.txt -q
python api_server.py &
BACKEND_PID=$!
cd ..

# Czekaj chwilę na uruchomienie backendu
sleep 3

# Uruchom frontend
echo "🎨 Uruchamianie frontend (Vue + Vite)..."
cd frontend
npm install -q
npm run dev &
FRONTEND_PID=$!
cd ..

echo "✅ Aplikacja uruchomiona!"
echo "📊 Backend: http://localhost:5000"
echo "🎨 Frontend: http://localhost:5173"
echo ""
echo "Aby zatrzymać serwisy, naciśnij Ctrl+C"

# Obsługa sygnału zatrzymania
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT

# Czekaj na zakończenie
wait
