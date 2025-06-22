-- Dodanie tabeli kolejki_startowe
CREATE TABLE IF NOT EXISTS kolejki_startowe (
    id SERIAL PRIMARY KEY,
    kategoria VARCHAR(50) NOT NULL,
    plec VARCHAR(10) NOT NULL,
    nr_startowy INTEGER NOT NULL,
    pozycja INTEGER NOT NULL,
    UNIQUE(kategoria, plec, nr_startowy)
);

-- Indeksy dla szybszego wyszukiwania
CREATE INDEX IF NOT EXISTS idx_kolejki_startowe_kategoria_plec ON kolejki_startowe(kategoria, plec);
CREATE INDEX IF NOT EXISTS idx_kolejki_startowe_nr_startowy ON kolejki_startowe(nr_startowy); 