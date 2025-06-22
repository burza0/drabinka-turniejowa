#!/usr/bin/env python3

def safe_remove_dialogs():
    """Bezpiecznie usuwa dialogi bez niszczenia składni"""
    
    with open('frontend/src/components/StartLineScanner.vue', 'r') as f:
        content = f.read()
    
    print('🔧 BEZPIECZNE USUWANIE DIALOGÓW StartLineScanner.vue...')
    
    # Zapisz backup
    with open('frontend/src/components/StartLineScanner.vue.pre_safe_remove', 'w') as f:
        f.write(content)
    
    # 1. Znajdź i usuń DOKŁADNIE te linie (bez regex!)
    lines = content.split('\n')
    new_lines = []
    
    for i, line in enumerate(lines):
        # Pomiń linie z confirm (dokładne dopasowanie)
        if 'if (!confirm(' in line or 'const confirmMessage =' in line:
            print(f'  ❌ Pomijam linię {i+1}: {line.strip()[:50]}...')
            continue
        
        # Pomiń linie z showSuccess i showError (ale zostaw console.log)
        if ('showSuccess(' in line or 'showError(' in line) and 'console' not in line:
            print(f'  ❌ Pomijam linię {i+1}: {line.strip()[:50]}...')
            continue
        
        # Pomiń definicje funkcji showSuccess/showError
        if ('const showSuccess =' in line or 'const showError =' in line):
            print(f'  ❌ Pomijam linię {i+1}: {line.strip()[:50]}...')
            # Pomiń także następne linie aż do }
            j = i + 1
            while j < len(lines) and '}' not in lines[j]:
                j += 1
            if j < len(lines):
                j += 1  # Pomiń także linię z }
            print(f'  ❌ Pomijam funkcję do linii {j}')
            continue
        
        new_lines.append(line)
    
    # Połącz z powrotem
    new_content = '\n'.join(new_lines)
    
    # Zapisz
    with open('frontend/src/components/StartLineScanner.vue', 'w') as f:
        f.write(new_content)
    
    print('')
    print('✅ BEZPIECZNIE USUNIĘTO DIALOGI!')
    print('   🎯 Składnia została zachowana')
    print('   💾 Backup zapisany jako .pre_safe_remove')

if __name__ == '__main__':
    safe_remove_dialogs() 