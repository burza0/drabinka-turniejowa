-- =============================================
-- SKATECROSS QR Enhanced Database Schema
-- Migration 04: Rozszerzona baza dla realnych danych
-- Wersja: 2.0.0
-- Data: 2025-06-22
-- =============================================

BEGIN;

-- === 1. ROZSZERZENIE TABELI ZAWODNIKÓW ===

-- Dodaj brakujące kolumny do zawodników
ALTER TABLE zawodnicy 
ADD COLUMN IF NOT EXISTS data_urodzenia DATE,
ADD COLUMN IF NOT EXISTS email VARCHAR(255),
ADD COLUMN IF NOT EXISTS telefon VARCHAR(20),
ADD COLUMN IF NOT EXISTS adres TEXT,
ADD COLUMN IF NOT EXISTS numery_licencyjne JSONB DEFAULT '{}',
ADD COLUMN IF NOT EXISTS ubezpieczenie_data_waznosci DATE,
ADD COLUMN IF NOT EXISTS zgoda_marketing BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS uwagi TEXT,
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Dodaj constraints
ALTER TABLE zawodnicy 
ADD CONSTRAINT IF NOT EXISTS check_plec CHECK (plec IN ('M', 'K', 'I')); -- Dodano 'I' dla inne/nieustalona

-- === 2. NOWA TABELA KATEGORII ===

