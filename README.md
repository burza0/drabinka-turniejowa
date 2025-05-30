# 🏆 SKATECROSS - System zarządzania zawodami z QR kodami

Profesjonalny system do zarządzania zawodami SKATECROSS z funkcjonalnością QR kodów dla szybkiego meldowania zawodników i zapisywania wyników.

![System SKATECROSS](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Vue 3](https://img.shields.io/badge/Vue-3.5.13-4FC08D)
![Flask](https://img.shields.io/badge/Flask-2.3.2-000000)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-336791)
![Heroku](https://img.shields.io/badge/Deploy-Heroku-430098)

## 🚀 URLs Produkcyjne

### 🏆 Panel Administratora (Vue 3)
```
https://drabinka-turniejowa-skatecross-17be0c216c6f.herokuapp.com
```
**Przeznaczenie:** Zarządzanie zawodnikami, wynikami i drabinką turniejową

### 📱 QR Scanner (Mobilny)
```
https://drabinka-turniejowa-skatecross-17be0c216c6f.herokuapp.com/qr-scanner
```
**Przeznaczenie:** Skanowanie QR kodów przez sędziów na urządzeniach mobilnych

### 🔌 API Backend
```
https://drabinka-turniejowa-skatecross-17be0c216c6f.herokuapp.com/api
```
**Przeznaczenie:** RESTful API dla wszystkich operacji systemowych

## 📋 Funkcjonalności

### 🏅 Panel Administratora
- ✅ **Zarządzanie zawodnikami** - dodawanie, edycja, usuwanie (251 zawodników)
- ✅ **Zapisywanie wyników** - czasy przejazdu, statusy (FINISHED, DNF, DSQ)
- ✅ **Drabinka turniejowa** - automatyczne generowanie ćwierćfinałów, półfinałów, finału
- ✅ **Statystyki** - podsumowania według kategorii i płci
- ✅ **Filtrowanie** - według klubów, kategorii, płci, statusów
- ✅ **Responsive design** - działa na wszystkich urządzeniach

### 📱 QR Scanner (Mobilny)
- ✅ **Check-in zawodników** - szybkie meldowanie przez skanowanie QR kodu
- ✅ **Zapisywanie wyników** - wprowadzanie czasów bezpośrednio na trasie
- ✅ **Weryfikacja statusu** - sprawdzanie pozycji i awansu do drabinki
- ✅ **Statystyki na żywo** - monitoring postępu zawodów
- ✅ **Offline support** - działa bez stałego połączenia internetowego

### 🔐 System QR Kodów
- ✅ **251 unikalnych kodów** wygenerowanych dla wszystkich zawodników
- ✅ **Format:** `SKATECROSS_{nr_startowy}_{unique_hash}`
- ✅ **Przykład:** `SKATECROSS_2_BEB529B1` (Anna Nowak, nr 2)
- ✅ **Baza checkpointów** - logowanie wszystkich skanów
- ✅ **Weryfikacja statusu** - pozycja w kategorii i awans do drabinki

## 🏗️ Architektura Systemu

### Frontend (Vue 3 + TypeScript)
```
frontend/
├── src/
│   ├── App.vue              # Główna aplikacja
│   ├── components/
│   │   ├── EditZawodnikModal.vue
│   │   └── ZawodnikCard.vue
│   └── main.ts
├── dist/                    # Zbudowana aplikacja
└── package.json
```

### Backend (Flask + Python)
```
backend/
├── api_server.py           # Główny serwer API
├── add_qr_columns.py       # Migracja bazy danych
├── generate_qr_codes.py    # Generator QR kodów
└── requirements.txt
```

### QR Scanner (HTML5 + JavaScript)
```
qr-scanner/
└── index.html             # Mobilna aplikacja do skanowania
```

### Baza Danych (PostgreSQL - Supabase)
```sql
-- Główne tabele
zawodnicy (nr_startowy, imie, nazwisko, kategoria, plec, klub, qr_code, checked_in, check_in_time)
wyniki (nr_startowy, czas_przejazdu_s, status)
kluby (id, nazwa, miasto, utworzony_date)
checkpoints (id, nr_startowy, checkpoint_name, qr_code, scan_time, device_id)
```

## 🛠️ Technologie

### Frontend
- **Vue 3.5.13** - Reaktywny framework UI
- **TypeScript** - Statyczne typowanie
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client
- **Heroicons** - Ikony SVG
- **Vite** - Build tool

### Backend
- **Flask 2.3.2** - Web framework
- **PostgreSQL** - Baza danych (Supabase)
- **psycopg2** - PostgreSQL adapter
- **Flask-CORS** - Cross-Origin Resource Sharing
- **python-dotenv** - Environment variables
- **qrcode[pil]** - Generowanie QR kodów

### QR Scanner
- **HTML5-QRCode** - Biblioteka do skanowania QR
- **Responsive Web Design** - Optymalizacja mobilna
- **Progressive Web App** - Możliwość instalacji jako aplikacja

### Hosting & Deploy
- **Heroku** - Platform as a Service
- **Supabase** - Backend as a Service (PostgreSQL)
- **Git** - Version control
- **GitHub** - Repository hosting

## 📊 Stan Systemu

```json
{
  "total_zawodnikow": 251,
  "z_qr_kodami": 251,
  "zameldowanych": 2,
  "bez_qr_kodow": 0,
  "procent_zameldowanych": 0.8,
  "checkpoints": [
    {"checkpoint_name": "check-in", "count": 2},
    {"checkpoint_name": "finish", "count": 1}
  ]
}
```

## 🎯 Użytkowanie

### 👥 Dla Organizatorów
1. Otwórz **Panel Administratora** na komputerze
2. Zarządzaj zawodnikami i wynikami
3. Śledź postęp w czasie rzeczywistym
4. Generuj drabinkę turniejową

### 📱 Dla Sędziów (Mobile)
1. Otwórz **QR Scanner** na telefonie/tablecie
2. Wybierz funkcję:
   - **Check-in** - meldowanie zawodników
   - **Wyniki** - zapisywanie czasów
   - **Weryfikuj** - sprawdzanie statusu
3. Skanuj QR kody zawodników
4. System automatycznie zapisuje dane

### 🏃‍♂️ Dla Zawodników
- Każdy zawodnik ma **unikalny QR kod**
- Kod może być wydrukowany na numerze startowym
- Skanowanie umożliwia szybkie działania bez ręcznego wpisywania danych

## 🔄 API Endpoints

### Zawodnicy
- `GET /api/zawodnicy` - Lista wszystkich zawodników
- `POST /api/zawodnicy` - Dodaj nowego zawodnika
- `PUT /api/zawodnicy/{nr}` - Edytuj zawodnika
- `DELETE /api/zawodnicy/{nr}` - Usuń zawodnika

### Wyniki
- `GET /api/wyniki` - Lista wszystkich wyników
- `PUT /api/wyniki` - Aktualizuj wynik

### Drabinka
- `GET /api/drabinka` - Drabinka turniejowa (ćwierćfinały, półfinały, finał)

### QR Kody
- `POST /api/qr/check-in` - Zamelduj zawodnika
- `POST /api/qr/scan-result` - Zapisz wynik przez QR
- `POST /api/qr/verify-result` - Weryfikuj status zawodnika
- `POST /api/qr/generate/{nr}` - Wygeneruj QR kod
- `GET /api/qr/stats` - Statystyki QR kodów

### Statystyki
- `GET /api/statystyki` - Statystyki według kategorii/płci
- `GET /api/kategorie` - Lista kategorii
- `GET /api/kluby` - Lista klubów

## 🚀 Deploy

### Heroku (Produkcja)
```bash
# Clone repository
git clone https://github.com/burza0/drabinka-turniejowa.git
cd drabinka-turniejowa

# Deploy to Heroku
git push heroku master
```

### Lokalne uruchomienie

#### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="postgresql://..."
python api_server.py
```

#### Frontend
```bash
cd frontend
npm install
npm run build  # Produkcja
npm run dev    # Development
```

#### QR Scanner
```bash
cd qr-scanner
python3 -m http.server 8080
# Lub serwowane przez backend na /qr-scanner
```

## 🔧 Konfiguracja

### Zmienne środowiskowe (.env)
```bash
DATABASE_URL=postgresql://user:pass@host:port/database
PORT=5000
HOST=0.0.0.0
FLASK_ENV=production
FLASK_DEBUG=False
```

### Baza danych (Supabase)
- Automatyczne migracje przez `add_qr_columns.py`
- Backup i restore wspierane
- SSL połączenia

## 📱 QR Kody - Szczegóły

### Format
```
SKATECROSS_{nr_startowy}_{8_char_hash}
```

### Przykłady
```
SKATECROSS_1_A1B2C3D4    # Zawodnik nr 1
SKATECROSS_2_BEB529B1    # Zawodnik nr 2 (Anna Nowak)
SKATECROSS_150_F7E8D9C2  # Zawodnik nr 150
```

### Generowanie
- Automatyczne przez `generate_qr_codes.py`
- Unikalne hashe UUID4
- Sprawdzanie duplikatów
- Możliwość regeneracji

### Workflow Skanowania
1. **Skanowanie** → Rozpoznanie tekstu `SKATECROSS_X_HASH`
2. **API Call** → `POST /api/qr/check-in` z kodem
3. **Baza danych** → `SELECT * FROM zawodnicy WHERE qr_code = ?`
4. **Odpowiedź** → Dane zawodnika + status operacji
5. **UI Update** → Wyświetlenie rezultatu

## 📈 Monitorowanie

### Logi Heroku
```bash
heroku logs --tail --app drabinka-turniejowa-skatecross
```

### Metryki
- Liczba skanów QR kodów
- Czas odpowiedzi API
- Użycie bazy danych
- Błędy i wyjątki

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📜 Copyright

**Copyright © 2025 Mariusz Burzyński. Wszelkie prawa zastrzeżone.**

## 👨‍💻 Autor

**Mariusz Burzyński** - System SKATECROSS z QR kodami

---

**🏆 System gotowy do zawodów SKATECROSS! Skanuj, zarządzaj, wygrywaj! 🚀**
