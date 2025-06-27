#!/bin/bash

echo "🚀 SKATECROSS v37.0 - AUTO STARTUP SCRIPT"
echo "========================================"

# Kolory dla lepszej czytelności
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funkcja do zabijania procesów na porcie
kill_port() {
    local port=$1
    local pids=$(lsof -ti:$port 2>/dev/null)
    if [ ! -z "$pids" ]; then
        echo -e "${YELLOW}🔪 Zabijam procesy na porcie $port: $pids${NC}"
        echo $pids | xargs kill -9 2>/dev/null
        sleep 2
    else
        echo -e "${GREEN}✅ Port $port jest wolny${NC}"
    fi
}

# Krok 1: Sprzątanie procesów
echo -e "\n${BLUE}📋 KROK 1: SPRZĄTANIE PROCESÓW${NC}"
kill_port 5001
kill_port 5173
kill_port 5174
kill_port 5175

# Sprawdzenie czy porty są rzeczywiście wolne
echo -e "\n${BLUE}🔍 Sprawdzam status portów...${NC}"
if lsof -ti:5001 >/dev/null 2>&1; then
    echo -e "${RED}❌ Port 5001 nadal zajęty!${NC}"
    lsof -i:5001
    exit 1
fi

if lsof -ti:5173 >/dev/null 2>&1; then
    echo -e "${RED}❌ Port 5173 nadal zajęty!${NC}"
    lsof -i:5173
    exit 1
fi

echo -e "${GREEN}✅ Wszystkie porty są wolne${NC}"

# Krok 2: Uruchomienie backendu
echo -e "\n${BLUE}📋 KROK 2: URUCHAMIAM BACKEND (port 5001)${NC}"
cd /Users/mariusz/drabinka-turniejowa/backend

# Sprawdzenie czy venv istnieje
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Brak środowiska wirtualnego venv!${NC}"
    exit 1
fi

# Uruchomienie backendu w tle
source venv/bin/activate && python3 api_server.py &
BACKEND_PID=$!

echo -e "${GREEN}✅ Backend uruchomiony (PID: $BACKEND_PID)${NC}"

# Czekamy na uruchomienie backendu
echo -e "${YELLOW}⏳ Czekam na backend...${NC}"
sleep 5

# Sprawdzenie czy backend odpowiada
for i in {1..10}; do
    if curl -s http://localhost:5001/api/version >/dev/null 2>&1; then
        VERSION=$(curl -s http://localhost:5001/api/version | grep -o '"version":"[^"]*"' | cut -d'"' -f4)
        echo -e "${GREEN}✅ Backend SKATECROSS $VERSION działa na porcie 5001${NC}"
        break
    fi
    echo -e "${YELLOW}⏳ Próba $i/10 - czekam na backend...${NC}"
    sleep 2
    if [ $i -eq 10 ]; then
        echo -e "${RED}❌ Backend nie odpowiada po 20 sekundach!${NC}"
        kill $BACKEND_PID 2>/dev/null
        exit 1
    fi
done

# Krok 3: Uruchomienie frontendu
echo -e "\n${BLUE}📋 KROK 3: URUCHAMIAM FRONTEND (port 5173)${NC}"
cd /Users/mariusz/drabinka-turniejowa/frontend

# Sprawdzenie Node.js
source ~/.nvm/nvm.sh
nvm use v24.2.0

# Uruchomienie frontendu w tle - WYMUŚ PORT 5173
npm run dev -- --port 5173 --host &
FRONTEND_PID=$!

echo -e "${GREEN}✅ Frontend uruchomiony (PID: $FRONTEND_PID)${NC}"

# Czekamy na uruchomienie frontendu
echo -e "${YELLOW}⏳ Czekam na frontend...${NC}"
sleep 8

# Sprawdzenie czy frontend odpowiada
for i in {1..10}; do
    if lsof -ti:5173 >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Frontend działa na porcie 5173${NC}"
        FRONTEND_READY=true
        break
    fi
    echo -e "${YELLOW}⏳ Próba $i/10 - czekam na frontend...${NC}"
    sleep 2
    if [ $i -eq 10 ]; then
        echo -e "${RED}❌ Frontend nie uruchomił się na porcie 5173!${NC}"
        echo "Sprawdzam które porty są zajęte przez frontend:"
        ps aux | grep vite | grep -v grep
        lsof -i | grep node
    fi
done

# Krok 4: Podsumowanie
echo -e "\n${BLUE}📋 KROK 4: STATUS SYSTEMU${NC}"
echo "========================================"

if curl -s http://localhost:5001/api/version >/dev/null 2>&1; then
    VERSION=$(curl -s http://localhost:5001/api/version | grep -o '"version":"[^"]*"' | cut -d'"' -f4)
    echo -e "${GREEN}✅ Backend: SKATECROSS $VERSION na http://localhost:5001${NC}"
else
    echo -e "${RED}❌ Backend: NIEDOSTĘPNY${NC}"
fi

if lsof -ti:5173 >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Frontend: Dostępny na https://localhost:5173${NC}"
    echo -e "${GREEN}✅ Sieć: Dostępny na https://192.168.0.178:5173${NC}"
else
    # Sprawdź inne porty
    for port in 5174 5175; do
        if lsof -ti:$port >/dev/null 2>&1; then
            echo -e "${YELLOW}⚠️  Frontend uruchomił się na porcie $port zamiast 5173${NC}"
            echo -e "${YELLOW}⚠️  URL: https://localhost:$port${NC}"
            break
        fi
    done
fi

echo -e "\n${BLUE}📝 INFORMACJE O PROCESACH:${NC}"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"

echo -e "\n${YELLOW}💡 Aby zatrzymać serwisy:${NC}"
echo "kill $BACKEND_PID $FRONTEND_PID"

echo -e "\n${GREEN}🎉 SKATECROSS v37.0 URUCHOMIONY!${NC}"
echo "========================================"

# Monitorowanie w pętli (opcjonalne)
echo -e "\n${BLUE}🔄 Monitoruję serwisy... (Ctrl+C aby zatrzymać)${NC}"
while true; do
    sleep 30
    
    # Sprawdź backend
    if ! curl -s http://localhost:5001/api/version >/dev/null 2>&1; then
        echo -e "${RED}❌ Backend przestał odpowiadać!${NC}"
        break
    fi
    
    # Sprawdź frontend
    if ! lsof -ti:5173 >/dev/null 2>&1 && ! lsof -ti:5174 >/dev/null 2>&1; then
        echo -e "${RED}❌ Frontend przestał działać!${NC}"
        break
    fi
    
    echo -e "${GREEN}✅ $(date '+%H:%M:%S') - Wszystko działa${NC}"
done 