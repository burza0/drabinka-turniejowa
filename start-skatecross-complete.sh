#!/bin/bash

# ============================================================================
# SKATECROSS v37.0 - KOMPLETNY SKRYPT URUCHOMIENIOWY
# ============================================================================
# Autor: AI Assistant dla Mariusz
# Data: 27.06.2025
# Wersja: FINAL - z czyszczeniem cache przeglądarki
# 
# UWZGLĘDNIA WSZYSTKIE PROBLEMY:
# - PWA Scanner musi być na porcie 5173 (NIE 5174!)
# - Cache przeglądarki blokuje nowe komponenty
# - Service Worker cache'uje stare wersje
# - Vite czasem wybiera losowe porty
# - Backend na 5001, Frontend TYLKO na 5173
# ============================================================================

# Kolory dla lepszej czytelności
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Konfiguracja
BACKEND_PORT=5001
FRONTEND_PORT=5173
PROJECT_DIR="/Users/mariusz/drabinka-turniejowa"
BACKEND_DIR="$PROJECT_DIR/backend"
FRONTEND_DIR="$PROJECT_DIR/frontend"

# Funkcje pomocnicze
print_header() {
    echo -e "\n${CYAN}${BOLD}============================================================================${NC}"
    echo -e "${CYAN}${BOLD} SKATECROSS v37.0 - KOMPLETNY STARTUP SCRIPT${NC}"
    echo -e "${CYAN}${BOLD}============================================================================${NC}"
    echo -e "${GREEN}🏁 System turniejowy z PWA Scanner - WSZYSTKO NA PORCIE 5173!${NC}"
    echo -e "${YELLOW}📝 Uwzględnia: czyszczenie cache, problemy z portami, PWA Scanner${NC}\n"
}

kill_port() {
    local port=$1
    local pids=$(lsof -ti:$port 2>/dev/null)
    if [ ! -z "$pids" ]; then
        echo -e "${YELLOW}🔪 Zabijam procesy na porcie $port: $pids${NC}"
        echo $pids | xargs kill -9 2>/dev/null
        sleep 1
        # Sprawdź czy udało się zabić
        if lsof -ti:$port >/dev/null 2>&1; then
            echo -e "${RED}❌ Nie udało się zabić procesów na porcie $port!${NC}"
            return 1
        fi
    fi
    echo -e "${GREEN}✅ Port $port jest wolny${NC}"
    return 0
}

cleanup_processes() {
    echo -e "\n${BLUE}📋 KROK 1: SPRZĄTANIE PROCESÓW I CACHE${NC}"
    
    # Zabij wszystkie procesy Node.js/Python związane z projektem
    echo -e "${YELLOW}🔪 Zabijam wszystkie procesy związane z SKATECROSS...${NC}"
    pkill -f "vite.*5173" 2>/dev/null || true
    pkill -f "vite.*5174" 2>/dev/null || true  
    pkill -f "vite.*5175" 2>/dev/null || true
    pkill -f "npm.*dev" 2>/dev/null || true
    pkill -f "python3.*api_server" 2>/dev/null || true
    
    # Zabij procesy na konkretnych portach
    for port in 5001 5173 5174 5175 5176; do
        kill_port $port
    done
    
    # Pauza żeby procesy się zakończyły
    sleep 3
    
    # Sprawdzenie końcowe
    echo -e "\n${BLUE}🔍 Sprawdzam status portów...${NC}"
    for port in 5001 5173 5174 5175; do
        if lsof -ti:$port >/dev/null 2>&1; then
            echo -e "${RED}❌ Port $port nadal zajęty!${NC}"
            lsof -i:$port
            echo -e "${RED}🛑 BŁĄD: Nie mogę wyczyścić portu $port. Kończę.${NC}"
            exit 1
        fi
    done
    
    echo -e "${GREEN}✅ Wszystkie porty są wolne!${NC}"
}

cleanup_frontend_cache() {
    echo -e "\n${PURPLE}🧹 CZYSZCZENIE CACHE FRONTEND${NC}"
    
    if [ -d "$FRONTEND_DIR" ]; then
        cd "$FRONTEND_DIR"
        
        # Wyczyść cache Vite
        echo -e "${YELLOW}🗑️  Czyszczę cache Vite...${NC}"
        rm -rf node_modules/.vite 2>/dev/null || true
        rm -rf .vite 2>/dev/null || true
        rm -rf dist 2>/dev/null || true
        rm -rf dev-dist 2>/dev/null || true
        
        # Wyczyść cache npm
        echo -e "${YELLOW}🗑️  Czyszczę cache npm...${NC}"
        npm cache clean --force 2>/dev/null || true
        
        echo -e "${GREEN}✅ Cache frontend wyczyszczony${NC}"
    else
        echo -e "${RED}❌ Katalog frontend nie istnieje: $FRONTEND_DIR${NC}"
        exit 1
    fi
}

