#!/usr/bin/env python3
"""
Inicjalizacja bazy danych SKATECROSS QR
Uruchamianie: python init_database.py
"""

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def init_database():
    """Inicjalizuje bazę danych z podstawowymi tabelami i przykładowymi danymi"""
    
    DB_URL = os.getenv('DATABASE_URL')
    if not DB_URL:
        print("❌ BŁĄD: Nie znaleziono DATABASE_URL w pliku .env")
        return False
    
    try:
        print("🔗 Łączenie z bazą danych...")
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # Tworzenie tabel
        print("📋 Tworzenie tabel...")
        
        # Tabela zawodników
        cur.execute("""
            CREATE TABLE IF NOT EXISTS zawodnicy (
                nr_startowy INTEGER PRIMARY KEY,
                imie VARCHAR(100) NOT NULL,
                nazwisko VARCHAR(100) NOT NULL,
                kategoria VARCHAR(50),
                plec CHAR(1),
                klub VARCHAR(200),
                qr_code TEXT,
                checked_in BOOLEAN DEFAULT FALSE,
                check_in_time TIMESTAMP,
                ostatni_skan TIMESTAMP
            );
        """)
        
        # Tabela wyników
        cur.execute("""
            CREATE TABLE IF NOT EXISTS wyniki (
                nr_startowy INTEGER PRIMARY KEY REFERENCES zawodnicy(nr_startowy),
                czas_przejazdu_s DECIMAL(10,3),
                status VARCHAR(20) DEFAULT 'NOT_STARTED'
            );
        """)
        
        # Tabela kolejki startowej
        cur.execute("""
            CREATE TABLE IF NOT EXISTS start_queue (
                id SERIAL PRIMARY KEY,
                kategoria VARCHAR(50),
                plec CHAR(1),
                numer_grupy INTEGER,
                nazwa VARCHAR(200),
                status VARCHAR(20) DEFAULT 'WAITING',
                estimated_time INTEGER DEFAULT 300
            );
        """)
        
        print("✅ Tabele utworzone")
        
        # Sprawdź czy są już dane
        cur.execute("SELECT COUNT(*) FROM zawodnicy")
        count = cur.fetchone()[0]
        
        if count == 0:
            print("📊 Dodawanie przykładowych danych...")
            
            # Przykładowi zawodnicy
            sample_data = [
                (1, "Jan", "Kowalski", "Junior A", "M", "RC Warszawa"),
                (2, "Anna", "Nowak", "Junior A", "K", "RC Warszawa"),
                (3, "Piotr", "Wiśniewski", "Junior A", "M", "RC Kraków"),
                (4, "Maria", "Dąbrowska", "Junior A", "K", "RC Kraków"),
                (5, "Tomasz", "Lewandowski", "Senior", "M", "RC Gdańsk"),
                (6, "Katarzyna", "Wójcik", "Senior", "K", "RC Gdańsk"),
                (7, "Michał", "Kamiński", "Senior", "M", "RC Wrocław"),
                (8, "Agnieszka", "Kaczmarek", "Senior", "K", "RC Wrocław"),
                (9, "Łukasz", "Zieliński", "Junior B", "M", "RC Poznań"),
                (10, "Magdalena", "Szymańska", "Junior B", "K", "RC Poznań"),
            ]
            
            for zawodnik in sample_data:
                cur.execute("""
                    INSERT INTO zawodnicy (nr_startowy, imie, nazwisko, kategoria, plec, klub)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, zawodnik)
                
                # Dodaj rekord w tabeli wyników
                cur.execute("""
                    INSERT INTO wyniki (nr_startowy, status)
                    VALUES (%s, 'NOT_STARTED')
                """, (zawodnik[0],))
            
            # Przykładowe grupy startowe
            groups = [
                ("Junior A", "M", 1, "Junior A Mężczyźni"),
                ("Junior A", "K", 2, "Junior A Kobiety"),
                ("Senior", "M", 3, "Senior Mężczyźni"),
                ("Senior", "K", 4, "Senior Kobiety"),
                ("Junior B", "M", 5, "Junior B Mężczyźni"),
                ("Junior B", "K", 6, "Junior B Kobiety"),
            ]
            
            for group in groups:
                cur.execute("""
                    INSERT INTO start_queue (kategoria, plec, numer_grupy, nazwa)
                    VALUES (%s, %s, %s, %s)
                """, group)
            
            print("✅ Przykładowe dane dodane")
        else:
            print(f"ℹ️  Znaleziono {count} zawodników w bazie danych")
        
        conn.commit()
        cur.close()
        conn.close()
        
        print("🎉 Baza danych zainicjalizowana pomyślnie!")
        print(f"👥 Zawodnicy: {count if count > 0 else 10}")
        print("🏁 Grupy startowe: 6")
        print("📊 Gotowe do użycia!")
        
        return True
        
    except psycopg2.Error as e:
        print(f"❌ BŁĄD BAZY DANYCH: {e}")
        return False
    except Exception as e:
        print(f"❌ BŁĄD: {e}")
        return False

if __name__ == "__main__":
    print("🏁 SKATECROSS QR - Inicjalizacja bazy danych")
    print("-" * 50)
    
    if init_database():
        print("\n✅ Inicjalizacja zakończona pomyślnie!")
        print("🚀 Możesz teraz uruchomić serwer: python start_server.py")
    else:
        print("\n❌ Inicjalizacja nie powiodła się")
        print("📖 Sprawdź SETUP.md dla instrukcji konfiguracji") 