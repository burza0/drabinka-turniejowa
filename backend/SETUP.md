# 🔧 SKATECROSS QR Backend Setup

## 📋 Wymagania

- Python 3.11+
- PostgreSQL 14+
- pip

## 🚀 Instalacja

### 1. Virtual Environment
```bash
cd backend
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 2. Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Setup

#### Utwórz bazę PostgreSQL:
```sql
CREATE DATABASE skatecross_qr;
CREATE USER qr_user WITH PASSWORD 'qr_password';
GRANT ALL PRIVILEGES ON DATABASE skatecross_qr TO qr_user;
```

#### Utwórz plik `.env`:
```env
DATABASE_URL=postgresql://qr_user:qr_password@localhost:5432/skatecross_qr
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_SECRET_KEY=dev-secret-key-change-in-production
SERVER_PORT=5001
```

### 4. Inicjalizacja tabel
```bash
python -c "
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cur = conn.cursor()

# Podstawowe tabele
cur.execute('''
CREATE TABLE IF NOT EXISTS zawodnicy (
    nr_startowy INTEGER PRIMARY KEY,
    imie VARCHAR(100) NOT NULL,
    nazwisko VARCHAR(100) NOT NULL,
    kategoria VARCHAR(50),
    plec CHAR(1),
    klub VARCHAR(200),
    qr_code TEXT,
    checked_in BOOLEAN DEFAULT FALSE,
    check_in_time TIMESTAMP,
    ostatni_skan TIMESTAMP
);

CREATE TABLE IF NOT EXISTS wyniki (
    nr_startowy INTEGER PRIMARY KEY REFERENCES zawodnicy(nr_startowy),
    czas_przejazdu_s DECIMAL(10,3),
    status VARCHAR(20) DEFAULT 'NOT_STARTED'
);

CREATE TABLE IF NOT EXISTS start_queue (
    id SERIAL PRIMARY KEY,
    kategoria VARCHAR(50),
    plec CHAR(1),
    numer_grupy INTEGER,
    nazwa VARCHAR(200),
    status VARCHAR(20) DEFAULT 'WAITING',
    estimated_time INTEGER DEFAULT 300
);
''')

conn.commit()
cur.close()
conn.close()
print('✅ Tabele utworzone')
"
```

## 🏃 Uruchomienie

```bash
python api_server.py
```

Server będzie dostępny na: `http://localhost:5001`

## 🔗 API Endpoints

### Zawodnicy
- `GET /api/zawodnicy` - Lista zawodników
- `GET /api/zawodnicy/{id}` - Pojedynczy zawodnik

### QR Kody
- `POST /api/qr/generate/{id}` - Generuj QR dla zawodnika
- `POST /api/qr/generate-bulk` - Masowe generowanie
- `GET /api/qr/stats` - Statystyki QR

### Centrum Startu
- `GET /api/grupy-startowe` - Lista grup
- `POST /api/grupa-aktywna` - Toggle grupy aktywnej
- `GET /api/start-queue` - Kolejka startowa
- `POST /api/qr/scan-result` - Skanowanie QR

## 🐛 Troubleshooting

### Database Connection Error
```
psql: FATAL: database "skatecross_qr" does not exist
```
**Rozwiązanie**: Utwórz bazę danych zgodnie z instrukcjami powyżej

### Port Already in Use
```
OSError: [Errno 98] Address already in use
```
**Rozwiązanie**: Zmień port w `api_server.py` lub zabij proces na porcie 5001

### Missing Dependencies
```
ModuleNotFoundError: No module named 'psycopg2'
```
**Rozwiązanie**: `pip install -r requirements.txt` 