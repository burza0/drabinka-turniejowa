#!/usr/bin/env python3

def fix_edit_zawodnik_syntax():
    """Naprawia błąd składni w EditZawodnikModal.vue"""
    
    with open('frontend/src/components/EditZawodnikModal.vue', 'r') as f:
        content = f.read()
    
    print('🔧 NAPRAWIAM SKŁADNIĘ EditZawodnikModal.vue...')
    
    # Usuń pozostały fragment z confirmed
    content = content.replace(
        'if (!originalData.value) return  if (!confirmed) return',
        'if (!originalData.value) return'
    )
    print('✅ Usunięto pozostały fragment "if (!confirmed) return"')
    
    # Zapisz naprawiony plik
    with open('frontend/src/components/EditZawodnikModal.vue', 'w') as f:
        f.write(content)
    
    print('')
    print('✅ SKŁADNIA EditZawodnikModal.vue NAPRAWIONA!')
    print('🎯 Plik powinien się teraz kompilować!')

if __name__ == '__main__':
    fix_edit_zawodnik_syntax() 