cleanup_browser_cache() {
    echo -e "\n${PURPLE}🌐 INSTRUKCJE CZYSZCZENIA CACHE PRZEGLĄDARKI${NC}"
    
    echo -e "${BOLD}${YELLOW}⚠️  WAŻNE: Po uruchomieniu systemu wykonaj RĘCZNIE:${NC}"
    echo -e "${CYAN}1. ${BOLD}Chrome/Edge:${NC}"
    echo -e "   • Naciśnij ${BOLD}Cmd + Shift + Delete${NC}"
    echo -e "   • Wybierz ${BOLD}\"All time\"${NC}"
    echo -e "   • Zaznacz ${BOLD}\"Cached images and files\"${NC}"
    echo -e "   • Kliknij ${BOLD}\"Clear data\"${NC}"
    echo -e "   • ${BOLD}LUB${NC} naciśnij ${BOLD}F12${NC} → Application → Clear Storage → Clear site data"
    
    echo -e "\n${CYAN}2. ${BOLD}Safari:${NC}"
    echo -e "   • Safari → Preferences → Privacy → Manage Website Data → Remove All"
    echo -e "   • ${BOLD}LUB${NC} Cmd + Option + E (Clear Cache)"
    
    echo -e "\n${CYAN}3. ${BOLD}Firefox:${NC}"
    echo -e "   • Cmd + Shift + Delete → Everything → Clear Now"
    
    echo -e "\n${GREEN}${BOLD}💡 SZYBKIE ROZWIĄZANIE: Otwórz tryb incognito!${NC}"
    echo -e "${GREEN}   Chrome: Cmd + Shift + N${NC}"
    echo -e "${GREEN}   Safari: Cmd + Shift + N${NC}"
    echo -e "${GREEN}   Firefox: Cmd + Shift + P${NC}"
    
    # Próba automatycznego czyszczenia dla Chrome
    echo -e "\n${YELLOW}🔄 Próbuję automatycznie wyczyścić cache Chrome...${NC}"
    CHROME_CACHE_DIR="$HOME/Library/Caches/Google/Chrome/Default"
    if [ -d "$CHROME_CACHE_DIR" ]; then
        # Zamknij Chrome jeśli jest uruchomiony
        osascript -e 'quit app "Google Chrome"' 2>/dev/null || true
        sleep 2
        
        # Wyczyść cache
        rm -rf "$CHROME_CACHE_DIR/Cache"/* 2>/dev/null || true
        rm -rf "$CHROME_CACHE_DIR/Code Cache"/* 2>/dev/null || true
        rm -rf "$CHROME_CACHE_DIR/Service Worker"/* 2>/dev/null || true
        
        echo -e "${GREEN}✅ Cache Chrome wyczyszczony automatycznie${NC}"
    fi
}

start_backend() {
    echo -e "\n${BLUE}📋 KROK 2: URUCHAMIAM BACKEND (port $BACKEND_PORT)${NC}"
    
    if [ ! -d "$BACKEND_DIR" ]; then
        echo -e "${RED}❌ Katalog backend nie istnieje: $BACKEND_DIR${NC}"
        exit 1
    fi
    
    cd "$BACKEND_DIR"
    
    # Sprawdź środowisko wirtualne
    if [ ! -d "venv" ]; then
        echo -e "${RED}❌ Brak środowiska wirtualnego venv!${NC}"
        echo -e "${YELLOW}💡 Utwórz venv: python3 -m venv venv${NC}"
        exit 1
    fi
    
    # Sprawdź czy api_server.py istnieje
    if [ ! -f "api_server.py" ]; then
        echo -e "${RED}❌ Brak pliku api_server.py!${NC}"
        exit 1
    fi
    
    # Uruchom backend
    echo -e "${YELLOW}🚀 Uruchamiam backend Flask...${NC}"
    source venv/bin/activate && python3 api_server.py &
    BACKEND_PID=$!
    
    echo -e "${GREEN}✅ Backend uruchomiony (PID: $BACKEND_PID)${NC}"
    
    # Czekaj na uruchomienie
    echo -e "${YELLOW}⏳ Czekam na backend...${NC}"
    for i in {1..15}; do
        if curl -s "http://localhost:$BACKEND_PORT/api/version" >/dev/null 2>&1; then
            VERSION=$(curl -s "http://localhost:$BACKEND_PORT/api/version" | grep -o '"version":"[^"]*"' | cut -d'"' -f4 2>/dev/null || echo "?")
            echo -e "${GREEN}✅ Backend SKATECROSS v$VERSION działa na porcie $BACKEND_PORT${NC}"
            return 0
        fi
        echo -e "${YELLOW}⏳ Próba $i/15 - czekam na backend...${NC}"
        sleep 2
    done
    
    echo -e "${RED}❌ Backend nie odpowiada po 30 sekundach!${NC}"
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
}

start_frontend() {
    echo -e "\n${BLUE}📋 KROK 3: URUCHAMIAM FRONTEND (port $FRONTEND_PORT)${NC}"
    
    if [ ! -d "$FRONTEND_DIR" ]; then
        echo -e "${RED}❌ Katalog frontend nie istnieje: $FRONTEND_DIR${NC}"
        exit 1
    fi
    
    cd "$FRONTEND_DIR"
    
    # Sprawdź Node.js
    echo -e "${YELLOW}🔧 Sprawdzam Node.js...${NC}"
    if ! command -v node &> /dev/null; then
        echo -e "${RED}❌ Node.js nie jest zainstalowany!${NC}"
        exit 1
    fi
    
    # Użyj NVM jeśli dostępne
    if [ -f "$HOME/.nvm/nvm.sh" ]; then
        echo -e "${YELLOW}🔧 Używam NVM...${NC}"
        source ~/.nvm/nvm.sh
        nvm use v24.2.0 2>/dev/null || nvm use node 2>/dev/null || true
    fi
    
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✅ Node.js: $NODE_VERSION${NC}"
    
    # Sprawdź package.json
    if [ ! -f "package.json" ]; then
        echo -e "${RED}❌ Brak pliku package.json!${NC}"
        exit 1
    fi
    
    # Sprawdź node_modules
    if [ ! -d "node_modules" ]; then
        echo -e "${YELLOW}📦 Instaluję zależności...${NC}"
        npm install
    fi
    
    # KRYTYCZNE: Wymuś port 5173 i zablokuj automatyczne przełączanie
    echo -e "${BOLD}${GREEN}🎯 Uruchamiam frontend WYMUSZAJĄC port $FRONTEND_PORT${NC}"
    echo -e "${YELLOW}⚠️  UWAGA: Frontend MUSI działać na porcie $FRONTEND_PORT (nie $((FRONTEND_PORT+1))!)${NC}"
    
    # Uruchom z wymuszonym portem i hostem
    npm run dev -- --port $FRONTEND_PORT --host --strictPort &
    FRONTEND_PID=$!
    
    echo -e "${GREEN}✅ Frontend uruchomiony (PID: $FRONTEND_PID)${NC}"
    
    # Czekaj na uruchomienie i sprawdź poprawny port
    echo -e "${YELLOW}⏳ Czekam na frontend...${NC}"
    for i in {1..20}; do
        if lsof -ti:$FRONTEND_PORT >/dev/null 2>&1; then
            echo -e "${GREEN}✅ Frontend działa na porcie $FRONTEND_PORT${NC}"
            
            # Sprawdź czy nie uruchomił się na innym porcie
            for wrong_port in $((FRONTEND_PORT+1)) $((FRONTEND_PORT+2)) $((FRONTEND_PORT+3)); do
                if lsof -ti:$wrong_port >/dev/null 2>&1; then
                    echo -e "${RED}❌ BŁĄD: Frontend uruchomił się także na porcie $wrong_port!${NC}"
                    echo -e "${YELLOW}🔪 Zabijam proces na niepożądanym porcie...${NC}"
                    lsof -ti:$wrong_port | xargs kill -9 2>/dev/null || true
                fi
            done
            
            return 0
        fi
        
        # Sprawdź czy przypadkiem nie uruchomił się na złym porcie
        for wrong_port in $((FRONTEND_PORT+1)) $((FRONTEND_PORT+2)) $((FRONTEND_PORT+3)); do
            if lsof -ti:$wrong_port >/dev/null 2>&1; then
                echo -e "${RED}❌ BŁĄD: Frontend uruchomił się na złym porcie $wrong_port zamiast $FRONTEND_PORT!${NC}"
                lsof -ti:$wrong_port | xargs kill -9 2>/dev/null || true
                kill $FRONTEND_PID 2>/dev/null || true
                exit 1
            fi
        done
        
        echo -e "${YELLOW}⏳ Próba $i/20 - czekam na frontend na porcie $FRONTEND_PORT...${NC}"
        sleep 2
    done
    
    echo -e "${RED}❌ Frontend nie uruchomił się na porcie $FRONTEND_PORT!${NC}"
    echo -e "${YELLOW}🔍 Sprawdzam które porty są zajęte przez frontend:${NC}"
    ps aux | grep vite | grep -v grep
    lsof -i | grep node | head -5
    kill $FRONTEND_PID 2>/dev/null || true
    exit 1
}

verify_system() {
    echo -e "\n${BLUE}📋 KROK 4: WERYFIKACJA SYSTEMU${NC}"
    
    # Test backend
    echo -e "${YELLOW}🔍 Testuję backend API...${NC}"
    if curl -s "http://localhost:$BACKEND_PORT/api/version" >/dev/null 2>&1; then
        VERSION=$(curl -s "http://localhost:$BACKEND_PORT/api/version" | grep -o '"version":"[^"]*"' | cut -d'"' -f4 2>/dev/null || echo "?")
        echo -e "${GREEN}✅ Backend: SKATECROSS v$VERSION na http://localhost:$BACKEND_PORT${NC}"
        
        # Test endpoint zawodników
        if curl -s "http://localhost:$BACKEND_PORT/api/zawodnicy?limit=1" >/dev/null 2>&1; then
            echo -e "${GREEN}✅ Backend API: Endpoint /api/zawodnicy działa${NC}"
        else
            echo -e "${YELLOW}⚠️  Backend API: Problem z endpoint /api/zawodnicy${NC}"
        fi
    else
        echo -e "${RED}❌ Backend: NIEDOSTĘPNY na porcie $BACKEND_PORT${NC}"
        return 1
    fi
    
    # Test frontend
    echo -e "${YELLOW}🔍 Testuję frontend...${NC}"
    if lsof -ti:$FRONTEND_PORT >/dev/null 2>&1; then
        echo -e "${GREEN}✅ Frontend: Dostępny na http://localhost:$FRONTEND_PORT${NC}"
        echo -e "${GREEN}✅ Sieć: Dostępny na http://192.168.0.178:$FRONTEND_PORT${NC}"
        
        # Test czy frontend ładuje się poprawnie
        if curl -s "http://localhost:$FRONTEND_PORT" | grep -i "skatecross" >/dev/null 2>&1; then
            echo -e "${GREEN}✅ Frontend: Aplikacja SKATECROSS ładuje się poprawnie${NC}"
        else
            echo -e "${YELLOW}⚠️  Frontend: Problem z ładowaniem aplikacji${NC}"
        fi
        
        # Test proxy
        if curl -s "http://localhost:$FRONTEND_PORT/api/version" >/dev/null 2>&1; then
            echo -e "${GREEN}✅ Proxy: Frontend → Backend działa poprawnie${NC}"
        else
            echo -e "${YELLOW}⚠️  Proxy: Problem z połączeniem Frontend → Backend${NC}"
        fi
    else
        echo -e "${RED}❌ Frontend: NIEDOSTĘPNY na porcie $FRONTEND_PORT${NC}"
        return 1
    fi
    
    # Sprawdź czy PWA Scanner będzie dostępny
    echo -e "${YELLOW}🔍 Sprawdzam komponenty PWA...${NC}"
    if [ -f "$FRONTEND_DIR/src/components/PWARouter.vue" ] && [ -f "$FRONTEND_DIR/src/components/PWAQRScanner.vue" ]; then
        echo -e "${GREEN}✅ PWA: Komponenty PWARouter i PWAQRScanner istnieją${NC}"
    else
        echo -e "${RED}❌ PWA: Brak komponentów PWA Scanner${NC}"
    fi
    
    return 0
}

show_final_status() {
    echo -e "\n${CYAN}${BOLD}============================================================================${NC}"
    echo -e "${GREEN}${BOLD} 🎉 SKATECROSS v37.0 URUCHOMIONY POMYŚLNIE!${NC}"
    echo -e "${CYAN}${BOLD}============================================================================${NC}"
    
    echo -e "\n${BOLD}📊 STATUS SERWISÓW:${NC}"
    echo -e "${GREEN}✅ Backend:  http://localhost:$BACKEND_PORT${NC}"
    echo -e "${GREEN}✅ Frontend: http://localhost:$FRONTEND_PORT${NC}"
    echo -e "${GREEN}✅ Sieć:    http://192.168.0.178:$FRONTEND_PORT${NC}"
    
    echo -e "\n${BOLD}📱 DOSTĘPNE FUNKCJE:${NC}"
    echo -e "${GREEN}• Dashboard - statystyki i przegląd${NC}"
    echo -e "${GREEN}• Zawodnicy - zarządzanie uczestnikami${NC}"
    echo -e "${GREEN}• Start Control - kontrola linii startu${NC}"
    echo -e "${GREEN}• Rankingi - wyniki i czasy${NC}"
    echo -e "${GREEN}• QR Dashboard - zarządzanie kodami QR${NC}"
    echo -e "${BOLD}${GREEN}• PWA Scanner - skaner QR (GŁÓWNA FUNKCJA!)${NC}"
    
    echo -e "\n${BOLD}🔧 INFORMACJE TECHNICZNE:${NC}"
    echo -e "Backend PID:  $BACKEND_PID"
    echo -e "Frontend PID: $FRONTEND_PID"
    
    echo -e "\n${BOLD}🛑 ZATRZYMANIE SYSTEMU:${NC}"
    echo -e "${RED}kill $BACKEND_PID $FRONTEND_PID${NC}"
    echo -e "${RED}# LUB użyj Ctrl+C w terminalach gdzie działają procesy${NC}"
    
    echo -e "\n${BOLD}${YELLOW}⚠️  WAŻNE - CACHE PRZEGLĄDARKI:${NC}"
    echo -e "${YELLOW}Jeśli PWA Scanner nie jest widoczny:${NC}"
    echo -e "${CYAN}1. Naciśnij F12 → Application → Clear Storage → Clear site data${NC}"
    echo -e "${CYAN}2. LUB użyj trybu incognito (Cmd + Shift + N)${NC}"
    echo -e "${CYAN}3. LUB wykonaj hard refresh (Cmd + Shift + R)${NC}"
    
    echo -e "\n${GREEN}${BOLD}🚀 System gotowy do użycia!${NC}"
    echo -e "${CYAN}${BOLD}============================================================================${NC}"
}

monitor_system() {
    echo -e "\n${BLUE}🔄 MONITOROWANIE SYSTEMU (Ctrl+C aby zatrzymać)${NC}"
    
    while true; do
        sleep 30
        
        # Sprawdź backend
        if ! curl -s "http://localhost:$BACKEND_PORT/api/version" >/dev/null 2>&1; then
            echo -e "${RED}❌ $(date '+%H:%M:%S') - Backend przestał odpowiadać!${NC}"
            break
        fi
        
        # Sprawdź frontend
        if ! lsof -ti:$FRONTEND_PORT >/dev/null 2>&1; then
            echo -e "${RED}❌ $(date '+%H:%M:%S') - Frontend przestał działać!${NC}"
            break
        fi
        
        # Sprawdź czy frontend nie przeskoczył na inny port
        for wrong_port in $((FRONTEND_PORT+1)) $((FRONTEND_PORT+2)) $((FRONTEND_PORT+3)); do
            if lsof -ti:$wrong_port >/dev/null 2>&1; then
                echo -e "${YELLOW}⚠️  $(date '+%H:%M:%S') - Wykryto frontend na niepożądanym porcie $wrong_port - zabijam...${NC}"
                lsof -ti:$wrong_port | xargs kill -9 2>/dev/null || true
            fi
        done
        
        echo -e "${GREEN}✅ $(date '+%H:%M:%S') - Wszystko działa poprawnie${NC}"
    done
    
    echo -e "${RED}🛑 Monitorowanie zatrzymane - wykryto problem z systemem${NC}"
}

# ============================================================================
# GŁÓWNA FUNKCJA
# ============================================================================
main() {
    print_header
    
    # Sprawdź czy jesteśmy w odpowiednim katalogu
    if [ ! -d "$PROJECT_DIR" ]; then
        echo -e "${RED}❌ Katalog projektu nie istnieje: $PROJECT_DIR${NC}"
        exit 1
    fi
    
    # Przejdź do katalogu projektu
    cd "$PROJECT_DIR"
    
    # Wykonaj wszystkie kroki
    cleanup_processes
    cleanup_frontend_cache
    cleanup_browser_cache
    start_backend
    start_frontend
    
    if verify_system; then
        show_final_status
        monitor_system
    else
        echo -e "${RED}❌ Weryfikacja systemu nie powiodła się!${NC}"
        exit 1
    fi
}

# Uruchom główną funkcję
main "$@" 