-- Bezpieczne usuwanie starych indeksów (jeśli istnieją)
DO $$ 
BEGIN
    -- Zawodnicy
    IF EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_zawodnicy_kategoria') THEN
        DROP INDEX idx_zawodnicy_kategoria;
    END IF;
    IF EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_zawodnicy_plec') THEN
        DROP INDEX idx_zawodnicy_plec;
    END IF;
    IF EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_zawodnicy_klub') THEN
        DROP INDEX idx_zawodnicy_klub;
    END IF;
    IF EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_zawodnicy_status') THEN
        DROP INDEX idx_zawodnicy_status;
    END IF;
    IF EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_zawodnicy_compound') THEN
        DROP INDEX idx_zawodnicy_compound;
    END IF;
    
    -- Walki
    IF EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_walki_grupa') THEN
        DROP INDEX idx_walki_grupa;
    END IF;
    IF EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_walki_status') THEN
        DROP INDEX idx_walki_status;
    END IF;
    IF EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_walki_zawodnik1') THEN
        DROP INDEX idx_walki_zawodnik1;
    END IF;
    IF EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_walki_zawodnik2') THEN
        DROP INDEX idx_walki_zawodnik2;
    END IF;
    IF EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_walki_compound') THEN
        DROP INDEX idx_walki_compound;
    END IF;
    
    -- Grupy
    IF EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_grupy_kategoria') THEN
        DROP INDEX idx_grupy_kategoria;
    END IF;
    IF EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_grupy_plec') THEN
        DROP INDEX idx_grupy_plec;
    END IF;
    IF EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_grupy_status') THEN
        DROP INDEX idx_grupy_status;
    END IF;
    IF EXISTS (SELECT 1 FROM pg_indexes WHERE indexname = 'idx_grupy_compound') THEN
        DROP INDEX idx_grupy_compound;
    END IF;
END $$;

-- Indeksy dla tabeli zawodników z INCLUDE dla często używanych kolumn
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_zawodnicy_kategoria 
ON zawodnicy(kategoria) INCLUDE (imie, nazwisko);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_zawodnicy_plec 
ON zawodnicy(plec) INCLUDE (imie, nazwisko);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_zawodnicy_klub 
ON zawodnicy(klub) INCLUDE (imie, nazwisko);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_zawodnicy_status 
ON zawodnicy(status) INCLUDE (nr_startowy);

-- Indeks złożony z częściowym filtrowaniem
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_zawodnicy_compound 
ON zawodnicy(kategoria, plec, status)
WHERE status IS NOT NULL;

-- Indeksy dla tabeli walk z optymalizacją pod częste zapytania
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_walki_grupa 
ON walki(grupa) INCLUDE (status);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_walki_status 
ON walki(status) INCLUDE (grupa);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_walki_zawodnik1 
ON walki(zawodnik1_id) INCLUDE (status, grupa);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_walki_zawodnik2 
ON walki(zawodnik2_id) INCLUDE (status, grupa);

-- Indeks złożony z częściowym filtrowaniem
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_walki_compound 
ON walki(grupa, status)
WHERE status != 'CANCELLED';

-- Indeksy dla tabeli grup z INCLUDE dla często używanych kolumn
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_grupy_kategoria 
ON grupy(kategoria) INCLUDE (nazwa);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_grupy_plec 
ON grupy(plec) INCLUDE (nazwa);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_grupy_status 
ON grupy(status) INCLUDE (nazwa);

-- Indeks złożony z częściowym filtrowaniem
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_grupy_compound 
ON grupy(kategoria, plec, status)
WHERE status != 'DELETED';

-- Indeksy dla tabeli wyniki
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_wyniki_status 
ON wyniki(status) INCLUDE (czas_przejazdu_s);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_wyniki_compound
ON wyniki(nr_startowy, status)
WHERE status = 'FINISHED';

-- Indeksy dla tabeli checkpoints
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_checkpoints_name 
ON checkpoints(checkpoint_name, timestamp DESC);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_checkpoints_timestamp 
ON checkpoints(timestamp DESC)
INCLUDE (nr_startowy, checkpoint_name);

-- Dodanie statystyk dla optymalizatora zapytań
ANALYZE zawodnicy;
ANALYZE walki;
ANALYZE grupy; 