# 🏁 DRABINKA PUCHAROWA SKATECROSS

Profesjonalny system do zarządzania wynikami i drabinką turniejową skatecross z zaawansowanymi funkcjami filtrowania i wizualizacji.

## 🎯 Funkcjonalności

### ✨ Główne cechy
- **150 zawodników** w 3 kategoriach wiekowych (MASTERS, OPEN, U18)
- **Podział płci** - równomierny rozkład 75 mężczyzn + 75 kobiet
- **Zaawansowane filtry** - kategoria + płeć w czasie rzeczywistym
- **Drabinka turniejowa** - grupy 4-osobowe z ćwierćfinałami, półfinałami i finałem
- **Ograniczenie uczestników** - maksymalnie 16 najlepszych do ćwierćfinałów na kategorię/płeć
- **Kolorowe wyświetlanie** - statusy, czasy, kategorie z intuicyjną kolorystyką
- **Responsywny design** - działa na wszystkich urządzeniach

### 📊 Sekcje aplikacji
1. **Podsumowanie** - statystyki ogólne pod głównym nagłówkiem
2. **Wyniki** - tabela z filtrami kategorii i płci, sortowaniem i statystykami
3. **Drabinka** - hierarchiczna struktura turniejowa zsynchronizowana z filtrami

## 🚀 Uruchamianie lokalnie

### Wymagania
- Python 3.8+
- Node.js 16+
- PostgreSQL (lub dostęp do Supabase)

### 1. Klonowanie repozytorium
```bash
git clone <repository-url>
cd drabinka-turniejowa
```

### 2. Konfiguracja backendu

#### Utworzenie środowiska wirtualnego
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# lub
venv\Scripts\activate     # Windows
```

#### Instalacja zależności
```bash
pip install flask flask-cors psycopg2 python-dotenv
```

#### Konfiguracja bazy danych
```bash
# Utwórz plik .env
echo 'DATABASE_URL=postgresql://username:password@host:port/database' > .env
```

### 3. Uruchomienie aplikacji

#### Backend
```bash
cd backend
source venv/bin/activate
python3 api_server.py
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

### 4. Dostęp do aplikacji
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000

## 🗄️ Struktura bazy danych

### Tabela `zawodnicy`
```sql
- nr_startowy (PRIMARY KEY)
- imie (VARCHAR)
- nazwisko (VARCHAR) 
- kategoria (VARCHAR) - MASTERS/OPEN/U18
- plec (VARCHAR) - M/K
```

### Tabela `wyniki`
```sql
- nr_startowy (FOREIGN KEY)
- czas_przejazdu_s (DECIMAL)
- status (VARCHAR) - FINISHED/DNF/DSQ
```

### Statystyki bazy
- **150 zawodników** łącznie
- **MASTERS**: 45 zawodników (22K + 23M)
- **OPEN**: 56 zawodników (28K + 28M) 
- **U18**: 49 zawodników (25K + 24M)
- **116 ukończonych** (77.3%), **15 DNF** (10.0%), **19 DSQ** (12.7%)

## 🔧 API Endpointy

- `GET /api/zawodnicy` - Lista wszystkich zawodników z płcią
- `GET /api/kategorie` - Lista kategorii wiekowych
- `GET /api/wyniki` - Wyniki z JOIN zawodników (imię, nazwisko, kategoria, płeć)
- `GET /api/drabinka` - Kompletna drabinka turniejowa z grupami i statystykami
- `GET /api/statystyki` - Statystyki według kategorii i płci

## 🎨 Funkcje frontendu

### Sekcja Wyniki
- **Filtry**: Kategoria + Płeć (niezależne)
- **Sortowanie**: FINISHED (po czasie) → DNF → DSQ
- **Kolorystyka**: 
  - Statusy: FINISHED (zielony), DNF (żółty), DSQ (czerwony)
  - Czasy: <45s (zielony), 45-50s (niebieski), 50-60s (żółty), >60s (czerwony)
  - Kategorie: U18 (zielony), OPEN (niebieski), MASTERS (fioletowy)
- **Statystyki**: Ukończone/DNF/DSQ + najlepszy czas

### Sekcja Drabinka
- **Synchronizacja z filtrami** - reaguje na wybór kategorii/płci w sekcji Wyniki
- **Struktura turniejowa**:
  - **Ćwierćfinały**: Grupy po 4, awansują 2 najlepszych
  - **Półfinały**: Zwycięzcy z ćwierćfinałów
  - **Finał**: Zwycięzcy z półfinałów
- **Ograniczenie**: Maksymalnie 16 najlepszych do ćwierćfinałów
- **Odpadli**: Lista zawodników poza drabinką (czerwony styl)
- **Statystyki grup**: Liczba grup w każdej rundzie

## 📁 Struktura projektu

