#!/bin/bash

# SKATECROSS - Skrypt zatrzymywania serwerów
# Wersja: 31.0

# Kolory dla output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${PURPLE}🛑 SKATECROSS - Zatrzymywanie serwerów v31${NC}"
echo "=================================================="

# Funkcja zatrzymywania procesu
kill_process() {
    local pid=$1
    local name=$2
    
    if [ ! -z "$pid" ] && kill -0 $pid 2>/dev/null; then
        echo -e "${YELLOW}🔄 Zatrzymuję $name (PID: $pid)${NC}"
        kill -TERM $pid 2>/dev/null || true
        sleep 2
        
        # Jeśli proces nadal działa, wymuś zatrzymanie
        if kill -0 $pid 2>/dev/null; then
            echo -e "${YELLOW}⚠️  Wymuszam zatrzymanie $name${NC}"
            kill -9 $pid 2>/dev/null || true
        fi
        
        # Sprawdź czy proces został zatrzymany
        if ! kill -0 $pid 2>/dev/null; then
            echo -e "${GREEN}✅ $name zatrzymany${NC}"
            return 0
        else
            echo -e "${RED}❌ Nie udało się zatrzymać $name${NC}"
            return 1
        fi
    else
        echo -e "${YELLOW}⚠️  $name nie jest uruchomiony${NC}"
        return 0
    fi
}

# Zatrzymaj procesy na podstawie zapisanych PID
if [ -f ".backend_pid" ]; then
    BACKEND_PID=$(cat .backend_pid)
    kill_process $BACKEND_PID "Backend API"
    rm -f .backend_pid
fi

if [ -f ".frontend_pid" ]; then
    FRONTEND_PID=$(cat .frontend_pid)
    kill_process $FRONTEND_PID "Frontend Vite"
    rm -f .frontend_pid
fi

# Dodatkowo sprawdź i zatrzymaj procesy na portach
echo -e "${BLUE}🔍 Sprawdzam procesy na portach...${NC}"

# Port 5000 (Backend)
BACKEND_PORT_PID=$(lsof -ti:5000 2>/dev/null || true)
if [ ! -z "$BACKEND_PORT_PID" ]; then
    echo -e "${YELLOW}🔄 Zatrzymuję proces na porcie 5000 (PID: $BACKEND_PORT_PID)${NC}"
    kill -9 $BACKEND_PORT_PID 2>/dev/null || true
fi

# Port 5173 (Frontend)
FRONTEND_PORT_PID=$(lsof -ti:5173 2>/dev/null || true)
if [ ! -z "$FRONTEND_PORT_PID" ]; then
    echo -e "${YELLOW}🔄 Zatrzymuję proces na porcie 5173 (PID: $FRONTEND_PORT_PID)${NC}"
    kill -9 $FRONTEND_PORT_PID 2>/dev/null || true
fi

# Zatrzymaj wszystkie procesy związane z projektem
echo -e "${BLUE}🧹 Czyszczenie pozostałych procesów...${NC}"

# Python api_server
pkill -f "python.*api_server.py" 2>/dev/null || true

# NPM dev processes
pkill -f "npm.*dev" 2>/dev/null || true

# Vite processes
pkill -f "vite" 2>/dev/null || true

# Sprawdź czy porty są wolne
sleep 2

if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${RED}❌ Port 5000 nadal zajęty${NC}"
else
    echo -e "${GREEN}✅ Port 5000 wolny${NC}"
fi

if lsof -Pi :5173 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${RED}❌ Port 5173 nadal zajęty${NC}"
else
    echo -e "${GREEN}✅ Port 5173 wolny${NC}"
fi

# Wyczyść pliki logów (opcjonalnie)
if [ "$1" = "--clean-logs" ]; then
    echo -e "${BLUE}🧹 Czyszczenie logów...${NC}"
    rm -f backend.log frontend.log
    echo -e "${GREEN}✅ Logi wyczyszczone${NC}"
fi

echo ""
echo -e "${GREEN}🎉 SERWERY ZATRZYMANE!${NC}"
echo "=================================================="
echo -e "${YELLOW}📋 Przydatne komendy:${NC}"
echo -e "   🚀 Uruchom ponownie: ${BLUE}./start_servers.sh${NC}"
echo -e "   🔍 Sprawdź procesy:   ${BLUE}ps aux | grep -E '(api_server|npm.*dev|vite)'${NC}"
echo -e "   🧹 Wyczyść logi:      ${BLUE}./stop_servers.sh --clean-logs${NC}"
echo "" 