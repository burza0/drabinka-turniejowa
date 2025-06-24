-- 🧹 SKATECROSS v36.0 - CLEANUP DATABASE SCRIPT
-- Usuwanie śmieci i naprawianie rozbieżności

-- =============================================
-- FAZA 1: CZYSZCZENIE SECTRO_SESSIONS
-- =============================================

-- 1.1: Anuluj wszystkie sesje bez kategoria/plec (śmieci po testach)
UPDATE sectro_sessions 
SET status = 'cancelled', end_time = CURRENT_TIMESTAMP
WHERE (kategoria IS NULL OR kategoria = '' OR plec IS NULL OR plec = '')
AND status = 'active';

-- 1.2: Anuluj stare sesje aktywne (starsze niż 7 dni)
UPDATE sectro_sessions 
SET status = 'cancelled', end_time = CURRENT_TIMESTAMP
WHERE status = 'active' 
AND created_at < CURRENT_TIMESTAMP - INTERVAL '7 days';

-- 1.3: Zachowaj tylko najnowsze sesje dla każdej grupy
WITH latest_sessions AS (
    SELECT kategoria, plec, MAX(created_at) as latest_date
    FROM sectro_sessions 
    WHERE status = 'active' 
    AND kategoria IS NOT NULL 
    AND plec IS NOT NULL
    GROUP BY kategoria, plec
)
UPDATE sectro_sessions 
SET status = 'cancelled', end_time = CURRENT_TIMESTAMP
WHERE status = 'active' 
AND kategoria IS NOT NULL 
AND plec IS NOT NULL
AND NOT EXISTS (
    SELECT 1 FROM latest_sessions ls 
    WHERE ls.kategoria = sectro_sessions.kategoria 
    AND ls.plec = sectro_sessions.plec 
    AND ls.latest_date = sectro_sessions.created_at
);

-- =============================================
-- FAZA 2: USUWANIE LEGACY TABEL
-- =============================================

-- 2.1: Usuwanie legacy kolejek
TRUNCATE TABLE start_queue;
TRUNCATE TABLE unified_start_queue;
TRUNCATE TABLE kolejki_startowe;
TRUNCATE TABLE aktywna_grupa_settings;

-- 2.2: Usuwanie legacy checkpoints (opcjonalnie)
-- DELETE FROM checkpoints WHERE checkpoint_name IN ('active-group-queue', 'hidden-from-queue');

-- =============================================
-- FAZA 3: CZYSZCZENIE WYNIKÓW
-- =============================================

-- 3.1: Zachowaj tylko wyniki z aktywnych sesji SECTRO
-- (Opcjonalnie - może zachować dla historii)
-- UPDATE wyniki SET status = 'ARCHIVED' WHERE status = 'FINISHED';

-- =============================================
-- FAZA 4: OPTYMALIZACJA SECTRO_RESULTS
-- =============================================

-- 4.1: Usuń wyniki z anulowanych sesji
DELETE FROM sectro_results 
WHERE session_id IN (
    SELECT id FROM sectro_sessions WHERE status = 'cancelled'
);

-- 4.2: Usuń measurements z anulowanych sesji
DELETE FROM sectro_measurements 
WHERE session_id IN (
    SELECT id FROM sectro_sessions WHERE status = 'cancelled'
);

-- 4.3: Usuń logi z anulowanych sesji
DELETE FROM sectro_logs 
WHERE session_id IN (
    SELECT id FROM sectro_sessions WHERE status = 'cancelled'
);

-- =============================================
-- FAZA 5: WERYFIKACJA PO CLEANUP
-- =============================================

-- Sprawdź aktywne sesje po cleanup
SELECT 'AKTYWNE SESJE PO CLEANUP:' as info;
SELECT id, nazwa, kategoria, plec, status, created_at 
FROM sectro_sessions 
WHERE status IN ('active', 'timing')
ORDER BY created_at DESC;

-- Sprawdź statystyki tabel
SELECT 'STATYSTYKI TABEL PO CLEANUP:' as info;
SELECT 
    'sectro_sessions' as tabela,
    COUNT(*) as total,
    COUNT(CASE WHEN status = 'active' THEN 1 END) as active
FROM sectro_sessions
UNION ALL
SELECT 
    'sectro_results' as tabela,
    COUNT(*) as total,
    COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed
FROM sectro_results
UNION ALL
SELECT 
    'zawodnicy' as tabela,
    COUNT(*) as total,
    COUNT(CASE WHEN checked_in = true THEN 1 END) as checked_in
FROM zawodnicy;

-- =============================================
-- BACKUP COMMANDS (uruchomić przed cleanup)
-- =============================================

-- CREATE TABLE sectro_sessions_backup AS SELECT * FROM sectro_sessions;
-- CREATE TABLE sectro_results_backup AS SELECT * FROM sectro_results;
-- CREATE TABLE sectro_measurements_backup AS SELECT * FROM sectro_measurements; 