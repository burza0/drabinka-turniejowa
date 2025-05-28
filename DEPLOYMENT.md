# 🚀 Deployment Guide - Drabinka Turniejowa

## 🌐 Opcje deploymentu

### 🥇 **Opcja 1: Vercel + Railway (Rekomendowane)**

#### Backend na Railway:
1. **Zaloguj się do [Railway](https://railway.app)**
2. **Połącz GitHub** repo
3. **Deploy** z głównej gałęzi
4. **Dodaj PostgreSQL** z Railway Database
5. **Skonfiguruj zmienne środowiskowe:**
   ```
   DATABASE_URL=postgresql://postgres:password@host:port/railway
   PORT=5000
   HOST=0.0.0.0
   FLASK_ENV=production
   ```

#### Frontend na Vercel:
1. **Zaloguj się do [Vercel](https://vercel.com)**
2. **Import projektu** z GitHub
3. **Skonfiguruj Build Settings:**
   - Framework Preset: `Vite`
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
4. **Dodaj zmienne środowiskowe:**
   ```
   VITE_API_URL=https://your-railway-app.railway.app
   ```

### 🥈 **Opcja 2: Heroku (All-in-one)**

```bash
# Zainstaluj Heroku CLI
npm install -g heroku

# Logowanie
heroku login

# Stwórz aplikację
heroku create drabinka-turniejowa

# Dodaj PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Deploy
git push heroku master

# Sprawdź logi
heroku logs --tail
```

### 🥉 **Opcja 3: Netlify + Railway**

#### Backend na Railway (jak wyżej)

#### Frontend na Netlify:
1. **Zaloguj się do [Netlify](https://netlify.com)**
2. **Drag & drop** folder `frontend/dist` (po `npm run build`)
3. **Lub połącz GitHub** i ustaw:
   - Build command: `cd frontend && npm run build`
   - Publish directory: `frontend/dist`

## 🔧 Przygotowanie lokalne

### 1. Build frontend
```bash
cd frontend
npm install
VITE_API_URL=https://your-backend-url.com npm run build
```

### 2. Test backend lokalnie
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
export DATABASE_URL="your-postgres-url"
python api_server.py
```

## 🗄️ Konfiguracja bazy danych

### Railway PostgreSQL:
1. Kliknij **Add Service** → **Database** → **PostgreSQL**
2. Skopiuj **Database URL** z sekcji Variables
3. Uruchom skrypty inicjalizacyjne:

```bash
# Skopiuj DATABASE_URL z Railway
export DATABASE_URL="postgresql://postgres:..."

cd backend
python rozszerz_do_250.py  # Jeśli baza pusta
python sprawdz_statystyki.py  # Weryfikacja
```

### Heroku PostgreSQL:
Automatycznie skonfigurowane przez addon

## 🔐 Zmienne środowiskowe

### Backend (Railway/Heroku):
```
DATABASE_URL=postgresql://...
PORT=5000
HOST=0.0.0.0
FLASK_ENV=production
```

### Frontend (Vercel/Netlify):
```
VITE_API_URL=https://your-backend-url.com
```

## ✅ Checklist deploymentu

- [ ] **Backend działa** (`/api/wyniki` zwraca dane)
- [ ] **Baza danych** wypełniona (250 zawodników)
- [ ] **CORS** skonfigurowany dla frontendu
- [ ] **Frontend** buduje się bez błędów
- [ ] **API URL** prawidłowo ustawiony
- [ ] **Domain** skonfigurowany (opcjonalnie)

## 🐛 Rozwiązywanie problemów

### CORS błędy:
```python
# backend/api_server.py
CORS(app, origins=["https://your-frontend-domain.vercel.app"])
```

### Build błędy frontend:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Baza danych problem:
```bash
# Sprawdź połączenie
cd backend
python -c "import psycopg2; conn = psycopg2.connect('your-db-url'); print('OK')"
```

## 🌍 Domeny własne

### Vercel:
1. **Settings** → **Domains**
2. Dodaj domenę (np. `drabinka.twoja-domena.pl`)
3. Skonfiguruj DNS (A/CNAME records)

### Railway:
1. **Settings** → **Domains**
2. Dodaj custom domain

## 📊 Monitoring

### Railway:
- **Metrics** tab pokazuje CPU/RAM
- **Logs** tab dla debugowania

### Vercel:
- **Analytics** dla ruchu
- **Functions** tab dla API calls

### Heroku:
```bash
heroku logs --tail
heroku ps:scale web=1
heroku restart
```

## 💰 Koszty

- **Railway**: $5/miesiąc za hobby plan + database
- **Vercel**: Darmowy dla hobby projektów
- **Netlify**: Darmowy dla hobby projektów  
- **Heroku**: $7/miesiąc za hobby plan

## 🚀 Live URL przykłady

Po deploymencie będziesz mieć:
- **Frontend**: `https://drabinka-turniejowa.vercel.app`
- **Backend**: `https://drabinka-turniejowa.railway.app`
- **API**: `https://drabinka-turniejowa.railway.app/api/wyniki`

## 📞 Wsparcie

W razie problemów sprawdź:
1. **Logi** serwisów
2. **Network** tab w przeglądarce (F12)
3. **Environment variables**
4. **Build logs** 