#!/usr/bin/env python3
import os
import psycopg2
from dotenv import load_dotenv
import logging

# Konfiguracja logowania
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Załaduj zmienne środowiskowe
load_dotenv()

# Połączenie z bazą danych
DB_URL = os.getenv('DATABASE_URL')

def fix_data():
    """Naprawia niespójności w danych"""
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # Znajdź zawodników bez wyników
        logging.info("Szukam zawodników bez wyników...")
        cur.execute("""
            SELECT z.nr_startowy, z.imie, z.nazwisko 
            FROM zawodnicy z 
            LEFT JOIN wyniki w ON z.nr_startowy = w.nr_startowy 
            WHERE w.nr_startowy IS NULL
        """)
        missing_wyniki = cur.fetchall()
        
        if missing_wyniki:
            logging.info(f"Znaleziono {len(missing_wyniki)} zawodników bez wyników:")
            for zawodnik in missing_wyniki:
                logging.info(f"  - #{zawodnik[0]} {zawodnik[1]} {zawodnik[2]}")
                
                # Dodaj brakujący rekord w tabeli wyniki
                cur.execute("""
                    INSERT INTO wyniki (nr_startowy, status)
                    VALUES (%s, 'NOT_STARTED')
                """, (zawodnik[0],))
                logging.info(f"    ✅ Dodano rekord wyników dla zawodnika #{zawodnik[0]}")
        
        # Znajdź wyniki bez zawodników
        logging.info("\nSprawdzam wyniki bez zawodników...")
        cur.execute("""
            SELECT w.nr_startowy, w.status 
            FROM wyniki w 
            LEFT JOIN zawodnicy z ON w.nr_startowy = z.nr_startowy 
            WHERE z.nr_startowy IS NULL
        """)
        orphaned_wyniki = cur.fetchall()
        
        if orphaned_wyniki:
            logging.info(f"Znaleziono {len(orphaned_wyniki)} wyników bez zawodników:")
            for wynik in orphaned_wyniki:
                logging.info(f"  - #{wynik[0]} (status: {wynik[1]})")
                
                # Usuń osierocone wyniki
                cur.execute("""
                    DELETE FROM wyniki 
                    WHERE nr_startowy = %s
                """, (wynik[0],))
                logging.info(f"    ✅ Usunięto osierocony wynik dla #{wynik[0]}")
        
        # Zatwierdź zmiany
        conn.commit()
        logging.info("\n✅ Wszystkie niespójności naprawione")
        
    except Exception as e:
        logging.error(f"❌ Błąd: {str(e)}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    fix_data() 