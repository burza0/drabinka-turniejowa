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
conn = psycopg2.connect(DB_URL)
cur = conn.cursor()

# Sprawdź aktualną liczbę zawodników
cur.execute('SELECT COUNT(*) FROM zawodnicy')
aktualna_liczba = cur.fetchone()[0]
print(f"📊 Aktualna liczba zawodników: {aktualna_liczba}")

cur.execute('SELECT MAX(nr_startowy) FROM zawodnicy')
max_nr = cur.fetchone()[0]
print(f"📊 Najwyższy numer startowy: {max_nr}")

# Sprawdź aktualny podział płci
cur.execute('SELECT plec, COUNT(*) FROM zawodnicy GROUP BY plec ORDER BY plec')
plcie = cur.fetchall()
print("📊 Aktualny podział płci:")
kobiety_aktualne = 0
mezczyzni_aktualni = 0
for plec, liczba in plcie:
    plec_nazwa = "Kobiety" if plec == 'K' else "Mężczyźni"
    print(f"  {plec_nazwa}: {liczba}")
    if plec == 'K':
        kobiety_aktualne = liczba
    else:
        mezczyzni_aktualni = liczba

# Ile zawodników dodać
docelowa_liczba = 150
do_dodania = docelowa_liczba - aktualna_liczba
print(f"\n🎯 Cel: {docelowa_liczba} zawodników")
print(f"➕ Do dodania: {do_dodania} zawodników")

if do_dodania <= 0:
    print("✅ Już mamy wystarczającą liczbę zawodników!")
    cur.close()
    conn.close()
    exit()

# Oblicz proporcjonalny podział dla nowych zawodników
# Cel: 75 kobiet i 75 mężczyzn łącznie (50/50)
docelowe_kobiety = 75
docelowi_mezczyzni = 75

kobiety_do_dodania = docelowe_kobiety - kobiety_aktualne
mezczyzni_do_dodania = docelowi_mezczyzni - mezczyzni_aktualni

print(f"\n🎯 Docelowy podział (50/50):")
print(f"  Kobiety: {docelowe_kobiety} (aktualne: {kobiety_aktualne}, do dodania: {kobiety_do_dodania})")
print(f"  Mężczyźni: {docelowi_mezczyzni} (aktualni: {mezczyzni_aktualni}, do dodania: {mezczyzni_do_dodania})")

# Listy imion i nazwisk
imiona_meskie = [
    "Adrian", "Aleksander", "Andrzej", "Antoni", "Arkadiusz", "Bartłomiej", "Bogdan", "Cezary",
    "Daniel", "Dariusz", "Dawid", "Dominik", "Emil", "Ernest", "Fabian", "Filip", "Franciszek",
    "Gabriel", "Grzegorz", "Henryk", "Igor", "Jacek", "Jakub", "Jan", "Jarosław", "Jerzy",
    "Józef", "Kamil", "Karol", "Konrad", "Krystian", "Krzysztof", "Łukasz", "Maciej", "Marcin",
    "Marek", "Mariusz", "Mateusz", "Michał", "Mirosław", "Norbert", "Oskar", "Patryk", "Paweł",
    "Piotr", "Przemysław", "Radosław", "Rafał", "Robert", "Sebastian", "Sławomir", "Stanisław",
    "Stefan", "Szymon", "Tomasz", "Waldemar", "Wiktor", "Wojciech", "Zbigniew", "Zygmunt",
    "Bartosz", "Damian", "Hubert", "Ryszard", "Tadeusz", "Wiesław", "Leszek", "Janusz"
]

