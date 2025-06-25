#!/bin/bash

# 🛑 SKATECROSS QR - Zatrzymanie aplikacji

# Kolory
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}🛑 Zatrzymuję aplikację SKATECROSS QR...${NC}"

# Zatrzymaj procesy na podstawie PID
if [ -f "backend/.backend_pid" ]; then
    BACKEND_PID=$(cat backend/.backend_pid)
    if kill $BACKEND_PID 2>/dev/null; then
        echo -e "${GREEN}✅ Backend zatrzymany (PID: $BACKEND_PID)${NC}"
    fi
    rm -f backend/.backend_pid
fi

if [ -f "frontend/.frontend_pid" ]; then
    FRONTEND_PID=$(cat frontend/.frontend_pid)
    if kill $FRONTEND_PID 2>/dev/null; then
        echo -e "${GREEN}✅ Frontend zatrzymany (PID: $FRONTEND_PID)${NC}"
    fi
    rm -f frontend/.frontend_pid
fi

# Zatrzymaj wszystkie procesy jako backup
pkill -f "python.*api_server" 2>/dev/null || true
pkill -f "node.*vite" 2>/dev/null || true

echo -e "${GREEN}🎉 Aplikacja zatrzymana!${NC}"
