# 🏆 Drabinka pucharowa Mistrzostw Polski w SKATECROSS

Profesjonalny system do zarządzania wynikami i drabinką turniejową SKATECROSS z zaawansowanymi funkcjami filtrowania, wizualizacji i nowoczesnym interfejsem użytkownika.

## 🎯 Funkcjonalności

### ✨ Główne cechy
- **250 zawodników** w 6 kategoriach wiekowych (Junior A, Junior B, Junior C, Junior D, Masters, Senior)
- **Podział płci** - równomierny rozkład 125 mężczyzn + 125 kobiet
- **Zaawansowane filtry** - kategoria + płeć w czasie rzeczywistym z licznikiem wyników
- **Drabinka turniejowa** - grupy 4-osobowe z ćwierćfinałami, półfinałami i finałem
- **Ograniczenie uczestników** - maksymalnie 16 najlepszych do ćwierćfinałów na kategorię/płeć
- **Kolorowe wyświetlanie** - statusy, czasy, kategorie z intuicyjną kolorystyką
- **Responsywny design** - działa na wszystkich urządzeniach
- **Nowoczesny interfejs** - profesjonalny design dla wielkich imprez sportowych

### 📊 Sekcje aplikacji
1. **Header** - "🏆 MISTRZOSTWA POLSKI SKATECROSS 2025" z wskaźnikiem "NA ŻYWO"
2. **Podsumowanie** - statystyki ogólne (zawodnicy, kategorie, podział płci)
3. **Filtry** - interaktywne przyciski kategorii i płci z licznikiem wyników
4. **Wyniki** - profesjonalna tabela z sortowaniem i kolorystyką
5. **Drabinka** - hierarchiczna struktura turniejowa zsynchronizowana z filtrami

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
- **Animacje i hover efekty** - płynne przejścia i interakcje
- **Doskonały kontrast** - ciemny tekst na jasnym tle dla czytelności
- **Nieprzezroczyste tła** - belka nawigacji i sekcje bez nakładania

### Sekcja Wyniki
- **Filtry**: Kategoria + Płeć (niezależne) z licznikiem wyników
- **Sortowanie**: FINISHED (po czasie) → DNF → DSQ
- **Kolorystyka**: 
  - Statusy: FINISHED (zielony ✅), DNF (czerwony ❌), DSQ (pomarańczowy 🚫)
  - Czasy: <45s (doskonały), 45-50s (dobry), 50-60s (średni), >60s (słaby)
  - Pozycje: Złoto 🥇, Srebro 🥈, Brąz 🥉
- **Badges**: Kolorowe znaczki dla kategorii, płci i statusów

### Sekcja Drabinka
- **Synchronizacja z filtrami** - reaguje na wybór kategorii/płci
- **Struktura turniejowa**:
  - **Ćwierćfinały**: Grupy po 4, awansują 2 najlepszych
  - **Półfinały**: Zwycięzcy z ćwierćfinałów
  - **Finał**: Zwycięzcy z półfinałów z animacją glow
- **Status turnieju**: "Turniej w toku" z pulsującą kropką
- **Medale**: 🥇🥈🥉 zamiast korony w finale
- **Odpadli**: Lista zawodników poza drabinką

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
│   │       ├── Wyniki.vue    # Tabela z filtrami i profesjonalnym designem
│   │       ├── Kategorie.vue # Filtry kategorii i płci z licznikami
│   │       └── Drabinka.vue  # Hierarchiczna drabinka turniejowa
│   ├── vite.config.js        # Konfiguracja z proxy API
│   └── package.json
├── run_local.sh               # Skrypt uruchamiający oba serwisy
├── README.md                  # Ten plik
└── .gitignore                 # venv/, .env, node_modules/
```

## 🎯 Logika drabinki turniejowej

### Algorytm tworzenia drabinki
1. **Filtrowanie** - według wybranej kategorii i płci
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

### v6.0 - Rozszerzenie do 250 zawodników (AKTUALNA)
- ✅ **250 zawodników** w 6 kategoriach (Junior A-D, Masters, Senior)
- ✅ **Nowy nagłówek**: "🏆 Drabinka pucharowa Mistrzostw Polski w SKATECROSS"
- ✅ **Profesjonalny design** dla wielkich imprez sportowych
- ✅ **Czcionka Inter** z gradientowymi headerami
- ✅ **Medale w finale** (🥇🥈🥉) zamiast korony
- ✅ **Nieprzezroczyste tła** - belka nawigacji nie zlewa się z treścią
- ✅ **Poprawione statusy** - zgodne z bazą danych (FINISHED/DNF/DSQ)
- ✅ **Liczniki filtrów** - wyświetlanie liczby znalezionych zawodników
- ✅ **Animacje i hover efekty** - płynne przejścia i interakcje

## 🚀 Przyszłe funkcjonalności

- [ ] Edycja wyników w czasie rzeczywistym
- [ ] Export drabinki do PDF
- [ ] System logowania i autoryzacji
- [ ] API do zarządzania turniejami
- [ ] Powiadomienia push o zmianach
- [ ] Integracja z systemami timing
- [ ] Tryb ciemny (dark mode)
- [ ] Wielojęzyczność (PL/EN)

## 🎨 Design System

### Kolory
- **Główny**: #1e40af (niebieski)
- **Akcent**: #dc2626 (czerwony), #f59e0b (pomarańczowy)
- **Sukces**: #059669 (zielony)
- **Tło**: #f8fafc (jasny szary)
- **Tekst**: #0f172a (ciemny)

### Typografia
- **Czcionka**: Inter (Google Fonts)
- **Rozmiary**: 18px bazowy, skalowane nagłówki
- **Wagi**: 400 (regular), 600 (semibold), 700 (bold), 800 (extrabold), 900 (black)

### Komponenty
- **Karty**: Białe tło, cienie, zaokrąglone rogi
- **Przyciski**: Gradientowe tła, hover efekty
- **Badges**: Kolorowe znaczki z ikonami
- **Tabele**: Profesjonalne z gradientowymi headerami

---

**Autor**: MB  
**Wersja**: 6.0  
**Ostatnia aktualizacja**: Maj 2025  
**Licencja**: MIT
