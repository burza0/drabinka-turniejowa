#!/usr/bin/env python3
import re
import os

def remove_dialogs_from_file(filepath):
    """Usuwa wszystkie dialogi z konkretnego pliku"""
    if not os.path.exists(filepath):
        print(f'⚠️ Plik {filepath} nie istnieje')
        return 0
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    changes_made = 0
    
    # 1. Usuń wszystkie linie z confirm() - zastąp return true
    confirm_lines = re.findall(r'.*if \(!confirm\([^)]*\)\).*\n', content)
    if confirm_lines:
        content = re.sub(r'\s*if \(!confirm\([^)]*\)\).*\n', '', content)
        changes_made += len(confirm_lines)
        print(f'  ✅ Usunięto {len(confirm_lines)} confirm() dialogów')
    
    # 2. Usuń samodzielne confirm() (bez if)
    standalone_confirm = re.findall(r'.*const confirmed = confirm\([^)]*\).*\n', content)
    if standalone_confirm:
        content = re.sub(r'\s*const confirmed = confirm\([^)]*\).*\n', '', content)
        changes_made += len(standalone_confirm)
        print(f'  ✅ Usunięto {len(standalone_confirm)} standalone confirm()')
    
    # 3. Usuń definicje confirmMessage
    confirm_msg_lines = re.findall(r'.*const confirmMessage = .*\n', content)
    if confirm_msg_lines:
        content = re.sub(r'\s*const confirmMessage = .*\n', '', content)
        changes_made += len(confirm_msg_lines)
        print(f'  ✅ Usunięto {len(confirm_msg_lines)} confirmMessage definicji')
    
    # 4. Usuń wszystkie wywołania alert()
    alert_calls = re.findall(r'\s*alert\([^)]*\)\s*\n', content)
    if alert_calls:
        content = re.sub(r'\s*alert\([^)]*\)\s*\n', '', content)
        changes_made += len(alert_calls)
        print(f'  ✅ Usunięto {len(alert_calls)} wywołań alert()')
    
    # 5. Usuń całe funkcje showSuccess i showError z alert()
    showSuccess_def = re.search(r'const showSuccess = \(message: string\) => \{[^}]*\}', content)
    if showSuccess_def:
        content = content.replace(showSuccess_def.group(0), '')
        changes_made += 1
        print('  ✅ Usunięto funkcję showSuccess')
    
    showError_def = re.search(r'const showError = \(message: string\) => \{[^}]*\}', content)
    if showError_def:
        content = content.replace(showError_def.group(0), '')
        changes_made += 1
        print('  ✅ Usunięto funkcję showError')
    
    # 6. Usuń wszystkie pozostałe wywołania showSuccess i showError
    showSuccess_calls = re.findall(r'\s*showSuccess\([^)]*\)\s*\n', content)
    if showSuccess_calls:
        content = re.sub(r'\s*showSuccess\([^)]*\)\s*\n', '', content)
        changes_made += len(showSuccess_calls)
        print(f'  ✅ Usunięto {len(showSuccess_calls)} wywołań showSuccess()')
    
    showError_calls = re.findall(r'\s*showError\([^)]*\)\s*\n', content)
    if showError_calls:
        content = re.sub(r'\s*showError\([^)]*\)\s*\n', '', content)
        changes_made += len(showError_calls)
        print(f'  ✅ Usunięto {len(showError_calls)} wywołań showError()')
    
    # Zapisz plik tylko jeśli były zmiany
    if changes_made > 0:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f'  📁 Zapisano {changes_made} zmian w {filepath}')
    
    return changes_made

def remove_all_dialogs():
    files_to_clean = [
        'frontend/src/components/StartLineScanner.vue',
        'frontend/src/components/EditZawodnikModal.vue', 
        'frontend/src/components/QrAdminDashboard.vue'
    ]
    
    total_changes = 0
    
    print('🔇 USUWANIE WSZYSTKICH DIALOGÓW I POWIADOMIEŃ...\n')
    
    for filepath in files_to_clean:
        print(f'📁 Czyszczę {filepath}:')
        changes = remove_dialogs_from_file(filepath)
        total_changes += changes
        if changes == 0:
            print('  ⚠️ Brak dialogów do usunięcia')
        print('')
    
    print('=' * 50)
    print(f'✅ UKOŃCZONO! Usunięto łącznie {total_changes} dialogów/powiadomień')
    print('')
    print('🔇 APLIKACJA JEST TERAZ CAŁKOWICIE CICHA:')
    print('   ✅ Brak confirm() dialogów')
    print('   ✅ Brak alert() popup')
    print('   ✅ Brak showSuccess() powiadomień')
    print('   ✅ Brak showError() powiadomień')
    print('   ✅ Wszystkie operacje wykonują się bez pytania!')

if __name__ == '__main__':
    remove_all_dialogs() 