CREATE TABLE IF NOT EXISTS kategorie (
    id SERIAL PRIMARY KEY,
    nazwa VARCHAR(50) UNIQUE NOT NULL,
    wiek_min INTEGER,
    wiek_max INTEGER,
    opis TEXT,
    aktywna BOOLEAN DEFAULT TRUE,
    kolejnosc_wyswietlania INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Wstaw standardowe kategorie
INSERT INTO kategorie (nazwa, wiek_min, wiek_max, opis, kolejnosc_wyswietlania) VALUES
('Mini', 4, 6, 'Najmłodsi zawodnicy, pierwsze kroki na rolkach', 1),
('Junior D', 7, 8, 'Początkujący juniorzy', 2),
('Junior C', 9, 10, 'Średni poziom juniorów', 3),
('Junior B', 11, 12, 'Zaawansowani juniorzy', 4),
('Junior A', 13, 14, 'Najstarsi juniorzy', 5),
('Cadet', 15, 16, 'Kategoria cadet', 6),
('Junior', 17, 18, 'Kategoria junior', 7),
('Senior', 19, 35, 'Kategoria senior', 8),
('Master 35+', 35, 45, 'Kategoria master 35+', 9),
('Master 45+', 45, 55, 'Kategoria master 45+', 10),
('Master 55+', 55, 999, 'Kategoria master 55+', 11)
ON CONFLICT (nazwa) DO NOTHING;

-- === 3. ROZSZERZENIE TABELI KLUBÓW ===

ALTER TABLE kluby 
ADD COLUMN IF NOT EXISTS adres TEXT,
ADD COLUMN IF NOT EXISTS kontakt_email VARCHAR(255),
ADD COLUMN IF NOT EXISTS kontakt_telefon VARCHAR(20),
ADD COLUMN IF NOT EXISTS strona_www VARCHAR(255),
ADD COLUMN IF NOT EXISTS logo_url VARCHAR(500),
ADD COLUMN IF NOT EXISTS aktywny BOOLEAN DEFAULT TRUE,
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- === 4. NOWA TABELA ZAWODÓW/EVENTÓW ===

CREATE TABLE IF NOT EXISTS eventy (
    id SERIAL PRIMARY KEY,
    nazwa VARCHAR(200) NOT NULL,
    data_start DATE NOT NULL,
    data_koniec DATE,
    lokalizacja VARCHAR(200),
    adres TEXT,
    typ_eventu VARCHAR(50) DEFAULT 'zawody' CHECK (typ_eventu IN ('zawody', 'trening', 'oboz', 'turniej')),
    status VARCHAR(20) DEFAULT 'planowane' CHECK (status IN ('planowane', 'aktywne', 'zakonczone', 'anulowane')),
    opis TEXT,
    organizator VARCHAR(200),
    kontakt_organizator JSONB DEFAULT '{}',
    regulamin_url VARCHAR(500),
    rejestracja_otwarta BOOLEAN DEFAULT TRUE,
    rejestracja_deadline TIMESTAMP,
    oplata_startowa DECIMAL(10,2),
    max_uczestnikow INTEGER,
    config JSONB DEFAULT '{}', -- Konfiguracja specyficzna dla eventu
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- === 5. NOWA TABELA REJESTRACJI ===

CREATE TABLE IF NOT EXISTS rejestracje (
    id SERIAL PRIMARY KEY,
    event_id INTEGER REFERENCES eventy(id) ON DELETE CASCADE,
    nr_startowy INTEGER REFERENCES zawodnicy(nr_startowy) ON DELETE CASCADE,
    data_rejestracji TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'zarejestrowany' CHECK (status IN ('zarejestrowany', 'potwierdzony', 'anulowany', 'niestawienie')),
    oplata_status VARCHAR(20) DEFAULT 'nieoplacone' CHECK (oplata_status IN ('nieoplacone', 'oplacone', 'zwrocone')),
    uwagi TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(event_id, nr_startowy)
);

-- === 6. ROZSZERZENIE TABELI WYNIKÓW ===

-- Usuń ograniczenie PRIMARY KEY z nr_startowy (może być wiele wyników dla zawodnika w różnych eventach)
ALTER TABLE wyniki DROP CONSTRAINT IF EXISTS wyniki_pkey;
ALTER TABLE wyniki ADD COLUMN IF NOT EXISTS id SERIAL;
ALTER TABLE wyniki ADD CONSTRAINT wyniki_pkey PRIMARY KEY (id);

-- Dodaj kolumny
ALTER TABLE wyniki 
ADD COLUMN IF NOT EXISTS event_id INTEGER REFERENCES eventy(id) ON DELETE CASCADE,
ADD COLUMN IF NOT EXISTS kategoria_w_wynikach VARCHAR(50),
ADD COLUMN IF NOT EXISTS czas_start TIMESTAMP,
ADD COLUMN IF NOT EXISTS czas_meta TIMESTAMP,
ADD COLUMN IF NOT EXISTS split_times JSONB DEFAULT '[]',
ADD COLUMN IF NOT EXISTS pozycja_w_kategorii INTEGER,
ADD COLUMN IF NOT EXISTS pozycja_generalna INTEGER,
ADD COLUMN IF NOT EXISTS punkty DECIMAL(10,2) DEFAULT 0,
ADD COLUMN IF NOT EXISTS uwagi TEXT,
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Nowy unique constraint
ALTER TABLE wyniki ADD CONSTRAINT unique_zawodnik_event UNIQUE (nr_startowy, event_id);

-- === 7. NOWA TABELA RANKINGÓW ===

CREATE TABLE IF NOT EXISTS rankingi (
    id SERIAL PRIMARY KEY,
    sezon INTEGER NOT NULL,
    typ_rankingu VARCHAR(50) NOT NULL CHECK (typ_rankingu IN ('indywidualny', 'generalny', 'klubowy_total', 'klubowy_top3', 'medalowy')),
    nr_startowy INTEGER REFERENCES zawodnicy(nr_startowy),
    klub_id INTEGER REFERENCES kluby(id),
    kategoria VARCHAR(50),
    plec CHAR(1),
    pozycja INTEGER NOT NULL,
    punkty DECIMAL(10,2) DEFAULT 0,
    liczba_startow INTEGER DEFAULT 0,
    najlepszy_czas DECIMAL(10,3),
    medale JSONB DEFAULT '{"zlote": 0, "srebrne": 0, "brazowe": 0}',
    dane_szczegolowe JSONB DEFAULT '{}',
    ostatnia_aktualizacja TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- === 8. NOWA TABELA SYSTEMU PUNKTOWEGO ===

CREATE TABLE IF NOT EXISTS system_punktowy (
    id SERIAL PRIMARY KEY,
    nazwa VARCHAR(100) NOT NULL,
    opis TEXT,
    pozycje_punkty JSONB NOT NULL, -- {"1": 100, "2": 80, "3": 60, ...}
    aktywny BOOLEAN DEFAULT TRUE,
    sezon INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dodaj standardowy system punktowy
INSERT INTO system_punktowy (nazwa, opis, pozycje_punkty, aktywny, sezon) VALUES
('Standard SKATECROSS 2025', 'Standardowy system punktowy dla sezonu 2025', 
 '{"1": 100, "2": 80, "3": 60, "4": 50, "5": 45, "6": 40, "7": 36, "8": 32, "9": 29, "10": 26, "11": 24, "12": 22, "13": 20, "14": 18, "15": 16, "16": 15, "17": 14, "18": 13, "19": 12, "20": 11, "21": 10, "22": 9, "23": 8, "24": 7, "25": 6, "26": 5, "27": 4, "28": 3, "29": 2, "30": 1, "31": 1, "32": 1}', 
 true, 2025)
ON CONFLICT DO NOTHING;

-- === 9. NOWA TABELA IMPORTÓW/EKSPORTÓW ===

CREATE TABLE IF NOT EXISTS import_export_logs (
    id SERIAL PRIMARY KEY,
    typ VARCHAR(20) NOT NULL CHECK (typ IN ('import', 'export')),
    format VARCHAR(20) NOT NULL CHECK (format IN ('csv', 'xlsx', 'json', 'xml')),
    tabela VARCHAR(50) NOT NULL,
    nazwa_pliku VARCHAR(255),
    rozmiar_pliku INTEGER,
    liczba_rekordow INTEGER,
    status VARCHAR(20) DEFAULT 'w_toku' CHECK (status IN ('w_toku', 'sukces', 'bledny', 'anulowany')),
    bledy JSONB DEFAULT '[]',
    ostrzezenia JSONB DEFAULT '[]',
    metadane JSONB DEFAULT '{}',
    user_id VARCHAR(100), -- ID użytkownika wykonującego operację
    czas_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    czas_koniec TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- === 10. NOWA TABELA AUDIT TRAIL ===

CREATE TABLE IF NOT EXISTS audit_log (
    id SERIAL PRIMARY KEY,
    tabela VARCHAR(50) NOT NULL,
    rekord_id INTEGER NOT NULL,
    akcja VARCHAR(20) NOT NULL CHECK (akcja IN ('INSERT', 'UPDATE', 'DELETE')),
    stare_dane JSONB,
    nowe_dane JSONB,
    user_id VARCHAR(100),
    ip_address INET,
    user_agent TEXT,
    czas_akcji TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- === 11. INDEKSY WYDAJNOŚCIOWE ===

-- Indeksy dla zawodników
CREATE INDEX IF NOT EXISTS idx_zawodnicy_email ON zawodnicy(email);
CREATE INDEX IF NOT EXISTS idx_zawodnicy_telefon ON zawodnicy(telefon);
CREATE INDEX IF NOT EXISTS idx_zawodnicy_data_urodzenia ON zawodnicy(data_urodzenia);
CREATE INDEX IF NOT EXISTS idx_zawodnicy_updated_at ON zawodnicy(updated_at);

-- Indeksy dla eventów
CREATE INDEX IF NOT EXISTS idx_eventy_data_start ON eventy(data_start);
CREATE INDEX IF NOT EXISTS idx_eventy_status ON eventy(status);
CREATE INDEX IF NOT EXISTS idx_eventy_typ ON eventy(typ_eventu);

-- Indeksy dla rejestracji
CREATE INDEX IF NOT EXISTS idx_rejestracje_event_id ON rejestracje(event_id);
CREATE INDEX IF NOT EXISTS idx_rejestracje_status ON rejestracje(status);
CREATE INDEX IF NOT EXISTS idx_rejestracje_data ON rejestracje(data_rejestracji);

-- Indeksy dla wyników
CREATE INDEX IF NOT EXISTS idx_wyniki_event_id ON wyniki(event_id);
CREATE INDEX IF NOT EXISTS idx_wyniki_pozycja_kategoria ON wyniki(pozycja_w_kategorii);
CREATE INDEX IF NOT EXISTS idx_wyniki_pozycja_generalna ON wyniki(pozycja_generalna);
CREATE INDEX IF NOT EXISTS idx_wyniki_punkty ON wyniki(punkty);

-- Indeksy dla rankingów
CREATE INDEX IF NOT EXISTS idx_rankingi_sezon_typ ON rankingi(sezon, typ_rankingu);
CREATE INDEX IF NOT EXISTS idx_rankingi_pozycja ON rankingi(pozycja);
CREATE INDEX IF NOT EXISTS idx_rankingi_kategoria_plec ON rankingi(kategoria, plec);

-- Indeksy dla audit
CREATE INDEX IF NOT EXISTS idx_audit_log_tabela ON audit_log(tabela);
CREATE INDEX IF NOT EXISTS idx_audit_log_czas ON audit_log(czas_akcji);
CREATE INDEX IF NOT EXISTS idx_audit_log_user ON audit_log(user_id);

-- === 12. TRIGGERY DO AUTOMATYCZNYCH AKTUALIZACJI ===

-- Trigger dla updated_at w zawodnikach
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_zawodnicy_updated_at 
    BEFORE UPDATE ON zawodnicy 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_kluby_updated_at 
    BEFORE UPDATE ON kluby 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_eventy_updated_at 
    BEFORE UPDATE ON eventy 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_rejestracje_updated_at 
    BEFORE UPDATE ON rejestracje 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_wyniki_updated_at 
    BEFORE UPDATE ON wyniki 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Trigger dla audit log
CREATE OR REPLACE FUNCTION audit_trigger_function()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        INSERT INTO audit_log (tabela, rekord_id, akcja, stare_dane, user_id)
        VALUES (TG_TABLE_NAME, OLD.id, TG_OP, row_to_json(OLD), current_setting('app.current_user_id', true));
        RETURN OLD;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO audit_log (tabela, rekord_id, akcja, stare_dane, nowe_dane, user_id)
        VALUES (TG_TABLE_NAME, NEW.id, TG_OP, row_to_json(OLD), row_to_json(NEW), current_setting('app.current_user_id', true));
        RETURN NEW;
    ELSIF TG_OP = 'INSERT' THEN
        INSERT INTO audit_log (tabela, rekord_id, akcja, nowe_dane, user_id)
        VALUES (TG_TABLE_NAME, NEW.id, TG_OP, row_to_json(NEW), current_setting('app.current_user_id', true));
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ language 'plpgsql';

-- === 13. WIDOKI DLA RAPORTÓW ===

-- Widok zawodników z kategoriami
CREATE OR REPLACE VIEW v_zawodnicy_full AS
SELECT 
    z.*,
    k.nazwa as kategoria_pelna_nazwa,
    k.wiek_min,
    k.wiek_max,
    EXTRACT(YEAR FROM AGE(z.data_urodzenia)) as wiek,
    kl.nazwa as klub_nazwa,
    kl.miasto as klub_miasto
FROM zawodnicy z
LEFT JOIN kategorie k ON z.kategoria = k.nazwa
LEFT JOIN kluby kl ON z.klub = kl.nazwa;

-- Widok aktualnych wyników
CREATE OR REPLACE VIEW v_wyniki_aktualne AS
SELECT 
    w.*,
    z.imie,
    z.nazwisko,
    z.kategoria,
    z.plec,
    z.klub,
    e.nazwa as event_nazwa,
    e.data_start as event_data
FROM wyniki w
JOIN zawodnicy z ON w.nr_startowy = z.nr_startowy
LEFT JOIN eventy e ON w.event_id = e.id;

-- === 14. FUNCTIONS POMOCNICZE ===

-- Funkcja do obliczania wieku na podstawie daty urodzenia
CREATE OR REPLACE FUNCTION oblicz_wiek(data_urodzenia DATE)
RETURNS INTEGER AS $$
BEGIN
    IF data_urodzenia IS NULL THEN
        RETURN NULL;
    END IF;
    RETURN EXTRACT(YEAR FROM AGE(data_urodzenia));
END;
$$ LANGUAGE plpgsql;

-- Funkcja do obliczania punktów na podstawie pozycji
CREATE OR REPLACE FUNCTION oblicz_punkty(pozycja INTEGER, system_id INTEGER DEFAULT 1)
RETURNS DECIMAL(10,2) AS $$
DECLARE
    punkty_json JSONB;
    punkty_val TEXT;
BEGIN
    SELECT pozycje_punkty INTO punkty_json
    FROM system_punktowy 
    WHERE id = system_id AND aktywny = true;
    
    IF punkty_json IS NULL THEN
        RETURN 0;
    END IF;
    
    punkty_val := punkty_json->>pozycja::text;
    
    IF punkty_val IS NULL THEN
        RETURN 0;
    END IF;
    
    RETURN punkty_val::DECIMAL(10,2);
END;
$$ LANGUAGE plpgsql;

-- === 15. KOMENTARZE DOKUMENTACYJNE ===

COMMENT ON TABLE zawodnicy IS 'Rozszerzona tabela zawodników z pełnymi danymi osobowymi';
COMMENT ON TABLE kategorie IS 'Definicje kategorii wiekowych z limitami';
COMMENT ON TABLE eventy IS 'Wydarzenia/zawody w systemie';
COMMENT ON TABLE rejestracje IS 'Rejestracje zawodników na wydarzenia';
COMMENT ON TABLE wyniki IS 'Rozszerzone wyniki z pełnymi czasami i punktami';
COMMENT ON TABLE rankingi IS 'Obliczone rankingi różnych typów';
COMMENT ON TABLE system_punktowy IS 'Systemy punktowe dla różnych sezonów';
COMMENT ON TABLE import_export_logs IS 'Logi operacji import/export';
COMMENT ON TABLE audit_log IS 'Audit trail wszystkich zmian w systemie';

COMMIT;

-- === 16. PRZYKŁADOWE DANE (opcjonalne) ===

-- Możesz odkomentować poniższe linie do dodania przykładowych danych testowych

/*
-- Przykładowy event
INSERT INTO eventy (nazwa, data_start, lokalizacja, typ_eventu, status) VALUES
('SKATECROSS Cup 2025 - Runda 1', '2025-07-15', 'Warszawa', 'zawody', 'planowane');

-- Przykładowe rejestracje (assuming zawodnicy already exist)
INSERT INTO rejestracje (event_id, nr_startowy, status, oplata_status) 
SELECT 1, nr_startowy, 'potwierdzony', 'oplacone' 
FROM zawodnicy 
LIMIT 5;
*/

-- Wyświetl podsumowanie
DO $$
BEGIN
    RAISE NOTICE 'Migration 04 completed successfully!';
    RAISE NOTICE 'Enhanced database schema for real data management created.';
    RAISE NOTICE 'New tables: kategorie, eventy, rejestracje, rankingi, system_punktowy, import_export_logs, audit_log';
    RAISE NOTICE 'Enhanced tables: zawodnicy, kluby, wyniki with additional columns';
    RAISE NOTICE 'Created indexes, triggers, views and helper functions';
END $$; 