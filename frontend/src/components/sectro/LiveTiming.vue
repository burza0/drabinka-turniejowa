<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
    <h3 class="text-lg font-bold mb-4 text-gray-900 dark:text-white">Live Timing Dashboard</h3>
    
    <!-- Status Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
      <div class="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
        <div :class="[
          'text-2xl font-bold',
          sessionActive ? 'text-green-600' : 'text-gray-500'
        ]">
          {{ sessionActive ? 'AKTYWNY' : 'NIEAKTYWNY' }}
        </div>
        <div class="text-sm text-gray-500 dark:text-gray-400">Status sesji</div>
      </div>
      
      <div class="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
        <div class="text-2xl font-bold text-gray-900 dark:text-white">{{ currentTime }}</div>
        <div class="text-sm text-gray-500 dark:text-gray-400">Czas bieżący</div>
      </div>
      
      <div class="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
        <div class="text-2xl font-bold text-blue-600">{{ frameCount }}</div>
        <div class="text-sm text-gray-500 dark:text-gray-400">Ramki odebrane</div>
      </div>
    </div>

    <!-- Aktualny biegacz z czasem -->
    <div v-if="activeAthlete && activeAthlete.start_time" class="mb-6 p-4 bg-blue-100 dark:bg-blue-900 rounded-lg">
      <h4 class="font-medium mb-2 text-gray-900 dark:text-white">Aktualny biegacz</h4>
      <div class="flex items-center justify-between">
        <div>
          <div class="text-lg font-bold">
            #{{ activeAthlete.nr_startowy }} - {{ activeAthlete.imie }} {{ activeAthlete.nazwisko }}
          </div>
          <div class="text-sm text-gray-600 dark:text-gray-300">
            {{ activeAthlete.kategoria }} {{ activeAthlete.plec }} | {{ activeAthlete.klub }}
          </div>
        </div>
        <div class="text-center">
          <div class="text-3xl font-bold font-mono text-blue-700 dark:text-blue-300">
            {{ formatRaceTime(elapsedTime) }}
          </div>
          <div class="text-sm text-gray-500 dark:text-gray-400">Czas biegu</div>
        </div>
        <button 
          @click="sendFinishFrame(activeAthlete)"
          class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-md"
        >
          🏁 FINISH
        </button>
      </div>
    </div>

    <!-- Hardware Status -->
    <div class="mb-6 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
      <h4 class="font-medium mb-2 text-gray-900 dark:text-white">Status urządzenia SECTRO</h4>
      <div class="flex items-center space-x-4">
        <div class="flex items-center space-x-2">
          <div :class="[
            'w-3 h-3 rounded-full',
            hardwareConnected ? 'bg-green-500' : 'bg-red-500'
          ]"></div>
          <span class="text-sm text-gray-600 dark:text-gray-300">
            {{ hardwareConnected ? 'Połączono' : 'Rozłączono' }}
          </span>
        </div>
        
        <div class="text-sm text-gray-500 dark:text-gray-400">
          Port: {{ hardwarePort }}
        </div>
        
        <div class="text-sm text-gray-500 dark:text-gray-400">
          Ostatnia ramka: {{ lastFrameTime }}
        </div>
      </div>
    </div>

    <!-- Next Athlete Input -->
    <div class="mb-6">
      <label class="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">
        Numer startowy następnego zawodnika:
      </label>
      <div class="flex space-x-3">
        <input 
          v-model="nextAthlete" 
          type="number"
          class="flex-1 p-3 text-xl border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white" 
          placeholder="Wprowadź numer..."
          @keyup.enter="setNextAthlete"
        >
        
        <button 
          @click="setNextAthlete"
          :disabled="!nextAthlete"
          class="bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white px-6 py-2 rounded-md flex items-center space-x-2"
        >
          <span>✅</span>
          <span>Ustaw</span>
        </button>
      </div>
      
      <div v-if="currentAthlete" class="mt-2 p-2 bg-blue-50 dark:bg-blue-900 rounded text-sm">
        <strong>Aktualny zawodnik:</strong> 
        Nr {{ currentAthlete.nr_startowy }} - {{ currentAthlete.imie }} {{ currentAthlete.nazwisko }}
        ({{ currentAthlete.kategoria }} {{ currentAthlete.plec }})
      </div>
    </div>

    <!-- Manual Frame Input (for testing) -->
    <div class="mb-6 p-4 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg">
      <h4 class="font-medium mb-2 text-gray-900 dark:text-white">Test manualny ramki SECTRO</h4>
      <div class="flex space-x-3">
        <input 
          v-model="testFrame" 
          class="flex-1 p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white" 
          placeholder="np. CZL1123456789"
          @keyup.enter="sendTestFrame"
        >
        
        <button 
          @click="sendTestFrame"
          :disabled="!testFrame || !currentAthlete"
          class="bg-purple-600 hover:bg-purple-700 disabled:bg-gray-400 text-white px-4 py-2 rounded-md"
        >
          Wyślij
        </button>
      </div>
      
      <div class="mt-2 text-xs text-gray-500 dark:text-gray-400">
        Format: CZL[wejście][timestamp] - np. CZL1123456789 (START), CZL4123459123 (FINISH)
      </div>
    </div>

    <!-- Lista zawodników w kolejce startowej -->
    <div v-if="showStartQueue" class="mb-6 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
      <h4 class="font-medium mb-2 text-gray-900 dark:text-white">Kolejka startowa zawodników</h4>
      
      <div v-if="isLoadingQueue" class="text-center py-4">
        <span class="text-blue-600 dark:text-blue-400">Ładowanie listy zawodników...</span>
      </div>
      
      <div v-else-if="startQueue.length === 0" class="text-center py-4">
        <span class="text-gray-500 dark:text-gray-400">Brak zawodników w kolejce startowej</span>
      </div>
      
      <div v-else class="max-h-96 overflow-y-auto">
        <table class="w-full text-sm">
          <thead class="bg-gray-100 dark:bg-gray-600">
            <tr>
              <th class="px-4 py-2 text-left">Nr</th>
              <th class="px-4 py-2 text-left">Zawodnik</th>
              <th class="px-4 py-2 text-left">Kategoria</th>
              <th class="px-4 py-2 text-left">Klub</th>
              <th class="px-4 py-2 text-center">Akcje</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(athlete, index) in startQueue" :key="athlete.nr_startowy" 
                :class="[
                  {'bg-blue-50 dark:bg-blue-900': currentAthlete && currentAthlete.nr_startowy === athlete.nr_startowy},
                  {'bg-green-50 dark:bg-green-900': isAthleteActive(athlete.nr_startowy)}
                ]">
              <td class="px-4 py-2 font-bold">{{ athlete.nr_startowy }}</td>
              <td class="px-4 py-2">{{ athlete.imie }} {{ athlete.nazwisko }}</td>
              <td class="px-4 py-2">{{ athlete.kategoria }} {{ athlete.plec }}</td>
              <td class="px-4 py-2">{{ athlete.klub }}</td>
              <td class="px-4 py-2 text-center">
                <button 
                  @click="selectAthlete(athlete)"
                  class="bg-green-600 hover:bg-green-700 text-white px-2 py-1 rounded-md text-xs"
                >
                  Wybierz
                </button>
                <button 
                  @click="sendStartFrame(athlete)"
                  :disabled="isAthleteActive(athlete.nr_startowy)"
                  class="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-2 py-1 rounded-md text-xs ml-1"
                >
                  START
                </button>
                <button 
                  @click="sendFinishFrame(athlete)"
                  :disabled="!isAthleteActive(athlete.nr_startowy)"
                  class="bg-purple-600 hover:bg-purple-700 disabled:bg-gray-400 text-white px-2 py-1 rounded-md text-xs ml-1"
                >
                  FINISH
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <div class="mt-4 flex justify-end">
        <button 
          @click="refreshStartQueue"
          class="bg-gray-600 hover:bg-gray-700 text-white px-3 py-1 rounded-md text-sm"
        >
          🔄 Odśwież listę
        </button>
      </div>
    </div>

    <!-- Session Controls -->
    <div class="flex justify-between items-center pt-4 border-t border-gray-200 dark:border-gray-600">
      <div class="space-x-3">
        <button 
          @click="startSession"
          :disabled="sessionActive"
          class="bg-green-600 hover:bg-green-700 disabled:bg-gray-400 text-white px-4 py-2 rounded-md"
        >
          ▶️ Start
        </button>
        
        <button 
          @click="pauseSession"
          :disabled="!sessionActive"
          class="bg-yellow-600 hover:bg-yellow-700 disabled:bg-gray-400 text-white px-4 py-2 rounded-md"
        >
          ⏸️ Pauza
        </button>
        
        <button 
          @click="stopSession"
          :disabled="!sessionActive"
          class="bg-red-600 hover:bg-red-700 disabled:bg-gray-400 text-white px-4 py-2 rounded-md"
        >
          ⏹️ Stop
        </button>
      </div>
      
      <div class="text-sm text-gray-500 dark:text-gray-400">
        Sesja: {{ session ? session.nazwa : 'Brak' }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import axios from 'axios'

// Props
const props = defineProps({
  session: {
    type: Object,
    default: null
  }
})

// Emits
const emit = defineEmits(['session-updated', 'athlete-started', 'athlete-finished'])

// Reactive data
const currentTime = ref('')
const frameCount = ref(0)
const nextAthlete = ref('')
const testFrame = ref('')
const currentAthlete = ref(null)
const hardwareConnected = ref(false)
const hardwarePort = ref('/dev/ttyUSB0')
const lastFrameTime = ref('Brak')
const startQueue = ref([])
const isLoadingQueue = ref(false)
const showStartQueue = ref(false)
const activeAthletes = ref([])  // Lista zawodników z aktywnym pomiarem czasu
const activeAthlete = ref(null) // Obecnie biegnący zawodnik (ten, którego czas pokazujemy)
const elapsedTime = ref(0)      // Czas, który upłynął od startu

// Computed
const sessionActive = computed(() => {
  return props.session && props.session.status === 'active'
})

// Methods
const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString('pl-PL')
  
  // Aktualizuj czas biegu dla aktywnego zawodnika
  if (activeAthlete.value && activeAthlete.value.start_time) {
    const currentTimeSeconds = now.getHours() * 3600 + now.getMinutes() * 60 + now.getSeconds() + (now.getMilliseconds() / 1000)
    elapsedTime.value = currentTimeSeconds - activeAthlete.value.start_time
  }
}

