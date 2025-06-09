-- SECTRO Live Timing Module - Database Migration
-- Created: 2025-06-08
-- Purpose: Add tables for SECTRO live timing functionality

-- Drop tables if exist (for clean reinstall)
DROP TABLE IF EXISTS sectro_logs CASCADE;
DROP TABLE IF EXISTS sectro_results CASCADE;
DROP TABLE IF EXISTS sectro_measurements CASCADE;
DROP TABLE IF EXISTS sectro_sessions CASCADE;

-- Tabela sesji pomiarów SECTRO
CREATE TABLE sectro_sessions (
    id SERIAL PRIMARY KEY,
    nazwa VARCHAR(100) NOT NULL,
    kategoria VARCHAR(50),
    plec CHAR(1),
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP NULL,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'paused', 'completed', 'cancelled')),
    config JSON DEFAULT '{}',
    wejscie_start INTEGER DEFAULT 1,        -- Numer wejścia dla START (domyślnie 1)
    wejscie_finish INTEGER DEFAULT 4,       -- Numer wejścia dla FINISH (domyślnie 4)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela pomiarów z urządzenia SECTRO
CREATE TABLE sectro_measurements (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES sectro_sessions(id) ON DELETE CASCADE,
    nr_startowy INTEGER REFERENCES zawodnicy(nr_startowy),
    measurement_type VARCHAR(10) NOT NULL CHECK (measurement_type IN ('START', 'FINISH', 'SPLIT')),
    wejscie INTEGER NOT NULL,               -- Numer wejścia SECTRO (1-8)
    timestamp_sectro DECIMAL(15,3) NOT NULL, -- Czas z urządzenia (sekundy od północy)
    timestamp_received TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    raw_frame TEXT NOT NULL,                -- Oryginalna ramka (np. "CZL1123456789")
    processed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela wyników końcowych
CREATE TABLE sectro_results (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES sectro_sessions(id) ON DELETE CASCADE,
    nr_startowy INTEGER REFERENCES zawodnicy(nr_startowy),
    start_time DECIMAL(15,3),               -- Czas startu (timestamp SECTRO)
    finish_time DECIMAL(15,3),              -- Czas mety (timestamp SECTRO)
    total_time DECIMAL(10,3),               -- Czas przejazdu w sekundach
    splits JSON DEFAULT '[]',               -- Split times (array of objects)
    status VARCHAR(20) DEFAULT 'completed' CHECK (status IN ('completed', 'disqualified', 'dns', 'dnf', 'in_progress')),
    position INTEGER,                       -- Pozycja w klasyfikacji
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(session_id, nr_startowy)
);

-- Tabela logów SECTRO
CREATE TABLE sectro_logs (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES sectro_sessions(id) ON DELETE CASCADE,
    log_type VARCHAR(20) NOT NULL CHECK (log_type IN ('INFO', 'ERROR', 'FRAME', 'CONNECTION', 'WARNING')),
    message TEXT NOT NULL,
    raw_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indeksy dla wydajności
CREATE INDEX idx_sectro_measurements_session_id ON sectro_measurements(session_id);
CREATE INDEX idx_sectro_measurements_nr_startowy ON sectro_measurements(nr_startowy);
CREATE INDEX idx_sectro_measurements_timestamp ON sectro_measurements(timestamp_sectro);
CREATE INDEX idx_sectro_results_session_id ON sectro_results(session_id);
CREATE INDEX idx_sectro_results_total_time ON sectro_results(total_time);
CREATE INDEX idx_sectro_logs_session_id ON sectro_logs(session_id);
CREATE INDEX idx_sectro_logs_created_at ON sectro_logs(created_at);

-- Trigger do automatycznego ustawiania updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_sectro_sessions_updated_at 
    BEFORE UPDATE ON sectro_sessions 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_sectro_results_updated_at 
    BEFORE UPDATE ON sectro_results 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Przykładowe dane testowe (opcjonalne)
INSERT INTO sectro_sessions (nazwa, kategoria, plec, status) 
VALUES ('Test Session', 'Junior A', 'M', 'active');

-- Komentarze dla dokumentacji
COMMENT ON TABLE sectro_sessions IS 'Sesje pomiarów SECTRO - zawody/treningi';
COMMENT ON TABLE sectro_measurements IS 'Surowe pomiary z urządzenia SECTRO';
COMMENT ON TABLE sectro_results IS 'Przetworzone wyniki końcowe';
COMMENT ON TABLE sectro_logs IS 'Logi aktywności modułu SECTRO';

COMMENT ON COLUMN sectro_measurements.timestamp_sectro IS 'Czas w sekundach od północy z urządzenia SECTRO';
COMMENT ON COLUMN sectro_measurements.raw_frame IS 'Oryginalna ramka ASCII np. CZL1123456789';
COMMENT ON COLUMN sectro_results.total_time IS 'Czas przejazdu finish_time - start_time w sekundach'; 