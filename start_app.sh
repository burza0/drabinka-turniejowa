#!/bin/bash

# �� SKATECROSS QR - Automatyczne uruchomienie aplikacji

# Kolory
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🚀 SKATECROSS QR - Automatyczne uruchomienie${NC}"

# Wyczyść zmienne środowiskowe
unset PORT

# Funkcja do znajdowania wolnego portu
find_free_port() {
    local start_port=$1
    local port=$start_port
    while lsof -i :$port >/dev/null 2>&1; do
        ((port++))
    done
    echo $port
}

# Zatrzymaj istniejące procesy
echo -e "${YELLOW}🛑 Zatrzymuję istniejące procesy...${NC}"
pkill -f "python.*api_server" 2>/dev/null || true
pkill -f "node.*vite" 2>/dev/null || true
sleep 2

# Znajdź wolne porty
echo -e "${YELLOW}🔍 Szukam wolnych portów...${NC}"
BACKEND_PORT=$(find_free_port 5003)
FRONTEND_PORT=$(find_free_port 5177)

echo -e "${GREEN}✅ Backend port: $BACKEND_PORT${NC}"
echo -e "${GREEN}✅ Frontend port: $FRONTEND_PORT${NC}"

# Konfiguruj backend
echo -e "${YELLOW}⚙️ Konfiguruję backend...${NC}"
cd backend
cat > .env << ENVEOF
DATABASE_URL=postgresql://postgres.dfjhfaqvbynrhgdbvjfh:Minimum1!@aws-0-eu-north-1.pooler.supabase.com:6543/postgres
PORT=${BACKEND_PORT}
HOST=0.0.0.0
FLASK_ENV=development
FLASK_DEBUG=True
ENVEOF

# Uruchom backend
echo -e "${YELLOW}📊 Uruchamiam backend na porcie ${BACKEND_PORT}...${NC}"
source venv/bin/activate 2>/dev/null
python api_server.py > backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > .backend_pid

sleep 3

# Konfiguruj frontend
echo -e "${YELLOW}⚙️ Konfiguruję frontend...${NC}"
cd ../frontend
sed -i.bak "s/localhost:[0-9]\+/localhost:${BACKEND_PORT}/g" vite.config.ts

# Uruchom frontend
echo -e "${YELLOW}🎨 Uruchamiam frontend na porcie ${FRONTEND_PORT}...${NC}"
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
npm run dev -- --port ${FRONTEND_PORT} > frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > .frontend_pid

sleep 3

# Sprawdź serwery
if lsof -i :${BACKEND_PORT} >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend: http://localhost:${BACKEND_PORT}${NC}"
else
    echo -e "${RED}❌ Backend się nie uruchomił${NC}"
fi

if lsof -i :${FRONTEND_PORT} >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Frontend: http://localhost:${FRONTEND_PORT}${NC}"
    echo -e "${BLUE}🌐 Otwieram w przeglądarce...${NC}"
    open "http://localhost:${FRONTEND_PORT}"
else
    echo -e "${RED}❌ Frontend się nie uruchomił${NC}"
fi

echo ""
echo -e "${GREEN}🎉 Gotowe! Użyj './stop_app.sh' aby zatrzymać${NC}"
