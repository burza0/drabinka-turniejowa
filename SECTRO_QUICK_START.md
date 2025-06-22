# 🚀 SECTRO LIVE TIMING - PRZEWODNIK SZYBKIEGO STARTU

## 🎯 KROK 1: MIGRACJA BAZY DANYCH (5 min)

### Połącz się z bazą i wykonaj migrację:
```bash
# Z katalogu głównego projektu
psql $DATABASE_URL -f backend/migrations/03_add_sectro_tables.sql
```

### Sprawdź czy tabele zostały utworzone:
```sql
-- Sprawdź w bazie danych
\dt sectro*
```

**Oczekiwany rezultat:** 4 tabele: `sectro_sessions`, `sectro_measurements`, `sectro_results`, `sectro_logs`

---

## 🔧 KROK 2: INTEGRACJA BACKEND (10 min)

### Dodaj SECTRO blueprint do głównego api_server.py:

```python
# Na początku pliku backend/api_server.py dodaj import:
from sectro.sectro_api import sectro_bp

# Po linii app = Flask(__name__) dodaj:
app.register_blueprint(sectro_bp)
```

### Utwórz __init__.py w module sectro:
```bash
cd backend/sectro
python3 sectro_api.py  # To utworzy __init__.py automatycznie
```

### Dodaj zależności do requirements.txt:
```bash
echo "pyserial==3.5" >> backend/requirements.txt
```

---

## 🎨 KROK 3: FRONTEND ROUTING (5 min)

### Dodaj routing w frontend/src/router/index.js:
```javascript
// Import na początku pliku
import SectroView from '@/views/SectroView.vue'

// W tablicy routes dodaj:
{
  path: '/sectro',
  name: 'Sectro',
  component: SectroView,
  meta: { title: 'SECTRO Live Timing' }
}
```

### Dodaj link w menu głównym:
```vue
<!-- W głównym menu aplikacji dodaj: -->
<router-link to="/sectro" class="nav-link">
  ⏱️ Live Timing
</router-link>
```

---

## 🧪 KROK 4: TEST PODSTAWOWEJ FUNKCJONALNOŚCI (10 min)

### 1. Uruchom backend i frontend:
```bash
# Terminal 1 - Backend
cd backend
python3 api_server.py

# Terminal 2 - Frontend  
cd frontend
npm run dev
```

### 2. Przejdź do http://localhost:5177/sectro

### 3. Test API endpoints:
```bash
# Test tworzenia sesji
curl -X POST http://localhost:5000/api/sectro/sessions \
  -H "Content-Type: application/json" \
  -d '{"nazwa": "Test Session", "kategoria": "Junior A", "plec": "M"}'

# Test pobierania sesji
curl http://localhost:5000/api/sectro/sessions

# Test parsera ramek
cd backend/sectro
python3 sectro_parser.py
```

**Oczekiwany rezultat:** 
- ✅ Aplikacja uruchamia się bez błędów
- ✅ Strona `/sectro` ładuje się
- ✅ API endpoints odpowiadają JSON
- ✅ Parser testuje się poprawnie

---

## 📱 KROK 5: KOMPLETNE KOMPONENTY (30 min)

### Utwórz brakujące komponenty Vue:

**SectroSetup.vue:**
```vue
<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
    <h2 class="text-xl font-bold mb-4">Nowa Sesja SECTRO</h2>
    <form @submit.prevent="createSession">
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium mb-2">Nazwa sesji</label>
          <input v-model="sessionData.nazwa" 
                 class="w-full p-2 border rounded-md" 
                 required>
        </div>
        <div>
          <label class="block text-sm font-medium mb-2">Kategoria</label>
          <select v-model="sessionData.kategoria" class="w-full p-2 border rounded-md">
            <option>Junior A</option>
            <option>Junior B</option>
            <option>Senior</option>
          </select>
        </div>
      </div>
      <button type="submit" 
              class="mt-4 bg-blue-600 text-white px-6 py-2 rounded-md">
        Utwórz Sesję
      </button>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'SectroSetup',
  emits: ['session-created'],
  setup(props, { emit }) {
    const sessionData = ref({
      nazwa: '',
      kategoria: 'Junior A',
      plec: 'M'
    })

    const createSession = async () => {
      // Tutaj będzie API call
      emit('session-created', sessionData.value)
    }

    return { sessionData, createSession }
  }
}
</script>
```

