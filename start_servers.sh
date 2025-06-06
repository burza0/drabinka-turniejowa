#!/bin/bash

# SKATECROSS - Skrypt uruchamiania serwerów
# Wersja: 31.0

set -e

# Kolory dla output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Konfiguracja
BACKEND_PORT=5000
FRONTEND_PORT=5173
DATABASE_URL='postgresql://postgres.dfjhfaqvbynrhgdbvjfh:Minimum1!@aws-0-eu-north-1.pooler.supabase.com:6543/postgres'

echo -e "${PURPLE}🚀 SKATECROSS - Uruchamianie serwerów v31${NC}"
echo "=================================================="

# Funkcja sprawdzania czy port jest zajęty
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0  # Port zajęty
    else
        return 1  # Port wolny
    fi
}

# Funkcja zatrzymywania procesu na porcie
kill_process_on_port() {
    local port=$1
    local process_name=$2
    
    if check_port $port; then
        echo -e "${YELLOW}⚠️  Port $port jest zajęty przez $process_name${NC}"
        local pid=$(lsof -ti:$port)
        if [ ! -z "$pid" ]; then
            echo -e "${YELLOW}🔄 Zatrzymuję proces PID: $pid${NC}"
            kill -9 $pid 2>/dev/null || true
            sleep 2
        fi
    fi
}

# Sprawdź i zatrzymaj istniejące procesy
echo -e "${BLUE}🔍 Sprawdzam istniejące procesy...${NC}"
kill_process_on_port $BACKEND_PORT "Backend API"
kill_process_on_port $FRONTEND_PORT "Frontend Vite"

# Sprawdź czy jesteśmy w głównym katalogu projektu
if [ ! -f "backend/api_server.py" ] || [ ! -f "frontend/package.json" ]; then
    echo -e "${RED}❌ Błąd: Uruchom skrypt z głównego katalogu projektu drabinka-turniejowa${NC}"
    exit 1
fi

# Sprawdź czy istnieje venv
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Błąd: Brak virtualenv. Uruchom: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt${NC}"
    exit 1
fi

# Aktywuj venv
source venv/bin/activate

echo -e "${GREEN}✅ Virtual environment aktywowany${NC}"

# Uruchom backend w tle
echo -e "${BLUE}🔧 Uruchamianie Backend API...${NC}"
export DATABASE_URL="$DATABASE_URL"
nohup python3 backend/api_server.py > backend.log 2>&1 &
BACKEND_PID=$!

# Czekaj na uruchomienie backendu
echo -e "${YELLOW}⏳ Czekam na uruchomienie backendu...${NC}"
for i in {1..15}; do
    if curl -s http://localhost:$BACKEND_PORT/api/version >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Backend API uruchomiony (PID: $BACKEND_PID)${NC}"
        break
    fi
    if [ $i -eq 15 ]; then
        echo -e "${RED}❌ Backend nie uruchomił się w czasie 15 sekund${NC}"
        echo -e "${YELLOW}📋 Sprawdź logi: tail -f backend.log${NC}"
        exit 1
    fi
    sleep 1
done

# Uruchom frontend w tle
echo -e "${BLUE}🎨 Uruchamianie Frontend Vite...${NC}"
cd frontend
nohup npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

# Czekaj na uruchomienie frontendu
echo -e "${YELLOW}⏳ Czekam na uruchomienie frontendu...${NC}"
for i in {1..20}; do
    if curl -s http://localhost:$FRONTEND_PORT/ >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Frontend Vite uruchomiony (PID: $FRONTEND_PID)${NC}"
        break
    fi
    if [ $i -eq 20 ]; then
        echo -e "${RED}❌ Frontend nie uruchomił się w czasie 20 sekund${NC}"
        echo -e "${YELLOW}📋 Sprawdź logi: tail -f frontend.log${NC}"
        exit 1
    fi
    sleep 1
done

# Sprawdź wersję API
API_VERSION=$(curl -s http://localhost:$BACKEND_PORT/api/version | grep -o '"version":"[^"]*"' | cut -d'"' -f4 2>/dev/null || echo "unknown")

echo ""
echo -e "${GREEN}🎉 SERWERY URUCHOMIONE POMYŚLNIE!${NC}"
echo "=================================================="
echo -e "${BLUE}🔧 Backend API:${NC}"
echo -e "   📍 URL: ${GREEN}http://localhost:$BACKEND_PORT${NC}"
echo -e "   🆔 PID: ${YELLOW}$BACKEND_PID${NC}"
echo -e "   📋 Wersja: ${PURPLE}$API_VERSION${NC}"
echo -e "   🗄️  Baza: ${GREEN}Supabase${NC}"
echo ""
echo -e "${BLUE}🎨 Frontend:${NC}"
echo -e "   📍 URL: ${GREEN}http://localhost:$FRONTEND_PORT${NC}"
echo -e "   🆔 PID: ${YELLOW}$FRONTEND_PID${NC}"
echo -e "   ⚡ HMR: ${GREEN}Aktywny${NC}"
echo ""
echo -e "${PURPLE}📱 Główna aplikacja: ${GREEN}http://localhost:$FRONTEND_PORT/${NC}"
echo ""
echo -e "${YELLOW}📋 Przydatne komendy:${NC}"
echo -e "   🔍 Logi backend:  ${BLUE}tail -f backend.log${NC}"
echo -e "   🔍 Logi frontend: ${BLUE}tail -f frontend.log${NC}"
echo -e "   ⏹️  Zatrzymaj:     ${BLUE}./stop_servers.sh${NC}"
echo -e "   📊 Procesy:       ${BLUE}ps aux | grep -E '(api_server|npm.*dev)'${NC}"
echo ""
echo -e "${GREEN}✨ Gotowe do testowania!${NC}"

# Zapisz PID do plików dla łatwego zatrzymywania
echo $BACKEND_PID > .backend_pid
echo $FRONTEND_PID > .frontend_pid 