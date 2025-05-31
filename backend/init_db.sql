-- Tabela zawodników
CREATE TABLE IF NOT EXISTS zawodnicy (
    nr_startowy INT PRIMARY KEY,
    imie VARCHAR(50),
    nazwisko VARCHAR(50),
    kategoria VARCHAR(20),
    plec CHAR(1),
    klub VARCHAR(100),
    qr_code VARCHAR(50),
    checked_in BOOLEAN DEFAULT FALSE,
    check_in_time TIMESTAMP
);

-- Tabela wyników
CREATE TABLE IF NOT EXISTS wyniki (
    id SERIAL PRIMARY KEY,
    nr_startowy INT REFERENCES zawodnicy(nr_startowy),
    czas_przejazdu_s FLOAT,
    status VARCHAR(20) DEFAULT 'NOT_STARTED',
    UNIQUE(nr_startowy)
);

-- Tabela checkpointów
CREATE TABLE IF NOT EXISTS checkpoints (
    id SERIAL PRIMARY KEY,
    nr_startowy INT REFERENCES zawodnicy(nr_startowy),
    checkpoint_name VARCHAR(50),
    qr_code VARCHAR(50),
    device_id VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela klubów
CREATE TABLE IF NOT EXISTS kluby (
    id SERIAL PRIMARY KEY,
    nazwa VARCHAR(100) UNIQUE,
    miasto VARCHAR(100),
    utworzony_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indeksy
CREATE INDEX IF NOT EXISTS idx_checkpoints_nr_startowy ON checkpoints(nr_startowy);
CREATE INDEX IF NOT EXISTS idx_checkpoints_checkpoint_name ON checkpoints(checkpoint_name);
CREATE INDEX IF NOT EXISTS idx_checkpoints_combined ON checkpoints(nr_startowy, checkpoint_name);
CREATE INDEX IF NOT EXISTS idx_zawodnicy_kategoria_plec ON zawodnicy(kategoria, plec);
CREATE INDEX IF NOT EXISTS idx_zawodnicy_checked_in ON zawodnicy(checked_in); 