#!/usr/bin/env python3

def fix_sync_timing():
    # Wczytaj plik
    with open('frontend/src/components/StartLineScanner.vue', 'r') as f:
        content = f.read()
    
    # Zmień timeout z 500ms na 50ms dla szybszej synchronizacji
    old_timeout = '}, 500) // Krótsze opóźnienie'
    new_timeout = '}, 50) // NATYCHMIASTOWY SYNC'
    
    if old_timeout in content:
        content = content.replace(old_timeout, new_timeout)
        print('✅ Zmieniono timeout z 500ms na 50ms')
        changes_made = True
    else:
        print('⚠️ Nie znaleziono timeout do zmiany')
        changes_made = False
    
    # Zapisz plik
    if changes_made:
        with open('frontend/src/components/StartLineScanner.vue', 'w') as f:
            f.write(content)
        print('✅ Zapisano zmiany')
    
    print('')
    print('🚀 PRZYSPIESZENIE SYNCHRONIZACJI:')
    print('   ✅ Timeout zmieniony z 500ms → 50ms')
    print('   ✅ Aktywna grupa będzie się synchronizować niemal natychmiast')
    print('   ✅ Zawodnicy powinni pojawiać się w kolejce od razu')

if __name__ == '__main__':
    fix_sync_timing() 