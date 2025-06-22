# 🏁 SKATECROSS QR - Drabinka Turniejowa

> **Profesjonalny system zarządzania zawodami SKATECROSS** z systemem QR kodów, drabiną turniejową i live timingiem.

![Version](https://img.shields.io/badge/version-1.0.0-green.svg)
![Flask](https://img.shields.io/badge/flask-3.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)

## 🌟 GŁÓWNE FUNKCJONALNOŚCI

### 🏁 **Centrum Startu**
- **Grupy startowe** - Zarządzanie grupami zawodników
- **QR Scanner** - Skanowanie kodów QR przed startem
- **Live Status** - Status zawodników w czasie rzeczywistym

### 👥 **Zarządzanie Zawodnikami**
- **Rejestracja zawodników** - Kompletna baza danych
- **Generowanie QR kodów** - Unikalne kody dla każdego zawodnika
- **Filtrowanie i sortowanie** - Zaawansowane wyszukiwanie

### 🏆 **Drabinka Turniejowa**
- **System eliminacji** - Pełna drabinka pucharowa
- **Ranking zawodników** - Automatyczne sortowanie wyników
- **Statystyki** - Kompletne statystyki zawodów

### 📊 **Live Timing (SECTRO)**
- **Pomiar czasów** - Precyzyjny timing przejazdu
- **Real-time wyniki** - Na żywo aktualizowane rezultaty
- **Ranking na żywo** - Bieżące pozycje zawodników

---

## 🏗️ ARCHITEKTURA SYSTEMU

### 📁 **Backend Flask**
```
backend/
├── api/
│   ├── zawodnicy.py        👤 Zarządzanie zawodnikami
│   ├── qr_generation.py    🔲 Generowanie QR kodów
│   ├── centrum_startu.py   🏁 Centrum startu i grupy
│   └── __init__.py         🔧 Konfiguracja API
├── sectro/
│   └── sectro_api.py       ⏱️ SECTRO Live Timing
├── utils/
│   └── database.py         🗄️ Baza danych PostgreSQL
└── requirements.txt        📦 Zależności
```

### 🌐 **Frontend Vue 3**
```
frontend/
├── src/
│   ├── components/
│   │   ├── Dashboard.vue           📊 Główny dashboard
│   │   ├── QrAdminDashboard.vue    🔲 Panel QR
│   │   ├── StartLineScanner.vue    🏁 Skaner centrum startu
│   │   ├── DrabinkaPucharowa.vue   🏆 Drabinka turniejowa
│   │   └── Rankingi.vue           📈 Rankingi i statystyki
│   └── views/
│       └── SectroView.vue          ⏱️ Live Timing SECTRO
└── package.json
```

---

## 🚀 QUICK START

### **1. Uruchom Backend**
```bash
# Aktywuj środowisko wirtualne
source venv/bin/activate

# Uruchom serwer
python3 api_server_simple.py
# Backend dostępny: http://localhost:5001
```

### **2. Uruchom Frontend**
```bash
# Przejdź do katalogu frontend
cd frontend

# Uruchom dev server
npm run dev
# Frontend dostępny: http://localhost:5173
```

### **3. Lub użyj skryptu automatycznego**
```bash
# Uruchom oba serwery jednocześnie
./start_servers.sh

# Zatrzymaj serwery
./stop_servers.sh
```

---

## 🛒 API ENDPOINTS

### **👥 ZAWODNICY**
```bash
GET  /api/zawodnicy                   # Lista wszystkich zawodników
POST /api/zawodnicy                   # Dodaj nowego zawodnika
PUT  /api/zawodnicy/{id}              # Edytuj zawodnika
DELETE /api/zawodnicy/{id}            # Usuń zawodnika
```

### **🔲 QR KODY**
```bash
GET  /api/qr/dashboard               # Dashboard QR
POST /api/qr/generate                # Generuj kod QR
GET  /api/qr/manual-checkins         # Ręczne zameldowania
```

### **🏁 CENTRUM STARTU**
```bash
GET  /api/grupy-startowe             # Lista grup startowych
POST /api/scan-qr                    # Skanuj QR kod
GET  /api/start-status               # Status centrum startu
```

### **⏱️ SECTRO TIMING**
```bash
POST /api/sectro/sessions            # Nowa sesja timing'u
GET  /api/sectro/results             # Wyniki live timing
POST /api/sectro/checkpoint          # Dodaj checkpoint
```

### **📊 RANKINGI**
```bash
GET  /api/rankings/individual        # Ranking indywidualny
GET  /api/rankings/general           # Ranking generalny
GET  /api/rankings/clubs/total       # Ranking klubów
GET  /api/rankings/medals            # Statystyki medali
```

---

## 🎯 STRUKTURA ZAWODÓW

### **📋 Fazy Zawodów:**
1. **Rejestracja** - Dodawanie zawodników do systemu
2. **Generowanie QR** - Unikalne kody dla każdego zawodnika
3. **Centrum Startu** - Skanowanie QR przed startem
4. **Live Timing** - Pomiar czasów na trasie (SECTRO)
5. **Drabinka** - System eliminacji i finały
6. **Rankingi** - Końcowe wyniki i statystyki

### **🏆 System Punktowy:**
- **Miejsca 1-3** - Punkty za podium
- **Finał** - Dodatkowe punkty za udział
- **Ranking klubów** - Suma punktów zawodników
- **Statystyki** - DNF, DSQ, ukończenia

---

## 🔧 KONFIGURACJA

### **📊 Dashboard**
- **Port Backend:** 5001
- **Port Frontend:** 5173
- **Baza danych:** PostgreSQL (Supabase)
- **Środowisko:** Development/Production

### **🏁 Centrum Startu**
- **Skaner QR** - Automatyczne rozpoznawanie kodów
- **Grupy startowe** - Podział zawodników
- **Status tracking** - Monitoring postępów

### **⏱️ SECTRO Integration**
- **Live Timing** - Połączenie z systemem SECTRO
- **Checkpointy** - Pomiar czasów na trasie
- **Real-time results** - Wyniki na żywo

---

## 📱 UŻYTKOWANIE

### **🔒 Tryb Admin**
- **Zarządzanie zawodnikami** - Dodawanie, edycja, usuwanie
- **Generowanie QR** - Masowe operacje na kodach
- **Centrum Startu** - Kontrola przystupu do startu
- **Live Timing** - Monitoring czasów w temps réel

### **👁️ Tryb Widza**
- **Dashboard** - Przegląd statystyk
- **Rankingi** - Aktualne wyniki
- **Drabinka** - Struktura zawodów
- **Live Results** - Wyniki na żywo

---

## 🛠️ STACK TECHNOLOGICZNY

### **Backend:**
- **Flask 3.0** - Framework web
- **Python 3.11+** - Język programowania
- **PostgreSQL** - Baza danych
- **qrcode 7.4.2** - Generowanie QR

### **Frontend:**
- **Vue 3** - Framework JavaScript
- **Vite** - Build tool i dev server
- **Tailwind CSS** - Framework CSS
- **TypeScript** - Tipowanie statyczne

---

## 🏆 TYPY ZAWODÓW

### **📊 Kategorie Wiekowe:**
- **Junior A/B** - Młodzież
- **Senior** - Dorośli
- **Master** - Weterani
- **Open** - Otwarta kategoria

### **⚡ Formaty Wyścigów:**
- **Time Trial** - Jazda na czas
- **Elimination** - System eliminacyjny
- **Final** - Finały kategorii
- **Team** - Zawody drużynowe

---

## 📋 WYMAGANIA SYSTEMOWE

### **🖥️ Serwer:**
- **Python 3.11+**
- **Node.js 18+**
- **PostgreSQL 14+**
- **2GB RAM minimum**

### **📱 Klient:**
- **Nowoczesna przeglądarka** (Chrome 90+, Firefox 88+)
- **Obsługa JavaScript**
- **Połączenie internetowe**
- **Skaner QR** (opcjonalnie kamera)

---

*Made with 🏁 for SKATECROSS racing • SKATECROSS QR v1.0.0* 