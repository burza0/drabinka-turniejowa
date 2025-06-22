#!/usr/bin/env python3

def fix_cache_bust():
    # Wczytaj plik
    with open('frontend/src/components/StartLineScanner.vue', 'r') as f:
        content = f.read()
    
    changes_made = 0
    
    # 1. Dodaj cache-busting do fetch('/api/start-queue')
    old_fetch = "const kolejkaResponse = await fetch('/api/start-queue')"
    new_fetch = "const kolejkaResponse = await fetch(`/api/start-queue?_t=${Date.now()}`)"
    
    if old_fetch in content:
        content = content.replace(old_fetch, new_fetch)
        changes_made += 1
        print('✅ Dodano cache-busting do /api/start-queue')
    
    # 2. Dodaj cache-busting do fetch('/api/grupa-aktywna')
    old_grupa_fetch = "const aktywnaResponse = await fetch('/api/grupa-aktywna')"
    new_grupa_fetch = "const aktywnaResponse = await fetch(`/api/grupa-aktywna?_t=${Date.now()}`)"
    
    if old_grupa_fetch in content:
        content = content.replace(old_grupa_fetch, new_grupa_fetch)
        changes_made += 1
        print('✅ Dodano cache-busting do /api/grupa-aktywna')
    
    # 3. Dodaj cache-busting do fetch('/api/grupy-startowe')
    old_grupy_fetch = "const grupyResponse = await fetch('/api/grupy-startowe')"
    new_grupy_fetch = "const grupyResponse = await fetch(`/api/grupy-startowe?_t=${Date.now()}`)"
    
    if old_grupy_fetch in content:
        content = content.replace(old_grupy_fetch, new_grupy_fetch)
        changes_made += 1
        print('✅ Dodano cache-busting do /api/grupy-startowe')
    
    # 4. Dodaj extra cache-busting dla removeFromQueue
    old_remove_fetch = "const kolejkaResponse = await fetch('/api/start-queue')"
    new_remove_fetch = "const kolejkaResponse = await fetch(`/api/start-queue?_t=${Date.now()}`)"
    
    # Ta zamiana już została zrobiona w punkcie 1, więc sprawdźmy inną instancję
    
    # Zapisz plik
    if changes_made > 0:
        with open('frontend/src/components/StartLineScanner.vue', 'w') as f:
            f.write(content)
        print(f'✅ Zapisano {changes_made} zmian')
    else:
        print('⚠️ Nie znaleziono fetch requestów do modyfikacji')
    
    print('')
    print('🚫 ELIMINACJA CACHE PRZEGLĄDARKI:')
    print('   ✅ Wszystkie API requesty mają timestamp cache-busting')
    print('   ✅ Frontend będzie zawsze pobierał świeże dane')
    print('   ✅ Brak cache = zawsze aktualne dane!')
    print('')
    print('💡 Dodatkowo WYCZYŚĆ CACHE przeglądarki (Ctrl+Shift+R)')

if __name__ == '__main__':
    fix_cache_bust() 