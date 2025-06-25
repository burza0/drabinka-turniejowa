# SKATECROSS QR System v1.0.0

## 🏗️ Modular Architecture v32.0

System QR do zarządzania zawodnikami SKATECROSS z modułową architekturą Flask blueprintów.

## 📋 Funkcjonalności

### ✅ Zaimplementowane
- **QR Code Generation** - Generowanie kodów QR dla zawodników
- **Zawodnicy Management** - Zarządzanie danymi zawodników
- **Grupy Startowe** - Tworzenie i zarządzanie grupami
- **QR Scanning** - Skanowanie kodów QR
- **Demo Data** - 8 zawodników demonstracyjnych w pamięci
- **Modular API** - Architektura blueprintów Flask

### 🔧 Architektura

```
skatecross-qr/
├── backend/
│   ├── api/
│   │   ├── __init__.py          # Rejestracja blueprintów
│   │   ├── zawodnicy.py         # API zawodników
│   │   ├── qr_generation.py     # Generowanie QR
│   │   └── centrum_startu.py    # Grupy startowe
│   └── utils/
│       └── database.py          # Demo data w pamięci
├── api_server_modular.py        # Główny serwer
├── VERSION                      # 1.0.0
└── README_QR.md                # Ta dokumentacja
```

## 🚀 Uruchomienie

### Backend (Port 5001)
```bash
cd skatecross-qr
python3 api_server_modular.py
```

### Test API
```bash
# Sprawdź wersję
curl http://localhost:5001/api/version

# Lista zawodników
curl http://localhost:5001/api/zawodnicy

# Grupy startowe
curl http://localhost:5001/api/grupy-startowe

# Statystyki QR
curl http://localhost:5001/api/qr/stats
```

## 📊 Demo Data

System zawiera 8 zawodników demonstracyjnych:
- **Junior A**: Piotr Nowak (M), Katarzyna Kaczmarek (K)
- **Junior B**: Anna Kowalska (K), Michał Dąbrowski (M)
- **Senior**: Maria Wiśniewska (K), Marcin Zieliński (M)
- **Master**: Tomasz Wójcik (M), Aleksandra Szymańska (K)

## 🔗 API Endpoints

### Zawodnicy
- `GET /api/zawodnicy` - Lista wszystkich zawodników
- `GET /api/zawodnicy/{nr_startowy}` - Szczegóły zawodnika
- `GET /api/zawodnicy/kategoria/{kategoria}?plec=M/K` - Zawodnicy z kategorii

### QR Generation
- `GET /api/qr/generate/{nr_startowy}` - Generuj QR kod
- `POST /api/qr/batch` - Generuj wiele QR kodów
- `GET /api/qr/stats` - Statystyki systemu

### Centrum Startu
- `GET /api/grupy-startowe` - Lista grup startowych
- `POST /api/scan-qr` - Skanuj QR kod
- `POST /api/activate-group` - Aktywuj grupę
- `GET /api/grupa-status` - Status aktywnej grupy

### System
- `GET /api/version` - Informacje o wersji
- `GET /` - Strona główna API

## 🛠️ Technologie

- **Backend**: Python 3, Flask
- **Architecture**: Modular Blueprints
- **QR Codes**: qrcode library
- **Data**: In-Memory (demo)
- **CORS**: Enabled

## 📝 Wersjonowanie

- **v1.0.0** - Initial Release
  - Modular Architecture v32.0
  - Demo data (8 zawodników)
  - QR generation & scanning
  - Blueprints architecture
  - Complete API endpoints

---

**SKATECROSS QR v1.0.0** - Modular Architecture for Tournament Management! 🏁 