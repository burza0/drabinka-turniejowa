# Pusty plik Python – do uzupełnienia kodem# Logger SECTRO – MOCK (do rozbudowy)
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")

def insert_wynik(nr_startowy, czas_przejazdu_s, status):
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO wyniki (nr_startowy, czas_przejazdu_s, status)
        VALUES (%s, %s, %s)
        ON CONFLICT (nr_startowy) DO UPDATE SET czas_przejazdu_s = EXCLUDED.czas_przejazdu_s, status = EXCLUDED.status
    """, (nr_startowy, czas_przejazdu_s, status))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    # Przykładowy insert testowy (usuń w wersji produkcyjnej)
    insert_wynik(1, 17.62, 'OK')
    insert_wynik(2, 18.54, 'OK')
    insert_wynik(3, None, 'DNF')
    insert_wynik(4, 20.33, 'OK')
    print("Wyniki testowe zapisane do bazy.")

