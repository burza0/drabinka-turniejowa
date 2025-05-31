#!/usr/bin/env python3
import os
import time
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

def refresh_stats():
    """Odświeża materialized views"""
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # Rozpocznij odświeżanie
        start_time = time.time()
        logging.info("Rozpoczynam odświeżanie materialized views...")
        
        # Odśwież każdy materialized view osobno
        cur.execute("""
            REFRESH MATERIALIZED VIEW CONCURRENTLY mv_statystyki_kategorie_plec;
            REFRESH MATERIALIZED VIEW CONCURRENTLY mv_statystyki_wyniki;
            REFRESH MATERIALIZED VIEW CONCURRENTLY mv_statystyki_qr;
        """)
        conn.commit()
        
        # Zakończ i zapisz czas
        end_time = time.time()
        duration = end_time - start_time
        logging.info(f"Odświeżanie zakończone pomyślnie (czas: {duration:.2f}s)")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        logging.error(f"Błąd podczas odświeżania statystyk: {e}")

def main():
    """Główna pętla programu"""
    logging.info("Uruchamiam proces automatycznego odświeżania statystyk...")
    
    while True:
        try:
            refresh_stats()
            # Odczekaj 5 minut przed kolejnym odświeżeniem
            time.sleep(300)
        except KeyboardInterrupt:
            logging.info("Zatrzymuję proces odświeżania...")
            break
        except Exception as e:
            logging.error(f"Nieoczekiwany błąd: {e}")
            # W przypadku błędu odczekaj 1 minutę przed ponowną próbą
            time.sleep(60)

if __name__ == '__main__':
    main() 