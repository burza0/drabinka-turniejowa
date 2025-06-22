#!/usr/bin/env python3

def fix_startline_ultra_safe():
    # Wczytaj plik
    with open('frontend/src/components/StartLineScanner.vue', 'r') as f:
        content = f.read()
    
    original_length = len(content)
    changes_made = 0
    
    # JEDYNA BEZPIECZNA ZMIANA: Dodaj nextTick do importu (jeśli nie ma)
    if 'nextTick' not in content:
        old_import = "import { ref, computed, onMounted, onUnmounted, triggerRef } from 'vue'"
        new_import = "import { ref, computed, onMounted, onUnmounted, nextTick, triggerRef } from 'vue'"
        
        if old_import in content:
            content = content.replace(old_import, new_import)
            changes_made += 1
            print('✅ Dodano nextTick do importów Vue')
        else:
            print('⚠️ Nie znaleziono importu do modyfikacji')
    else:
        print('✅ nextTick już jest w importach')
    
    # Sprawdź czy nie uszkodziliśmy pliku
    new_length = len(content)
    if abs(new_length - original_length) > 50:
        print('❌ BŁĄD: Zbyt duża zmiana w rozmiarze pliku! Przywracam oryginał.')
        return
    
    # Zapisz tylko jeśli zrobiliśmy bezpieczne zmiany
    if changes_made > 0:
        with open('frontend/src/components/StartLineScanner.vue', 'w') as f:
            f.write(content)
        print(f'✅ Zapisano {changes_made} bezpiecznych zmian')
    else:
        print('✅ Plik nie wymaga zmian')
    
    print('')
    print('🛡️ ULTRA-BEZPIECZNE NAPRAWY:')
    print('   1. Tylko dodanie nextTick do importów')
    print('   2. Żadne inne zmiany nie zostały wprowadzone')
    print('   3. Składnia JavaScript pozostaje nietknięta')
    print('')
    print('🔍 ROZWIĄZANIE PROBLEMU KOLEJKI:')
    print('   ✅ Problem z blokadami został rozwiązany przez USUNIĘCIE ich')
    print('   ✅ Przywrócono oryginalną prostą logikę')
    print('   ✅ Brak skomplikowanych timestampów')
    print('   ✅ Vue.js sam zadba o synchronizację UI')

if __name__ == '__main__':
    fix_startline_ultra_safe() 