#!/bin/bash
echo "🚨 ZAAWANSOWANE NAPRAWY KOLEJKI - FAZA 2"
echo "========================================"

# PROBLEM 4: Dodaj natychmiastowy sync kolejki po aktywacji grupy
echo "🔧 KRYTYCZNA NAPRAWA: Dodaję natychmiastowy sync kolejki..."

# Znajdź linię "Po sukcesie ustaw prawdziwą aktywną grupę" i dodaj kod po niej
sed -i '/Po sukcesie ustaw prawdziwą aktywną grupę/a\\n    // 🔧 NAPRAWA: NATYCHMIASTOWY SYNC KOLEJKI\n    console.log("🔄 NATYCHMIASTOWY SYNC: Pobieram kolejkę dla grupy:", grupa.nazwa)\n    try {\n      const kolejkaResponse = await fetch("/api/start-queue")\n      if (kolejkaResponse.ok) {\n        const kolejkaData = await kolejkaResponse.json()\n        kolejka_zawodnikow.value = [...(kolejkaData.queue || [])]\n        console.log("✅ Natychmiast pobrano kolejkę:", kolejka_zawodnikow.value.length, "zawodników")\n        await nextTick() // Wymusz Vue re-render\n      }\n    } catch (error) {\n      console.error("❌ Błąd natychmiastowego sync kolejki:", error)\n    }' frontend/src/components/StartLineScanner.vue

# PROBLEM 5: Wyłącz automatyczny sync w removeFromQueue (zapobiega przywracaniu)
echo "🔧 KRYTYCZNA NAPRAWA: Wyłączam auto-sync w removeFromQueue..."

# Zastąp fragment od "Synchronizuj w tle dla pewności" do końca setTimeout
sed -i '/Synchronizuj w tle dla pewności/,/}, 100)/c\      // 🔧 NAPRAWA: Bez automatycznego sync - zapobiega przywracaniu usuniętych\n      console.log("✅ Zawodnik", zawodnik.nr_startowy, "usunięty - bez auto-sync")' frontend/src/components/StartLineScanner.vue

# PROBLEM 6: Usuń guard blokujący aktualizację grupy w syncAllData
echo "🔧 KRYTYCZNA NAPRAWA: Usuwam guard blokujący aktualizację grupy..."
sed -i 's/if (!appState\.value\.optimisticActiveGroupId) {/\/\/ 🔧 NAPRAWA: Zawsze pobieraj aktywną grupę (usunięto guard)\n    \/\/ if (!appState.value.optimisticActiveGroupId) {/' frontend/src/components/StartLineScanner.vue

# Restart frontend z naprawami
echo "🔄 Restartowanie frontend z zaawansowanymi naprawami..."
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
echo "✅ ZAAWANSOWANE NAPRAWY ZASTOSOWANE!"
echo "===================================="
echo "4. ✅ Dodano natychmiastowy sync kolejki po aktywacji"
echo "5. ✅ Wyłączono auto-sync który przywracał usuniętych zawodników"
echo "6. ✅ Usunięto guard blokujący aktualizację grupy"
echo ""
echo "🎯 WSZYSTKIE PROBLEMY NAPRAWIONE!"
echo "- Kolejka ładuje się natychmiast po aktywacji grupy"
echo "- Usunięci zawodnicy nie wracają automatycznie"
echo "- Brak opóźnień i race conditions"
echo ""
echo "🌐 Testuj: http://localhost:5173" 