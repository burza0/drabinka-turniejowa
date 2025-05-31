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

def check_data():
    """Sprawdza dane w tabelach"""
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # Sprawdź tabelę zawodników
        logging.info("Sprawdzam tabelę zawodników...")
        cur.execute("""
            SELECT COUNT(*) FROM zawodnicy
        """)
        total = cur.fetchone()[0]
        logging.info(f"Łączna liczba zawodników: {total}")
        
        # Sprawdź kategorie i płeć
        cur.execute("""
            SELECT kategoria, plec, COUNT(*) 
            FROM zawodnicy 
            GROUP BY kategoria, plec 
            ORDER BY kategoria, plec
        """)
        rows = cur.fetchall()
        logging.info("\nPodział na kategorie i płeć:")
        for row in rows:
            logging.info(f"  {row[0]} {row[1]}: {row[2]} zawodników")
        
        # Sprawdź połączenie z tabelą wyniki
        logging.info("\nSprawdzam połączenie z tabelą wyniki...")
        cur.execute("""
            SELECT 
                COUNT(*) as total_wyniki,
                COUNT(*) FILTER (WHERE w.status = 'FINISHED') as finished,
                COUNT(*) FILTER (WHERE w.status = 'NOT_STARTED') as not_started,
                COUNT(*) FILTER (WHERE w.status = 'DNF') as dnf,
                COUNT(*) FILTER (WHERE w.status = 'DSQ') as dsq
            FROM wyniki w
        """)
        wyniki = cur.fetchone()
        logging.info(f"Łączna liczba wyników: {wyniki[0]}")
        logging.info(f"  - FINISHED: {wyniki[1]}")
        logging.info(f"  - NOT_STARTED: {wyniki[2]}")
        logging.info(f"  - DNF: {wyniki[3]}")
        logging.info(f"  - DSQ: {wyniki[4]}")
        
        # Sprawdź niespójności
        logging.info("\nSprawdzam niespójności...")
        cur.execute("""
            SELECT COUNT(*) 
            FROM zawodnicy z 
            LEFT JOIN wyniki w ON z.nr_startowy = w.nr_startowy 
            WHERE w.nr_startowy IS NULL
        """)
        missing_wyniki = cur.fetchone()[0]
        if missing_wyniki > 0:
            logging.warning(f"⚠️ {missing_wyniki} zawodników nie ma przypisanych wyników!")
        
        cur.execute("""
            SELECT COUNT(*) 
            FROM wyniki w 
            LEFT JOIN zawodnicy z ON w.nr_startowy = z.nr_startowy 
            WHERE z.nr_startowy IS NULL
        """)
        orphaned_wyniki = cur.fetchone()[0]
        if orphaned_wyniki > 0:
            logging.warning(f"⚠️ {orphaned_wyniki} wyników nie ma przypisanych zawodników!")
        
        # Sprawdź indeksy
        logging.info("\nSprawdzam indeksy...")
        cur.execute("""
            SELECT 
                schemaname, 
                tablename, 
                indexname, 
                indexdef 
            FROM pg_indexes 
            WHERE schemaname = 'public' 
            AND tablename IN ('zawodnicy', 'wyniki')
            ORDER BY tablename, indexname
        """)
        indexes = cur.fetchall()
        logging.info("Znalezione indeksy:")
        for idx in indexes:
            logging.info(f"  - {idx[2]} na tabeli {idx[1]}")
            logging.info(f"    {idx[3]}")
        
    except Exception as e:
        logging.error(f"❌ Błąd: {str(e)}")
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    check_data() 