imiona_zenskie = [
    "Agata", "Agnieszka", "Aleksandra", "Alicja", "Anna", "Barbara", "Beata", "Celina", "Danuta",
    "Dorota", "Ewa", "Grażyna", "Halina", "Irena", "Iwona", "Jadwiga", "Joanna", "Jolanta",
    "Justyna", "Karina", "Katarzyna", "Krystyna", "Lidia", "Magdalena", "Małgorzata", "Maria",
    "Mariola", "Monika", "Natalia", "Olga", "Patrycja", "Paulina", "Renata", "Sandra", "Sylwia",
    "Teresa", "Urszula", "Weronika", "Wioletta", "Zofia", "Żaneta", "Adrianna", "Angelika",
    "Anita", "Bożena", "Edyta", "Elżbieta", "Emilia", "Gabriela", "Helena", "Izabela", "Julia",
    "Karolina", "Klaudia", "Lucyna", "Marta", "Martyna", "Milena", "Nikola", "Oliwia", "Roma",
    "Ewelina", "Kamila", "Agnieszka", "Zuzanna", "Aleksandra", "Wiktoria", "Amelia", "Lena"
]

nazwiska = [
    "Nowak", "Kowalski", "Wiśniewski", "Dąbrowski", "Lewandowski", "Wójcik", "Kamiński", "Kowalczyk",
    "Zieliński", "Szymański", "Woźniak", "Kozłowski", "Jankowski", "Wojciechowski", "Kwiatkowski",
    "Kaczmarek", "Mazur", "Krawczyk", "Piotrowski", "Grabowski", "Nowakowski", "Pawłowski", "Michalski",
    "Nowicki", "Adamczyk", "Dudek", "Zając", "Wieczorek", "Jabłoński", "Król", "Majewski", "Olszewski",
    "Jaworski", "Wróbel", "Malinowski", "Pawlak", "Witkowski", "Walczak", "Stępień", "Górski",
    "Rutkowski", "Michalak", "Sikora", "Ostrowski", "Baran", "Duda", "Szewczyk", "Tomaszewski",
    "Pietrzak", "Marciniak", "Wróblewski", "Zalewski", "Jakubowski", "Jasiński", "Zawadzki", "Sadowski",
    "Bąk", "Chmielewski", "Włodarczyk", "Borkowski", "Czarnecki", "Sawicki", "Sokołowski", "Urbański",
    "Kubiak", "Maciejewski", "Szczepański", "Kucharski", "Wilk", "Kalinowski", "Lis", "Mazurek",
    "Wysocki", "Adamski", "Kaźmierczak", "Wasilewski", "Sobczak", "Czerwiński", "Andrzejewski", "Cieślak",
    "Kowal", "Bednarek", "Kołodziej", "Szulc", "Baranowski", "Laskowski", "Brzeziński", "Makowski"
]

kategorie = ["U18", "OPEN", "MASTERS"]

# Funkcja do generowania losowego czasu
def generuj_czas(kategoria):
    if kategoria == "U18":
        return round(random.uniform(38.0, 65.0), 3)
    elif kategoria == "OPEN":
        return round(random.uniform(35.0, 58.0), 3)
    else:  # MASTERS
        return round(random.uniform(40.0, 70.0), 3)

# Dodawanie zawodników
print(f"\n🚀 Rozpoczynam dodawanie {do_dodania} zawodników od numeru {max_nr + 1}")

nr_startowy = max_nr + 1
dodani = 0

# Dodaj mężczyzn
if mezczyzni_do_dodania > 0:
    print(f"\n🚹 Dodaję {mezczyzni_do_dodania} mężczyzn...")
    for i in range(mezczyzni_do_dodania):
        imie = random.choice(imiona_meskie)
        nazwisko = random.choice(nazwiska)
        kategoria = random.choice(kategorie)
        plec = 'M'
        
        # 80% szans na ukończenie
        if random.random() < 0.8:
            status = 'FINISHED'
            czas = generuj_czas(kategoria)
        elif random.random() < 0.7:  # 14% DNF (0.2 * 0.7)
            status = 'DNF'
            czas = None
        else:  # 6% DSQ
            status = 'DSQ'
            czas = None
        
        try:
            # Dodaj do tabeli zawodnicy
            cur.execute("""
                INSERT INTO zawodnicy (nr_startowy, imie, nazwisko, kategoria, plec)
                VALUES (%s, %s, %s, %s, %s)
            """, (nr_startowy, imie, nazwisko, kategoria, plec))
            
            # Dodaj do tabeli wyniki
            if czas:
                cur.execute("""
                    INSERT INTO wyniki (nr_startowy, czas_przejazdu_s, status)
                    VALUES (%s, %s, %s)
                """, (nr_startowy, czas, status))
            else:
                cur.execute("""
                    INSERT INTO wyniki (nr_startowy, status)
                    VALUES (%s, %s)
                """, (nr_startowy, status))
            
            print(f"  {nr_startowy:3d}. {imie} {nazwisko} ({kategoria}) - {status}")
            nr_startowy += 1
            dodani += 1
            
        except Exception as e:
            print(f"❌ Błąd dodawania zawodnika {nr_startowy}: {e}")
            conn.rollback()
            break

