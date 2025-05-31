-- Materialized view dla statystyk zawodników według kategorii i płci
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

-- Indeks na materialized view dla szybszego dostępu
CREATE UNIQUE INDEX idx_mv_statystyki_kategorie_plec 
ON mv_statystyki_kategorie_plec (kategoria, plec);

-- Materialized view dla statystyk wyników
CREATE MATERIALIZED VIEW mv_statystyki_wyniki AS
SELECT 
    w.status,
    COUNT(*) as liczba,
    MIN(CAST(w.czas_przejazdu_s AS FLOAT)) FILTER (WHERE w.status = 'FINISHED') as najlepszy_czas,
    MAX(CAST(w.czas_przejazdu_s AS FLOAT)) FILTER (WHERE w.status = 'FINISHED') as najgorszy_czas,
    AVG(CAST(w.czas_przejazdu_s AS FLOAT)) FILTER (WHERE w.status = 'FINISHED') as sredni_czas,
    z.kategoria,
    z.plec
FROM wyniki w
JOIN zawodnicy z ON w.nr_startowy = z.nr_startowy
GROUP BY w.status, z.kategoria, z.plec
ORDER BY w.status, z.kategoria, z.plec;

-- Indeks na materialized view dla wyników
CREATE UNIQUE INDEX idx_mv_statystyki_wyniki 
ON mv_statystyki_wyniki (status, kategoria, plec);

-- Materialized view dla statystyk QR i checkpointów
CREATE MATERIALIZED VIEW mv_statystyki_qr AS
SELECT 
    COUNT(*) as total_zawodnikow,
    COUNT(*) FILTER (WHERE qr_code IS NOT NULL) as z_qr_kodami,
    COUNT(*) FILTER (WHERE checked_in = TRUE) as zameldowanych,
    COUNT(*) FILTER (WHERE qr_code IS NULL) as bez_qr_kodow,
    kategoria,
    plec
FROM zawodnicy
GROUP BY kategoria, plec;

-- Indeks na materialized view dla QR
CREATE UNIQUE INDEX idx_mv_statystyki_qr 
ON mv_statystyki_qr (kategoria, plec);

-- Funkcja do odświeżania wszystkich materialized views
CREATE OR REPLACE FUNCTION refresh_all_materialized_views()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_statystyki_kategorie_plec;
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_statystyki_wyniki;
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_statystyki_qr;
END;
$$ LANGUAGE plpgsql; 