#!/usr/bin/env python3

def fix_queue_activation():
    """OSTATECZNA NAPRAWA problemu aktywacji kolejki"""
    
    with open('frontend/src/components/StartLineScanner.vue', 'r') as f:
        content = f.read()
    
    print('🔧 NAPRAWIAM GŁÓWNY PROBLEM AKTYWACJI KOLEJKI...')
    
    # 1. USUŃ GUARD który blokuje ładowanie aktywnej grupy
    old_guard = """    // 3. Aktywna grupa (tylko jeśli nie ma optymistycznej)
    if (!appState.value.optimisticActiveGroupId) {"""
    
    new_guard = """    // 3. Aktywna grupa - ZAWSZE ładuj z backend (cache-busting)
    {"""
    
    content = content.replace(old_guard, new_guard)
    print('✅ Usunięto guard blokujący ładowanie aktywnej grupy')
    
    # 2. Dodaj cache-busting do WSZYSTKICH API calls
    api_calls = [
        "fetch('/api/grupy-startowe')",
        "fetch('/api/grupa-aktywna')", 
        "fetch('/api/start-queue')"
    ]
    
    for call in api_calls:
        if call in content:
            new_call = call.replace("')", f"?_t=${{Date.now()}}')")
            content = content.replace(call, new_call)
            print(f'✅ Dodano cache-busting do {call}')
    
    # 3. NATYCHMIASTOWY sync po aktywacji (bez setTimeout)
    old_timeout = """setTimeout(async () => {
      try {
        appState.value.syncingData = true
        await syncAllData('po aktywacji grupy')
      } catch (error) {
        console.error('❌ Błąd synchronizacji po aktywacji:', error)
      } finally {
        appState.value.syncingData = false
      }
    }, 500) // Krótsze opóźnienie"""
    
    new_immediate = """// NATYCHMIASTOWY sync po aktywacji grupy
    appState.value.syncingData = true
    try {
      await syncAllData('po aktywacji grupy')
      console.log('🎯 SYNC ZAKOŃCZONY PO AKTYWACJI')
    } catch (error) {
      console.error('❌ Błąd synchronizacji po aktywacji:', error)
    } finally {
      appState.value.syncingData = false
    }"""
    
    content = content.replace(old_timeout, new_immediate)
    print('✅ Zastąpiono setTimeout natychmiastowym sync')
    
    # 4. Wyczyść optimisticActiveGroupId po sukcesie
    old_success = """    // Po sukcesie ustaw prawdziwą aktywną grupę
    aktualna_grupa.value = grupa"""
    
    new_success = """    // Po sukcesie ustaw prawdziwą aktywną grupę i wyczyść optymistyczną
    aktualna_grupa.value = grupa
    appState.value.optimisticActiveGroupId = null"""
    
    content = content.replace(old_success, new_success)
    print('✅ Dodano czyszczenie optimisticActiveGroupId po sukcesie')
    
    # Zapisz
    with open('frontend/src/components/StartLineScanner.vue', 'w') as f:
        f.write(content)
    
    print('')
    print('✅ GŁÓWNY PROBLEM AKTYWACJI KOLEJKI NAPRAWIONY!')
    print('   🔧 Usunięto guard blokujący sync aktywnej grupy')
    print('   🔧 Dodano cache-busting do wszystkich API calls')  
    print('   🔧 Natychmiastowy sync po aktywacji (bez setTimeout)')
    print('   🔧 Czyszczenie optimisticActiveGroupId po sukcesie')
    print('')
    print('🎯 TERAZ AKTYWACJA GRUPY POWINNA DZIAŁAĆ!')

if __name__ == '__main__':
    fix_queue_activation() 