# Dodaj kobiety
if kobiety_do_dodania > 0:
    print(f"\n🚺 Dodaję {kobiety_do_dodania} kobiet...")
    for i in range(kobiety_do_dodania):
        imie = random.choice(imiona_zenskie)
        nazwisko = random.choice(nazwiska)
        kategoria = random.choice(kategorie)
        plec = 'K'
        
        # 80% szans na ukończenie
        if random.random() < 0.8:
            status = 'FINISHED'
            czas = generuj_czas(kategoria)
        elif random.random() < 0.7:  # 14% DNF
            status = 'DNF'
            czas = None
        else:  # 6% DSQ
            status = 'DSQ'
            czas = None
        
        try:
            # Dodaj do tabeli zawodnicy
            cur.execute("""
                INSERT INTO zawodnicy (nr_startowy, imie, nazwisko, kategoria, plec)
                VALUES (%s, %s, %s, %s, %s)
            """, (nr_startowy, imie, nazwisko, kategoria, plec))
            
            # Dodaj do tabeli wyniki
            if czas:
                cur.execute("""
                    INSERT INTO wyniki (nr_startowy, czas_przejazdu_s, status)
                    VALUES (%s, %s, %s)
                """, (nr_startowy, czas, status))
            else:
                cur.execute("""
                    INSERT INTO wyniki (nr_startowy, status)
                    VALUES (%s, %s)
                """, (nr_startowy, status))
            
            print(f"  {nr_startowy:3d}. {imie} {nazwisko} ({kategoria}) - {status}")
            nr_startowy += 1
            dodani += 1
            
        except Exception as e:
            print(f"❌ Błąd dodawania zawodnika {nr_startowy}: {e}")
            conn.rollback()
            break

# Zatwierdź zmiany
conn.commit()

# Sprawdź końcowe statystyki
print(f"\n📊 Statystyki po dodaniu:")
cur.execute("""
    SELECT z.kategoria, z.plec, COUNT(*) 
    FROM zawodnicy z
    GROUP BY z.kategoria, z.plec 
    ORDER BY z.kategoria, z.plec
""")
statystyki = cur.fetchall()

for kategoria, plec, liczba in statystyki:
    plec_nazwa = "Mężczyźni" if plec == 'M' else "Kobiety"
    print(f"  {kategoria}: {plec_nazwa} - {liczba}")

# Sprawdź końcowy podział płci
cur.execute('SELECT plec, COUNT(*) FROM zawodnicy GROUP BY plec ORDER BY plec')
plcie_koncowe = cur.fetchall()
print(f"\n📊 Końcowy podział płci:")
for plec, liczba in plcie_koncowe:
    plec_nazwa = "Kobiety" if plec == 'K' else "Mężczyźni"
    procent = (liczba / 150) * 100
    print(f"  {plec_nazwa}: {liczba} ({procent:.1f}%)")

cur.execute('SELECT COUNT(*) FROM zawodnicy')
koncowa_liczba = cur.fetchone()[0]

print(f"\n✅ Łącznie zawodników w bazie: {koncowa_liczba}")
print(f"➕ Dodano: {dodani} nowych zawodników")
print(f"🎉 Rozszerzanie listy zawodników do 150 zakończone pomyślnie!")

# Zamknij połączenie
cur.close()
conn.close() 