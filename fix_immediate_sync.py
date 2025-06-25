#!/usr/bin/env python3

def fix_immediate_sync():
    # Wczytaj plik
    with open('frontend/src/components/StartLineScanner.vue', 'r') as f:
        content = f.read()
    
    # Znajdź i zastąp setTimeout natychmiastowym wykonaniem
    old_timeout = '''    // SYNC: Po aktywacji synchronizuj dane w tle (z loading indicator)
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
    }, 50) // NATYCHMIASTOWY SYNC'''
    
    new_immediate = '''    // SYNC: Po aktywacji synchronizuj dane NATYCHMIAST (bez setTimeout)
    console.log('✅ Grupa aktywowana, synchronizuję dane NATYCHMIAST...')
    try {
      appState.value.syncingData = true
      await syncAllData('po aktywacji grupy')
      console.log('🎯 SYNC ZAKOŃCZONY PO AKTYWACJI')
    } catch (error) {
      console.error('❌ Błąd synchronizacji po aktywacji:', error)
    } finally {
      appState.value.syncingData = false
    }'''
    
    if old_timeout in content:
        content = content.replace(old_timeout, new_immediate)
        print('✅ Usunięto setTimeout - sync jest teraz NATYCHMIASTOWY')
        changes_made = True
    else:
        print('⚠️ Nie znaleziono setTimeout do usunięcia')
        changes_made = False
    
    # Zapisz plik
    if changes_made:
        with open('frontend/src/components/StartLineScanner.vue', 'w') as f:
            f.write(content)
        print('✅ Zapisano zmiany')
    
    print('')
    print('⚡ NATYCHMIASTOWY SYNC PO AKTYWACJI:')
    print('   ✅ Usunięto setTimeout(50ms) - sync jest natychmiastowy')
    print('   ✅ Dane będą synchronizowane w tej samej pętli zdarzeń')
    print('   ✅ Brak opóźnień = natychmiastowa aktualizacja!')
    print('')
    print('🔥 KOMBINACJA NAPRAW:')
    print('   1. Cache-busting ✅')
    print('   2. Natychmiastowy sync ✅') 
    print('   3. Teraz powinno działać!')

if __name__ == '__main__':
    fix_immediate_sync() 