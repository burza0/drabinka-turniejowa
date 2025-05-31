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

def check_and_create_views():
    """Sprawdza i tworzy materialized views jeśli nie istnieją"""
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # Sprawdź czy views istnieją
        cur.execute("""
            SELECT viewname 
            FROM pg_catalog.pg_views
            WHERE schemaname = 'public'
            UNION
            SELECT matviewname
            FROM pg_catalog.pg_matviews
            WHERE schemaname = 'public'
        """)
        
        existing_views = [row[0] for row in cur.fetchall()]
        logging.info(f"Istniejące widoki: {existing_views}")
        
        # Utwórz mv_statystyki_kategorie_plec jeśli nie istnieje
        if 'mv_statystyki_kategorie_plec' not in existing_views:
            logging.info("Tworzę mv_statystyki_kategorie_plec...")
            cur.execute("""
                CREATE MATERIALIZED VIEW mv_statystyki_kategorie_plec AS
                SELECT 
                    kategoria,
                    plec,
                    COUNT(*) as liczba,
                    COUNT(*) FILTER (WHERE checked_in = TRUE) as zameldowani,
                    COUNT(*) FILTER (WHERE qr_code IS NOT NULL) as z_qr_kodami
                FROM zawodnicy 
                WHERE kategoria IS NOT NULL AND plec IS NOT NULL
                GROUP BY kategoria, plec 
                ORDER BY kategoria, plec;
                
                CREATE UNIQUE INDEX idx_mv_statystyki_kategorie_plec 
                ON mv_statystyki_kategorie_plec (kategoria, plec);
            """)
            logging.info("✅ mv_statystyki_kategorie_plec utworzony")
        
        # Utwórz mv_statystyki_wyniki jeśli nie istnieje
        if 'mv_statystyki_wyniki' not in existing_views:
            logging.info("Tworzę mv_statystyki_wyniki...")
            cur.execute("""
                CREATE MATERIALIZED VIEW mv_statystyki_wyniki AS
                SELECT 
                    z.kategoria,
                    z.plec,
                    w.status,
                    COUNT(*) as liczba,
                    MIN(w.czas_przejazdu_s) as najlepszy_czas,
                    MAX(w.czas_przejazdu_s) as najgorszy_czas,
                    AVG(w.czas_przejazdu_s) as sredni_czas
                FROM zawodnicy z
                JOIN wyniki w ON z.nr_startowy = w.nr_startowy
                WHERE z.kategoria IS NOT NULL AND z.plec IS NOT NULL
                GROUP BY z.kategoria, z.plec, w.status;
                
                CREATE UNIQUE INDEX idx_mv_statystyki_wyniki 
                ON mv_statystyki_wyniki (kategoria, plec, status);
            """)
            logging.info("✅ mv_statystyki_wyniki utworzony")
        
        # Utwórz mv_statystyki_qr jeśli nie istnieje
        if 'mv_statystyki_qr' not in existing_views:
            logging.info("Tworzę mv_statystyki_qr...")
            cur.execute("""
                CREATE MATERIALIZED VIEW mv_statystyki_qr AS
                SELECT 
                    kategoria,
                    COUNT(*) as total_zawodnikow,
                    COUNT(*) FILTER (WHERE qr_code IS NOT NULL) as z_qr_kodami,
                    COUNT(*) FILTER (WHERE checked_in = TRUE) as zameldowanych,
                    COUNT(*) FILTER (WHERE qr_code IS NULL) as bez_qr_kodow
                FROM zawodnicy
                WHERE kategoria IS NOT NULL
                GROUP BY kategoria;
                
                CREATE UNIQUE INDEX idx_mv_statystyki_qr 
                ON mv_statystyki_qr (kategoria);
            """)
            logging.info("✅ mv_statystyki_qr utworzony")
        
        # Odśwież wszystkie materialized views
        for view in ['mv_statystyki_kategorie_plec', 'mv_statystyki_wyniki', 'mv_statystyki_qr']:
            if view in existing_views:
                logging.info(f"Odświeżam {view}...")
                cur.execute(f"REFRESH MATERIALIZED VIEW {view}")
                logging.info(f"✅ {view} odświeżony")
        
        conn.commit()
        logging.info("✅ Wszystkie operacje zakończone sukcesem")
        
    except Exception as e:
        logging.error(f"❌ Błąd: {str(e)}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

if __name__ == '__main__':
    check_and_create_views() 