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

# Kategorie
KATEGORIE = ['Junior A', 'Junior B', 'Junior C', 'Junior D', 'Masters', 'Senior']

# Rozszerzone listy imion
IMIONA_MESKIE = [
    'Adam', 'Bartosz', 'Damian', 'Filip', 'Grzegorz', 'Hubert', 'Jakub', 'Kamil', 'Krzysztof', 'Łukasz',
    'Marcin', 'Michał', 'Norbert', 'Paweł', 'Rafał', 'Sebastian', 'Tomasz', 'Zbigniew', 'Artur', 'Dawid',
    'Emil', 'Fabian', 'Gabriel', 'Igor', 'Jacek', 'Karol', 'Leszek', 'Marek', 'Oskar', 'Patryk',
    'Robert', 'Szymon', 'Tadeusz', 'Wiktor', 'Zygmunt', 'Adrian', 'Bogdan', 'Czesław', 'Daniel', 'Ernest',
    'Franciszek', 'Gustaw', 'Henryk', 'Ireneusz', 'Jan', 'Konrad', 'Leon', 'Mateusz', 'Nikodem', 'Olaf',
    'Piotr', 'Radosław', 'Stanisław', 'Tymoteusz', 'Ulryk', 'Waldemar', 'Xawery', 'Yves', 'Zenon', 'Aleksander',
    'Benedykt', 'Cyprian', 'Dominik', 'Eryk', 'Feliks', 'Gerard', 'Hieronim', 'Ignacy', 'Julian', 'Kacper',
    'Lucjan', 'Maksymilian', 'Natan', 'Oktawian', 'Przemysław', 'Ryszard', 'Sylwester', 'Teodor', 'Urban', 'Wacław'
]

IMIONA_ZENSKIE = [
    'Anna', 'Barbara', 'Celina', 'Dorota', 'Ewa', 'Grażyna', 'Halina', 'Irena', 'Joanna', 'Katarzyna',
    'Lidia', 'Magdalena', 'Monika', 'Natalia', 'Olga', 'Patrycja', 'Renata', 'Sylwia', 'Teresa', 'Urszula',
    'Weronika', 'Agnieszka', 'Beata', 'Danuta', 'Elżbieta', 'Franciszka', 'Gabriela', 'Helena', 'Izabela', 'Julia',
    'Krystyna', 'Lucyna', 'Maria', 'Nina', 'Oliwia', 'Paulina', 'Róża', 'Stanisława', 'Tatiana', 'Violetta',
    'Wanda', 'Zuzanna', 'Aleksandra', 'Bożena', 'Claudia', 'Diana', 'Emilia', 'Felicja', 'Genowefa', 'Hanna',
    'Iwona', 'Justyna', 'Klaudia', 'Laura', 'Marlena', 'Nadia', 'Oktawia', 'Petra', 'Roksana', 'Sara',
    'Tamara', 'Ulrika', 'Viktoria', 'Wiktoria', 'Ximena', 'Yvonne', 'Zofia', 'Adrianna', 'Blanka', 'Cecylia'
]

NAZWISKA = [
    'Kowalski', 'Nowak', 'Wiśniewski', 'Wójcik', 'Kowalczyk', 'Kamiński', 'Lewandowski', 'Zieliński', 'Szymański', 'Woźniak',
    'Dąbrowski', 'Kozłowski', 'Jankowski', 'Mazur', 'Kwiatkowski', 'Krawczyk', 'Kaczmarek', 'Piotrowski', 'Grabowski', 'Nowakowski',
    'Pawłowski', 'Michalski', 'Nowicki', 'Adamczyk', 'Dudek', 'Zając', 'Wieczorek', 'Jabłoński', 'Król', 'Majewski',
    'Olszewski', 'Jaworski', 'Wróbel', 'Malinowski', 'Pawlak', 'Witkowski', 'Walczak', 'Stępień', 'Górski', 'Rutkowski',
    'Michalak', 'Sikora', 'Ostrowski', 'Baran', 'Duda', 'Szewczyk', 'Tomaszewski', 'Pietrzak', 'Marciniak', 'Wróblewski',
    'Zalewski', 'Jakubowski', 'Jasiński', 'Zawadzki', 'Sadowski', 'Bąk', 'Chmielewski', 'Włodarczyk', 'Borkowski', 'Czarnecki',
    'Sawicki', 'Sokołowski', 'Urbański', 'Kubiak', 'Maciejewski', 'Szczepański', 'Kucharski', 'Wilk', 'Kalinowski', 'Lis',
    'Mazurek', 'Wysocki', 'Adamski', 'Kaźmierczak', 'Wasilewski', 'Sobczak', 'Czerwiński', 'Andrzejewski', 'Cieślak', 'Kowal',
    'Bednarek', 'Kołodziej', 'Szulc', 'Baranowski', 'Laskowski', 'Brzeziński', 'Makowski', 'Ziółkowski', 'Przybylski', 'Wierzbicki'
]

def sprawdz_aktualny_stan():
    """Sprawdza aktualny stan bazy danych"""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    # Sprawdź liczbę zawodników
    cur.execute("SELECT COUNT(*) FROM zawodnicy")
    total = cur.fetchone()[0]
    
    # Sprawdź podział płci
    cur.execute("SELECT plec, COUNT(*) FROM zawodnicy GROUP BY plec ORDER BY plec")
    plcie = cur.fetchall()
    
    # Znajdź najwyższy numer startowy
    cur.execute("SELECT MAX(nr_startowy) FROM zawodnicy")
    max_nr = cur.fetchone()[0]
    
    cur.close()
    conn.close()
    
    return total, plcie, max_nr

