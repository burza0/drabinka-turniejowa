#!/bin/bash

# ============================================================================
# SKATECROSS v37.0 - PROSTY I CZYSTY SKRYPT STARTOWY
# ============================================================================
# Zastępuje wszystkie 8 poprzednich skryptów jednym prostym rozwiązaniem
# ============================================================================

set -e

# Kolory
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

BACKEND_PORT=5001
FRONTEND_PORT=5175
PROJECT_DIR="/Users/mariusz/drabinka-turniejowa"

echo -e "${BLUE}🚀 SKATECROSS v37.0 - CLEAN START${NC}"
echo -e "${BLUE}===============================================${NC}"

# Sprawdź czy jesteśmy w odpowiednim katalogu
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}❌ Katalog projektu nie istnieje: $PROJECT_DIR${NC}"
    exit 1
fi

cd "$PROJECT_DIR"

# Krok 1: Zabij stare procesy
echo -e "${YELLOW}🔪 Czyszczę stare procesy...${NC}"
pkill -f "python3.*api_server" 2>/dev/null || true
pkill -f "vite.*5175" 2>/dev/null || true
pkill -f "vite.*5173" 2>/dev/null || true

# Zabij procesy na portach
for port in 5001 5173 5175; do
    lsof -ti:$port 2>/dev/null | xargs kill -9 2>/dev/null || true
done

sleep 2
echo -e "${GREEN}✅ Procesy wyczyszczone${NC}"

# Krok 2: Start Backend
echo -e "${YELLOW}🚀 Uruchamiam Backend (port $BACKEND_PORT)...${NC}"
cd backend

if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Brak venv! Uruchom: python3 -m venv venv${NC}"
    exit 1
fi

if [ ! -f "api_server.py" ]; then
    echo -e "${RED}❌ Brak api_server.py!${NC}"
    exit 1
fi

# Uruchom backend w production mode (BEZ DEBUG!)
source venv/bin/activate
FLASK_ENV=production FLASK_DEBUG=0 nohup python3 api_server.py > ../backend.log 2>&1 &
BACKEND_PID=$!

# Czekaj na backend
echo -e "${YELLOW}⏳ Czekam na backend...${NC}"
for i in {1..15}; do
    if curl -s "http://localhost:$BACKEND_PORT/api/version" >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Backend działa na porcie $BACKEND_PORT${NC}"
        break
    fi
    if [ $i -eq 15 ]; then
        echo -e "${RED}❌ Backend nie odpowiada!${NC}"
        kill $BACKEND_PID 2>/dev/null || true
        exit 1
    fi
    sleep 2
done

# Krok 3: Start Frontend
echo -e "${YELLOW}🚀 Uruchamiam Frontend (port $FRONTEND_PORT)...${NC}"
cd ../frontend

if [ ! -f "package.json" ]; then
    echo -e "${RED}❌ Brak package.json!${NC}"
    exit 1
fi

if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}📦 Instaluję zależności...${NC}"
    npm install
fi

# Uruchom frontend na porcie 5175 z no-cache config
nohup npx vite --config vite.config.nocache.ts --host --port $FRONTEND_PORT > ../frontend.log 2>&1 &
FRONTEND_PID=$!

# Czekaj na frontend
echo -e "${YELLOW}⏳ Czekam na frontend...${NC}"
for i in {1..15}; do
    if lsof -ti:$FRONTEND_PORT >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Frontend działa na porcie $FRONTEND_PORT${NC}"
        break
    fi
    if [ $i -eq 15 ]; then
        echo -e "${RED}❌ Frontend nie uruchomił się!${NC}"
        kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
        exit 1
    fi
    sleep 2
done

# Status końcowy
echo -e "\n${GREEN}🎉 SKATECROSS v37.0 URUCHOMIONY!${NC}"
echo -e "${GREEN}===============================================${NC}"
echo -e "✅ Backend:  http://localhost:$BACKEND_PORT"
echo -e "✅ Frontend: http://localhost:$FRONTEND_PORT"
echo -e "✅ Sieć:    http://192.168.0.178:$FRONTEND_PORT"
echo -e "\n${YELLOW}🛑 Aby zatrzymać: kill $BACKEND_PID $FRONTEND_PID${NC}"

# Otwórz w przeglądarce
if command -v open >/dev/null 2>&1; then
    open "http://localhost:$FRONTEND_PORT" 2>/dev/null || true
fi

echo -e "\n${BLUE}✨ System gotowy!${NC}" 