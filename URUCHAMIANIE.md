# 🚀 SKATECROSS QR - Instrukcja uruchamiania

## ⚡ Szybkie uruchomienie (ROZWIĄZUJE PROBLEMY Z PORTAMI)

```bash
./quick_start.sh
```

**To polecenie:**
- ✅ Automatycznie znajdzie wolne porty
- ✅ Uruchomi backend z bazą danych  
- ✅ Uruchomi frontend z proxy
- ✅ Otworzy aplikację w przeglądarce
- ✅ Pokaże wszystkie dane z bazy (251 zawodników)

## 🛑 Zatrzymanie

```bash
killall Python && killall node
```

## 📊 Status

Backend API działa poprawnie:
- ✅ Połączenie z bazą Supabase PostgreSQL
- ✅ 251 zawodników w bazie  
- ✅ Wszystkie endpointy API działają
- ✅ QR kody generowane
- ✅ System centrum startu gotowy

## 🔧 Rozwiązanie problemów z portami

**Problem:** Port 5000 zajęty przez AirPlay na macOS
**Rozwiązanie:** `quick_start.sh` automatycznie znajduje wolne porty

**Zawsze używaj `./quick_start.sh` - oszczędzi Ci godziny walki z portami!**

## �� Funkcjonalności

- 👥 Zarządzanie zawodnikami
- 🔲 Generowanie kodów QR
- 🏁 Centrum startu z SECTRO
- 📊 Rankingi na żywo  
- 🏆 Drabinka turniejowa
- 📈 Statystyki klubów
