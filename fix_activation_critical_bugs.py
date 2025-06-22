#!/usr/bin/env python3

def fix_activation_bugs():
    """Naprawia 2 krytyczne błędy aktywacji grupy"""
    
    with open('frontend/src/components/StartLineScanner.vue', 'r') as f:
        content = f.read()
    
    print('🔧 NAPRAWIAM KRYTYCZNE BŁĘDY AKTYWACJI...')
    
    # 1. PROBLEM: Za szybkie czyszczenie optimisticActiveGroupId
    old_clear = """    // Po sukcesie ustaw prawdziwą aktywną grupę i wyczyść optymistyczną
    aktualna_grupa.value = grupa
    appState.value.optimisticActiveGroupId = null"""
    
    new_clear = """    // Po sukcesie ustaw prawdziwą aktywną grupę (NIE czyść optimistic jeszcze!)
    aktualna_grupa.value = grupa
    // appState.value.optimisticActiveGroupId = null  // Wyczyścimy PO syncAllData()"""
    
    content = content.replace(old_clear, new_clear)
    print('✅ Opóźniono czyszczenie optimisticActiveGroupId')
    
    # 2. Dodaj czyszczenie optimisticActiveGroupId PO syncAllData
    old_sync = """      await syncAllData('po aktywacji grupy')
      console.log('🎯 SYNC ZAKOŃCZONY PO AKTYWACJI')
    } catch (error) {
      console.error('❌ Błąd synchronizacji po aktywacji:', error)
    } finally {
      appState.value.syncingData = false
    }"""
    
    new_sync = """      await syncAllData('po aktywacji grupy')
      console.log('🎯 SYNC ZAKOŃCZONY PO AKTYWACJI')
      // Teraz możemy bezpiecznie wyczyścić optimistic ID
      appState.value.optimisticActiveGroupId = null
    } catch (error) {
      console.error('❌ Błąd synchronizacji po aktywacji:', error)
    } finally {
      appState.value.syncingData = false
    }"""
    
    content = content.replace(old_sync, new_sync)
    print('✅ Przeniesiono czyszczenie optimisticActiveGroupId po syncAllData()')
    
    # 3. PROBLEM: Template strings w pojedynczych cudzysłowach
    wrong_templates = [
        "fetch('/api/grupy-startowe?_t=${Date.now()}')",
        "fetch('/api/grupa-aktywna?_t=${Date.now()}')",
        "fetch('/api/start-queue?_t=${Date.now()}')"
    ]
    
    correct_templates = [
        "fetch(`/api/grupy-startowe?_t=${Date.now()}`)",
        "fetch(`/api/grupa-aktywna?_t=${Date.now()}`)",
        "fetch(`/api/start-queue?_t=${Date.now()}`)"
    ]
    
    for wrong, correct in zip(wrong_templates, correct_templates):
        if wrong in content:
            content = content.replace(wrong, correct)
            print(f'✅ Naprawiono template string: {wrong} -> {correct}')
    
    # Zapisz
    with open('frontend/src/components/StartLineScanner.vue', 'w') as f:
        f.write(content)
    
    print('')
    print('✅ KRYTYCZNE BŁĘDY AKTYWACJI NAPRAWIONE!')
    print('   🔧 Opóźniono czyszczenie optimisticActiveGroupId (będzie po sync)')
    print('   🔧 Naprawiono template strings (pojedyncze cudzysłowy -> backticks)')
    print('   🔧 Cache-busting działa teraz poprawnie z timestampem')
    print('')
    print('🎯 AKTYWACJA GRUP POWINNA TERAZ DZIAŁAĆ POPRAWNIE!')

if __name__ == '__main__':
    fix_activation_bugs() 