```
drabinka-turniejowa/
├── backend/                    # Flask API
│   ├── api_server.py          # Główny serwer z logiką drabinki
│   ├── add_zawodnicy.py       # Skrypt dodający 50 zawodników (5-54)
│   ├── add_zawodnicy_proporcjonalnie.py # Skrypt dodający 96 zawodników (55-150)
│   ├── uzupelnij_dane.py      # Skrypt generujący realistyczne wyniki
│   ├── sprawdz_statystyki.py  # Skrypt sprawdzający statystyki bazy
│   ├── venv/                  # Środowisko wirtualne (nie w git)
│   └── .env                   # Konfiguracja bazy (nie w git)
├── frontend/                   # Vue.js frontend
│   ├── src/
│   │   ├── App.vue           # Główny komponent z podsumowaniem
│   │   └── components/
│   │       ├── Wyniki.vue    # Tabela z filtrami i statystykami
│   │       └── Drabinka.vue  # Hierarchiczna drabinka turniejowa
│   ├── vite.config.js        # Konfiguracja z proxy API
│   └── package.json
├── README.md                   # Ten plik
└── .gitignore                 # venv/, .env, node_modules/
```

## 🎯 Logika drabinki turniejowej

### Algorytm tworzenia drabinki
1. **Sortowanie** - wszyscy zawodnicy według czasu (najlepsi pierwsi)
2. **Ograniczenie** - maksymalnie 16 najlepszych do ćwierćfinałów
3. **Podział na grupy** - grupy 4-osobowe w ćwierćfinałach
4. **Awans** - 2 najlepszych z każdej grupy do następnej rundy
5. **Finał** - zwycięzcy półfinałów

### Przykład drabinki (OPEN Mężczyźni)
- **29 zawodników** łącznie → **16 w ćwierćfinałach** → **13 odpadło**
- **4 grupy ćwierćfinałowe** → **8 awansuje** do półfinałów
- **2 grupy półfinałowe** → **4 awansuje** do finału
- **1 grupa finałowa** → **1 zwycięzca**

## 🔧 Konfiguracja

### Zmienne środowiskowe (.env)
```bash
DATABASE_URL=postgresql://username:password@host:port/database
```

### Proxy frontend → backend (vite.config.js)
```javascript
proxy: {
  '/api': {
    target: 'http://localhost:5000',
    changeOrigin: true
  }
}
```

## 🐛 Rozwiązywanie problemów

### Backend nie uruchamia się
```bash
cd backend
source venv/bin/activate
python3 api_server.py
```

### Frontend nie łączy się z API
1. Sprawdź czy backend działa: `curl http://localhost:5000/api/wyniki`
2. Sprawdź konsole przeglądarki (F12)
3. Sprawdź konfigurację proxy w `vite.config.js`

### Baza danych pusta
```bash
cd backend
python3 add_zawodnicy.py              # Dodaje zawodników 5-54
python3 add_zawodnicy_proporcjonalnie.py  # Dodaje zawodników 55-150
python3 uzupelnij_dane.py             # Generuje wyniki
python3 sprawdz_statystyki.py         # Sprawdza statystyki
```

## 📈 Historia rozwoju

### v1.0 - Podstawowa funkcjonalność
- ✅ 4 zawodników testowych
- ✅ Podstawowe API (zawodnicy, wyniki)
- ✅ Prosty frontend Vue.js

### v2.0 - Rozszerzenie bazy
- ✅ 54 zawodników (dodano 50)
- ✅ Kolumna płci (M/K)
- ✅ 3 kategorie: MASTERS, OPEN, U18

### v3.0 - Pełna baza i drabinki
- ✅ 150 zawodników (proporcjonalny podział)
- ✅ Realistyczne wyniki (116 FINISHED, 15 DNF, 19 DSQ)
- ✅ Podstawowa drabinka turniejowa

### v4.0 - Zaawansowane funkcje
- ✅ Filtry kategorii + płci
- ✅ Kolorowe wyświetlanie
- ✅ Statystyki i podsumowania
- ✅ Responsywny design

### v5.0 - Profesjonalna drabinka (AKTUALNA)
- ✅ Grupy 4-osobowe z awansem 2 najlepszych
- ✅ Ograniczenie do 16 zawodników w ćwierćfinałach
- ✅ Hierarchiczna struktura: ćwierćfinały → półfinały → finał
- ✅ Synchronizacja filtrów między sekcjami
- ✅ Wyświetlanie odpadłych zawodników
- ✅ Nowy nagłówek: "DRABINKA PUCHAROWA SKATECROSS"
- ✅ Podsumowanie na górze strony

## 🚀 Przyszłe funkcjonalności

- [ ] Edycja wyników w czasie rzeczywistym
- [ ] Export drabinki do PDF
- [ ] System logowania i autoryzacji
- [ ] API do zarządzania turniejami
- [ ] Powiadomienia push o zmianach
- [ ] Integracja z systemami timing

---

**Autor**: System SECTRO Timing  
**Wersja**: 5.0  
**Ostatnia aktualizacja**: Maj 2025
