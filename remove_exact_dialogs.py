#!/usr/bin/env python3

def remove_exact_dialogs():
    """Usuwa dokładnie te linie z dialogami"""
    
    with open('frontend/src/components/StartLineScanner.vue', 'r') as f:
        lines = f.readlines()
    
    print('🔧 USUWANIE DOKŁADNYCH LINII Z DIALOGAMI...')
    
    # Linie do usunięcia (numer linii -> oczekiwany fragment)
    lines_to_remove = {
        487: "showSuccess(`✅ Aktywowano grupę: ${grupa.nazwa}`)",
        494: "showError(`Błąd aktywacji: ${error.message}`)",
        531: "showSuccess('🧹 Wyczyszczono aktywną grupę')",
        539: "showError(`Błąd: ${error.message}`)",
        681: "const confirmMessage = `Czy na pewno chcesz usunąć zawodnika #${zawodnik.nr_startowy} ${zawodnik.imie} ${zawodnik.nazwisko} z kolejki?`",
        682: "if (!confirm(confirmMessage)) return",
        709: "showSuccess(`Usunięto zawodnika #${zawodnik.nr_startowy} z kolejki`)",
        718: "showError(`Błąd: ${error.message}`)",
        727: "const confirmMessage = type === 'all'",
        728: "if (!confirm(confirmMessage)) return",
        740: "showSuccess(`Wyczyszczono kolejkę: ${type}`)",
        746: "showError(`Błąd: ${error.message}`)"
    }
    
    new_lines = []
    removed_count = 0
    
    for i, line in enumerate(lines, 1):
        if i in lines_to_remove:
            expected = lines_to_remove[i]
            if expected in line.strip():
                print(f'  ❌ Usuwam linię {i}: {line.strip()[:60]}...')
                removed_count += 1
                continue
            else:
                print(f'  ⚠️ Linia {i} nie pasuje do oczekiwanej: {line.strip()[:40]}...')
        
        new_lines.append(line)
    
    # Zapisz
    with open('frontend/src/components/StartLineScanner.vue', 'w') as f:
        f.writelines(new_lines)
    
    print('')
    print(f'✅ USUNIĘTO {removed_count} LINII Z DIALOGAMI!')
    print('   🔇 Aplikacja jest teraz cicha')

if __name__ == '__main__':
    remove_exact_dialogs() 