-- Migration 01: Create new start_queue table
-- Date: 2025-06-07
-- Purpose: Unified queue architecture to replace checkpoint-based system

BEGIN;

-- 🏗️ NOWA TABELA KOLEJKI
CREATE TABLE IF NOT EXISTS start_queue (
    id SERIAL PRIMARY KEY,
    nr_startowy INTEGER NOT NULL,
    
    -- 🎯 ŹRÓDŁO DODANIA DO KOLEJKI
    source_type VARCHAR(20) NOT NULL CHECK (source_type IN ('scanned', 'active_group')),
    source_metadata JSONB DEFAULT '{}',
    
    -- 📅 TIMESTAMPS
    added_at TIMESTAMP DEFAULT NOW(),
    scanned_at TIMESTAMP NULL,  -- Kiedy został zeskanowany (jeśli w ogóle)
    
    -- 🔄 STATUS
    status VARCHAR(20) NOT NULL DEFAULT 'waiting' 
           CHECK (status IN ('waiting', 'called', 'finished', 'hidden', 'removed')),
    
    -- 🎪 METADANE
    group_info JSONB DEFAULT '{}', -- kategoria, płeć, nazwa grupy
    queue_position INTEGER DEFAULT 0, -- pozycja w kolejce
    
    -- 🔍 INDEKSY
    CONSTRAINT unique_athlete_in_queue UNIQUE (nr_startowy),
    FOREIGN KEY (nr_startowy) REFERENCES zawodnicy(nr_startowy) ON DELETE CASCADE
);

-- 📈 INDEKSY WYDAJNOŚCIOWE
CREATE INDEX idx_start_queue_status ON start_queue(status);
CREATE INDEX idx_start_queue_source_type ON start_queue(source_type);
CREATE INDEX idx_start_queue_added_at ON start_queue(added_at);
CREATE INDEX idx_start_queue_position ON start_queue(queue_position);

-- 📊 WIDOK KOLEJKI (dla kompatybilności)
CREATE OR REPLACE VIEW v_current_queue AS
SELECT 
    sq.id,
    sq.nr_startowy,
    z.imie,
    z.nazwisko,
    z.kategoria,
    z.plec,
    z.klub,
    sq.source_type,
    sq.status,
    sq.added_at,
    sq.scanned_at,
    sq.queue_position,
    sq.group_info,
    -- Kompatybilność z starym systemem
    CASE 
        WHEN sq.source_type = 'scanned' THEN 'skanowany'
        ELSE 'grupa_aktywna'
    END as legacy_source_type
FROM start_queue sq
JOIN zawodnicy z ON sq.nr_startowy = z.nr_startowy
WHERE sq.status IN ('waiting', 'called')
ORDER BY sq.queue_position, sq.added_at;

COMMIT; 