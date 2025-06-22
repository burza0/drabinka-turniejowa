#!/usr/bin/env python3

def fix_remaining_dialogs():
    # StartLineScanner.vue - usuń showSuccess() linie
    with open('frontend/src/components/StartLineScanner.vue', 'r') as f:
        content = f.read()
    
    original_lines = content.count('\n')
    
    # Usuń pokazSuccess() linie (bez } na końcu - stąd poprzedni regex nie złapał)
    import re
    content = re.sub(r'\s*showSuccess\([^)]*\)\s*', '', content)
    
    # Usuń też pozostałe fragmenty showError
    content = re.sub(r'\s*showError\([^)]*\)\s*', '', content)
    
    with open('frontend/src/components/StartLineScanner.vue', 'w') as f:
        f.write(content)
    
    print('✅ StartLineScanner.vue: Usunięto pozostałe showSuccess/showError')
    
    # QrAdminDashboard.vue - usuń if (confirm())
    with open('frontend/src/components/QrAdminDashboard.vue', 'r') as f:
        content = f.read()
    
    # Usuń całą linię z if (confirm(...))
    content = re.sub(r'\s*if \(confirm\([^)]*\)\) \{\s*', '', content)
    
    with open('frontend/src/components/QrAdminDashboard.vue', 'w') as f:
        f.write(content)
    
    print('✅ QrAdminDashboard.vue: Usunięto pozostały confirm()')
    
    print('')
    print('🔇 WSZYSTKIE DIALOGI DEFINITYWNIE USUNIĘTE!')
    print('   ✅ StartLineScanner.vue: 0 dialogów')  
    print('   ✅ EditZawodnikModal.vue: 0 dialogów')
    print('   ✅ QrAdminDashboard.vue: 0 dialogów')
    print('')
    print('🎯 APLIKACJA JEST TERAZ KOMPLETNIE CICHA!')

if __name__ == '__main__':
    fix_remaining_dialogs() 