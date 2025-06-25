#!/usr/bin/env python3
"""
Skrypt do debugowania stanu tabeli kolejki_startowe
"""

import sys
import os

# Dodaj backend do ścieżki Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.database import get_all, init_db_pool

def debug_queue():
    """Debuguje stan tabeli kolejki_startowe"""
    
    print("🔧 Inicjalizacja połączenia z bazą danych...")
    init_db_pool()
    
    print("📊 Sprawdzam zawartość tabeli kolejki_startowe:")
    kolejki = get_all("SELECT * FROM kolejki_startowe ORDER BY id")
    if kolejki:
        for k in kolejki:
            print(f"  ID: {k['id']}, Kategoria: {k['kategoria']}, Płeć: {k['plec']}, Nr: {k['nr_startowy']}, Pozycja: {k['pozycja']}")
    else:
        print("  ❌ Tabela kolejki_startowe jest pusta!")
    
    print("\n📊 Sprawdzam zawodników Junior A M:")
    zawodnicy = get_all("SELECT nr_startowy, imie, nazwisko FROM zawodnicy WHERE kategoria = %s AND plec = %s", ("Junior A", "M"))
    if zawodnicy:
        for z in zawodnicy:
            print(f"  Nr: {z['nr_startowy']}, {z['imie']} {z['nazwisko']}")
    else:
        print("  ❌ Brak zawodników Junior A M!")
    
    print("\n📊 Sprawdzam pełne zapytanie JOIN:")
    join_result = get_all("""
        SELECT z.nr_startowy, z.imie, z.nazwisko, z.kategoria, z.plec, z.klub, z.qr_code
        FROM kolejki_startowe k
        JOIN zawodnicy z ON k.nr_startowy = z.nr_startowy
        WHERE k.kategoria = %s AND k.plec = %s
        ORDER BY k.pozycja ASC
    """, ("Junior A", "M"))
    if join_result:
        for j in join_result:
            print(f"  Nr: {j['nr_startowy']}, {j['imie']} {j['nazwisko']}, Klub: {j['klub']}")
    else:
        print("  ❌ Brak wyników z JOIN!")

if __name__ == "__main__":
    debug_queue() 