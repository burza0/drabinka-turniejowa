#!/usr/bin/env python3

def remove_all_dialogs():
    # Wczytaj plik
    with open('frontend/src/components/StartLineScanner.vue', 'r') as f:
        content = f.read()
    
    changes_made = 0
    
    # 1. Usuń wszystkie linie z confirm()
    import re
    
    # Usuń linie z confirm() - zastąp return true
    confirm_lines = re.findall(r'.*if \(!confirm\([^)]*\)\) return.*\n', content)
    if confirm_lines:
        content = re.sub(r'\s*if \(!confirm\([^)]*\)\) return.*\n', '', content)
        changes_made += len(confirm_lines)
        print(f'✅ Usunięto {len(confirm_lines)} confirm() dialogów')
    
    # 2. Usuń definicje confirmMessage
    confirm_msg_lines = re.findall(r'.*const confirmMessage = .*\n', content)
    if confirm_msg_lines:
        content = re.sub(r'\s*const confirmMessage = .*\n', '', content)
        changes_made += len(confirm_msg_lines)
        print(f'✅ Usunięto {len(confirm_msg_lines)} confirmMessage definicji')
    
    # 3. Usuń całe funkcje showSuccess i showError z alert()
    showSuccess_def = re.search(r'const showSuccess = \(message: string\) => \{[^}]*\}', content)
    if showSuccess_def:
        content = content.replace(showSuccess_def.group(0), '')
        changes_made += 1
        print('✅ Usunięto funkcję showSuccess z alert()')
    
    showError_def = re.search(r'const showError = \(message: string\) => \{[^}]*\}', content)
    if showError_def:
        content = content.replace(showError_def.group(0), '')
        changes_made += 1
        print('✅ Usunięto funkcję showError z alert()')
    
    # 4. Usuń wszystkie pozostałe wywołania showSuccess i showError
    showSuccess_calls = re.findall(r'\s*showSuccess\([^)]*\)\s*\n', content)
    if showSuccess_calls:
        content = re.sub(r'\s*showSuccess\([^)]*\)\s*\n', '', content)
        changes_made += len(showSuccess_calls)
        print(f'✅ Usunięto {len(showSuccess_calls)} wywołań showSuccess()')
    
    showError_calls = re.findall(r'\s*showError\([^)]*\)\s*\n', content)
    if showError_calls:
        content = re.sub(r'\s*showError\([^)]*\)\s*\n', '', content)
        changes_made += len(showError_calls)
        print(f'✅ Usunięto {len(showError_calls)} wywołań showError()')
    
    # 5. Usuń pojedyncze wywołania alert()
    alert_calls = re.findall(r'\s*alert\([^)]*\)\s*\n', content)
    if alert_calls:
        content = re.sub(r'\s*alert\([^)]*\)\s*\n', '', content)
        changes_made += len(alert_calls)
        print(f'✅ Usunięto {len(alert_calls)} wywołań alert()')
    
    # Zapisz plik
    if changes_made > 0:
        with open('frontend/src/components/StartLineScanner.vue', 'w') as f:
            f.write(content)
        print(f'✅ Zapisano {changes_made} zmian')
    else:
        print('⚠️ Nie znaleziono dialogów do usunięcia')
    
    print('')
    print('🔇 USUNIĘTO WSZYSTKIE DIALOGI I POWIADOMIENIA:')
    print('   ✅ Brak confirm() dialogów')
    print('   ✅ Brak alert() popup')
    print('   ✅ Brak showSuccess()')
    print('   ✅ Brak showError()')
    print('   ✅ CAŁKOWICIE CICHA APLIKACJA!')

if __name__ == '__main__':
    remove_all_dialogs() 