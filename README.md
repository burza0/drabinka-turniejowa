# 🏆 SKATECROSS Tournament Management System

Nowoczesny system zarządzania turniejami SKATECROSS z zaawansowanym interfejsem Vue.js + TypeScript, trybem administratora, ciemnym motywem i responsywnym designem mobilnym.

## 🎯 Funkcjonalności

### ✨ Główne cechy
- **250 zawodników** z 7 klubów w 6 kategoriach wiekowych (Junior A-D, Masters, Senior)
- **Zaawansowane filtry chipowe** - multi-select dla klubów, kategorii, płci i statusów
- **Responsywne karty mobilne** - kompaktowy układ na najwęższych ekranach
- **Tryb administratora** - możliwość edycji i usuwania zawodników
- **Tryb ciemny** - pełne wsparcie dark mode z przełącznikiem
- **Drabinka turniejowa** - grupy 4-osobowe z automatycznym awansem
- **Statystyki real-time** - karty z aktualnymi danymi turnieju
- **Rekord toru** - śledzenie najlepszego czasu z nazwiskiem rekordzisty

### 📱 Responsywny design
- **Desktop**: Tabele z pełnymi informacjami
- **Mobile**: Karty zawodników w kompaktowym układzie:
  ```
  ┌─────────────────────────────────────────┐
  │ [33] Urszula Witkowski  🏢 Club 🏷️ Cat │
  │      ⏰ 1:23.45           [STATUS]      │
  │      [Edytuj] [Usuń]                    │
  └─────────────────────────────────────────┘
  ```
- **Karty statystyk**: 2x2 na mobile, 4x1 na desktop
- **Filtry mobilne**: Chipowe przyciski z kolorową identyfikacją

### 🎛️ System filtrowania
- **Filtry chipowe**: Multi-select przyciski z kolorami
- **Real-time liczniki**: Pokazują liczbę wybranych filtrów
- **Szybkie akcje**: Buttons dla typowych kombinacji filtrów
- **Wyczyść wszystko**: Reset filtrów jednym kliknięciem
- **Licznik wyników**: Dynamiczne wyświetlanie przefiltrowanych zawodników

### 👨‍💼 Tryb administratora
- **Toggle w headerze**: Przełącznik admin/user
- **Wizualne wskaźniki**: Badge "🔧 ADMIN" i zmiana avatara
- **Kolumna akcji**: Przyciski edycji i usuwania zawodników
- **Notyfikacja**: Alert o trybie administratora

### 🌙 Tryb ciemny
- **Pełne wsparcie**: Wszystkie komponenty i kolory
- **Przełącznik**: Słońce/księżyc w headerze
- **Smooth transitions**: Płynne przejścia między motywami
- **Persistent**: Zachowuje wybór użytkownika

## 🗄️ Struktura bazy danych

### Tabela `zawodnicy`
```sql
- nr_startowy (PRIMARY KEY)
- imie (VARCHAR)
- nazwisko (VARCHAR) 
- kategoria (VARCHAR) - Junior A/B/C/D, Masters, Senior
- plec (VARCHAR) - M/K
- klub (VARCHAR) - 7 klubów sportowych
```

### Tabela `wyniki`
```sql
- nr_startowy (FOREIGN KEY)
- czas_przejazdu_s (DECIMAL)
- status (VARCHAR) - FINISHED/DNF/DSQ
```

### Aktualne dane
- **250 zawodników** z 7 klubów (35-36 zawodników/klub)
- **195 ukończonych** (78%), **29 DNF** (11.6%), **26 DSQ** (10.4%)
- **Rekord toru**: 35.008s (Irena Pietrzak)

## 🚀 Uruchamianie

### Wymagania
- **Backend**: Python 3.8+, Flask
- **Frontend**: Node.js 16+, Vue 3, TypeScript
- **Baza**: PostgreSQL/Supabase

### Instalacja i uruchomienie

