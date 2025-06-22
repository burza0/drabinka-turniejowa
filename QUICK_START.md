# 🚀 Szybki Start - SKATECROSS QR

> **Uruchom w 3 minuty!** 

## ⚡ Kroki

### 1️⃣ Sklonuj i zainstaluj
```bash
git clone <your-repo-url>
cd skatecross-qr
npm install
```

### 2️⃣ Uruchom dev server
```bash
npm run dev
```

### 3️⃣ Otwórz aplikację
```
🌐 http://localhost:5173
```

## 🔗 Backend

**Projekt ma własny niezależny backend!** 

### Pierwsza instalacja:
```bash
# 1. Setup backendu
cd backend
pip install -r requirements.txt

# 2. Skonfiguruj bazę PostgreSQL
cp env_example .env
# Edytuj .env z danymi swojej bazy PostgreSQL

# 3. Inicjalizuj bazę danych
python init_database.py

# 4. Uruchom serwer
python start_server.py
```

**Server będzie dostępny na**: `http://localhost:5001`  
Vite automatycznie przekierowuje `/api/*` → `http://localhost:5001`

## 🎛️ Aplikacja

Po uruchomieniu masz dostęp do:

### 🏁 **Centrum Startu**
- ✅ Zarządzanie grupami startowymi
- 📱 QR Scanner zawodników  
- 📊 Kolejka startowa
- ⚡ Real-time synchronizacja

### 🖨️ **Drukowanie QR**
- 📋 Lista zawodników z filtrami
- 🔲 Generowanie QR kodów (pojedyncze/masowe)
- 🖨️ System drukowania naklejek
- ⚡ Operacje grupowe

## 🌙 UI Features

- **🔧 Admin Toggle** - przełącznik w prawym górnym rogu
- **🌙 Dark Mode** - automatyczny dark/light mode
- **📱 Responsive** - działa na mobile/tablet/desktop

## 🛠️ Przydatne komendy

```bash
# Build produkcyjny
npm run build

# Podgląd buildu  
npm run preview

# Reset dependencies
rm -rf node_modules && npm install
```

## 🔧 Troubleshooting

### ❌ Backend Error
```
Error: Network Error
```
**Rozwiązanie**: Sprawdź czy backend działa na `localhost:5001`

### ❌ Build Error
```
npm run build # sprawdź błędy
```

### ❌ TypeScript Error
```
npx vue-tsc --noEmit # sprawdź błędy TS
```

## ⚙️ Konfiguracja (opcjonalna)

### Zmiana portu backendu
Edytuj `vite.config.ts`:
```typescript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:5001', // ← domyślny port dla tego projektu
      changeOrigin: true
    }
  }
}
```

### Zmienne środowiskowe
Stwórz `.env.local`:
```env
VITE_API_BASE_URL=http://localhost:5001
```

---

## ✅ **Gotowe!**

Powinieneś mieć działającą aplikację z **Centrum Startu** i **Drukowanie QR** na `http://localhost:5173` 🎉

> 💡 **Tip**: Uruchom backend w osobnym terminalu żeby móc pracować z oboma projektami jednocześnie. 