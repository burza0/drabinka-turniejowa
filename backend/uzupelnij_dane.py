#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
import os
from dotenv import load_dotenv
import random

load_dotenv()

# Połączenie z bazą danych
DB_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

print("🔧 Uzupełnianie danych...")

# 1. Uzupełnij płeć dla zawodników 1-4
print("\n👥 Uzupełnianie płci dla zawodników 1-4...")

# Sprawdź istniejących zawodników 1-4
cur.execute("SELECT nr_startowy, imie, nazwisko FROM zawodnicy WHERE nr_startowy BETWEEN 1 AND 4 ORDER BY nr_startowy")
zawodnicy_1_4 = cur.fetchall()

for nr_startowy, imie, nazwisko in zawodnicy_1_4:
    # Określ płeć na podstawie imienia (proste heurystyki)
    imiona_meskie = ['Adam', 'Bartosz', 'Cezary', 'Damian', 'Emil', 'Filip', 'Grzegorz', 'Hubert',
                     'Igor', 'Jakub', 'Kamil', 'Łukasz', 'Marcin', 'Norbert', 'Oskar', 'Paweł',
                     'Rafał', 'Sebastian', 'Tomasz', 'Wojciech', 'Zbigniew', 'Artur', 'Krzysztof',
                     'Michał', 'Piotr', 'Jan', 'Andrzej', 'Marek', 'Robert', 'Stanisław']
    
    if imie in imiona_meskie:
        plec = 'M'
    else:
        plec = 'K'
    
    cur.execute("UPDATE zawodnicy SET plec = %s WHERE nr_startowy = %s", (plec, nr_startowy))
    print(f"  {nr_startowy}. {imie} {nazwisko} -> płeć: {'Mężczyzna' if plec == 'M' else 'Kobieta'}")

# 2. Wygeneruj wyniki dla wszystkich zawodników
print("\n🏁 Generowanie wyników dla wszystkich zawodników...")

# Pobierz wszystkich zawodników
cur.execute("SELECT nr_startowy, imie, nazwisko, kategoria FROM zawodnicy ORDER BY nr_startowy")
wszyscy_zawodnicy = cur.fetchall()

# Usuń istniejące wyniki (jeśli są)
cur.execute("DELETE FROM wyniki")
print("  Usunięto poprzednie wyniki")

# Generuj czasy w zależności od kategorii
czasy_bazowe = {
    'U18': (45.0, 65.0),      # młodzież: 45-65 sekund
    'OPEN': (40.0, 55.0),     # dorośli: 40-55 sekund  
    'MASTERS': (50.0, 70.0)   # masters: 50-70 sekund
}

statusy = ['FINISHED', 'FINISHED', 'FINISHED', 'FINISHED', 'FINISHED', 'DNF', 'DSQ']  # 5/7 kończy

for nr_startowy, imie, nazwisko, kategoria in wszyscy_zawodnicy:
    status = random.choice(statusy)
    
    if status == 'FINISHED':
        # Wygeneruj realistyczny czas
        min_czas, max_czas = czasy_bazowe.get(kategoria, (45.0, 65.0))
        czas = round(random.uniform(min_czas, max_czas), 2)
        czas_str = f"{czas:.2f}"
    else:
        czas_str = None
    
    cur.execute("""
        INSERT INTO wyniki (nr_startowy, czas_przejazdu_s, status) 
        VALUES (%s, %s, %s)
    """, (nr_startowy, czas_str, status))
    
    if status == 'FINISHED':
        print(f"  {nr_startowy:3d}. {imie} {nazwisko} ({kategoria}) -> {czas_str}s")
    else:
        print(f"  {nr_startowy:3d}. {imie} {nazwisko} ({kategoria}) -> {status}")

# Zatwierdź zmiany
conn.commit()

# Pokaż statystyki
print("\n📊 Statystyki wyników:")
cur.execute("SELECT status, COUNT(*) FROM wyniki GROUP BY status ORDER BY status")
stats_wyniki = cur.fetchall()

for status, count in stats_wyniki:
    print(f"  {status}: {count} zawodników")

cur.execute("SELECT COUNT(*) FROM wyniki WHERE status = 'FINISHED'")
finished_count = cur.fetchone()[0]

if finished_count > 0:
    cur.execute("""
        SELECT MIN(CAST(czas_przejazdu_s AS FLOAT)), 
               MAX(CAST(czas_przejazdu_s AS FLOAT)),
               AVG(CAST(czas_przejazdu_s AS FLOAT))
        FROM wyniki 
        WHERE status = 'FINISHED'
    """)
    min_czas, max_czas, avg_czas = cur.fetchone()
    print(f"\n⏱️  Czasy (tylko ukończeni):")
    print(f"  Najlepszy: {min_czas:.2f}s")
    print(f"  Najgorszy: {max_czas:.2f}s") 
    print(f"  Średni: {avg_czas:.2f}s")

# Pokaż top 5 wyników
print(f"\n🏆 TOP 5 wyników:")
cur.execute("""
    SELECT w.nr_startowy, z.imie, z.nazwisko, z.kategoria, z.plec, w.czas_przejazdu_s
    FROM wyniki w
    JOIN zawodnicy z ON w.nr_startowy = z.nr_startowy
    WHERE w.status = 'FINISHED'
    ORDER BY CAST(w.czas_przejazdu_s AS FLOAT) ASC
    LIMIT 5
""")
top_wyniki = cur.fetchall()

for i, (nr, imie, nazwisko, kategoria, plec, czas) in enumerate(top_wyniki, 1):
    plec_symbol = "🚹" if plec == 'M' else "🚺"
    print(f"  {i}. {plec_symbol} {imie} {nazwisko} ({kategoria}) - {czas}s")

# Zamknij połączenie
cur.close()
conn.close()

print("\n✅ Uzupełnianie danych zakończone pomyślnie!") 