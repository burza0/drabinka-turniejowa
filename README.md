# 🏁 SKATECROSS v36.0 - Unified Tournament Management System

**Profesjonalny system zarządzania turniejami skatecross z integracją QR, pomiarami czasu SECTRO i zaawansowanym centrum startu.**

## 🚀 Najważniejsze funkcje

### 📊 **Unified Start Control** (FAZA 3 - UKOŃCZONA)
- **Centrum Startu + SECTRO** - zintegrowany system meldowania i pomiarów
- **Zarządzanie grupami startowymi** - tworzenie, moderowanie, usuwanie grup
- **Real-time dashboard** - 251 zawodników, 14 klubów, dynamiczne statusy
- **QR Scanner** - automatyczne meldowanie przez skanowanie kodów
- **Backup meldowanie** - ręczne meldowanie z powodami organizatora

### 🔲 **System QR**
- **Bulk generowanie** - kody QR dla wszystkich 251 zawodników
- **Drukowanie etykiet** - profesjonalne naklejki z danymi zawodnika
- **Admin Dashboard** - statystyki, zarządzanie, historia meldowań
- **Advanced Print** - zaawansowane opcje druku i formatowania

### ⏱️ **Integracja SECTRO**
- **Automatyczne sesje** - tworzenie sesji pomiarowych dla grup
- **Real-time pomiary** - start, finish, total time
- **Status tracking** - WAITING → REGISTERED → READY → TIMING → FINISHED
- **Priority system** - sortowanie według statusu i czasu

### 📈 **Analityka i Raporty**
- **Dashboard główny** - przegląd systemu, statystyki turnieju
- **Rankingi** - kategorie, kluby, czasy przejazdu
- **Eksport danych** - CSV, raporty, backup
- **Historia aktywności** - szczegółowe logi systemowe

## 🛠️ **Architektura Techniczna**

### **Backend (Python/Flask)**
```
📦 Backend Architecture
├── 🐍 Flask API Server (Python 3.11+)
├── 🗄️ Supabase PostgreSQL (Cloud Database)
├── 🔄 Unified Start Manager (Core Logic)
├── 📊 SECTRO Integration (Time Measurements)
├── 🔲 QR Generation System
├── 🏁 Tournament Management
└── 📈 Analytics & Reporting
```

**Główne moduły:**
- `unified_start_manager.py` - logika biznesowa unified systemu
- `api/unified_start_api.py` - endpointy REST API
- `api/zawodnicy.py` - zarządzanie zawodnikami
- `api/qr_generation.py` - system kodów QR
- `utils/database.py` - connection pool PostgreSQL

### **Frontend (Vue 3/TypeScript)**
```
📦 Frontend Architecture
├── ⚡ Vue 3 + TypeScript + Vite
├── 🎨 Tailwind CSS (Modern UI)
├── 📱 Responsive Design
├── 🔄 Real-time Updates
├── 🧩 Component Architecture
└── 🚀 Hot Reload Development
```

**Kluczowe komponenty:**
- `UnifiedStartControl.vue` - centrum zarządzania startem
- `StartGroupsCard.vue` - grupy startowe z zarządzaniem
- `QRScannerCard.vue` - skaner QR z backup opcjami
- `QrAdminDashboard.vue` - admin panel systemu QR
- `Dashboard.vue` - główny dashboard systemu

## 🔧 **Instalacja i Uruchomienie**

### **Wymagania systemowe:**
- **Python 3.11+** z pip
- **Node.js 24.2.0+** z npm
- **Supabase PostgreSQL** (cloud database)
- **macOS/Linux/Windows**

### **Backend Setup:**
```bash
# 1. Przejdź do katalogu backend
cd /Users/mariusz/drabinka-turniejowa/backend

# 2. Aktywuj środowisko wirtualne
source venv/bin/activate

# 3. Uruchom serwer API
python3 api_server.py
```
**✅ Backend działa na: http://localhost:5001**

