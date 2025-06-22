#!/bin/bash
echo "🔧 NAPRAWA PROBLEMÓW Z AKTYWACJĄ GRUP"

# 1. Backup
cp frontend/src/components/StartLineScanner.vue frontend/src/components/StartLineScanner.vue.backup
echo "✅ Utworzono backup"

# 2. Usuń problematyczne setTimeout opóźnienia
sed -i 's/}, 500)/}, 100)/g' frontend/src/components/StartLineScanner.vue
sed -i 's/}, 1000)/}, 200)/g' frontend/src/components/StartLineScanner.vue
echo "✅ Zmniejszono opóźnienia setTimeout"

# 3. Restart frontend dla zastosowania zmian
if [ -f .frontend_pid ]; then
    frontend_pid=$(cat .frontend_pid)
    if ps -p $frontend_pid > /dev/null; then
        kill $frontend_pid
        echo "✅ Zatrzymano stary frontend"
        sleep 2
    fi
fi

echo "🚀 Uruchamiam frontend z naprawami..."
cd frontend && npm run dev > ../frontend.log 2>&1 &
echo $! > ../.frontend_pid
cd ..

sleep 3
echo "✅ NAPRAWY ZASTOSOWANE!"
echo "Frontend: http://localhost:5173"
echo "Backend: http://localhost:5000"
echo ""
echo "TESTUJ TERAZ:"
echo "1. Aktywuj grupę - powinno być szybko (1-2s)"
echo "2. Sprawdź ładowanie kolejki - powinno być natychmiastowe"
echo "3. Przełączaj grupy - brak zombie zawodników" 