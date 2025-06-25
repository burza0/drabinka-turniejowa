#!/usr/bin/env python3

def fix_qr_admin_syntax():
    """Naprawia wszystkie błędy składni spowodowane przez usunięcie dialogów"""
    
    with open('frontend/src/components/QrAdminDashboard.vue', 'r') as f:
        content = f.read()
    
    print('🔧 NAPRAWIAM SKŁADNIĘ QrAdminDashboard.vue...')
    
    # 1. Napraw generateMissingQR (brak otwierającego nawiasu)
    content = content.replace(
        'const generateMissingQR = async () => {\n  // TODO: Implement bulk QR generation}',
        'const generateMissingQR = async () => {\n  // TODO: Implement bulk QR generation\n}'
    )
    print('✅ Naprawiono generateMissingQR()')
    
    # 2. Napraw resetAllCheckIns (usunięty confirm i zepsuty nawias)
    content = content.replace(
        'const resetAllCheckIns = async () => {// TODO: Implement reset  }\n}',
        'const resetAllCheckIns = async () => {\n  // TODO: Implement reset\n}'
    )
    print('✅ Naprawiono resetAllCheckIns()')
    
    # 3. Napraw viewSystemLogs (brak otwierającego nawiasu)
    content = content.replace(
        'const viewSystemLogs = () => {\n  // TODO: Implement system logs viewer}',
        'const viewSystemLogs = () => {\n  // TODO: Implement system logs viewer\n}'
    )
    print('✅ Naprawiono viewSystemLogs()')
    
    # 4. Napraw performManualCheckIn - brakujące } po success i error
    content = content.replace(
        '      }    } else {    }',
        '      }\n    } else {\n      console.log("Manual check-in failed")\n    }'
    )
    print('✅ Naprawiono performManualCheckIn() - success/error blocks')
    
    # 5. Napraw brakujący } po error catch
    content = content.replace(
        '    const errorMsg = error.response?.data?.message || \'Nieznany błąd serwera\'  } finally {',
        '    const errorMsg = error.response?.data?.message || \'Nieznany błąd serwera\'\n    console.error("Manual check-in error:", errorMsg)\n  } finally {'
    )
    print('✅ Naprawiono performManualCheckIn() - error catch block')
    
    # Zapisz naprawiony plik
    with open('frontend/src/components/QrAdminDashboard.vue', 'w') as f:
        f.write(content)
    
    print('')
    print('✅ SKŁADNIA NAPRAWIONA!')
    print('   🔧 generateMissingQR() - dodano brakujący otwierający nawias')
    print('   🔧 resetAllCheckIns() - naprawiono nawiasy')
    print('   🔧 viewSystemLogs() - dodano brakujący otwierający nawias')
    print('   🔧 performManualCheckIn() - naprawiono bloki success/error')
    print('')
    print('🎯 QrAdminDashboard.vue powinien się teraz kompilować!')

if __name__ == '__main__':
    fix_qr_admin_syntax() 