#!/usr/bin/env python3

import re

def fix_startline_scanner_simple():
    # Wczytaj plik
    with open('frontend/src/components/StartLineScanner.vue', 'r') as f:
        content = f.read()
    
    # PRZYWRÓĆ import nextTick (jeśli nie ma)
    if 'import { ref, computed, onMounted, onUnmounted, nextTick }' not in content:
        old_import = "import { ref, computed, onMounted, onUnmounted } from 'vue'"
        new_import = "import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'"
        content = content.replace(old_import, new_import)
    
    # USUŃ WSZYSTKIE skomplikowane blokady i timestampy
    # 1. Usuń justSyncedQueue z appState
    old_state = '''const appState = ref({
  loading: false,
  error: null,  
  lastUpdate: null,
  optimisticActiveGroupId: null,
  syncingData: false,
  syncingQueue: false,
  activatingGroupId: null,
  justSyncedQueue: null // Timestamp ostatniego natychmiastowego sync
})'''
    
    new_state = '''const appState = ref({
  loading: false,
  error: null,
  lastUpdate: null,
  optimisticActiveGroupId: null,
  syncingData: false,
  syncingQueue: false,
  activatingGroupId: null
})'''
    
    content = content.replace(old_state, new_state)
    
    # 2. USUŃ wszystkie blokady z syncAllData - przywróć prosty sync kolejki
    # Znajdź sekcję z kolejką i zastąp prostym kodem
    queue_pattern = r'// 4\. Kolejka startowa.*?(?=// 5\.|$)'
    simple_queue_sync = '''    // 4. Kolejka startowa - PROSTY SYNC BEZ BLOKAD
    const kolejkaResponse = await fetch('/api/start-queue')
    if (!kolejkaResponse.ok) throw new Error('Błąd ładowania kolejki')
    const kolejkaData = await kolejkaResponse.json()
    kolejka_zawodnikow.value = kolejkaData.queue || []
    console.log("📋 syncAllData: Pobrano kolejkę (", kolejka_zawodnikow.value.length, "zawodników)")

'''
    
    content = re.sub(queue_pattern, simple_queue_sync, content, flags=re.DOTALL)
    
    # 3. UPROŚĆ aktywację grupy - usuń timestamp i skomplikowane sprawdzenia
    # Znajdź funkcję setAktywnaGrupa i uprość ją
    aktywacja_pattern = r'// Po sukcesie ustaw prawdziwą aktywną grupę.*?aktualna_grupa\.value = grupa'
    
    simple_activation = '''    // Po sukcesie ustaw prawdziwą aktywną grupę
    aktualna_grupa.value = grupa
    
    // PROSTY SYNC: Pobierz kolejkę po aktywacji
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
    
    content = re.sub(aktywacja_pattern, simple_activation, content, flags=re.DOTALL)
    
    # 4. USUŃ wszystkie setTimeout i dodatkowe sprawdzenia po aktywacji
    # Znajdź i usuń setTimeout po aktywacji
    timeout_pattern = r'// SYNC: Po aktywacji synchronizuj dane.*?}, \d+\)'
    simple_sync = '''    // SYNC: Po aktywacji synchronizuj dane (bez timeout)
    console.log('✅ Grupa aktywowana, synchronizuję dane natychmiast...')
    try {
      appState.value.syncingData = true
      await syncAllData('po aktywacji grupy')
    } catch (error) {
      console.error('❌ Błąd synchronizacji po aktywacji:', error)
    } finally {
      appState.value.syncingData = false
    }'''
    
    content = re.sub(timeout_pattern, simple_sync, content, flags=re.DOTALL)
    
    # 5. USUŃ dodatkowe setTimeout z 5-sekundowym sprawdzeniem
    # Usuń wszystkie setTimeout(..., 5000)
    content = re.sub(r'setTimeout\(async \(\) => \{.*?\}, 5000\)', '', content, flags=re.DOTALL)
    
    # Zapisz plik
    with open('frontend/src/components/StartLineScanner.vue', 'w') as f:
        f.write(content)
    
    print('✅ UPROSZCZONO StartLineScanner.vue')
    print('✅ Usunięto wszystkie blokady i timestampy')
    print('✅ Przywrócono prosty sync kolejki')
    print('✅ Usunięto skomplikowane setTimeout')
    print('✅ Pozostawiono tylko natychmiastowy sync po aktywacji')
    print('')
    print('🎯 NOWE PODEJŚCIE: Brak race condition przez prostotę!')
    print('   1. Aktywuj grupę → natychmiast pobierz kolejkę')
    print('   2. Synchronizuj wszystkie dane → pobierz kolejkę ponownie')
    print('   3. Jeśli są różnice → Vue automatycznie zaktualizuje UI')

if __name__ == '__main__':
    fix_startline_scanner_simple() 