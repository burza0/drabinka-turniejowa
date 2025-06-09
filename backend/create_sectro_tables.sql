-- Quick SECTRO tables creation
CREATE TABLE IF NOT EXISTS sectro_sessions (
    id SERIAL PRIMARY KEY,
    nazwa VARCHAR(100) NOT NULL,
    kategoria VARCHAR(50),
    plec CHAR(1),
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP NULL,
    status VARCHAR(20) DEFAULT 'created',
    wejscie_start INTEGER DEFAULT 1,
    wejscie_finish INTEGER DEFAULT 4,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sectro_results (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES sectro_sessions(id),
    nr_startowy INTEGER,
    start_time DECIMAL(15,3),
    finish_time DECIMAL(15,3),
    total_time DECIMAL(10,3),
    status VARCHAR(20) DEFAULT 'completed',
    position INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(session_id, nr_startowy)
);

-- Test data
INSERT INTO sectro_sessions (nazwa, kategoria, plec, status) 
VALUES ('Test Session', 'Wszystkie', 'M', 'active') 
ON CONFLICT DO NOTHING; 