#!/usr/bin/env python3

def fix_backend_imports():
    """USUWA NIEPOTRZEBNE IMPORTY z backend/api_server.py"""
    
    with open('backend/api_server.py', 'r') as f:
        content = f.read()
    
    print('🔧 USUWAM NIEPOTRZEBNE IMPORTY BACKEND...')
    
    # Usuń niepotrzebne importy
    lines_to_remove = [
        'from cache import app_cache\n',
        'from api_endpoints_new import new_queue_api\n'
    ]
    
    for line in lines_to_remove:
        if line in content:
            content = content.replace(line, '')
            print(f'✅ Usunięto import: {line.strip()}')
    
    # Usuń registrację blueprint
    blueprint_line = 'app.register_blueprint(new_queue_api)\n'
    if blueprint_line in content:
        content = content.replace(blueprint_line, '')
        print('✅ Usunięto rejestrację blueprint new_queue_api')
    
    # Zapisz naprawiony plik
    with open('backend/api_server.py', 'w') as f:
        f.write(content)
    
    print('')
    print('✅ NIEPOTRZEBNE IMPORTY USUNIĘTE!')
    print('🎯 Backend powinien się teraz uruchamiać bez ModuleNotFoundError')

if __name__ == '__main__':
    fix_backend_imports() 