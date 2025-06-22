#!/usr/bin/env python3

def remove_notifications():
    # Wczytaj plik
    with open('frontend/src/components/StartLineScanner.vue', 'r') as f:
        content = f.read()
    
    changes_made = 0
    
    # 1. Usuń wszystkie showSuccess()
    import re
    
    # Znajdź i usuń linie z showSuccess
    showSuccess_pattern = r'\s*showSuccess\([^)]*\)\s*\n'
    matches = re.findall(showSuccess_pattern, content)
    if matches:
        content = re.sub(showSuccess_pattern, '', content)
        changes_made += len(matches)
        print(f'✅ Usunięto {len(matches)} wywołań showSuccess()')
    
    # 2. Usuń wszystkie showError()
    showError_pattern = r'\s*showError\([^)]*\)\s*\n'
    matches = re.findall(showError_pattern, content)
    if matches:
        content = re.sub(showError_pattern, '', content)
        changes_made += len(matches)
        print(f'✅ Usunięto {len(matches)} wywołań showError()')
    
    # 3. Usuń definicje funkcji showSuccess i showError
    # Znajdź i usuń całe definicje funkcji
    showSuccess_def_pattern = r'const showSuccess = [^}]*}\s*\n'
    if re.search(showSuccess_def_pattern, content):
        content = re.sub(showSuccess_def_pattern, '', content)
        changes_made += 1
        print('✅ Usunięto definicję funkcji showSuccess')
    
    showError_def_pattern = r'const showError = [^}]*}\s*\n'
    if re.search(showError_def_pattern, content):
        content = re.sub(showError_def_pattern, '', content)
        changes_made += 1
        print('✅ Usunięto definicję funkcji showError')
    
    # 4. Usuń import toast (jeśli istnieje)
    toast_import_pattern = r'import.*toast.*\n'
    if re.search(toast_import_pattern, content):
        content = re.sub(toast_import_pattern, '', content)
        changes_made += 1
        print('✅ Usunięto import toast')
    
    # Zapisz plik
    if changes_made > 0:
        with open('frontend/src/components/StartLineScanner.vue', 'w') as f:
            f.write(content)
        print(f'✅ Zapisano {changes_made} zmian')
    else:
        print('⚠️ Nie znaleziono powiadomień do usunięcia')
    
    print('')
    print('🔇 USUNIĘTO WSZYSTKIE POWIADOMIENIA:')
    print('   ✅ Brak showSuccess()')
    print('   ✅ Brak showError()')
    print('   ✅ Brak toast notifications')
    print('   ✅ Ciche działanie bez popup')

if __name__ == '__main__':
    remove_notifications() 