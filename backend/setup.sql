CREATE TABLE zawodnicy (
    nr_startowy INT PRIMARY KEY,
    imie VARCHAR(50),
    nazwisko VARCHAR(50),
    kategoria VARCHAR(20)
);

CREATE TABLE wyniki (
    id SERIAL PRIMARY KEY,
    nr_startowy INT REFERENCES zawodnicy(nr_startowy),
    czas_przejazdu_s VARCHAR(20),
    status VARCHAR(20),
    UNIQUE(nr_startowy)
);