### **Frontend Setup:**
```bash
# 1. Przejdź do katalogu frontend
cd /Users/mariusz/drabinka-turniejowa/frontend

# 2. Skonfiguruj Node.js
source ~/.nvm/nvm.sh
nvm use v24.2.0

# 3. Uruchom serwer dev
npm run dev -- --port 5173
```
**✅ Frontend działa na: http://localhost:5173**

### **⚠️ Kolejność uruchomienia:**
1. **NAJPIERW** - Backend (port 5001)
2. **POTEM** - Frontend (port 5173)

*Backend musi być uruchomiony przed frontendem - inaczej proxy errors!*

## 📊 **Baza Danych**

### **Główne tabele:**
```sql
-- Zawodnicy (251 rekordów)
zawodnicy: nr_startowy, imie, nazwisko, kategoria, plec, klub, 
           qr_code, checked_in, check_in_time

-- Sesje SECTRO
sectro_sessions: id, nazwa, status, created_at, start_time, end_time

-- Wyniki pomiarów
sectro_results: nr_startowy, session_id, start_time, finish_time, 
                total_time, status

-- Grupy startowe  
grupy_startowe: kategoria, plec, status, created_at
```

### **Statystyki systemu:**
- **251 zawodników** z 14 klubów
- **6 kategorii** (Junior A-D, Masters, Senior)
- **Unified API** - 15+ endpointów REST
- **Real-time updates** co 30 sekund

## 🔗 **API Endpoints**

### **Unified Start Control:**
```http
GET    /api/unified/dashboard-data    # Dashboard z grupami i statystykami
POST   /api/unified/register-athlete  # Meldowanie zawodnika (QR/manual)
GET    /api/unified/group-details     # Szczegóły grupy z zawodnikami
POST   /api/unified/remove-athlete    # Usunięcie zawodnika z grupy
POST   /api/unified/delete-group      # Usunięcie całej grupy
GET    /api/unified/health           # Status systemu
```

### **Zarządzanie zawodnikami:**
```http
GET    /api/zawodnicy                # Lista zawodników (z paginacją)
GET    /api/zawodnicy/{nr}           # Szczegóły zawodnika
POST   /api/zawodnicy                # Dodanie zawodnika
PUT    /api/zawodnicy/{nr}           # Edycja zawodnika
DELETE /api/zawodnicy/{nr}           # Usunięcie zawodnika
```

### **System QR:**
```http
GET    /api/qr/generate/{nr}         # Generowanie pojedynczego QR
POST   /api/qr/bulk-generate         # Bulk generowanie QR kodów
GET    /api/qr/dashboard             # Dashboard QR (DEPRECATED)
```

## 🏆 **Funkcjonalności Biznesowe**

### **1. Zarządzanie Turniejem**
- ✅ Import zawodników z CSV
- ✅ Kategoryzacja (kategoria + płeć)
- ✅ Zarządzanie klubami
- ✅ Generowanie numerów startowych
- ✅ Export danych i raportów

### **2. System Meldowania**
- ✅ QR Code scanning (automaty)
- ✅ Ręczne meldowanie (backup)
- ✅ Powody meldowania (awaria, brak QR, decyzja organizatora)
- ✅ Walidacja i zabezpieczenia
- ✅ Historia meldowań

### **3. Grupy Startowe**
- ✅ Automatyczne tworzenie grup (kategoria + płeć)
- ✅ Moderowanie zawartości grup
- ✅ Usuwanie zawodników z grup
- ✅ Usuwanie całych grup
- ✅ Integracja z sesjami SECTRO

### **4. Pomiary Czasu**
- ✅ Integracja z systemem SECTRO
- ✅ Automatyczne sesje dla grup
- ✅ Real-time pomiary (start/finish/total)
- ✅ Status tracking zawodników
- ✅ Priority system wyświetlania

### **5. Monitoring i Analityka**
- ✅ Real-time dashboard
- ✅ Statystyki turnieju
- ✅ Historia aktywności
- ✅ Performance monitoring
- ✅ Error handling i recovery

