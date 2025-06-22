# 🚀 SECTRO LIVE TIMING MODULE - PLAN IMPLEMENTACJI

## 📁 STRUKTURA KATALOGÓW

### Backend - Nowe pliki:
```
backend/
├── sectro/                          # Nowy moduł SECTRO
│   ├── __init__.py
│   ├── sectro_parser.py             # Parser ramek SECTRO
│   ├── sectro_api.py                # API endpoints
│   ├── sectro_hardware.py           # Komunikacja z urządzeniem
│   └── sectro_database.py           # Operacje na bazie
├── websockets/                      # WebSocket dla live updates
│   ├── __init__.py
│   └── live_timing_ws.py
└── migrations/
    └── 03_add_sectro_tables.sql     # Migracja bazy
```

### Frontend - Nowe komponenty:
```
frontend/src/
├── components/
│   ├── sectro/                      # Komponenty SECTRO
│   │   ├── LiveTiming.vue           # Główny dashboard
│   │   ├── SectroSetup.vue          # Konfiguracja urządzenia  
│   │   ├── TimingSession.vue        # Sesja pomiarów
│   │   ├── LiveResults.vue          # Live wyniki
│   │   └── SectroLogs.vue           # Logi i historia
│   └── shared/
│       └── WebSocketConnection.vue   # WebSocket client
├── views/
│   └── SectroView.vue               # Główna strona SECTRO
└── composables/
    ├── useSectro.js                 # Composable SECTRO
    └── useWebSocket.js              # WebSocket management
```

## 🗄️ BAZA DANYCH - NOWE TABELE