// Formatuj czas wyścigu w formacie MM:SS.sss
const formatRaceTime = (seconds) => {
  if (!seconds || seconds <= 0) return '00:00.000'
  
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  
  return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toFixed(3).padStart(6, '0')}`
}

// Sprawdź czy zawodnik jest aktywny (wystartował, ale nie skończył)
const isAthleteActive = (nrStartowy) => {
  return activeAthletes.value.some(a => a.nr_startowy === nrStartowy)
}

const setNextAthlete = async () => {
  if (!nextAthlete.value) return
  
  try {
    // Pobierz dane zawodnika
    const response = await axios.get(`/api/zawodnicy/${nextAthlete.value}`)
    
    if (response.data.success) {
      currentAthlete.value = response.data.zawodnik
      console.log('✅ Ustawiono zawodnika:', currentAthlete.value)
      nextAthlete.value = ''
    } else {
      alert('Nie znaleziono zawodnika z numerem: ' + nextAthlete.value)
    }
  } catch (error) {
    console.error('❌ Błąd pobierania zawodnika:', error)
    alert('Błąd podczas pobierania danych zawodnika')
  }
}

const sendTestFrame = async () => {
  if (!testFrame.value || !currentAthlete.value || !props.session) return
  
  try {
    const response = await axios.post('/api/sectro/measurements', {
      session_id: props.session.id,
      nr_startowy: currentAthlete.value.nr_startowy,
      raw_frame: testFrame.value
    })
    
    if (response.data.success) {
      frameCount.value++
      lastFrameTime.value = new Date().toLocaleTimeString('pl-PL')
      
      const frameInfo = response.data.frame
      console.log('✅ Ramka przetworzona:', frameInfo)
      
      // Emit events based on frame type
      if (frameInfo.type === 'START') {
        emit('athlete-started', {
          athlete: currentAthlete.value,
          frame: frameInfo
        })
      } else if (frameInfo.type === 'FINISH') {
        emit('athlete-finished', {
          athlete: currentAthlete.value,
          frame: frameInfo,
          result: response.data.result
        })
      }
      
      testFrame.value = ''
    } else {
      alert('Błąd przetwarzania ramki: ' + response.data.error)
    }
  } catch (error) {
    console.error('❌ Błąd wysyłania ramki:', error)
    alert('Błąd podczas wysyłania ramki')
  }
}

const startSession = async () => {
  if (!props.session) return
  
  try {
    console.log('Uruchamianie sesji:', props.session.id)
    const response = await axios.post(`/api/sectro/sessions/${props.session.id}/start`)
    
    if (response.data.success) {
      emit('session-updated')
      console.log('✅ Sesja uruchomiona')
      showStartQueue.value = true // Pokazujemy kolejkę
      console.log('Pokazuję kolejkę zawodników - showStartQueue:', showStartQueue.value)
      await refreshStartQueue()
    }
  } catch (error) {
    console.error('❌ Błąd uruchamiania sesji:', error)
  }
}

const pauseSession = async () => {
  if (!props.session) return
  
  try {
    // Update status to paused (implement this endpoint in API)
    console.log('⏸️ Sesja wstrzymana')
  } catch (error) {
    console.error('❌ Błąd wstrzymywania sesji:', error)
  }
}

const stopSession = async () => {
  if (!props.session) return
  
  try {
    const response = await axios.post(`/api/sectro/sessions/${props.session.id}/stop`)
    
    if (response.data.success) {
      emit('session-updated')
      console.log('⏹️ Sesja zatrzymana')
      showStartQueue.value = false
      // Zatrzymaj wszystkie aktywne pomiary
      activeAthletes.value = []
      activeAthlete.value = null
    }
  } catch (error) {
    console.error('❌ Błąd zatrzymywania sesji:', error)
  }
}

// Nowe funkcje do obsługi kolejki startowej
const refreshStartQueue = async () => {
  if (!props.session) return
  
  isLoadingQueue.value = true
  try {
    const response = await axios.get(`/api/start-queue?_t=${Date.now()}`)
    
    if (response.data.success) {
      startQueue.value = response.data.queue || []
      console.log('✅ Pobrano kolejkę startową:', startQueue.value.length, 'zawodników')
    } else {
      console.error('❌ Błąd pobierania kolejki:', response.data.error)
    }
  } catch (error) {
    console.error('❌ Błąd pobierania kolejki startowej:', error)
  } finally {
    isLoadingQueue.value = false
  }
}

const selectAthlete = (athlete) => {
  currentAthlete.value = athlete
  console.log('✅ Wybrano zawodnika z kolejki:', currentAthlete.value)
}

const generateSectroFrame = (inputNumber) => {
  const now = new Date()
  const hours = now.getHours().toString().padStart(2, '0')
  const minutes = now.getMinutes().toString().padStart(2, '0')
  const seconds = now.getSeconds().toString().padStart(2, '0')
  const milliseconds = Math.floor(now.getMilliseconds()).toString().padStart(3, '0')
  return `CZL${inputNumber}${hours}${minutes}${seconds}${milliseconds}`
}

const sendStartFrame = async (athlete) => {
  if (!props.session) return
  
  try {
    const startFrame = generateSectroFrame('1')
    const response = await axios.post('/api/sectro/measurements', {
      session_id: props.session.id,
      nr_startowy: athlete.nr_startowy,
      raw_frame: startFrame
    })
    
    if (response.data.success) {
      frameCount.value++
      lastFrameTime.value = new Date().toLocaleTimeString('pl-PL')
      console.log('✅ Wysłano START dla zawodnika:', athlete.nr_startowy)
      
      // Zapisz czas startu i dodaj zawodnika do aktywnych
      const now = new Date()
      const startTimeSeconds = now.getHours() * 3600 + now.getMinutes() * 60 + now.getSeconds() + (now.getMilliseconds() / 1000)
      
      // Dodaj zawodnika do aktywnych
      const activeAthleteInfo = {
        ...athlete,
        start_time: startTimeSeconds
      }
      
      // Dodaj do listy aktywnych i ustaw jako aktualnie biegnącego
      activeAthletes.value.push(activeAthleteInfo)
      activeAthlete.value = activeAthleteInfo
      elapsedTime.value = 0 // Zeruj licznik
      
      // Emituj event o starcie zawodnika
      emit('athlete-started', {
        athlete: athlete,
        frame: response.data.frame
      })
      
      currentAthlete.value = athlete
    } else {
      alert('Błąd przetwarzania ramki START: ' + response.data.error)
    }
  } catch (error) {
    console.error('❌ Błąd wysyłania ramki START:', error)
    alert('Błąd podczas wysyłania ramki START')
  }
}

const sendFinishFrame = async (athlete) => {
  if (!props.session) return
  
  try {
    const finishFrame = generateSectroFrame('4')
    const response = await axios.post('/api/sectro/measurements', {
      session_id: props.session.id,
      nr_startowy: athlete.nr_startowy,
      raw_frame: finishFrame
    })
    
    if (response.data.success) {
      frameCount.value++
      lastFrameTime.value = new Date().toLocaleTimeString('pl-PL')
      console.log('✅ Wysłano FINISH dla zawodnika:', athlete.nr_startowy)
      
      // Usuń zawodnika z aktywnych
      activeAthletes.value = activeAthletes.value.filter(a => a.nr_startowy !== athlete.nr_startowy)
      
      // Jeśli to był aktywny zawodnik, znajdź następnego lub wyzeruj
      if (activeAthlete.value && activeAthlete.value.nr_startowy === athlete.nr_startowy) {
        if (activeAthletes.value.length > 0) {
          activeAthlete.value = activeAthletes.value[0]
        } else {
          activeAthlete.value = null
        }
      }
      
      // Emituj event o ukończeniu biegu
      emit('athlete-finished', {
        athlete: athlete,
        frame: response.data.frame,
        result: response.data.result
      })
      
      // Nie odświeżaj kolejki - może ukryć panel!
      // refreshStartQueue wywoływane przez auto-refresh wystarczy
    } else {
      alert('Błąd przetwarzania ramki FINISH: ' + response.data.error)
    }
  } catch (error) {
    console.error('❌ Błąd wysyłania ramki FINISH:', error)
    alert('Błąd podczas wysyłania ramki FINISH')
  }
}

// Funkcja, która będzie wywoływana zawsze gdy zmieni się status sesji
const updateDisplayBasedOnSessionStatus = () => {
  console.log('Aktualizacja stanu na podstawie statusu sesji:', sessionActive.value)
  if (sessionActive.value) {
    showStartQueue.value = true
    refreshStartQueue()
  } else {
    console.log('🔒 Sesja nieaktywna - ukrywam kolejkę i zatrzymuję pomiary')
    showStartQueue.value = false
    // Zatrzymaj wszystkie aktywne pomiary
    activeAthletes.value = []
    activeAthlete.value = null
  }
}

// Lifecycle
let timeInterval
let queueRefreshInterval
onMounted(() => {
  timeInterval = setInterval(updateTime, 100) // Aktualizuj co 100ms dla płynności licznika czasu
  updateTime()
  
  // Auto-refresh kolejki startowej co 10 sekund (tylko gdy jest widoczna)
  queueRefreshInterval = setInterval(() => {
    if (showStartQueue.value && sessionActive.value) {
      refreshStartQueue()
    }
  }, 10000)
  
  // Check hardware status
  // TODO: Implement hardware status checking
  
  // Sprawdź czy sesja jest aktywna i załaduj kolejkę startową
  console.log('Komponent zamontowany, status sesji:', sessionActive.value)
  updateDisplayBasedOnSessionStatus()
})

// Obserwuj zmiany w statusie sesji
watch(() => props.session?.status, (newStatus, oldStatus) => {
  console.log('Status sesji zmienił się:', oldStatus, '->', newStatus)
  updateDisplayBasedOnSessionStatus()
})

onUnmounted(() => {
  if (timeInterval) clearInterval(timeInterval)
  if (queueRefreshInterval) clearInterval(queueRefreshInterval)
})
</script> 