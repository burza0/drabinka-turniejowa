#!/usr/bin/env python3
"""
Skrypt do utworzenia tabeli kolejki_startowe w bazie danych
"""

import sys
import os

# Dodaj backend do ścieżki Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.database import execute_query, init_db_pool, get_all

def create_queue_table():
    """Tworzy tabelę kolejki_startowe w bazie danych"""
    
    print("🔧 Inicjalizacja połączenia z bazą danych...")
    init_db_pool()
    
    # Zapytanie do utworzenia tabeli
    create_table_query = """
    CREATE TABLE IF NOT EXISTS kolejki_startowe (
        id SERIAL PRIMARY KEY,
        kategoria VARCHAR(50) NOT NULL,
        plec VARCHAR(10) NOT NULL,
        nr_startowy INTEGER NOT NULL,
        pozycja INTEGER NOT NULL,
        UNIQUE(kategoria, plec, nr_startowy)
    );
    """
    
    # Zapytania do utworzenia indeksów
    create_indexes_queries = [
        "CREATE INDEX IF NOT EXISTS idx_kolejki_startowe_kategoria_plec ON kolejki_startowe(kategoria, plec);",
        "CREATE INDEX IF NOT EXISTS idx_kolejki_startowe_nr_startowy ON kolejki_startowe(nr_startowy);"
    ]
    
    try:
        print("📋 Tworzenie tabeli kolejki_startowe...")
        execute_query(create_table_query)
        print("✅ Tabela kolejki_startowe została utworzona")
        
        print("🔍 Tworzenie indeksów...")
        for query in create_indexes_queries:
            execute_query(query)
        print("✅ Indeksy zostały utworzone")
        
        # Sprawdzenie czy tabela została utworzona
        check_query = "SELECT COUNT(*) as count FROM information_schema.tables WHERE table_name = 'kolejki_startowe';"
        result = get_all(check_query)
        if result and len(result) > 0 and result[0]['count'] > 0:
            print("✅ Potwierdzenie: tabela kolejki_startowe istnieje w bazie danych")
        else:
            print("❌ Błąd: tabela kolejki_startowe nie została znaleziona")
            
    except Exception as e:
        print(f"❌ Błąd podczas tworzenia tabeli: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_queue_table()
    print("🎉 Migracja zakończona pomyślnie!") 