#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
import os
from dotenv import load_dotenv

# Załaduj zmienne środowiskowe
load_dotenv()

# Połączenie z bazą danych
DB_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

print('📊 SZCZEGÓŁOWE STATYSTYKI KOŃCOWE:')
print()

# Łączna liczba zawodników
cur.execute('SELECT COUNT(*) FROM zawodnicy')
total = cur.fetchone()[0]
print(f'Łączna liczba zawodników: {total}')
print()

# Podział płci
cur.execute('SELECT plec, COUNT(*) FROM zawodnicy GROUP BY plec ORDER BY plec')
plcie = cur.fetchall()
print('Podział płci:')
for p, l in plcie:
    nazwa = "Kobiety" if p == "K" else "Mężczyźni"
    print(f'  {nazwa}: {l} ({l/total*100:.1f}%)')
print()

# Podział według kategorii i płci
cur.execute('SELECT kategoria, plec, COUNT(*) FROM zawodnicy GROUP BY kategoria, plec ORDER BY kategoria, plec')
stats = cur.fetchall()
print('Podział według kategorii i płci:')
for k, p, l in stats:
    nazwa = "Kobiety" if p == "K" else "Mężczyźni"
    print(f'  {k}: {nazwa} - {l}')
print()

# Podział według statusów
cur.execute('SELECT w.status, COUNT(*) FROM wyniki w GROUP BY w.status ORDER BY w.status')
statusy = cur.fetchall()
print('Podział według statusów:')
for s, l in statusy:
    print(f'  {s}: {l} ({l/total*100:.1f}%)')
print()

# Sprawdź czy wszystkie zawodnicy mają wyniki
cur.execute('SELECT COUNT(*) FROM zawodnicy z LEFT JOIN wyniki w ON z.nr_startowy = w.nr_startowy WHERE w.nr_startowy IS NULL')
bez_wynikow = cur.fetchone()[0]
if bez_wynikow > 0:
    print(f'⚠️  Zawodnicy bez wyników: {bez_wynikow}')
else:
    print('✅ Wszyscy zawodnicy mają wyniki')

print()
print('🎉 Baza danych gotowa do użycia!')

# Zamknij połączenie
cur.close()
conn.close() 