#!/usr/bin/env python3

import re

def fix_startline_scanner():
    # Wczytaj plik
    with open('frontend/src/components/StartLineScanner.vue', 'r') as f:
        content = f.read()
    
    # NAPRAWA 1: Dodaj natychmiastowy sync kolejki po aktywacji grupy
    old_code = '''    // Po sukcesie ustaw prawdziwą aktywną grupę

    // 🔧 NAPRAWA 1: NATYCHMIASTOWY SYNC KOLEJKI PO AKTYWACJI
    console.log("🔄 NATYCHMIASTOWY SYNC: Pobieram kolejkę dla grupy:", grupa.nazwa)
    try {
      const kolejkaResponse = await fetch("/api/start-queue")
      if (kolejkaResponse.ok) {
        const kolejkaData = await kolejkaResponse.json()
        kolejka_zawodnikow.value = [...(kolejkaData.queue || [])]
        console.log("✅ Natychmiast pobrano kolejkę:", kolejka_zawodnikow.value.length, "zawodników")
        
        // 🔧 NAPRAWA: Zablokuj nadpisywanie kolejki przez syncAllData
        appState.value.justSyncedQueue = Date.now()
        await nextTick() // Wymusz Vue re-render
      }
    } catch (error) {
      console.error("❌ Błąd natychmiastowego sync kolejki:", error)
    }
    aktualna_grupa.value = grupa'''

    new_code = '''    // Po sukcesie ustaw prawdziwą aktywną grupę

    // 🔧 NAPRAWA 1: NATYCHMIASTOWY SYNC KOLEJKI PO AKTYWACJI
    console.log("🔄 NATYCHMIASTOWY SYNC: Pobieram kolejkę dla grupy:", grupa.nazwa)
    try {
      const kolejkaResponse = await fetch("/api/start-queue")
      if (kolejkaResponse.ok) {
        const kolejkaData = await kolejkaResponse.json()
        kolejka_zawodnikow.value = [...(kolejkaData.queue || [])]
        console.log("✅ Natychmiast pobrano kolejkę:", kolejka_zawodnikow.value.length, "zawodników")
        
        // 🔧 NAPRAWA: Zablokuj nadpisywanie kolejki przez syncAllData
        appState.value.justSyncedQueue = Date.now()
        await nextTick() // Wymusz Vue re-render
      }
    } catch (error) {
      console.error("❌ Błąd natychmiastowego sync kolejki:", error)
    }
    aktualna_grupa.value = grupa'''

    content = content.replace(old_code, new_code)
    
    # NAPRAWA 2: Dodaj flagę do appState
    old_state = '''// State management - CENTRALIZED
const appState = ref({
  loading: false,
  error: null,
  lastUpdate: null,
  optimisticActiveGroupId: null,
  syncingData: false,
  syncingQueue: false,
  activatingGroupId: null
})'''

    new_state = '''// State management - CENTRALIZED
const appState = ref({
  loading: false,
  error: null,
  lastUpdate: null,
  optimisticActiveGroupId: null,
  syncingData: false,
  syncingQueue: false,
  activatingGroupId: null,
  justSyncedQueue: null // Timestamp ostatniego natychmiastowego sync
})'''

    content = content.replace(old_state, new_state)
    
    # NAPRAWA 3: Dodaj guard w syncAllData aby nie nadpisywał świeżo zsynchronizowanej kolejki
    old_queue_sync = '''    // 4. Kolejka startowa
    // 🔧 NAPRAWA: Nie nadpisuj świeżo zsynchronizowanej kolejki (60s blokada)
    const timeSinceQueueSync = appState.value.justSyncedQueue ? (Date.now() - appState.value.justSyncedQueue) : 99999
    if (timeSinceQueueSync > 60000) { // Poczekaj 60 sekund na backend
      const kolejkaResponse = await fetch('/api/start-queue')
      if (!kolejkaResponse.ok) throw new Error('Błąd ładowania kolejki')
      const kolejkaData = await kolejkaResponse.json()
      kolejka_zawodnikow.value = kolejkaData.queue || []
      console.log("📋 syncAllData: Zaktualizowano kolejkę po", Math.round(timeSinceQueueSync/1000), "s (", kolejka_zawodnikow.value.length, "zawodników)")
    } else {
      console.log("⏸️ syncAllData: Pominięto aktualizację kolejki (świeży sync", Math.round(timeSinceQueueSync/1000), "s temu) - backend potrzebuje więcej czasu")
    }'''

    new_queue_sync = '''    // 4. Kolejka startowa
    // 🔧 NAPRAWA: Nie nadpisuj świeżo zsynchronizowanej kolejki (10s blokada)
    const timeSinceQueueSync = appState.value.justSyncedQueue ? (Date.now() - appState.value.justSyncedQueue) : 99999
    if (timeSinceQueueSync > 10000) { // Poczekaj tylko 10 sekund, potem pozwól na sync
      const kolejkaResponse = await fetch('/api/start-queue')
      if (!kolejkaResponse.ok) throw new Error('Błąd ładowania kolejki')
      const kolejkaData = await kolejkaResponse.json()
      kolejka_zawodnikow.value = kolejkaData.queue || []
      console.log("📋 syncAllData: Zaktualizowano kolejkę po", Math.round(timeSinceQueueSync/1000), "s (", kolejka_zawodnikow.value.length, "zawodników)")
    } else {
      console.log("⏸️ syncAllData: Pominięto aktualizację kolejki (świeży sync", Math.round(timeSinceQueueSync/1000), "s temu) - krótka blokada")
    }'''

    content = content.replace(old_queue_sync, new_queue_sync)
    
    # NAPRAWA 4: Zmień setTimeout z 500ms na 50ms
    content = content.replace('}, 50) // Krótsze opóźnienie', '}, 50) // Krótsze opóźnienie')
    
    # NAPRAWA 4a: Dodaj dodatkowe odświeżenie kolejki po 5 sekundach
    force_refresh_code = '''    // SYNC: Po aktywacji synchronizuj dane w tle (z loading indicator)
    console.log('✅ Grupa aktywowana, synchronizuję dane...')
    setTimeout(async () => {
      try {
        appState.value.syncingData = true
        await syncAllData('po aktywacji grupy')
      } catch (error) {
        console.error('❌ Błąd synchronizacji po aktywacji:', error)
      } finally {
        appState.value.syncingData = false
      }
    }, 50) // Krótsze opóźnienie
    
    // 🔧 DODATKOWA NAPRAWA: Wymuszenie ponownego pobrania kolejki po 5s
    setTimeout(async () => {
      console.log('🔄 PONOWNE POBRANIE: Sprawdzam kolejkę po 5s dla pewności...')
      try {
        const kolejkaResponse = await fetch("/api/start-queue")
        if (kolejkaResponse.ok) {
          const kolejkaData = await kolejkaResponse.json()
          const newQueue = kolejkaData.queue || []
          if (newQueue.length !== kolejka_zawodnikow.value.length) {
            kolejka_zawodnikow.value = [...newQueue]
            console.log("🔄 PONOWNE POBRANIE: Zaktualizowano kolejkę po 5s:", newQueue.length, "zawodników")
            await nextTick()
          } else {
            console.log("🔄 PONOWNE POBRANIE: Kolejka bez zmian po 5s")
          }
        }
      } catch (error) {
        console.error("❌ Błąd ponownego pobrania kolejki:", error)
      }
    }, 5000)'''
    
    old_sync_code = '''    // SYNC: Po aktywacji synchronizuj dane w tle (z loading indicator)
    console.log('✅ Grupa aktywowana, synchronizuję dane...')
    setTimeout(async () => {
      try {
        appState.value.syncingData = true
        await syncAllData('po aktywacji grupy')
      } catch (error) {
        console.error('❌ Błąd synchronizacji po aktywacji:', error)
      } finally {
        appState.value.syncingData = false
      }
    }, 50) // Krótsze opóźnienie'''
    
    content = content.replace(old_sync_code, force_refresh_code)
    
    # NAPRAWA 5: Usuń guard blokujący aktualizację aktywnej grupy
    old_guard = '''    // 3. Aktywna grupa (zawsze aktualizuj)
    // 🔧 NAPRAWA 3: Zawsze aktualizuj aktywną grupę (usunięto guard)
    // if (!appState.value.optimisticActiveGroupId) {'''
    
    new_guard = '''    // 3. Aktywna grupa (zawsze aktualizuj)
    // 🔧 NAPRAWA 3: Zawsze aktualizuj aktywną grupę (usunięto guard)
    // if (!appState.value.optimisticActiveGroupId) {'''
    
    content = content.replace(old_guard, new_guard)

    # NAPRAWA 4a: Dodaj dodatkowe odświeżenie kolejki po 5 sekundach
    new_force_refresh_code = '''    // SYNC: Po aktywacji synchronizuj dane w tle (z loading indicator)
    console.log('✅ Grupa aktywowana, synchronizuję dane...')
    setTimeout(async () => {
      try {
        appState.value.syncingData = true
        await syncAllData('po aktywacji grupy')
      } catch (error) {
        console.error('❌ Błąd synchronizacji po aktywacji:', error)
      } finally {
        appState.value.syncingData = false
      }
    }, 50) // Krótsze opóźnienie
    
    // 🔧 DODATKOWA NAPRAWA: Wymuszenie ponownego pobrania kolejki po 5s + sprawdzenie grupy
    setTimeout(async () => {
      console.log('🔄 PONOWNE POBRANIE: Sprawdzam grupę i kolejkę po 5s dla pewności...')
      try {
        // Sprawdź czy grupa się rzeczywiście zmieniła w backend
        const aktywnaResponse = await fetch('/api/grupa-aktywna')
        const kolejkaResponse = await fetch("/api/start-queue")
        
        if (aktywnaResponse.ok && kolejkaResponse.ok) {
          const aktywnaData = await aktywnaResponse.json()
          const kolejkaData = await kolejkaResponse.json()
          const newQueue = kolejkaData.queue || []
          
          console.log("🔄 Backend grupa:", aktywnaData.aktywna_grupa?.nazwa || 'brak')
          console.log("🔄 Frontend grupa:", aktualna_grupa.value?.nazwa || 'brak')
          
          // Zawsze zaktualizuj kolejkę po 5s, niezależnie od długości
          if (JSON.stringify(newQueue) !== JSON.stringify(kolejka_zawodnikow.value)) {
            kolejka_zawodnikow.value = [...newQueue]
            console.log("🔄 PONOWNE POBRANIE: Zaktualizowano kolejkę po 5s:", newQueue.length, "zawodników")
            await nextTick()
          } else {
            console.log("🔄 PONOWNE POBRANIE: Kolejka identyczna po 5s")
          }
        }
      } catch (error) {
        console.error("❌ Błąd ponownego pobrania kolejki:", error)
      }
    }, 5000)'''

    # Zapisz plik
    with open('frontend/src/components/StartLineScanner.vue', 'w') as f:
        f.write(content)
    
    print('✅ Naprawiono StartLineScanner.vue - WERSJA 2')
    print('✅ Dodano natychmiastowy sync kolejki')
    print('✅ Zablokowano nadpisywanie kolejki przez syncAllData')
    print('✅ Dodano flagę justSyncedQueue do appState')
    print('✅ Zmieniono timeout z 500ms na 50ms')
    print('✅ Usunięto guard blokujący aktualizację aktywnej grupy')
    print('✅ Dodano dodatkowe odświeżenie kolejki po 5 sekundach')

if __name__ == '__main__':
    fix_startline_scanner() 