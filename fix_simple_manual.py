#!/usr/bin/env python3

def fix_startline_scanner_minimal():
    # Wczytaj plik
    with open('frontend/src/components/StartLineScanner.vue', 'r') as f:
        content = f.read()
    
    # NAPRAWA 1: Dodaj nextTick do importów (jeśli nie ma)
    if 'nextTick' not in content:
        content = content.replace(
            "import { ref, computed, onMounted, onUnmounted } from 'vue'",
            "import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'"
        )
        print('✅ Dodano nextTick do importów')
    
    # NAPRAWA 2: Po aktywacji grupy - dodaj natychmiastowy sync kolejki
    old_activation = '''    // Po sukcesie ustaw prawdziwą aktywną grupę
    aktualna_grupa.value = grupa'''
    
    new_activation = '''    // Po sukcesie ustaw prawdziwą aktywną grupę
    aktualna_grupa.value = grupa
    
    // 🔄 NATYCHMIASTOWY SYNC: Pobierz kolejkę dla nowej grupy
    console.log("🔄 AKTYWACJA: Pobieram kolejkę dla grupy:", grupa.nazwa)
    try {
      const kolejkaResponse = await fetch("/api/start-queue")
      if (kolejkaResponse.ok) {
        const kolejkaData = await kolejkaResponse.json()
        kolejka_zawodnikow.value = [...(kolejkaData.queue || [])]
        console.log("✅ AKTYWACJA: Pobrano kolejkę:", kolejka_zawodnikow.value.length, "zawodników")
        await nextTick()
      }
    } catch (error) {
      console.error("❌ Błąd pobrania kolejki po aktywacji:", error)
    }'''
    
    if old_activation in content:
        content = content.replace(old_activation, new_activation)
        print('✅ Dodano natychmiastowy sync kolejki po aktywacji')
    else:
        print('⚠️ Nie znaleziono sekcji aktywacji grupy')
    
    # Zapisz plik
    with open('frontend/src/components/StartLineScanner.vue', 'w') as f:
        f.write(content)
    
    print('')
    print('🎯 MINIMALNE NAPRAWY ZASTOSOWANE:')
    print('   1. Import nextTick z Vue')
    print('   2. Natychmiastowy sync kolejki po aktywacji grupy')
    print('   3. Brak skomplikowanych blokad czy timestampów!')
    print('')
    print('🚀 Teraz aktywacja powinniość działać szybko!')

if __name__ == '__main__':
    fix_startline_scanner_minimal() 