### Tabela: sectro_sessions
```sql
CREATE TABLE sectro_sessions (
    id SERIAL PRIMARY KEY,
    nazwa VARCHAR(100) NOT NULL,
    kategoria VARCHAR(50),
    plec CHAR(1),
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP NULL,
    status VARCHAR(20) DEFAULT 'active',
    config JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabela: sectro_measurements  
```sql
CREATE TABLE sectro_measurements (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES sectro_sessions(id),
    nr_startowy INTEGER REFERENCES zawodnicy(nr_startowy),
    measurement_type VARCHAR(10) NOT NULL, -- 'START', 'FINISH', 'SPLIT'
    wejscie INTEGER NOT NULL,               -- Numer wejścia SECTRO (1-8)
    timestamp_sectro DECIMAL(15,3),         -- Czas z urządzenia
    timestamp_received TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    raw_frame TEXT,                         -- Oryginalna ramka
    processed BOOLEAN DEFAULT FALSE
);
```

### Tabela: sectro_results
```sql  
CREATE TABLE sectro_results (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES sectro_sessions(id),
    nr_startowy INTEGER REFERENCES zawodnicy(nr_startowy),
    start_time DECIMAL(15,3),
    finish_time DECIMAL(15,3), 
    total_time DECIMAL(10,3),               -- Czas przejazdu w sekundach
    splits JSON,                            -- Split times (jeśli więcej punktów)
    status VARCHAR(20) DEFAULT 'completed', -- completed, disqualified, dns
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(session_id, nr_startowy)
);
```

### Tabela: sectro_logs
```sql
CREATE TABLE sectro_logs (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES sectro_sessions(id),
    log_type VARCHAR(20),                   -- 'INFO', 'ERROR', 'FRAME', 'CONNECTION'
    message TEXT,
    raw_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔧 BACKEND API ENDPOINTS

### sectro_api.py - Nowe endpointy:
```python
/api/sectro/sessions                 [GET, POST]    # Lista/tworzenie sesji
/api/sectro/sessions/{id}            [GET, PUT, DELETE] # Operacje na sesji
/api/sectro/sessions/{id}/start      [POST]         # Start pomiaru
/api/sectro/sessions/{id}/stop       [POST]         # Stop pomiaru  
/api/sectro/sessions/{id}/results    [GET]          # Wyniki sesji
/api/sectro/measurements             [GET, POST]    # Pomiary
/api/sectro/hardware/status          [GET]          # Status urządzenia
/api/sectro/hardware/connect         [POST]         # Połącz z SECTRO
/api/sectro/hardware/disconnect      [POST]         # Rozłącz SECTRO
/api/sectro/logs                     [GET]          # Historia logów
```

### WebSocket endpoints:
```python
/ws/live-timing/{session_id}         # Live updates wyników
/ws/sectro-status                    # Status urządzenia
```

## 🎨 FRONTEND KOMPONENTY

### 1. SectroView.vue - Główna strona
```vue
<template>
  <div class="sectro-main">
    <h1>SECTRO Live Timing</h1>
    <SectroSetup v-if="!connected" @connected="onConnected" />
    <LiveTiming v-else :session="currentSession" />
  </div>
</template>
```

### 2. LiveTiming.vue - Dashboard live
```vue
<template>
  <div class="live-timing">
    <div class="timer-display">{{ currentTime }}</div>
    <div class="waiting-queue">
      <h3>Kolejny zawodnik:</h3>
      <input v-model="nextAthlete" placeholder="Nr startowy" />
    </div>
    <LiveResults :results="liveResults" />
  </div>
</template>
```

### 3. LiveResults.vue - Tabela wyników
```vue
<template>
  <div class="results-table">
    <table>
      <thead>
        <tr>
          <th>Nr</th>
          <th>Imię Nazwisko</th>
          <th>Czas</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="result in sortedResults" :key="result.nr_startowy">
          <td>{{ result.nr_startowy }}</td>
          <td>{{ result.imie }} {{ result.nazwisko }}</td>
          <td>{{ formatTime(result.total_time) }}</td>
          <td>{{ result.status }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
```

## ⚡ ROUTING - DODANIE DO APLIKACJI

### router/index.js - Nowa ruta:
```javascript
{
  path: '/sectro',
  name: 'Sectro',
  component: () => import('@/views/SectroView.vue'),
  meta: { title: 'SECTRO Live Timing' }
}
```

### App.vue - Dodanie do menu:
```vue
<router-link to="/sectro" class="nav-link">
  ⏱️ Live Timing
</router-link>
```

## 🚀 HARMONOGRAM IMPLEMENTACJI

### TYDZIEŃ 1: Backend Foundation
- **Dzień 1-2:** Migracja bazy danych, podstawowe tabele
- **Dzień 3-4:** sectro_parser.py - parser ramek SECTRO  
- **Dzień 5-7:** sectro_api.py - podstawowe API endpoints

### TYDZIEŃ 2: Hardware Integration
- **Dzień 1-3:** sectro_hardware.py - komunikacja z urządzeniem
- **Dzień 4-5:** WebSocket server dla live updates
- **Dzień 6-7:** Testowanie z rzeczywistym SECTRO

### TYDZIEŃ 3: Frontend Development  
- **Dzień 1-2:** Podstawowe komponenty Vue.js
- **Dzień 3-4:** LiveTiming dashboard
- **Dzień 5-7:** Integracja WebSocket, live updates

### TYDZIEŃ 4: Integration & Testing
- **Dzień 1-3:** Integracja z istniejącą aplikacją
- **Dzień 4-5:** Testowanie na pełnym workflow
- **Dzień 6-7:** Bug fixing, polish UX

## 🔧 KLUCZOWE FUNKCJONALNOŚCI

### MUSI MIEĆ (MVP):
- ✅ Połączenie z urządzeniem SECTRO
- ✅ Parser ramek CZL/CHL  
- ✅ Pomiar START → FINISH
- ✅ Zapis wyników do bazy
- ✅ Podstawowy dashboard

### NICE TO HAVE:
- 📊 Live charts/graphs
- 📱 Mobile responsive view
- 🔔 Sound notifications
- 📈 Real-time rankings
- 🎯 Split times support

## 🎯 NASTĘPNE KROKI

1. **Zatwierdź plan** - czy wszystko wygląda OK?
2. **Setup environment** - dependencies, baza danych
3. **Początek kodowania** - zacznijmy od migracji bazy!

**GOTOWY DO STARTU?** 🚀 