-- Migration 02: Migrate existing checkpoint data to start_queue
-- Date: 2025-06-07
-- Purpose: Transfer current queue state from checkpoints to unified table

BEGIN;

-- 🔄 MIGRACJA SKANOWANYCH ZAWODNIKÓW
INSERT INTO start_queue (
    nr_startowy, 
    source_type, 
    source_metadata,
    added_at,
    scanned_at,
    status,
    group_info,
    queue_position
)
SELECT DISTINCT
    c.nr_startowy,
    'scanned' as source_type,
    jsonb_build_object(
        'original_checkpoint', 'start-line-verify',
        'device_id', c.device_id,
        'qr_code', c.qr_code
    ) as source_metadata,
    c.timestamp as added_at,
    c.timestamp as scanned_at,
    'waiting' as status,
    jsonb_build_object(
        'kategoria', z.kategoria,
        'plec', z.plec,
        'klub', z.klub
    ) as group_info,
    ROW_NUMBER() OVER (ORDER BY c.timestamp) as queue_position
FROM checkpoints c
JOIN zawodnicy z ON c.nr_startowy = z.nr_startowy
WHERE c.checkpoint_name = 'start-line-verify'
ON CONFLICT (nr_startowy) DO NOTHING;

-- 🎯 MIGRACJA ZAWODNIKÓW Z AKTYWNEJ GRUPY (NIE UKRYTYCH)
WITH active_group AS (
    SELECT kategoria, plec, nazwa, numer_grupy 
    FROM aktywna_grupa_settings 
    LIMIT 1
),
active_group_athletes AS (
    SELECT DISTINCT z.nr_startowy, z.imie, z.nazwisko, z.kategoria, z.plec, z.klub
    FROM zawodnicy z
    CROSS JOIN active_group ag
    WHERE z.kategoria = ag.kategoria 
    AND z.plec = ag.plec
    AND z.checked_in = TRUE
    -- Wykluczamy już skanowanych
    AND z.nr_startowy NOT IN (
        SELECT nr_startowy FROM start_queue WHERE source_type = 'scanned'
    )
    -- Wykluczamy ukrytych
    AND z.nr_startowy NOT IN (
        SELECT nr_startowy FROM checkpoints WHERE checkpoint_name = 'hidden-from-queue'
    )
)
INSERT INTO start_queue (
    nr_startowy,
    source_type,
    source_metadata,
    added_at,
    status,
    group_info,
    queue_position
)
SELECT 
    aga.nr_startowy,
    'active_group' as source_type,
    jsonb_build_object(
        'grupa_numer', (SELECT numer_grupy FROM active_group),
        'grupa_nazwa', (SELECT nazwa FROM active_group),
        'auto_added', true
    ) as source_metadata,
    NOW() as added_at,
    'waiting' as status,
    jsonb_build_object(
        'kategoria', aga.kategoria,
        'plec', aga.plec,
        'klub', aga.klub
    ) as group_info,
    (SELECT COALESCE(MAX(queue_position), 0) FROM start_queue) + ROW_NUMBER() OVER (ORDER BY aga.imie, aga.nazwisko) as queue_position
FROM active_group_athletes aga
ON CONFLICT (nr_startowy) DO NOTHING;

-- 🔍 MIGRACJA UKRYTYCH ZAWODNIKÓW (status = 'hidden')
INSERT INTO start_queue (
    nr_startowy,
    source_type,
    source_metadata,
    added_at,
    status,
    group_info,
    queue_position
)
SELECT DISTINCT
    c.nr_startowy,
    'active_group' as source_type,
    jsonb_build_object(
        'original_checkpoint', 'hidden-from-queue',
        'hidden_at', c.timestamp,
        'migration_note', 'Ukryty w starym systemie'
    ) as source_metadata,
    c.timestamp as added_at,
    'hidden' as status,
    jsonb_build_object(
        'kategoria', z.kategoria,
        'plec', z.plec,
        'klub', z.klub
    ) as group_info,
    0 as queue_position  -- Ukryci nie mają pozycji
FROM checkpoints c
JOIN zawodnicy z ON c.nr_startowy = z.nr_startowy
WHERE c.checkpoint_name = 'hidden-from-queue'
ON CONFLICT (nr_startowy) DO NOTHING;

-- 📊 PODSUMOWANIE MIGRACJI
CREATE TEMP TABLE migration_summary AS
SELECT 
    source_type,
    status,
    COUNT(*) as count
FROM start_queue
GROUP BY source_type, status;

COMMIT; 