#### Backend (Flask API)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install flask flask-cors psycopg2-binary python-dotenv
# Skonfiguruj .env z DATABASE_URL
python3 api_server.py
# Serwer: http://localhost:5000
```

#### Frontend (Vue.js + TypeScript)
```bash
cd frontend
npm install
npm run dev
# Aplikacja: http://localhost:5173 (lub 5174/5175)
```

## 🔧 API Endpointy

- `GET /api/zawodnicy` - Lista zawodników z JOIN wyników (klub, kategoria, płeć, czas, status)
- `GET /api/drabinka` - Drabinka turniejowa z grupami ćwierćfinał/półfinał/finał
- `GET /api/statystyki` - Statystyki według kategorii i płci

## 🎨 Tech Stack

### Frontend
- **Vue 3** - Composition API
- **TypeScript** - Pełna typizacja
- **Vite** - Build tool i dev server  
- **Tailwind CSS** - Utility-first styling
- **Heroicons** - Spójny zestaw ikon
- **Axios** - HTTP client

### Backend
- **Flask** - Python web framework
- **Flask-CORS** - Cross-origin requests
- **psycopg2** - PostgreSQL adapter
- **python-dotenv** - Environment variables

### Komponenty Vue
```
App.vue                    # Główny layout z headerem i nawigacją
├── StatsCard.vue         # Karty statystyk (4 główne metryki)
├── StatusBadge.vue       # Kolorowe badges statusów
├── ZawodnikCard.vue      # Karty zawodników na mobile
├── DrabinkaPucharowa.vue # Drabinka turniejowa
└── Rankingi.vue          # Placeholder dla rankingów
```

## 📁 Struktura projektu

```
drabinka-turniejowa/
├── backend/
│   ├── api_server.py           # Flask API z endpoints
│   ├── requirements.txt        # Python dependencies
│   └── .env                    # Database config (nie w git)
├── frontend/
│   ├── src/
│   │   ├── App.vue            # Main layout, filtry, tabela/karty
│   │   ├── style.css          # Global styles
│   │   └── components/
│   │       ├── StatsCard.vue   # Responsywne karty statystyk
│   │       ├── StatusBadge.vue # FINISHED/DNF/DSQ badges
│   │       ├── ZawodnikCard.vue # Kompaktowe karty mobile
│   │       ├── DrabinkaPucharowa.vue # Tournament bracket
│   │       └── Rankingi.vue    # Rankings placeholder
│   ├── index.html             # HTML template
│   ├── package.json           # Dependencies & scripts
│   ├── tailwind.config.js     # Tailwind + dark mode config
│   ├── tsconfig.json          # TypeScript config
│   └── vite.config.ts         # Vite config z proxy
├── README.md                   # Ten plik
└── .gitignore                 # venv/, node_modules/, .env
```

## 🎯 Kluczowe features

### Filtry chipowe
- **Multi-select**: Możliwość wyboru kilku opcji jednocześnie
- **Kolorowa identyfikacja**: Różne kolory dla klubów/kategorii/płci/statusów
- **Liczniki**: "(X wybranych)" przy każdej grupie filtrów
- **Szybkie akcje**: Przyciski "Wszystkie kluby", "Tylko ukończone", etc.

### Karty mobilne (ZawodnikCard)
- **Kompaktowy layout**: 3 główne linie + opcjonalne akcje admin
- **Ikony zamiast tekstu**: 🏢 klub, 🏷️ kategoria, ⏰ czas
- **Größe czcionki**: text-lg dla głównych danych, text-2xl dla czasu
- **Status z czasem**: W jednej linii z kolorowym tłem

### Tryb administratora
- **Toggle switch**: W headerze obok avatara
- **Wizualne wskaźniki**: "🔧 ADMIN" badge, A zamiast U w avatarze
- **Akcje**: Przyciski edycji/usuwania w kartach i tabeli
- **Conditional rendering**: Akcje widoczne tylko w trybie admin

### Dark mode
- **Comprehensive**: Wszystkie komponenty z dark variants
- **Toggle UI**: Słońce/księżyc w headerze
- **Class-based**: `dark:` prefixes w Tailwind
- **Smooth transitions**: 200ms duration na wszystkich elementach

## 📊 Statystyki turnieju

### Karty główne
1. **Wszyscy zawodnicy**: 250 (ikona UsersIcon, niebieski)
2. **Ukończyli**: 195 (ikona CheckCircleIcon, zielony)  
3. **DNF/DSQ**: 55 (ikona XCircleIcon, czerwony)
4. **Rekord toru**: 0:35.01 (ikona ClockIcon, fioletowy)
   - Subtitle: "Rekord: Irena Pietrzak"

### Responsywne układy
- **Desktop**: 4 karty w rzędzie
- **Tablet**: 2 karty w rzędzie  
- **Mobile**: 2 karty w rzędzie (zmniejszone paddingi i czcionki)

## 🔄 Workflow developmentu

### Git workflow
```bash
git add .
git commit -m "feat: opis zmian"
git push origin main
```

### Development
```bash
# Backend (terminal 1)
cd backend && source venv/bin/activate && python api_server.py

# Frontend (terminal 2)  
cd frontend && npm run dev

# Otwórz: http://localhost:5173
```

## 🚀 Deployment

System gotowy do wdrożenia na:
- **Frontend**: Vercel, Netlify, GitHub Pages
- **Backend**: Heroku, Railway, Render
- **Database**: Supabase, PostgreSQL on cloud

---

**Autor**: System zaprojektowany dla profesjonalnych turniejów SKATECROSS  
**Tech Lead**: Vue.js 3 + TypeScript + Tailwind CSS + Flask  
**Wersja**: 2024 - Responsive Mobile-First Design
