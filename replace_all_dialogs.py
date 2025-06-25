#!/usr/bin/env python3

def replace_all_dialogs():
    """Zamienia wszystkie dialogi na console.log bez usuwania linii"""
    
    with open('frontend/src/components/StartLineScanner.vue', 'r') as f:
        content = f.read()
    
    print('🔧 ZAMIENIANIE WSZYSTKICH DIALOGÓW NA console.log...')
    
    # 1. Zamień wszystkie confirm() na true
    import re
    confirms = re.findall(r'if \(!confirm\([^)]*\)\) return', content)
    for confirm in confirms:
        content = content.replace(confirm, '// if (!confirm(...)) return  // USUNIĘTO DIALOG')
        print(f'  ✅ Zastąpiono: {confirm[:50]}...')
    
    # 2. Zamień wszystkie const confirmMessage na komentarz
    conf_msgs = re.findall(r'const confirmMessage = [^`]*`[^`]*`', content)
    for msg in conf_msgs:
        content = content.replace(msg, '// ' + msg + '  // USUNIĘTO DIALOG')
        print(f'  ✅ Zastąpiono: {msg[:50]}...')
    
    # 3. Zamień wszystkie showSuccess() na console.log
    show_success = re.findall(r'showSuccess\([^)]*\)', content)
    for success in show_success:
        new_call = success.replace('showSuccess', 'console.log')
        content = content.replace(success, new_call)
        print(f'  ✅ Zastąpiono: {success} -> {new_call}')
    
    # 4. Zamień wszystkie showError() na console.error
    show_errors = re.findall(r'showError\([^)]*\)', content)
    for error in show_errors:
        new_call = error.replace('showError', 'console.error')
        content = content.replace(error, new_call)
        print(f'  ✅ Zastąpiono: {error} -> {new_call}')
    
    # Zapisz
    with open('frontend/src/components/StartLineScanner.vue', 'w') as f:
        f.write(content)
    
    print('')
    print('✅ WSZYSTKIE DIALOGI ZASTĄPIONE!')
    print('   🔇 confirm() -> // komentarz (zawsze true)')
    print('   🔇 showSuccess() -> console.log()')
    print('   🔇 showError() -> console.error()')
    print('   🎯 Aplikacja jest teraz cicha!')

if __name__ == '__main__':
    replace_all_dialogs() 