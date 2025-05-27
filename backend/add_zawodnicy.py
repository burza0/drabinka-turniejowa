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

# Najpierw dodajmy kolumnę płci do tabeli zawodnicy (jeśli nie istnieje)
try:
    cur.execute("ALTER TABLE zawodnicy ADD COLUMN plec VARCHAR(1)")
    print("✅ Dodano kolumnę 'plec' do tabeli zawodnicy")
except psycopg2.errors.DuplicateColumn:
    print("ℹ️ Kolumna 'plec' już istnieje")
    conn.rollback()

# Kategorie wiekowe
kategorie = ['U18', 'OPEN', 'MASTERS']

# Imiona męskie
imiona_meskie = [
    'Adam', 'Bartosz', 'Cezary', 'Damian', 'Emil', 'Filip', 'Grzegorz', 'Hubert',
    'Igor', 'Jakub', 'Kamil', 'Łukasz', 'Marcin', 'Norbert', 'Oskar', 'Paweł',
    'Rafał', 'Sebastian', 'Tomasz', 'Wojciech', 'Zbigniew', 'Artur', 'Krzysztof',
    'Michał', 'Piotr'
]

# Imiona żeńskie
imiona_zenskie = [
    'Anna', 'Barbara', 'Celina', 'Dorota', 'Ewa', 'Franciszka', 'Grażyna', 'Halina',
    'Irena', 'Joanna', 'Katarzyna', 'Lidia', 'Magdalena', 'Natalia', 'Olga', 'Paulina',
    'Renata', 'Sylwia', 'Teresa', 'Urszula', 'Weronika', 'Zofia', 'Agnieszka',
    'Monika', 'Beata'
]

# Nazwiska
nazwiska = [
    'Nowak', 'Kowalski', 'Wiśniewski', 'Dąbrowski', 'Lewandowski', 'Wójcik', 'Kamiński',
    'Kowalczyk', 'Zieliński', 'Szymański', 'Woźniak', 'Kozłowski', 'Jankowski', 'Mazur',
    'Krawczyk', 'Piotrowski', 'Grabowski', 'Nowakowski', 'Pawłowski', 'Michalski',
    'Adamczyk', 'Dudek', 'Zając', 'Wieczorek', 'Jabłoński', 'Król', 'Majewski',
    'Olszewski', 'Jaworski', 'Wróbel', 'Malinowski', 'Pawlak', 'Witkowski', 'Walczak',
    'Stępień', 'Górski', 'Rutkowski', 'Michalak', 'Sikora', 'Ostrowski', 'Baran',
    'Duda', 'Szewczyk', 'Tomaszewski', 'Pietrzak', 'Marciniak', 'Wróblewski', 'Zalewski',
    'Jakubowski', 'Jasiński'
]

# Sprawdź najwyższy numer startowy
cur.execute("SELECT MAX(nr_startowy) FROM zawodnicy")
max_nr = cur.fetchone()[0]
if max_nr is None:
    max_nr = 0

print(f"Rozpoczynam dodawanie zawodników od numeru {max_nr + 1}")

# Dodaj 25 mężczyzn
print("\n🚹 Dodaję 25 mężczyzn...")
for i in range(25):
    nr_startowy = max_nr + 1 + i
    imie = random.choice(imiona_meskie)
    nazwisko = random.choice(nazwiska)
    kategoria = random.choice(kategorie)
    plec = 'M'
    
    cur.execute("""
        INSERT INTO zawodnicy (nr_startowy, imie, nazwisko, kategoria, plec) 
        VALUES (%s, %s, %s, %s, %s)
    """, (nr_startowy, imie, nazwisko, kategoria, plec))
    
    print(f"  {nr_startowy:3d}. {imie} {nazwisko} ({kategoria})")

# Dodaj 25 kobiet
print("\n🚺 Dodaję 25 kobiet...")
for i in range(25):
    nr_startowy = max_nr + 26 + i
    imie = random.choice(imiona_zenskie)
    nazwisko = random.choice(nazwiska)
    kategoria = random.choice(kategorie)
    plec = 'K'
    
    cur.execute("""
        INSERT INTO zawodnicy (nr_startowy, imie, nazwisko, kategoria, plec) 
        VALUES (%s, %s, %s, %s, %s)
    """, (nr_startowy, imie, nazwisko, kategoria, plec))
    
    print(f"  {nr_startowy:3d}. {imie} {nazwisko} ({kategoria})")

# Zatwierdź zmiany
conn.commit()

# Pokaż statystyki
print("\n📊 Statystyki zawodników:")
cur.execute("""
    SELECT kategoria, plec, COUNT(*) 
    FROM zawodnicy 
    GROUP BY kategoria, plec 
    ORDER BY kategoria, plec
""")
stats = cur.fetchall()

for kategoria, plec, count in stats:
    plec_nazwa = "Mężczyźni" if plec == 'M' else "Kobiety"
    print(f"  {kategoria}: {plec_nazwa} - {count}")

cur.execute("SELECT COUNT(*) FROM zawodnicy")
total = cur.fetchone()[0]
print(f"\n✅ Łącznie zawodników w bazie: {total}")

# Zamknij połączenie
cur.close()
conn.close()

print("\n🎉 Dodawanie zawodników zakończone pomyślnie!") 