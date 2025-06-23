#!/bin/bash

# 🚀 SKATECROSS QR - Szybkie uruchomienie (rozwiązuje problemy z portami)

echo "🚀 SKATECROSS QR - Szybkie uruchomienie"

# Zatrzymaj procesy
pkill -f "python.*api_server" 2>/dev/null || true
pkill -f "node.*vite" 2>/dev/null || true
sleep 1

# Znajdź wolne porty
BACKEND_PORT=5001
while lsof -i :$BACKEND_PORT >/dev/null 2>&1; do ((BACKEND_PORT++)); done

FRONTEND_PORT=5173  
while lsof -i :$FRONTEND_PORT >/dev/null 2>&1; do ((FRONTEND_PORT++)); done

echo "✅ Backend: localhost:$BACKEND_PORT"
echo "✅ Frontend: localhost:$FRONTEND_PORT"

# Uruchom backend
cd backend
echo "PORT=$BACKEND_PORT" > .env
echo "DATABASE_URL=postgresql://postgres.dfjhfaqvbynrhgdbvjfh:Minimum1!@aws-0-eu-north-1.pooler.supabase.com:6543/postgres" >> .env
source venv/bin/activate
unset PORT
python api_server.py > backend.log 2>&1 &

# Uruchom frontend z proxy
cd ../frontend
sed -i.bak "s/localhost:[0-9]\+/localhost:$BACKEND_PORT/g" vite.config.ts
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
npm run dev -- --port $FRONTEND_PORT > frontend.log 2>&1 &

sleep 3
echo "🌐 Aplikacja: http://localhost:$FRONTEND_PORT"
open "http://localhost:$FRONTEND_PORT"
echo "📊 Backend API działa - dane z bazy dostępne!"
echo "🛑 Zatrzymaj: killall Python && killall node"
