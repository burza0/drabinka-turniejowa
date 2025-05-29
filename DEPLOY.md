# 🚀 DEPLOY - System zawodów SKATECROSS

## 📦 Architektura systemu

System składa się z **3 komponentów**:

### 1. 🗄️ **Backend API** (Flask + PostgreSQL)
- **Port:** 5000
- **Plik:** `backend/api_server.py`
- **Baza:** PostgreSQL (Supabase)

### 2. 💻 **Panel administratora** (Vue 3 + Vite)
- **Port:** 5173 (dev) / 80 (prod)
- **Katalog:** `frontend/`
- **Przeznaczenie:** Zarządzanie zawodnikami, wyniki, drabinka

### 3. 📱 **QR Scanner** (HTML5 + JavaScript)
- **Port:** 8080 (dev) / 81 (prod)
- **Katalog:** `qr-scanner/`
- **Przeznaczenie:** Mobilna aplikacja do skanowania QR kodów

---

## 🔧 Wymagania systemowe

```bash
# System
Ubuntu 20.04+ / CentOS 8+ / Debian 11+

# Python
Python 3.8+
pip3

# Node.js (dla frontendu)
Node.js 18+
npm

# Baza danych
PostgreSQL 13+ (lub Supabase)

# Serwer HTTP
Nginx
```

---

## 🚀 Instrukcja deployu

### **Krok 1: Przygotowanie serwera**

```bash
# Update systemu
sudo apt update && sudo apt upgrade -y

# Instalacja wymaganych pakietów
sudo apt install python3 python3-pip python3-venv nginx postgresql-client git -y

# Instalacja Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y
```

### **Krok 2: Klonowanie repozytorium**

```bash
# Klonowanie projektu
git clone https://github.com/burza0/drabinka-turniejowa.git
cd drabinka-turniejowa

# Sprawdzenie wersji
git log --oneline -3
```

### **Krok 3: Konfiguracja backendu**

```bash
# Przejście do katalogu backend
cd backend

# Utworzenie virtual environment
python3 -m venv venv
source venv/bin/activate

# Instalacja zależności
pip install -r requirements.txt

# Konfiguracja zmiennych środowiskowych
cp .env.example .env
nano .env
```

**Zawartość `.env**:**
```bash
DATABASE_URL=postgresql://user:password@host:port/database
FLASK_ENV=production
FLASK_DEBUG=False
```

### **Krok 4: Migracja bazy danych**

```bash
# Aktywacja venv
source venv/bin/activate

# Uruchomienie migracji QR kodów
python3 add_qr_columns.py

# Generowanie QR kodów dla zawodników (opcjonalne)
python3 generate_qr_codes.py
```

### **Krok 5: Konfiguracja frontendu**

```bash
# Przejście do katalogu frontend
cd ../frontend

# Instalacja zależności
npm install

# Build aplikacji produkcyjnej
npm run build

# Pliki do deployu będą w katalogu dist/
```

### **Krok 6: Konfiguracja Nginx**

```bash
# Utworzenie konfiguracji Nginx
sudo nano /etc/nginx/sites-available/skatecross
```

**Zawartość pliku:**
```nginx
# Panel administratora (Vue 3)
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        root /path/to/drabinka-turniejowa/frontend/dist;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
    
    # API Backend
    location /api/ {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# QR Scanner (mobilny)
server {
    listen 81;
    server_name your-domain.com;
    
    location / {
        root /path/to/drabinka-turniejowa/qr-scanner;
        index index.html;
        add_header Access-Control-Allow-Origin *;
    }
}
```

```bash
# Aktywacja konfiguracji
sudo ln -s /etc/nginx/sites-available/skatecross /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### **Krok 7: Uruchomienie backendu (Systemd)**

```bash
# Utworzenie service dla systemd
sudo nano /etc/systemd/system/skatecross-api.service
```

**Zawartość service:**
```ini
[Unit]
Description=SKATECROSS API Server
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/drabinka-turniejowa/backend
Environment=PATH=/path/to/drabinka-turniejowa/backend/venv/bin
EnvironmentFile=/path/to/drabinka-turniejowa/backend/.env
ExecStart=/path/to/drabinka-turniejowa/backend/venv/bin/python api_server.py
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

```bash
# Uruchomienie service
sudo systemctl daemon-reload
sudo systemctl enable skatecross-api
sudo systemctl start skatecross-api
sudo systemctl status skatecross-api
```

---

## 🔍 Testowanie deployu

### **1. Backend API:**
```bash
curl http://your-domain.com/api/zawodnicy
curl http://your-domain.com/api/qr/stats
```

### **2. Panel administratora:**
```
http://your-domain.com
```

### **3. QR Scanner:**
```
http://your-domain.com:81
```

---

## 📊 Monitoring i logi

### **Backend:**
```bash
# Logi systemd
sudo journalctl -u skatecross-api -f

# Logi aplikacji
tail -f /path/to/backend/api_server.log
```

### **Nginx:**
```bash
# Logi dostępu
sudo tail -f /var/log/nginx/access.log

# Logi błędów
sudo tail -f /var/log/nginx/error.log
```

### **Baza danych:**
```bash
# Sprawdzenie połączenia
psql $DATABASE_URL -c "SELECT COUNT(*) FROM zawodnicy;"

# Sprawdzenie QR kodów
psql $DATABASE_URL -c "SELECT COUNT(*) FROM zawodnicy WHERE qr_code IS NOT NULL;"
```

---

## 🛠️ Troubleshooting

### **Problem: Backend nie odpowiada**
```bash
sudo systemctl status skatecross-api
sudo journalctl -u skatecross-api -n 50
```

### **Problem: Frontend 404**
```bash
sudo nginx -t
sudo systemctl status nginx
ls -la /path/to/frontend/dist/
```

### **Problem: Błąd bazy danych**
```bash
# Test połączenia
python3 -c "import psycopg2; conn = psycopg2.connect('$DATABASE_URL'); print('OK')"
```

### **Problem: QR Scanner nie działa**
```bash
# Sprawdź pliki
ls -la /path/to/qr-scanner/
curl http://localhost:81/index.html
```

---

## 🔒 SSL/HTTPS (Certbot)

```bash
# Instalacja Certbot
sudo apt install certbot python3-certbot-nginx -y

# Uzyskanie certyfikatu
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Dodaj: 0 2 * * * certbot renew --quiet
```

---

## 📈 Backup

### **Baza danych:**
```bash
# Backup
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore
psql $DATABASE_URL < backup_file.sql
```

### **Aplikacja:**
```bash
# Backup kodu
tar -czf skatecross_backup_$(date +%Y%m%d).tar.gz /path/to/drabinka-turniejowa/
```

---

## 🎯 URLs produkcyjne

- **Panel administratora:** `https://your-domain.com`
- **QR Scanner (mobilny):** `https://your-domain.com:81` 
- **API:** `https://your-domain.com/api`

**System gotowy do zawodów! 🏆** 