## 🔒 **Bezpieczeństwo**

### **Walidacja danych:**
- ✅ Sprawdzanie istnienia zawodników
- ✅ Zapobieganie podwójnemu meldowaniu
- ✅ Walidacja sesji SECTRO
- ✅ Zabezpieczenie przed usunięciem podczas pomiarów

### **Error handling:**
- ✅ Graceful fallbacks
- ✅ Retry mechanisms
- ✅ Connection pooling
- ✅ SSL database connections
- ✅ Detailed error logging

### **Data integrity:**
- ✅ Transaction safety
- ✅ Backup procedures
- ✅ Data validation
- ✅ Audit trails

## 📱 **Interfejs Użytkownika**

### **Modern Design:**
- 🎨 **Tailwind CSS** - modern utility-first framework
- 📱 **Responsive** - adaptuje się do wszystkich urządzeń
- 🌙 **Dark Mode** - wsparcie trybu ciemnego
- ⚡ **Real-time** - aktualizacje bez odświeżania
- 🧩 **Component-based** - modularna architektura

### **Główne widoki:**
1. **Dashboard** - przegląd systemu, statystyki
2. **Start Control** - unified centrum zarządzania startem
3. **QR Admin** - zarządzanie kodami QR, meldowania
4. **QR Print** - drukowanie etykiet (251 zawodników)
5. **Zawodnicy** - CRUD, edycja, paginacja

## 🚧 **Historia Rozwoju**

### **v36.0 (Aktualna) - Unified Start Control**
- ✅ Integracja Centrum Startu + SECTRO
- ✅ Zarządzanie grupami startowymi
- ✅ Naprawa wszystkich starych API endpoints
- ✅ Unified system meldowania
- ✅ Kompletna migracja z v2 na unified

### **v35.0 - SECTRO Integration**
- ✅ Integracja systemu pomiarów SECTRO
- ✅ Real-time status tracking
- ✅ Automatyczne sesje pomiarowe
- ✅ Priority system wyświetlania

### **v30.0 - QR System**
- ✅ System kodów QR
- ✅ Bulk generowanie i drukowanie
- ✅ Admin dashboard
- ✅ Scanning interface

### **v1.0-29.0 - Foundation**
- ✅ Podstawowe zarządzanie turniejami
- ✅ CRUD zawodników
- ✅ Baza danych PostgreSQL
- ✅ Vue.js frontend

## 🔮 **Roadmap**

### **v37.0 - Enhanced Analytics**
- 📊 Zaawansowane raporty i wykresy
- 📈 Performance analytics
- 🎯 Predictive insights
- 📱 Mobile app companion

### **v38.0 - Multi-Tournament**
- 🏟️ Obsługa wielu turniejów jednocześnie
- 👥 Zarządzanie organizatorami
- 🔐 Role-based permissions
- ☁️ Cloud deployment

### **v39.0 - IoT Integration**
- 📡 Integracja z urządzeniami IoT
- 📸 Automatic photo capture
- 🔊 Audio announcements
- 📺 Live streaming integration

## 📞 **Wsparcie**

### **Kontakt:**
- 📧 Email: [kontakt@skatecross.pl]
- 📱 Phone: [+48 XXX XXX XXX]
- 💬 Discord: [SKATECROSS Community]
- 📋 Issues: [GitHub Issues]

### **Dokumentacja:**
- 📖 **README.md** - ten plik
- 📝 **QUICK_START.md** - szybki start
- 🔧 **API_DOCS.md** - dokumentacja API
- 🏗️ **ARCHITECTURE.md** - architektura systemu

---

**© 2025 SKATECROSS Tournament Management System v36.0**  
*Professional software for skatecross tournament management with QR integration, SECTRO time measurements, and unified start control.*

**🔥 System gotowy do profesjonalnego użytku na turniejach skatecross! 🏁** 