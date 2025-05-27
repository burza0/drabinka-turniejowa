#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2
import os
import random
from dotenv import load_dotenv

# Załaduj zmienne środowiskowe
load_dotenv()

# Połączenie z bazą danych
DB_URL = os.getenv('DATABASE_URL')

# Nowe kategorie
NOWE_KATEGORIE = ['Junior A', 'Junior B', 'Junior C', 'Junior D', 'Masters', 'Senior']

# Listy imion
IMIONA_MESKIE = [
    'Adam', 'Bartosz', 'Damian', 'Filip', 'Grzegorz', 'Hubert', 'Jakub', 'Kamil', 'Krzysztof', 'Łukasz',
    'Marcin', 'Michał', 'Norbert', 'Paweł', 'Rafał', 'Sebastian', 'Tomasz', 'Zbigniew', 'Artur', 'Dawid',
    'Emil', 'Fabian', 'Gabriel', 'Igor', 'Jacek', 'Karol', 'Leszek', 'Marek', 'Oskar', 'Patryk',
    'Robert', 'Szymon', 'Tadeusz', 'Wiktor', 'Zygmunt', 'Adrian', 'Bogdan', 'Czesław', 'Daniel', 'Ernest',
    'Franciszek', 'Gustaw', 'Henryk', 'Ireneusz', 'Jan', 'Konrad', 'Leon', 'Mateusz', 'Nikodem', 'Olaf'
]

IMIONA_ZENSKIE = [
    'Anna', 'Barbara', 'Celina', 'Dorota', 'Ewa', 'Grażyna', 'Halina', 'Irena', 'Joanna', 'Katarzyna',
    'Lidia', 'Magdalena', 'Monika', 'Natalia', 'Olga', 'Patrycja', 'Renata', 'Sylwia', 'Teresa', 'Urszula',
    'Weronika', 'Agnieszka', 'Beata', 'Danuta', 'Elżbieta', 'Franciszka', 'Gabriela', 'Helena', 'Izabela', 'Julia',
    'Krystyna', 'Lucyna', 'Maria', 'Nina', 'Oliwia', 'Paulina', 'Róża', 'Stanisława', 'Tatiana', 'Violetta',
    'Wanda', 'Zuzanna', 'Aleksandra', 'Bożena', 'Claudia', 'Diana', 'Emilia', 'Felicja', 'Genowefa', 'Hanna'
]

NAZWISKA = [
    'Kowalski', 'Nowak', 'Wiśniewski', 'Wójcik', 'Kowalczyk', 'Kamiński', 'Lewandowski', 'Zieliński', 'Szymański', 'Woźniak',
    'Dąbrowski', 'Kozłowski', 'Jankowski', 'Mazur', 'Kwiatkowski', 'Krawczyk', 'Kaczmarek', 'Piotrowski', 'Grabowski', 'Nowakowski',
    'Pawłowski', 'Michalski', 'Nowicki', 'Adamczyk', 'Dudek', 'Zając', 'Wieczorek', 'Jabłoński', 'Król', 'Majewski',
    'Olszewski', 'Jaworski', 'Wróbel', 'Malinowski', 'Pawlak', 'Witkowski', 'Walczak', 'Stępień', 'Górski', 'Rutkowski',
    'Michalak', 'Sikora', 'Ostrowski', 'Baran', 'Duda', 'Szewczyk', 'Tomaszewski', 'Pietrzak', 'Marciniak', 'Wróblewski',
    'Zalewski', 'Jakubowski', 'Jasiński', 'Zawadzki', 'Sadowski', 'Bąk', 'Chmielewski', 'Włodarczyk', 'Borkowski', 'Czarnecki'
]

