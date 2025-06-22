#!/bin/bash
echo "🚨 NAPRAWA KRYTYCZNYCH PROBLEMÓW Z KOLEJKĄ"
echo "=========================================="

# Backup
cp frontend/src/components/StartLineScanner.vue frontend/src/components/StartLineScanner.vue.critical_backup
echo "✅ Backup utworzony"

# PROBLEM 1: Zmień setTimeout 500ms na 50ms (szybszy sync)
echo "🔧 Naprawiam Problem 1: Przyspieszam sync..."
sed -i 's/}, 500)/}, 50)/g' frontend/src/components/StartLineScanner.vue

# PROBLEM 2: Zmień setTimeout 1000ms na 100ms 
echo "🔧 Naprawiam Problem 2: Przyspieszam auto-sync..."
sed -i 's/}, 1000)/}, 100)/g' frontend/src/components/StartLineScanner.vue

# PROBLEM 3: Dodaj import nextTick do Vue
echo "🔧 Naprawiam Problem 3: Dodaję Vue reactivity..."
sed -i 's/import { ref, computed, onMounted, onUnmounted }/import { ref, computed, onMounted, onUnmounted, nextTick, triggerRef }/' frontend/src/components/StartLineScanner.vue

# Restart frontend
echo "🔄 Restartowanie frontend..."
if [ -f .frontend_pid ]; then
    frontend_pid=$(cat .frontend_pid)
    if ps -p $frontend_pid > /dev/null; then
        kill $frontend_pid
        sleep 2
    fi
fi

cd frontend && npm run dev > ../frontend.log 2>&1 &
echo $! > ../.frontend_pid
cd ..

sleep 3
echo ""
echo "✅ PODSTAWOWE NAPRAWY ZASTOSOWANE!"
echo "=================================="
echo "1. ✅ Przyspieszono synchronizację (500ms→50ms)"
echo "2. ✅ Przyspieszono auto-sync (1000ms→100ms)" 
echo "3. ✅ Dodano Vue reactivity helpers"
echo ""
echo "🌐 Frontend: http://localhost:5173"
echo "🔧 Backend: http://localhost:5000"
echo ""
echo "TESTUJ TERAZ - powinno być dużo szybsze!" 