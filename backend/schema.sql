-- Indeksy dla tabeli checkpoints
CREATE INDEX IF NOT EXISTS idx_checkpoints_nr_startowy ON checkpoints(nr_startowy);
CREATE INDEX IF NOT EXISTS idx_checkpoints_checkpoint_name ON checkpoints(checkpoint_name);
CREATE INDEX IF NOT EXISTS idx_checkpoints_combined ON checkpoints(nr_startowy, checkpoint_name);
 
-- Indeksy dla tabeli zawodnicy
CREATE INDEX IF NOT EXISTS idx_zawodnicy_kategoria_plec ON zawodnicy(kategoria, plec);
CREATE INDEX IF NOT EXISTS idx_zawodnicy_checked_in ON zawodnicy(checked_in); 