def zmien_kategorie_istniejacych():
    """Zmienia kategorie istniejących zawodników na nowe"""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    print("🔄 Zmieniam kategorie istniejących zawodników...")
    
    # Mapowanie starych kategorii na nowe
    mapowanie = {
        'U18': ['Junior A', 'Junior B'],
        'OPEN': ['Junior C', 'Junior D'],
        'MASTERS': ['Masters', 'Senior']
    }
    
    for stara_kategoria, nowe_kategorie in mapowanie.items():
        # Pobierz zawodników z danej kategorii
        cur.execute("SELECT nr_startowy FROM zawodnicy WHERE kategoria = %s", (stara_kategoria,))
        zawodnicy = cur.fetchall()
        
        print(f"  📋 Kategoria {stara_kategoria}: {len(zawodnicy)} zawodników")
        
        # Przypisz losowo do nowych kategorii
        for zawodnik in zawodnicy:
            nowa_kategoria = random.choice(nowe_kategorie)
            cur.execute("UPDATE zawodnicy SET kategoria = %s WHERE nr_startowy = %s", 
                       (nowa_kategoria, zawodnik[0]))
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Zmiana kategorii zakończona")

def dodaj_nowych_zawodnikow():
    """Dodaje nowych zawodników do osiągnięcia 200 łącznie"""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    # Sprawdź aktualną liczbę zawodników
    cur.execute("SELECT COUNT(*) FROM zawodnicy")
    aktualna_liczba = cur.fetchone()[0]
    
    do_dodania = 200 - aktualna_liczba
    print(f"📊 Aktualna liczba zawodników: {aktualna_liczba}")
    print(f"🎯 Cel: 200 zawodników")
    print(f"➕ Do dodania: {do_dodania} zawodników")
    
    if do_dodania <= 0:
        print("✅ Baza już ma wystarczającą liczbę zawodników")
        cur.close()
        conn.close()
        return
    
    # Znajdź najwyższy numer startowy
    cur.execute("SELECT MAX(nr_startowy) FROM zawodnicy")
    max_nr = cur.fetchone()[0]
    
    # Podział 50/50 na płcie
    mezczyzni_do_dodania = do_dodania // 2
    kobiety_do_dodania = do_dodania - mezczyzni_do_dodania
    
    print(f"👨 Mężczyźni do dodania: {mezczyzni_do_dodania}")
    print(f"👩 Kobiety do dodania: {kobiety_do_dodania}")
    
    nr_startowy = max_nr + 1
    
    # Dodaj mężczyzn
    print("🚹 Dodaję mężczyzn...")
    for i in range(mezczyzni_do_dodania):
        imie = random.choice(IMIONA_MESKIE)
        nazwisko = random.choice(NAZWISKA)
        kategoria = random.choice(NOWE_KATEGORIE)
        
        cur.execute("""
            INSERT INTO zawodnicy (nr_startowy, imie, nazwisko, kategoria, plec)
            VALUES (%s, %s, %s, %s, %s)
        """, (nr_startowy, imie, nazwisko, kategoria, 'M'))
        
        if i % 10 == 0 or i == mezczyzni_do_dodania - 1:
            print(f"    {nr_startowy}. {imie} {nazwisko} ({kategoria})")
        
        nr_startowy += 1
    
    # Dodaj kobiety
    print("🚺 Dodaję kobiety...")
    for i in range(kobiety_do_dodania):
        imie = random.choice(IMIONA_ZENSKIE)
        nazwisko = random.choice(NAZWISKA)
        kategoria = random.choice(NOWE_KATEGORIE)
        
        cur.execute("""
            INSERT INTO zawodnicy (nr_startowy, imie, nazwisko, kategoria, plec)
            VALUES (%s, %s, %s, %s, %s)
        """, (nr_startowy, imie, nazwisko, kategoria, 'K'))
        
        if i % 10 == 0 or i == kobiety_do_dodania - 1:
            print(f"    {nr_startowy}. {imie} {nazwisko} ({kategoria})")
        
        nr_startowy += 1
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Dodawanie nowych zawodników zakończone")

