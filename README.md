# 🏆 SKATECROSS Tournament Management System

Nowoczesny system zarządzania turniejami SKATECROSS z zaawansowanym interfejsem Vue.js + TypeScript, trybem administratora, ciemnym motywem i responsywnym designem mobilnym.

**🌐 Aplikacja LIVE**: https://drabinka-turniejowa-skatecross-17be0c216c6f.herokuapp.com/

## 🎯 Funkcjonalności

### ✨ Główne cechy
- **250 zawodników** z 7 klubów w 6 kategoriach wiekowych (Junior A-D, Masters, Senior)
- **Zaawansowane filtry chipowe** - multi-select dla klubów, kategorii, płci i statusów
- **Responsywne karty mobilne** - kompaktowy układ na najwęższych ekranach
- **Tryb administratora** - możliwość edycji i usuwania zawodników
- **Tryb ciemny** - pełne wsparcie dark mode z przełącznikiem
- **Drabinka turniejowa** - grupy 4-osobowe z automatycznym awansem i filtrami
- **Statystyki real-time** - karty z aktualnymi danymi turnieju
- **Rekord toru** - śledzenie najlepszego czasu z nazwiskiem rekordzisty
- **Pole wyszukiwania** - w jednej linii z tytułem na desktopie

### 📱 Responsywny design
- **Desktop**: Tabele z pełnymi informacjami + pole wyszukiwania w headerze
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
- **Domyślne ustawienia**: Wszystkie filtry początkowo odznaczone
- **Logika filtrowania**: Puste filtry = wszystko widoczne, wypełnione = tylko wybrane
- **Szybkie akcje**: Buttons dla typowych kombinacji filtrów
- **Wyczyść wszystko**: Reset filtrów jednym kliknięciem
- **Licznik wyników**: Dynamiczne wyświetlanie przefiltrowanych zawodników

### 🏆 Drabinka Pucharowa
- **Grupy turniejowe**: Ćwierćfinały, półfinały, finały
- **Filtry kategorii i płci**: Domyślnie odznaczone, pokazują wszystko
- **Statystyki uproszczone**: Tylko łączna liczba zawodników i w ćwierćfinałach
- **Kolorowe wskaźniki**: Awansujący zawodnicy podświetleni
- **Podział na płcie**: Oddzielne sekcje dla mężczyzn i kobiet

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
- **Backend**: Python 3.8+, Flask, Flask-CORS
- **Frontend**: Node.js 16+, Vue 3, TypeScript
- **Baza**: PostgreSQL/Supabase

### Instalacja i uruchomienie

#### Backend (Flask API)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Lub ręcznie:
# pip install flask flask-cors psycopg2-binary python-dotenv
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

## 🔄 Workflow developmentu

### Git workflow
```bash
git add .
git commit -m "feat: opis zmian"
git push origin master        # Backup na GitHub
git push heroku master       # Deployment na produkcję
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

### Produkcja - Heroku
- **URL**: https://drabinka-turniejowa-skatecross-17be0c216c6f.herokuapp.com/
- **Wersja**: v18 (najnowsza)
- **Backend + Frontend**: Zintegrowane na jednej dyno
- **Baza danych**: PostgreSQL na Heroku

---

**Autor**: System zaprojektowany dla profesjonalnych turniejów SKATECROSS  
**Tech Lead**: Vue.js 3 + TypeScript + Tailwind CSS + Flask  
**Wersja**: 2024 v18 - Responsive Mobile-First Design  
**Deployment**: Heroku Production Ready
