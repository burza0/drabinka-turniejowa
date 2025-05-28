# 🏆 Drabinka pucharowa Mistrzostw Polski w SKATECROSS

Profesjonalny system do zarządzania wynikami i drabinką turniejową SKATECROSS z zaawansowanymi funkcjami filtrowania, wizualizacji i nowoczesnym responsywnym interfejsem użytkownika.

## 🎯 Funkcjonalności

### ✨ Główne cechy
- **250 zawodników** w 6 kategoriach wiekowych (Junior A, Junior B, Junior C, Junior D, Masters, Senior)
- **Podział płci** - równomierny rozkład 125 mężczyzn + 125 kobiet
- **Wielokrotne filtry kategorii** - możliwość wyboru kilku kategorii jednocześnie + płeć w czasie rzeczywistym
- **Responsywne karty mobilne** - format kart na najmniejszych ekranach dla lepszej czytelności
- **Drabinka turniejowa** - grupy 4-osobowe z ćwierćfinałami, półfinałami i finałem
- **Ograniczenie uczestników** - maksymalnie 16 najlepszych do ćwierćfinałów na kategorię/płeć
- **Kolorowe wyświetlanie** - statusy, czasy, kategorie z intuicyjną kolorystyką
- **Pełna responsywność** - płynne przejście między widokiem desktop a mobile
- **Nowoczesny interfejs** - profesjonalny design dla wielkich imprez sportowych

### 📱 Responsywność mobilna
- **Widok desktop**: Standardowe tabele z pełnymi informacjami
- **Widok mobile (≤600px)**: Karty zawodników w formacie:
  ```
  +----------------------------------------------------+
  | [1] Szymon Baran                                   |
  | Nr startowy: 170   |   Kategoria: Junior B         |
  | Status: ✅ Ukończył |   Czas: 40.830s              |
  +----------------------------------------------------+
  ```
- **Ujednolicone nagłówki**: Identyczny design między sekcjami "Wyniki" i "Drabinka"
- **Optymalne szerokości kolumn**: Wszystkie elementy mieszczą się w ramce bez przewijania
- **Statystyki 2x2**: Karty statystyk w układzie dwóch linii na mobilnych

### 📊 Sekcje aplikacji
1. **Header** - "🏆 MISTRZOSTWA POLSKI SKATECROSS 2025" z responsywnym logo
2. **Podsumowanie** - statystyki ogólne w układzie 2x2 na mobile, 4x1 na desktop
3. **Filtry** - wielokrotny wybór kategorii + płeć z licznikiem wyników i aktywną listą filtrów
4. **Wyniki** - profesjonalna tabela z kartami mobilnymi i kolorystyką
5. **Drabinka** - hierarchiczna struktura turniejowa z kartami mobilnymi

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

### 2. Szybkie uruchomienie
```bash
# Uruchomienie obu serwisów jednocześnie
./run_local.sh
```

### 3. Ręczne uruchomienie

#### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Skonfiguruj .env z DATABASE_URL
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
- kategoria (VARCHAR) - Junior A/B/C/D, Masters, Senior
- plec (VARCHAR) - M/K
```

### Tabela `wyniki`
```sql
- nr_startowy (FOREIGN KEY)
- czas_przejazdu_s (DECIMAL)
- status (VARCHAR) - FINISHED/DNF/DSQ
```

### Aktualne statystyki bazy
- **250 zawodników** łącznie (125M + 125K)
- **Junior A**: 36 zawodników (16M + 20K)
- **Junior B**: 39 zawodników (16M + 23K)
- **Junior C**: 45 zawodników (25M + 20K)
- **Junior D**: 47 zawodników (27M + 20K)
- **Masters**: 46 zawodników (22M + 24K)
- **Senior**: 37 zawodników (19M + 18K)
- **195 ukończonych** (78%), **29 DNF** (11.6%), **26 DSQ** (10.4%)

## 🔧 API Endpointy

- `GET /api/zawodnicy` - Lista wszystkich zawodników z płcią
- `GET /api/kategorie` - Lista kategorii z liczbą zawodników
- `GET /api/wyniki` - Wyniki z JOIN zawodników (imię, nazwisko, kategoria, płeć)
- `GET /api/drabinka` - Kompletna drabinka turniejowa z grupami i statystykami
- `GET /api/statystyki` - Statystyki według kategorii i płci

## 🎨 Funkcje frontendu

### Nowoczesny design
- **Czcionka Inter** - profesjonalna typografia
- **Gradientowe headery** - niebieski główny (#1e40af) z akcentami
- **Animacje i hover efekty** - płynne przejścia i interakcje (wyłączone na mobile)
- **Doskonały kontrast** - ciemny tekst na jasnym tle dla czytelności
- **Sportowe tło** - dynamiczne gradientowe tło z elementami SVG
- **Ujednolicone nagłówki** - identyczny design między sekcjami

### Filtry zaawansowane
- **Wielokrotny wybór kategorii**: Możliwość zaznaczenia kilku kategorii jednocześnie
- **Dodawanie/usuwanie**: Kliknięcie dodaje kategorię, ponowne kliknięcie usuwa
- **Aktywna lista filtrów**: Badge dla każdej wybranej kategorii z przyciskiem X
- **Licznik wyników**: Dynamiczny podgląd liczby znalezionych zawodników
- **Przycisk wyczyść**: Jednym kliknięciem usuwa wszystkie filtry

### Sekcja Wyniki
- **Filtry**: Wielokrotny wybór kategorii + Płeć (niezależne) z licznikiem
- **Sortowanie**: FINISHED (po czasie) → DNF → DSQ
- **Kolorystyka**: 
  - Statusy: FINISHED (zielony ✅), DNF (czerwony ❌), DSQ (pomarańczowy 🚫)
  - Czasy: <45s (doskonały), 45-50s (dobry), 50-60s (średni), >60s (słaby)
  - Pozycje: Złoto 🥇, Srebro 🥈, Brąz 🥉
- **Karty mobilne**: Format kart z pozycją w badge i szczegółami w liniach
- **Optymalne kolumny**: Szerokości dostosowane aby STATUS nie wychodził za ramkę

### Sekcja Drabinka
- **Synchronizacja z filtrami** - reaguje na wybór kategorii/płci
- **Struktura turniejowa**:
  - **Ćwierćfinały**: Grupy po 4, awansują 2 najlepszych
  - **Półfinały**: Zwycięzcy z ćwierćfinałów
  - **Finał**: Zwycięzcy z półfinałów z animacją glow
- **Status turnieju**: "Turniej w toku" z pulsującą kropką
- **Medale**: 🥇🥈🥉 zamiast korony w finale
- **Karty mobilne**: Format kart z badge'ami awansu i medali
- **Brak podwójnych tłem**: Czyste białe karty mobilne bez kolorowych nakładek

## 📁 Struktura projektu

```
drabinka-turniejowa/
├── backend/                    # Flask API
│   ├── api_server.py          # Główny serwer z logiką drabinki
│   ├── rozszerz_do_250.py     # Skrypt rozszerzający bazę do 250 zawodników
│   ├── zmien_kategorie_i_rozszerz.py # Zmiana kategorii na Junior A-D
│   ├── sprawdz_statystyki.py  # Skrypt sprawdzający statystyki bazy
│   ├── uzupelnij_dane.py      # Skrypt generujący realistyczne wyniki
│   ├── venv/                  # Środowisko wirtualne (nie w git)
│   ├── requirements.txt       # Zależności Python
│   └── .env                   # Konfiguracja bazy (nie w git)
├── frontend/                   # Vue.js frontend
│   ├── src/
│   │   ├── App.vue           # Główny komponent z headerem i nawigacją
│   │   ├── style.css         # Globalne style CSS
│   │   └── components/
│   │       ├── Wyniki.vue    # Tabela z filtrami i kartami mobilnymi
│   │       ├── Kategorie.vue # Wielokrotne filtry kategorii i płci
│   │       └── Drabinka.vue  # Drabinka z kartami mobilnymi
│   ├── vite.config.js        # Konfiguracja z proxy API
│   └── package.json
├── run_local.sh               # Skrypt uruchamiający oba serwisy
├── README.md                  # Ten plik
└── .gitignore                 # venv/, .env, node_modules/
```

## 🎯 Logika drabinki turniejowej

### Algorytm tworzenia drabinki
1. **Filtrowanie** - według wybranych kategorii i płci
2. **Sortowanie** - wszyscy zawodnicy według czasu (najlepsi pierwsi)
3. **Ograniczenie** - maksymalnie 16 najlepszych do ćwierćfinałów
4. **Podział na grupy** - grupy 4-osobowe w ćwierćfinałach
5. **Awans** - 2 najlepszych z każdej grupy do następnej rundy
6. **Finał** - zwycięzcy półfinałów z medalami

### Przykład drabinki (Junior A Mężczyźni)
- **16 zawodników** łącznie → **16 w ćwierćfinałach** → **0 odpadło**
- **4 grupy ćwierćfinałowe** → **8 awansuje** do półfinałów
- **2 grupy półfinałowe** → **4 awansuje** do finału
- **1 grupa finałowa** → **1 zwycięzca** 🥇

## 📱 Responsywność i UX

### Media queries
- **Desktop (>600px)**: Pełne tabele, 4 kolumny statystyk
- **Tablet (601-900px)**: Statystyki 2x2, zmniejszone fonty
- **Mobile (≤600px)**: Karty mobilne, sticky navigation
- **Bardzo małe (≤400px)**: Minimalne paddingi, kompaktowe karty

### Optymalizacje mobilne
- **Sticky menu**: Zawsze widoczne na górze ekranu
- **Karty zamiast tabel**: Lepsze UX na małych ekranach
- **Usunięte efekty hover**: Bez niepotrzebnych animacji na touch
- **Optymalne rozmiary**: Przyciski i elementy dostosowane do dotyku
- **Czytelne fonty**: Odpowiednie rozmiary dla różnych ekranów

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

### Baza danych pusta lub nieaktualna
```bash
cd backend
python3 rozszerz_do_250.py        # Rozszerza bazę do 250 zawodników
python3 sprawdz_statystyki.py     # Sprawdza statystyki
```

### Problemy z filtrami
- Sprawdź endpoint `/api/kategorie` - powinien zwracać obiekt z `kategorie` i `total_zawodnikow`
- Sprawdź konsole przeglądarki pod kątem błędów JavaScript
- Upewnij się, że filtry używają tablicy `kategorie` zamiast pojedynczej `kategoria`

### Problemy z responsywnością
- Sprawdź media queries w CSS
- Sprawdź czy elementy mają klasy `mobile-only`, `desktop-only`
- Upewnij się, że nie ma nadpisujących stylów na końcu plików CSS

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
- ✅ Realistyczne wyniki
- ✅ Podstawowa drabinka turniejowa

### v4.0 - Zaawansowane funkcje
- ✅ Filtry kategorii + płci
- ✅ Kolorowe wyświetlanie
- ✅ Statystyki i podsumowania
- ✅ Responsywny design

### v5.0 - Profesjonalna drabinka
- ✅ Grupy 4-osobowe z awansem 2 najlepszych
- ✅ Ograniczenie do 16 zawodników w ćwierćfinałach
- ✅ Hierarchiczna struktura turniejowa
- ✅ Synchronizacja filtrów między sekcjami

### v6.0 - Rozszerzenie do 250 zawodników
- ✅ **250 zawodników** w 6 kategoriach (Junior A-D, Masters, Senior)
- ✅ **Nowy nagłówek**: "🏆 Drabinka pucharowa Mistrzostw Polski w SKATECROSS"
- ✅ **Profesjonalny design** dla wielkich imprez sportowych
- ✅ **Czcionka Inter** z gradientowymi headerami
- ✅ **Medale w finale** (🥇🥈🥉) zamiast korony
- ✅ **Sportowe tło** z dynamicznymi elementami SVG
- ✅ **Liczniki filtrów** - wyświetlanie liczby znalezionych zawodników

### v7.0 - Responsywność i UX (AKTUALNA)
- ✅ **Wielokrotny wybór kategorii** - możliwość zaznaczenia kilku kategorii
- ✅ **Karty mobilne** - format kart na ekranach ≤600px dla lepszej czytelności
- ✅ **Ujednolicone nagłówki** - identyczny design między sekcjami "Wyniki" i "Drabinka"
- ✅ **Optymalne szerokości kolumn** - STATUS nie wychodzi za ramkę tabeli
- ✅ **Statystyki 2x2** - układ w dwóch liniach na mobilnych ekranach
- ✅ **Usunięte podwójne tła** - czyste białe karty mobilne bez kolorowych nakładek
- ✅ **Wyłączone efekty hover** - lepsze UX na urządzeniach dotykowych
- ✅ **Sticky navigation** - menu zawsze widoczne na górze ekranu
- ✅ **Kompletna responsywność** - płynne przejście między desktop a mobile

## 🚀 Przyszłe funkcjonalności

- [ ] Edycja wyników w czasie rzeczywistym
- [ ] Export drabinki do PDF
- [ ] System logowania i autoryzacji
- [ ] API do zarządzania turniejami
- [ ] Powiadomienia push o zmianach
- [ ] Integracja z systemami timing
- [ ] Tryb ciemny (dark mode)
- [ ] Wielojęzyczność (PL/EN)
- [ ] Progressive Web App (PWA)
- [ ] Offline support

## 🎨 Design System

### Kolory
- **Główny**: #1e40af (niebieski)
- **Akcent**: #dc2626 (czerwony), #f59e0b (pomarańczowy)
- **Sukces**: #059669 (zielony)
- **Tło**: Dynamiczny gradient z elementami SVG
- **Tekst**: #0f172a (ciemny)

### Typografia
- **Czcionka**: Inter (Google Fonts)
- **Rozmiary**: Skalowane dla różnych ekranów
- **Wagi**: 400 (regular), 600 (semibold), 700 (bold), 800 (extrabold), 900 (black)

### Komponenty
- **Karty**: Białe tło, cienie, zaokrąglone rogi
- **Przyciski**: Gradientowe tła, aktywne stany
- **Badges**: Kolorowe znaczki z ikonami i przyciskami usuwania
- **Tabele**: Responsywne z kartami mobilnymi

### Responsywność
- **Breakpointy**: 400px, 480px, 600px, 768px, 900px
- **Mobile-first**: Projektowanie od najmniejszych ekranów
- **Touch-friendly**: Elementy dostosowane do dotyku

---

**Autor**: MB  
**Wersja**: 7.0  
**Ostatnia aktualizacja**: Styczeń 2025  
**Licencja**: MIT
