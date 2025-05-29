#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
import os
from dotenv import load_dotenv
import random

load_dotenv()

# Połączenie z bazą danych
DB_URL = os.getenv('DATABASE_URL')

# Lista klubów ze zrzutu
KLUBY = [
    "Rollschool Warszawa",
    "Dragon Roller Club Kyiv", 
    "Rollhouse Warszawa",
    "Crazy Sport Warszawa",
    "Freestyle Roller School",
    "Skating School Zabrze",
    "Czysta Forma Płock",
    "RollMasters Olsztyn",
    "Skating Academy Piaseczno",
    "Black & Yellow Skating Białystok",
    "RollRunners Poznań",
    "RollStreet Rzeszów",
    "Niezrzeszony"
]

def utworz_tabele_kluby():
    """Tworzy tabelę kluby"""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    print("🏢 Tworzę tabelę kluby...")
    
    # Usuń tabelę jeśli istnieje
    cur.execute("DROP TABLE IF EXISTS kluby CASCADE")
    
    # Utwórz nową tabelę kluby
    cur.execute("""
        CREATE TABLE kluby (
            id SERIAL PRIMARY KEY,
            nazwa VARCHAR(100) UNIQUE NOT NULL,
            miasto VARCHAR(50),
            utworzony_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Tabela kluby utworzona")

def dodaj_kluby():
    """Dodaje kluby do tabeli"""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    print("📋 Dodaję kluby...")
    
    for i, klub in enumerate(KLUBY, 1):
        # Określ miasto na podstawie nazwy klubu
        if "Warszawa" in klub:
            miasto = "Warszawa"
        elif "Kyiv" in klub:
            miasto = "Kyiv"
        elif "Zabrze" in klub:
            miasto = "Zabrze"
        elif "Płock" in klub:
            miasto = "Płock"
        elif "Olsztyn" in klub:
            miasto = "Olsztyn"
        elif "Piaseczno" in klub:
            miasto = "Piaseczno"
        elif "Białystok" in klub:
            miasto = "Białystok"
        elif "Poznań" in klub:
            miasto = "Poznań"
        elif "Rzeszów" in klub:
            miasto = "Rzeszów"
        else:
            miasto = "Nieznane"
        
        cur.execute("""
            INSERT INTO kluby (nazwa, miasto) 
            VALUES (%s, %s)
        """, (klub, miasto))
        
        print(f"  {i:2d}. {klub} ({miasto})")
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Kluby dodane")

def przypisz_zawodnikow_do_klubow():
    """Przypisuje zawodników losowo do klubów"""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    print("👥 Przypisuję zawodników do klubów...")
    
    # Pobierz wszystkich zawodników
    cur.execute("SELECT nr_startowy, imie, nazwisko FROM zawodnicy ORDER BY nr_startowy")
    zawodnicy = cur.fetchall()
    
    print(f"📊 Znaleziono {len(zawodnicy)} zawodników")
    
    # Przypisz losowo do klubów
    for nr_startowy, imie, nazwisko in zawodnicy:
        klub = random.choice(KLUBY)
        
        cur.execute("""
            UPDATE zawodnicy 
            SET klub = %s 
            WHERE nr_startowy = %s
        """, (klub, nr_startowy))
        
        if nr_startowy % 25 == 0 or nr_startowy <= 5:
            print(f"  {nr_startowy:3d}. {imie} {nazwisko} -> {klub}")
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Przypisywanie zawodników zakończone")

def pokaz_statystyki():
    """Pokazuje statystyki przypisań"""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    print("\n📊 STATYSTYKI KLUBÓW:")
    print("=" * 60)
    
    # Statystyki zawodników w klubach
    cur.execute("""
        SELECT klub, COUNT(*) as liczba_zawodnikow
        FROM zawodnicy 
        GROUP BY klub 
        ORDER BY liczba_zawodnikow DESC, klub
    """)
    
    statystyki = cur.fetchall()
    total_zawodnikow = sum(stat[1] for stat in statystyki)
    
    for i, (klub, liczba) in enumerate(statystyki, 1):
        procent = (liczba / total_zawodnikow) * 100
        print(f"{i:2d}. {klub:<35} {liczba:3d} zawodników ({procent:4.1f}%)")
    
    print(f"\n📈 Łącznie: {total_zawodnikow} zawodników w {len(statystyki)} klubach")
    
    # Podział płci w każdym klubie
    print(f"\n👥 Podział płci w klubach:")
    cur.execute("""
        SELECT klub, 
               SUM(CASE WHEN plec = 'M' THEN 1 ELSE 0 END) as mezczyzni,
               SUM(CASE WHEN plec = 'K' THEN 1 ELSE 0 END) as kobiety
        FROM zawodnicy 
        GROUP BY klub 
        ORDER BY klub
    """)
    
    for klub, mezczyzni, kobiety in cur.fetchall():
        total_klub = mezczyzni + kobiety
        if total_klub > 0:
            print(f"  {klub:<35} {mezczyzni}M + {kobiety}K = {total_klub}")
    
    cur.close()
    conn.close()

def main():
    print("🏢 DODAWANIE TABELI KLUBY I PRZYPISYWANIE ZAWODNIKÓW")
    print("=" * 60)
    
    try:
        # 1. Utwórz tabelę kluby
        utworz_tabele_kluby()
        
        # 2. Dodaj kluby
        dodaj_kluby()
        
        # 3. Przypisz zawodników do klubów
        przypisz_zawodnikow_do_klubow()
        
        # 4. Pokaż statystyki
        pokaz_statystyki()
        
        print(f"\n🎉 Proces zakończony pomyślnie!")
        print(f"✅ Tabela kluby utworzona")
        print(f"✅ {len(KLUBY)} klubów dodanych")
        print(f"✅ Wszyscy zawodnicy przypisani do klubów")
        
    except Exception as e:
        print(f"❌ Błąd: {e}")

if __name__ == "__main__":
    main() 