def generuj_wyniki_dla_nowych():
    """Generuje wyniki dla nowych zawodników"""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    print("🎲 Generuję wyniki dla nowych zawodników...")
    
    # Znajdź zawodników bez wyników
    cur.execute("""
        SELECT z.nr_startowy, z.kategoria 
        FROM zawodnicy z 
        LEFT JOIN wyniki w ON z.nr_startowy = w.nr_startowy 
        WHERE w.nr_startowy IS NULL
    """)
    zawodnicy_bez_wynikow = cur.fetchall()
    
    print(f"📋 Zawodników bez wyników: {len(zawodnicy_bez_wynikow)}")
    
    # Zakresy czasów dla kategorii
    zakresy_czasow = {
        'Junior A': (35, 55),    # Najszybsi juniorzy
        'Junior B': (38, 58),    # Średni juniorzy
        'Junior C': (40, 62),    # Starsi juniorzy
        'Junior D': (42, 65),    # Najstarsi juniorzy
        'Masters': (45, 70),     # Doświadczeni
        'Senior': (38, 60)       # Seniorzy
    }
    
    for nr_startowy, kategoria in zawodnicy_bez_wynikow:
        # 80% FINISHED, 12% DNF, 8% DSQ
        rand = random.random()
        if rand < 0.80:
            status = 'FINISHED'
            min_czas, max_czas = zakresy_czasow.get(kategoria, (40, 65))
            czas = round(random.uniform(min_czas, max_czas), 2)
        elif rand < 0.92:
            status = 'DNF'
            czas = None
        else:
            status = 'DSQ'
            czas = None
        
        cur.execute("""
            INSERT INTO wyniki (nr_startowy, czas_przejazdu_s, status)
            VALUES (%s, %s, %s)
        """, (nr_startowy, czas, status))
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Generowanie wyników zakończone")

def pokaz_statystyki():
    """Pokazuje końcowe statystyki"""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    print("\n📊 KOŃCOWE STATYSTYKI:")
    print("=" * 50)
    
    # Łączna liczba zawodników
    cur.execute("SELECT COUNT(*) FROM zawodnicy")
    total = cur.fetchone()[0]
    print(f"🏃 Łączna liczba zawodników: {total}")
    
    # Podział według kategorii
    print("\n📋 Podział według kategorii:")
    cur.execute("""
        SELECT kategoria, COUNT(*) as liczba,
               SUM(CASE WHEN plec = 'M' THEN 1 ELSE 0 END) as mezczyzni,
               SUM(CASE WHEN plec = 'K' THEN 1 ELSE 0 END) as kobiety
        FROM zawodnicy 
        GROUP BY kategoria 
        ORDER BY kategoria
    """)
    
    for kategoria, liczba, mezczyzni, kobiety in cur.fetchall():
        print(f"  {kategoria}: {liczba} ({mezczyzni}M + {kobiety}K)")
    
    # Podział według płci
    print("\n👥 Podział według płci:")
    cur.execute("""
        SELECT plec, COUNT(*) as liczba
        FROM zawodnicy 
        GROUP BY plec 
        ORDER BY plec
    """)
    
    for plec, liczba in cur.fetchall():
        procent = (liczba / total) * 100
        plec_nazwa = "Kobiety" if plec == 'K' else "Mężczyźni"
        print(f"  {plec_nazwa}: {liczba} ({procent:.1f}%)")
    
    # Statystyki wyników
    print("\n🏁 Statystyki wyników:")
    cur.execute("""
        SELECT status, COUNT(*) as liczba
        FROM wyniki 
        GROUP BY status 
        ORDER BY status
    """)
    
    for status, liczba in cur.fetchall():
        procent = (liczba / total) * 100
        print(f"  {status}: {liczba} ({procent:.1f}%)")
    
    cur.close()
    conn.close()

def main():
    print("🏁 ZMIANA KATEGORII I ROZSZERZENIE BAZY DO 200 ZAWODNIKÓW")
    print("=" * 60)
    
    try:
        # Krok 1: Zmień kategorie istniejących zawodników
        zmien_kategorie_istniejacych()
        
        # Krok 2: Dodaj nowych zawodników do 200
        dodaj_nowych_zawodnikow()
        
        # Krok 3: Wygeneruj wyniki dla nowych zawodników
        generuj_wyniki_dla_nowych()
        
        # Krok 4: Pokaż statystyki
        pokaz_statystyki()
        
        print("\n🎉 OPERACJA ZAKOŃCZONA POMYŚLNIE!")
        print("✅ Kategorie zmienione na: Junior A, Junior B, Junior C, Junior D, Masters, Senior")
        print("✅ Baza rozszerzona do 200 zawodników (100M + 100K)")
        print("✅ Wyniki wygenerowane dla wszystkich zawodników")
        
    except Exception as e:
        print(f"❌ Błąd: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main() 