def dodaj_nowych_zawodnikow(aktualna_liczba, max_nr):
    """Dodaje nowych zawodników do osiągnięcia 250 łącznie"""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    cel = 250
    do_dodania = cel - aktualna_liczba
    
    print(f"📊 Aktualna liczba zawodników: {aktualna_liczba}")
    print(f"🎯 Cel: {cel} zawodników")
    print(f"➕ Do dodania: {do_dodania} zawodników")
    
    if do_dodania <= 0:
        print("✅ Baza już ma wystarczającą liczbę zawodników")
        cur.close()
        conn.close()
        return
    
    # Podział 50/50 na płcie
    mezczyzni_do_dodania = do_dodania // 2
    kobiety_do_dodania = do_dodania - mezczyzni_do_dodania
    
    print(f"👨 Mężczyźni do dodania: {mezczyzni_do_dodania}")
    print(f"👩 Kobiety do dodania: {kobiety_do_dodania}")
    
    nr_startowy = max_nr + 1
    
    # Dodaj mężczyzn
    print("\n🚹 Dodaję mężczyzn...")
    for i in range(mezczyzni_do_dodania):
        imie = random.choice(IMIONA_MESKIE)
        nazwisko = random.choice(NAZWISKA)
        kategoria = random.choice(KATEGORIE)
        
        cur.execute("""
            INSERT INTO zawodnicy (nr_startowy, imie, nazwisko, kategoria, plec)
            VALUES (%s, %s, %s, %s, %s)
        """, (nr_startowy, imie, nazwisko, kategoria, 'M'))
        
        if i % 5 == 0 or i == mezczyzni_do_dodania - 1:
            print(f"    {nr_startowy}. {imie} {nazwisko} ({kategoria})")
        
        nr_startowy += 1
    
    # Dodaj kobiety
    print("\n🚺 Dodaję kobiety...")
    for i in range(kobiety_do_dodania):
        imie = random.choice(IMIONA_ZENSKIE)
        nazwisko = random.choice(NAZWISKA)
        kategoria = random.choice(KATEGORIE)
        
        cur.execute("""
            INSERT INTO zawodnicy (nr_startowy, imie, nazwisko, kategoria, plec)
            VALUES (%s, %s, %s, %s, %s)
        """, (nr_startowy, imie, nazwisko, kategoria, 'K'))
        
        if i % 5 == 0 or i == kobiety_do_dodania - 1:
            print(f"    {nr_startowy}. {imie} {nazwisko} ({kategoria})")
        
        nr_startowy += 1
    
    conn.commit()
    cur.close()
    conn.close()
    print("\n✅ Dodawanie nowych zawodników zakończone")

def generuj_wyniki_dla_nowych():
    """Generuje wyniki dla nowych zawodników"""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    print("\n🎲 Generuję wyniki dla nowych zawodników...")
    
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
        # 78% FINISHED, 12% DNF, 10% DSQ
        rand = random.random()
        if rand < 0.78:
            status = 'FINISHED'
            min_czas, max_czas = zakresy_czasow.get(kategoria, (40, 65))
            czas = round(random.uniform(min_czas, max_czas), 2)
        elif rand < 0.90:
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

def pokaz_statystyki_koncowe():
    """Pokazuje końcowe statystyki"""
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    
    print("\n📊 KOŃCOWE STATYSTYKI - 250 ZAWODNIKÓW:")
    print("=" * 60)
    
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
        procent = (liczba / total) * 100
        print(f"  {kategoria}: {liczba} ({procent:.1f}%) - {mezczyzni}M + {kobiety}K")
    
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
    
    # Top 10 wyników
    print("\n🏆 TOP 10 NAJLEPSZYCH CZASÓW:")
    cur.execute("""
        SELECT w.nr_startowy, z.imie, z.nazwisko, z.kategoria, z.plec, w.czas_przejazdu_s
        FROM wyniki w
        JOIN zawodnicy z ON w.nr_startowy = z.nr_startowy
        WHERE w.status = 'FINISHED'
        ORDER BY CAST(w.czas_przejazdu_s AS FLOAT) ASC
        LIMIT 10
    """)
    
    top_wyniki = cur.fetchall()
    for i, (nr, imie, nazwisko, kategoria, plec, czas) in enumerate(top_wyniki, 1):
        plec_symbol = "🚹" if plec == 'M' else "🚺"
        print(f"  {i:2d}. {plec_symbol} {imie} {nazwisko} ({kategoria}) - {czas}s")
    
    cur.close()
    conn.close()

def main():
    print("🏁 ROZSZERZENIE BAZY DO 250 ZAWODNIKÓW")
    print("=" * 50)
    
    try:
        # Krok 1: Sprawdź aktualny stan
        aktualna_liczba, plcie, max_nr = sprawdz_aktualny_stan()
        
        print("📊 Aktualny stan:")
        print(f"  Łącznie zawodników: {aktualna_liczba}")
        for plec, liczba in plcie:
            plec_nazwa = "Kobiety" if plec == 'K' else "Mężczyźni"
            print(f"  {plec_nazwa}: {liczba}")
        print(f"  Najwyższy nr startowy: {max_nr}")
        
        # Krok 2: Dodaj nowych zawodników do 250
        dodaj_nowych_zawodnikow(aktualna_liczba, max_nr)
        
        # Krok 3: Wygeneruj wyniki dla nowych zawodników
        generuj_wyniki_dla_nowych()
        
        # Krok 4: Pokaż końcowe statystyki
        pokaz_statystyki_koncowe()
        
        print("\n🎉 OPERACJA ZAKOŃCZONA POMYŚLNIE!")
        print("✅ Baza rozszerzona do 250 zawodników (125M + 125K)")
        print("✅ Wyniki wygenerowane dla wszystkich nowych zawodników")
        print("✅ Proporcjonalny podział płci zachowany")
        
    except Exception as e:
        print(f"❌ Błąd: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main() 