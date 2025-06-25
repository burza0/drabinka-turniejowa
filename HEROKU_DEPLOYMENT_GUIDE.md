# 🚀 SKATECROSS v36.1 - Przewodnik Wdrożenia na Heroku

## 📋 Przygotowanie przed wdrożeniem

### 1. Wymagania systemu
- ✅ Konto Heroku (https://heroku.com)
- ✅ Heroku CLI zainstalowane
- ✅ Git repository z kodem
- ✅ Konfiguracja Supabase PostgreSQL

### 2. Pliki konfiguracyjne (już przygotowane)
- ✅ `Procfile` - konfiguracja web worker
- ✅ `runtime.txt` - Python 3.9.20
- ✅ `app.json` - konfiguracja aplikacji
- ✅ `package.json` - build process
- ✅ `requirements.txt` - zależności Python

## 🛠️ Krok po kroku - Wdrożenie

### Krok 1: Logowanie do Heroku
```bash
heroku login
```

### Krok 2: Tworzenie aplikacji Heroku
```bash
heroku create skatecross-v36-production
# lub wybierz własną nazwę
```

### Krok 3: Konfiguracja zmiennych środowiskowych
```bash
# Supabase Configuration
heroku config:set SUPABASE_URL=https://your-project.supabase.co
heroku config:set SUPABASE_ANON_KEY=your_anon_key_here
heroku config:set SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here

# Flask Environment
heroku config:set FLASK_ENV=production
heroku config:set SYSTEM_VERSION=36.1

# SECTRO Integration
heroku config:set SECTRO_API_URL=http://localhost:8080
heroku config:set SECTRO_ENABLED=true
```

### Krok 4: Dodanie Heroku PostgreSQL (opcjonalne backup)
```bash
heroku addons:create heroku-postgresql:essential-0
```

### Krok 5: Deploy aplikacji
```bash
git add .
git commit -m "🚀 Production deployment v36.1"
git push heroku master
```

### Krok 6: Skalowanie aplikacji
```bash
heroku ps:scale web=1
```

### Krok 7: Sprawdzenie statusu
```bash
heroku ps
heroku logs --tail
```

## 🌐 Dostęp do aplikacji

Po wdrożeniu aplikacja będzie dostępna pod adresem:
```
https://your-app-name.herokuapp.com
```

## 📊 Struktura wdrożenia

### Backend (Flask)
- **Port**: Automatycznie przydzielony przez Heroku
- **Web server**: Gunicorn
- **Database**: Supabase PostgreSQL
- **API endpoints**: `/api/*`

### Frontend (Vue.js)
- **Build**: Automatyczny build podczas wdrożenia
- **Pliki statyczne**: Serwowane przez Flask
- **Entry point**: `/`

## 🔧 Konfiguracja środowiska

### Buildpacks (automatyczne)
1. `heroku/nodejs` - dla build frontendu
2. `heroku/python` - dla backendu Flask

### Zmienne środowiskowe
| Zmienna | Wymagana | Opis |
|---------|----------|------|
| `SUPABASE_URL` | ✅ | URL projektu Supabase |
| `SUPABASE_ANON_KEY` | ✅ | Klucz publiczny Supabase |
| `SUPABASE_SERVICE_ROLE_KEY` | ✅ | Klucz serwisowy Supabase |
| `FLASK_ENV` | ✅ | `production` |
| `SECTRO_API_URL` | ⚙️ | URL systemu SECTRO |
| `PORT` | 🤖 | Automatycznie przez Heroku |

## 🚨 Rozwiązywanie problemów

### Problem: Build failed
```bash
heroku logs --tail
# Sprawdź logi buildu
```

### Problem: Application error
```bash
heroku logs --tail
# Sprawdź logi aplikacji
```

### Problem: Database connection
```bash
heroku config
# Sprawdź czy zmienne Supabase są ustawione
```

### Restart aplikacji
```bash
heroku restart
```

## 📈 Monitorowanie

### Metryki aplikacji
```bash
heroku addons:create newrelic:wayne
```

### Logi w czasie rzeczywistym
```bash
heroku logs --tail
```

### Status aplikacji
```bash
heroku ps
heroku status
```

## 🔄 Aktualizacje

### Deploy nowej wersji
```bash
git add .
git commit -m "Update to v36.2"
git push heroku master
```

### Rollback do poprzedniej wersji
```bash
heroku rollback
```

## 💰 Koszty

### Plan Basic (zalecany)
- **Web dyno**: $7/miesiąc
- **PostgreSQL**: $9/miesiąc (opcjonalne)
- **Razem**: ~$16/miesiąc

### Plan Free (ograniczenia)
- **Web dyno**: 550 godzin/miesiąc (ograniczone)
- **PostgreSQL**: 10,000 wierszy (ograniczone)

## ✅ Checklist końcowy

- [ ] Aplikacja tworzy się bez błędów
- [ ] Zmienne środowiskowe ustawione
- [ ] Frontend ładuje się poprawnie
- [ ] API endpoints odpowiadają
- [ ] Połączenie z Supabase działa
- [ ] System SECTRO może łączyć się z API
- [ ] SSL/HTTPS działa automatycznie

## 🎯 Finalne URL endpoints

```
https://your-app.herokuapp.com/                    # Frontend
https://your-app.herokuapp.com/api/version         # API version
https://your-app.herokuapp.com/api/unified/*       # Unified API
```

**SKATECROSS v36.1 gotowy do produkcji! 🏁** 