**LiveTiming.vue:**
```vue
<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
    <h3 class="text-lg font-bold mb-4">Live Timing Dashboard</h3>
    
    <div class="grid grid-cols-3 gap-4 mb-6">
      <div class="text-center">
        <div class="text-2xl font-bold text-green-600">{{ activeSession ? 'AKTYWNY' : 'NIEAKTYWNY' }}</div>
        <div class="text-sm text-gray-500">Status</div>
      </div>
      <div class="text-center">
        <div class="text-2xl font-bold">{{ currentTime }}</div>
        <div class="text-sm text-gray-500">Czas bieżący</div>
      </div>
      <div class="text-center">
        <div class="text-2xl font-bold">{{ frameCount }}</div>
        <div class="text-sm text-gray-500">Ramki odebrane</div>
      </div>
    </div>

    <div class="mb-4">
      <label class="block text-sm font-medium mb-2">Numer startowy następnego zawodnika:</label>
      <input v-model="nextAthlete" 
             class="w-full p-3 text-xl border rounded-md" 
             placeholder="Wprowadź numer..."
             @keyup.enter="setNextAthlete">
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'

export default {
  name: 'LiveTiming',
  props: {
    session: Object
  },
  setup(props) {
    const currentTime = ref('')
    const frameCount = ref(0)
    const nextAthlete = ref('')
    const activeSession = ref(false)

    const updateTime = () => {
      currentTime.value = new Date().toLocaleTimeString()
    }

    const setNextAthlete = () => {
      console.log('Next athlete:', nextAthlete.value)
      nextAthlete.value = ''
    }

    let timeInterval
    onMounted(() => {
      timeInterval = setInterval(updateTime, 1000)
      updateTime()
    })

    onUnmounted(() => {
      if (timeInterval) clearInterval(timeInterval)
    })

    return {
      currentTime,
      frameCount,
      nextAthlete,
      activeSession,
      setNextAthlete
    }
  }
}
</script>
```

**LiveResults.vue:**
```vue
<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
    <h3 class="text-lg font-bold mb-4">Live Results</h3>
    
    <div class="overflow-x-auto">
      <table class="min-w-full">
        <thead class="bg-gray-50 dark:bg-gray-700">
          <tr>
            <th class="px-4 py-2 text-left">Pozycja</th>
            <th class="px-4 py-2 text-left">Nr</th>
            <th class="px-4 py-2 text-left">Imię Nazwisko</th>
            <th class="px-4 py-2 text-left">Czas</th>
            <th class="px-4 py-2 text-left">Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(result, index) in results" :key="result.nr_startowy">
            <td class="px-4 py-2">{{ index + 1 }}</td>
            <td class="px-4 py-2 font-bold">{{ result.nr_startowy }}</td>
            <td class="px-4 py-2">{{ result.imie }} {{ result.nazwisko }}</td>
            <td class="px-4 py-2 font-mono">{{ formatTime(result.total_time) }}</td>
            <td class="px-4 py-2">
              <span class="px-2 py-1 text-xs rounded-full bg-green-100 text-green-800">
                {{ result.status }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LiveResults',
  props: {
    sessionId: Number,
    results: Array
  },
  setup() {
    const formatTime = (seconds) => {
      if (!seconds) return '--:--'
      const minutes = Math.floor(seconds / 60)
      const remainingSeconds = (seconds % 60).toFixed(3)
      return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.padStart(6, '0')}`
    }

    return { formatTime }
  }
}
</script>
```

---

## 🎯 NASTĘPNE KROKI:

### **DZISIAJ (SETUP):**
1. ✅ Wykonaj migrację bazy danych
2. ✅ Dodaj routing frontend  
3. ✅ Test podstawowych endpoint
4. ✅ Utwórz podstawowe komponenty

### **JUTRO (HARDWARE):**
1. 🔧 Implementuj `sectro_hardware.py` 
2. 🔧 Test z prawdziwym urządzeniem SECTRO
3. 🔧 WebSocket dla live updates
4. 🔧 Error handling i reconnect

### **NASTĘPNY TYDZIEŃ (FEATURES):**
1. 📱 Mobile responsive design
2. 🔔 Sound notifications  
3. 📊 Live charts/graphs
4. 🎯 Split times support

---

## 🚨 ROZWIĄZYWANIE PROBLEMÓW:

### Problem: "ModuleNotFoundError: sectro"
```bash
# Rozwiązanie:
cd backend/sectro
touch __init__.py
python3 sectro_api.py
```

### Problem: "Table doesn't exist"
```bash
# Rozwiązanie:
psql $DATABASE_URL -c "\dt sectro*"  # Sprawdź tabele
psql $DATABASE_URL -f backend/migrations/03_add_sectro_tables.sql  # Ponów migrację
```

### Problem: "Component not found"
```bash
# Rozwiązanie:
# Sprawdź czy wszystkie pliki .vue zostały utworzone w frontend/src/components/sectro/
```

---

## 📞 GOTOWY NA NASTĘPNY KROK?

**Jeśli wszystko działa** - przejdziemy do implementacji komunikacji z hardware SECTRO!

**Jeśli są problemy** - opisz błędy i naprawimy je razem! 🚀 