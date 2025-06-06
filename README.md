# 🏆 SKATECROSS Tournament System

> **Profesjonalny system zarządzania turniejami łyżwiarskich** z funkcjami QR kodów, rankingami i drabinką turniejową.

![Version](https://img.shields.io/badge/version-v30.5.4-blue.svg)
![Backend](https://img.shields.io/badge/backend-Flask_3.0-green.svg)
![Frontend](https://img.shields.io/badge/frontend-Vue_3.5-brightgreen.svg)
![Database](https://img.shields.io/badge/database-PostgreSQL-blue.svg)
![Deploy](https://img.shields.io/badge/deploy-Heroku-purple.svg)

## 📖 Spis treści

- [🎯 Funkcjonalności](#-funkcjonalności)
- [🛠️ Stack technologiczny](#️-stack-technologiczny)
- [🚀 Szybki start](#-szybki-start)
- [📁 Struktura projektu](#-struktura-projektu)
- [🔧 Instalacja i konfiguracja](#-instalacja-i-konfiguracja)
- [🌐 Deployment](#-deployment)
- [📊 API Dokumentacja](#-api-dokumentacja)
- [⚡ Optymalizacje wydajności](#-optymalizacje-wydajności)
- [🎨 Screenshots](#-screenshots)
- [🤝 Contributing](#-contributing)

## 🎯 Funkcjonalności

### 👥 Zarządzanie zawodnikami
- ✅ **CRUD zawodników** - dodawanie, edycja, usuwanie
- 🏷️ **Kategorie i kluby** - organizacja zawodników
- 📊 **Statystyki** - liczniki, rekordy, podsumowania
- 🔍 **Zaawansowane filtrowanie** - po kategorii, klubie, płci, statusie
- 📱 **Responsive design** - działanie na wszystkich urządzeniach

### 🏆 Drabinka turniejowa
- 🌳 **Wizualizacja drabinki** - graficzne drzewo turniejowe
- ⚡ **Aktualizacja na żywo** - natychmiastowe odświeżanie wyników
- 🎯 **Zarządzanie meczami** - rozpoczynanie, finalizowanie
- 📈 **Progresja** - śledzenie postępu zawodników

### 📊 System rankingów
- 🥇 **Ranking indywidualny** - najlepsi zawodnicy
- 🏟️ **Ranking klubów** - punktacja zespołowa
- 🏅 **Ranking medalowy** - podium w kategoriach
- 📈 **System punktowy** - automatyczne naliczanie

### 🔲 System QR kodów
- 📱 **Generator QR** - masowe generowanie kodów
- 📲 **Skaner mobilny** - odczytywanie na urządzeniach
- ✅ **Check-in system** - rejestracja uczestników
- 🖨️ **Drukowanie** - gotowe do wydruku etykiety
- 🔄 **Synchronizacja** - real-time updates

### 🎛️ Panel administracyjny
- 👤 **Tryb admin** - zaawansowane funkcje
- 📊 **Dashboard** - przegląd systemu
- ⚙️ **Konfiguracja** - ustawienia turniejów
- 📱 **Centrum startu** - zarządzanie linią startową

## 🛠️ Stack technologiczny

### Backend
```
Flask 3.0          # Framework webowy
PostgreSQL         # Baza danych
SQLAlchemy 2.0     # ORM
Flask-Compress     # Kompresja gzip
Gunicorn          # WSGI server
ReportLab         # Generowanie PDF
```

### Frontend
```
Vue 3.5           # Framework UI
TypeScript 5.8    # Typowanie
Vite 6.3          # Build tool
TailwindCSS 3.4   # Styling
Heroicons 2.2     # Ikony
Axios 1.9         # HTTP client
QRCode.js 1.5     # Generator QR
```

### Infrastructure
```
Heroku            # Platform deployment
PostgreSQL        # Managed database
GitHub Actions    # CI/CD (opcjonalnie)
```

## 🚀 Szybki start

### Wymagania
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Git

### 1. Klonowanie repozytorium
```bash
git clone https://github.com/your-username/drabinka-turniejowa.git
cd drabinka-turniejowa
```

### 2. Uruchomienie środowiska deweloperskiego

#### Backend
```bash
# Utworzenie virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalacja dependencies
cd backend
pip install -r requirements.txt

# Konfiguracja bazy danych
cp .env.example .env
# Edytuj .env z właściwymi danymi

# Uruchomienie serwera
python api_server.py
```

#### Frontend
```bash
# Instalacja dependencies
cd frontend
npm install

# Uruchomienie dev server
npm run dev
```

### 3. Dostęp do aplikacji
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000
- **Admin panel**: Toggle w prawym górnym rogu

## 📁 Struktura projektu

```
drabinka-turniejowa/
├── 📂 backend/                 # Serwer Flask
│   ├── 📄 api_server.py       # Główny serwer API
│   ├── 📄 cache.py            # System cache'owania
│   ├── 📄 optimize_db_performance.py  # Optymalizacje DB
│   ├── 📄 requirements.txt    # Python dependencies
│   └── 📂 migrations/         # Migracje bazy danych
│
├── 📂 frontend/               # Aplikacja Vue
│   ├── 📂 src/
│   │   ├── 📂 components/     # Komponenty Vue
│   │   │   ├── 📄 DrabinkaPucharowa.vue
│   │   │   ├── 📄 QrAdminDashboard.vue
│   │   │   ├── 📄 Rankingi.vue
│   │   │   └── 📄 StartLineScanner.vue
│   │   ├── 📂 composables/    # Logika biznesowa
│   │   └── 📄 App.vue         # Główny komponent
│   ├── 📄 package.json        # Node dependencies
│   ├── 📄 vite.config.ts      # Konfiguracja Vite
│   └── 📄 tailwind.config.js  # Konfiguracja TailwindCSS
│
├── 📄 Procfile               # Konfiguracja Heroku
├── 📄 requirements.txt       # Python dependencies (root)
└── 📄 README.md             # Ten plik
```

## 🔧 Instalacja i konfiguracja

### Konfiguracja bazy danych

1. **Tworzenie bazy PostgreSQL**:
```sql
CREATE DATABASE skatecross_tournament;
CREATE USER tournament_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE skatecross_tournament TO tournament_user;
```

2. **Plik środowiskowy** (`.env`):
```env
DATABASE_URL=postgresql://tournament_user:your_password@localhost/skatecross_tournament
FLASK_ENV=development
FLASK_SECRET_KEY=your-secret-key-here
```

3. **Inicjalizacja tabel**:
```bash
python backend/create_tables.py
```

### Zmienne środowiskowe

| Zmienna | Opis | Przykład |
|---------|------|----------|
| `DATABASE_URL` | URL bazy PostgreSQL | `postgresql://user:pass@host/db` |
| `FLASK_ENV` | Środowisko Flask | `development`/`production` |
| `FLASK_SECRET_KEY` | Klucz szyfrowania | `random-secret-key` |

### Indeksy bazy danych

System automatycznie tworzy optymalne indeksy:
```bash
python backend/optimize_db_performance.py
```

Tworzone indeksy:
- `idx_zawodnicy_nr_startowy` - JOIN performance
- `idx_zawodnicy_kategoria` - filtrowanie kategorii
- `idx_zawodnicy_klub` - filtrowanie klubów
- `idx_wyniki_czas` - sortowanie czasów
- `idx_wyniki_status` - filtrowanie statusów

## 🌐 Deployment

### Heroku Deployment

1. **Przygotowanie**:
```bash
# Zalogowanie do Heroku
heroku login

# Tworzenie aplikacji
heroku create your-app-name

# Dodanie PostgreSQL
heroku addons:create heroku-postgresql:mini
```

2. **Deployment**:
```bash
# Deploy
git push heroku master

# Migracje
heroku run python backend/create_tables.py
```

3. **Zmienne środowiskowe**:
```bash
heroku config:set FLASK_ENV=production
heroku config:set FLASK_SECRET_KEY=your-production-key
```

### Struktura plików deployment

- `Procfile` - Konfiguracja Heroku
- `requirements.txt` - Python dependencies
- `runtime.txt` - Wersja Python

## 📊 API Dokumentacja

### Endpoints zawodników

| Method | Endpoint | Opis |
|--------|----------|------|
| `GET` | `/api/zawodnicy` | Lista wszystkich zawodników |
| `POST` | `/api/zawodnicy` | Dodanie nowego zawodnika |
| `GET` | `/api/zawodnicy/{id}` | Szczegóły zawodnika |
| `PUT` | `/api/zawodnicy/{id}` | Aktualizacja zawodnika |
| `DELETE` | `/api/zawodnicy/{id}` | Usunięcie zawodnika |

### Endpoints drabinki

| Method | Endpoint | Opis |
|--------|----------|------|
| `GET` | `/api/drabinka` | Struktura drabinki |
| `POST` | `/api/drabinka/mecz` | Aktualizacja wyniku meczu |

### Endpoints rankingów

| Method | Endpoint | Opis |
|--------|----------|------|
| `GET` | `/api/rankings/individual` | Ranking indywidualny |
| `GET` | `/api/rankings/clubs/total` | Ranking klubów |
| `GET` | `/api/rankings/medals` | Ranking medalowy |

### Endpoints QR

| Method | Endpoint | Opis |
|--------|----------|------|
| `POST` | `/api/qr/generate/{id}` | Generowanie QR dla zawodnika |
| `POST` | `/api/qr/generate-bulk` | Masowe generowanie QR |
| `GET` | `/api/qr/stats` | Statystyki QR |
| `POST` | `/api/qr/check-in` | Check-in zawodnika |

### Przykłady użycia

#### Pobranie zawodników
```javascript
const response = await axios.get('/api/zawodnicy');
console.log(response.data); // Array zawodników
```

#### Dodanie zawodnika
```javascript
const newZawodnik = {
  nr_startowy: 101,
  imie: "Jan",
  nazwisko: "Kowalski",
  kategoria: "Senior",
  plec: "M",
  klub: "RC Warszawa"
};

const response = await axios.post('/api/zawodnicy', newZawodnik);
```

#### Generowanie QR kodu
```javascript
const response = await axios.post(`/api/qr/generate/${zawodnikId}`);
console.log(response.data.qr_code); // Generated QR code
```

## ⚡ Optymalizacje wydajności

### v30.5.4 Performance Improvements

#### Backend optimizations
- ✅ **PostgreSQL indexes** - 10x szybsze queries
- ✅ **Connection pooling** - efektywne zarządzanie połączeniami
- ✅ **Gzip compression** - 85% redukcja rozmiaru API responses
- ✅ **Query optimization** - optymalne zapytania SQL

#### Frontend optimizations
- ✅ **Bundle splitting** - 57% redukcja initial bundle size
- ✅ **Vendor chunking** - cache-friendly vendor libraries
- ✅ **Lazy loading** - komponenty ładowane on-demand
- ✅ **Tree shaking** - eliminacja unused code

#### Performance metrics
```
API Response Times:
├── /api/zawodnicy: 1.2s → 0.8s (-33%)
├── /api/drabinka: 1.1s → 0.7s (-36%)
└── /api/rankings: 0.5s → 0.3s (-40%)

Bundle Sizes:
├── Main JS: 267KB → 154KB (-42%)
├── Gzipped: 74KB → 32KB (-57%)
└── Vendor chunks: Cached separately
```

### Monitoring i cache

```bash
# Cache statistics
curl /api/admin/cache-stats

# Performance metrics
curl /api/admin/performance-metrics
```

## 🎨 Screenshots

### Dashboard główny
![Dashboard](docs/screenshots/dashboard.png)

### Zarządzanie zawodnikami
![Zawodnicy](docs/screenshots/zawodnicy.png)

### Drabinka turniejowa
![Drabinka](docs/screenshots/drabinka.png)

### System QR kodów
![QR System](docs/screenshots/qr-system.png)

### Panel rankingów
![Rankingi](docs/screenshots/rankingi.png)

## 🤝 Contributing

### Jak wnieść wkład

1. **Fork** repozytorium
2. **Utwórz** branch dla swojej funkcji (`git checkout -b feature/amazing-feature`)
3. **Commituj** zmiany (`git commit -m 'Add amazing feature'`)
4. **Push** do branch (`git push origin feature/amazing-feature`)
5. **Otwórz** Pull Request

### Konwencje

#### Commit messages
```
feat: dodanie nowej funkcjonalności
fix: naprawa błędu
docs: aktualizacja dokumentacji
style: zmiany formatowania
refactor: refaktoryzacja kodu
test: dodanie testów
chore: zmiany w konfiguracji
```

#### Code style
- **Backend**: PEP 8 (Python)
- **Frontend**: ESLint + Prettier
- **TypeScript**: Strict mode
- **CSS**: TailwindCSS utility-first

### Rozwój lokalny

```bash
# Uruchomienie z hot reload
npm run dev     # Frontend
python api_server.py  # Backend

# Linting
npm run lint    # Frontend
pylint backend/ # Backend

# Testy
npm test        # Frontend
pytest backend/ # Backend
```

## 📜 Licencja

Ten projekt jest licencjonowany na licencji MIT - zobacz plik [LICENSE](LICENSE) dla szczegółów.

## 🔗 Linki

- **Live Demo**: [https://drabinka-turniejowa-skatecross.herokuapp.com](https://drabinka-turniejowa-skatecross.herokuapp.com)
- **API Docs**: [/api/docs](https://drabinka-turniejowa-skatecross.herokuapp.com/api/docs)
- **Issues**: [GitHub Issues](https://github.com/your-username/drabinka-turniejowa/issues)

## 👥 Autorzy

- **Mariusz** - *Initial work* - [GitHub](https://github.com/your-username)

## 🙏 Podziękowania

- Społeczność **SKATECROSS** za feedback i testowanie
- **Vue.js** team za wspaniały framework
- **Flask** community za solidne podstawy
- **TailwindCSS** za piękne style
- **Heroku** za prostą platformę deployment

---

<div align="center">

**[⬆ Powrót na górę](#-skatecross-tournament-system)**

Made with ❤️ for SKATECROSS community

</div>
