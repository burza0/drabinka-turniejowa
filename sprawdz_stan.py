#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
import os
from dotenv import load_dotenv

# Załaduj zmienne środowiskowe
load_dotenv()

# Połączenie z bazą danych
DB_URL = os.getenv('DATABASE_URL')

def sprawdz_stan():
    """Sprawdza aktualny stan bazy danych"""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    print("📊 AKTUALNY STAN BAZY DANYCH")
    print("=" * 40)
    
    # Łączna liczba zawodników
    cur.execute("SELECT COUNT(*) FROM zawodnicy")
    total = cur.fetchone()[0]
    print(f"🏃 Łączna liczba zawodników: {total}")
    
    # Podział według płci
    print("\n👥 Podział według płci:")
    cur.execute("SELECT plec, COUNT(*) FROM zawodnicy GROUP BY plec ORDER BY plec")
    for plec, liczba in cur.fetchall():
        procent = (liczba / total) * 100
        plec_nazwa = "Kobiety" if plec == 'K' else "Mężczyźni"
        print(f"  {plec_nazwa}: {liczba} ({procent:.1f}%)")
    
    # Podział według kategorii
    print("\n📋 Podział według kategorii:")
    cur.execute("SELECT kategoria, COUNT(*) FROM zawodnicy GROUP BY kategoria ORDER BY kategoria")
    for kategoria, liczba in cur.fetchall():
        procent = (liczba / total) * 100
        print(f"  {kategoria}: {liczba} ({procent:.1f}%)")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    sprawdz_stan() 