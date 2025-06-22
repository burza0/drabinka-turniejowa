<template>
  <div class="p-6 max-w-7xl mx-auto">
    <!-- Header -->
    <div class="flex items-center justify-between mb-8">
      <div class="flex items-center space-x-4">
        <div class="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
          <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </div>
        <div>
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Centrum Startu v2.0</h1>
          <p class="text-gray-600 dark:text-gray-400">Zintegrowane z SECTRO Live Timing</p>
        </div>
      </div>
      
      <div class="flex items-center space-x-3">
        <button 
          @click="refreshData"
          :disabled="loading"
          class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center space-x-2"
        >
          <svg v-if="loading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="m4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>{{ loading ? 'Ładowanie...' : 'Odśwież' }}</span>
        </button>
        
        <button 
          @click="showCleanupModal = true"
          class="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700"
        >
          🧹 Wyczyść
        </button>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Grupy Startowe</p>
            <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ stats.grupy_startowe || 0 }}</p>
          </div>
          <div class="w-12 h-12 bg-blue-100 dark:bg-blue-900/20 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Zameldowani</p>
            <p class="text-2xl font-bold text-green-600 dark:text-green-400">{{ stats.zawodnicy?.zameldowani || 0 }}</p>
          </div>
          <div class="w-12 h-12 bg-green-100 dark:bg-green-900/20 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Sesje SECTRO</p>
            <p class="text-2xl font-bold text-purple-600 dark:text-purple-400">{{ stats.sectro?.active_sessions || 0 }}</p>
          </div>
          <div class="w-12 h-12 bg-purple-100 dark:bg-purple-900/20 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">W Kolejce</p>
            <p class="text-2xl font-bold text-orange-600 dark:text-orange-400">{{ queue.length }}</p>
          </div>
          <div class="w-12 h-12 bg-orange-100 dark:bg-orange-900/20 rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-orange-600 dark:text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content Grid -->
    <div class="grid grid-cols-1 xl:grid-cols-3 gap-8">
      
      <!-- Left Column: Grupy Startowe -->
      <div class="xl:col-span-2 space-y-6">
        
        <!-- QR Scanner -->
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">🔍 Meldowanie Zawodników</h3>
          
          <div class="flex space-x-4">
            <input
              v-model="qrInput"
              @keyup.enter="handleCheckin"
              type="text"
              placeholder="QR kod lub numer startowy..."
              class="flex-1 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              @click="handleCheckin"
              :disabled="!qrInput || loading"
              class="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 font-medium"
            >
              ✅ Zamelduj
            </button>
            <button
              @click="handleCheckout"
              :disabled="!qrInput || loading"
              class="px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 font-medium"
            >
              ❌ Wymelduj
            </button>
          </div>
          
          <!-- Last Action Result -->
          <div v-if="lastResult" :class="getResultClass(lastResult.success)" class="mt-4 p-4 rounded-lg">
            <p class="font-medium">{{ lastResult.message }}</p>
            <p v-if="lastResult.zawodnik" class="text-sm mt-1">
              {{ lastResult.zawodnik.imie }} {{ lastResult.zawodnik.nazwisko }} 
              ({{ lastResult.zawodnik.kategoria }} {{ lastResult.zawodnik.plec }})
            </p>
          </div>
        </div>

        <!-- Grupy Startowe -->
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
          <div class="p-6 border-b border-gray-200 dark:border-gray-700">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">🏁 Grupy Startowe</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">Kliknij aby aktywować grupę i utworzyć sesję SECTRO</p>
          </div>
          
          <div class="p-6">
            <div v-if="loading" class="text-center py-8">
              <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
              <p class="text-gray-500 mt-2">Ładowanie grup...</p>
            </div>
            
            <div v-else-if="grupy.length === 0" class="text-center py-8">
              <div class="text-4xl mb-2">🏁</div>
              <p class="text-gray-500">Brak grup startowych</p>
              <p class="text-sm text-gray-400">Zamelduj zawodników aby utworzyć grupy</p>
            </div>
            
            <div v-else class="space-y-4">
              <div 
                v-for="grupa in grupy" 
                :key="grupa.key"
                class="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
              >
                <div class="flex items-center justify-between">
                  <div class="flex-1">
                    <h4 class="font-semibold text-gray-900 dark:text-white">{{ grupa.nazwa }}</h4>
                    <p class="text-sm text-gray-600 dark:text-gray-400">
                      {{ grupa.liczba_zawodnikow }} zawodników • {{ grupa.estimated_time }}s
                    </p>
                    <div v-if="grupa.sectro_session_id" class="text-xs text-purple-600 dark:text-purple-400 mt-1">
                      SECTRO Session #{{ grupa.sectro_session_id }}
                    </div>
                  </div>
                  
                  <div class="flex items-center space-x-3">
                    <span :class="getStatusClass(grupa.status)" class="px-2 py-1 rounded-full text-xs font-medium">
                      {{ getStatusText(grupa.status) }}
                    </span>
                    
                    <button
                      @click="toggleGrupa(grupa)"
                      :disabled="loading"
                      :class="getActionButtonClass(grupa.status)"
                      class="px-4 py-2 rounded-lg font-medium text-sm disabled:opacity-50"
                    >
                      {{ getActionButtonText(grupa.status) }}
                    </button>
                  </div>
                </div>
                
                <!-- Zawodnicy Details -->
                <div v-if="expandedGroups[grupa.key]" class="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
                    <div v-for="zawodnik in grupa.zawodnicy" :key="zawodnik.nr_startowy" 
                         class="flex items-center space-x-2 text-sm">
                      <span class="w-8 h-8 bg-gray-100 dark:bg-gray-700 rounded-full flex items-center justify-center text-xs font-bold">
                        {{ zawodnik.nr_startowy }}
                      </span>
                      <span>{{ zawodnik.imie }} {{ zawodnik.nazwisko }}</span>
                    </div>
                  </div>
                </div>
                
                <button
                  @click="expandedGroups[grupa.key] = !expandedGroups[grupa.key]"
                  class="mt-2 text-sm text-blue-600 dark:text-blue-400 hover:underline"
                >
                  {{ expandedGroups[grupa.key] ? 'Zwiń' : 'Rozwiń' }} listę zawodników
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column: Kolejka -->
      <div class="space-y-6">
        
        <!-- Kolejka Startowa -->
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700">
          <div class="p-6 border-b border-gray-200 dark:border-gray-700">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">⚡ Kolejka Startowa</h3>
            <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">Zawodnicy gotowi do startu</p>
          </div>
          
          <div class="p-6">
            <div v-if="queue.length === 0" class="text-center py-8">
              <div class="text-4xl mb-2">⏳</div>
              <p class="text-gray-500">Kolejka pusta</p>
              <p class="text-sm text-gray-400">Aktywuj grupę aby dodać zawodników</p>
            </div>
            
            <div v-else class="space-y-3">
              <div 
                v-for="(zawodnik, index) in queue" 
                :key="zawodnik.nr_startowy"
                class="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg"
              >
                <div class="flex items-center space-x-3">
                  <div :class="getQueuePositionClass(index)" class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold">
                    {{ index + 1 }}
                  </div>
                  <div>
                    <p class="font-medium text-gray-900 dark:text-white">
                      #{{ zawodnik.nr_startowy }} {{ zawodnik.imie }} {{ zawodnik.nazwisko }}
                    </p>
                    <p class="text-xs text-gray-600 dark:text-gray-400">
                      {{ zawodnik.kategoria }} {{ zawodnik.plec }} • {{ zawodnik.source_type }}
                    </p>
                    <div v-if="zawodnik.session_name" class="text-xs text-purple-600 dark:text-purple-400">
                      {{ zawodnik.session_name }}
                    </div>
                  </div>
                </div>
                
                <div class="flex items-center space-x-2">
                  <span :class="getSectroStatusClass(zawodnik.sectro_status)" class="px-2 py-1 rounded text-xs font-medium">
                    {{ zawodnik.sectro_status }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
      </div>
    </div>

    <!-- Cleanup Modal -->
    <div v-if="showCleanupModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 rounded-xl p-6 max-w-md w-full mx-4">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">🧹 Czyszczenie Systemu</h3>
        
        <div class="space-y-4">
          <button
            @click="cleanup('old_sessions')"
            class="w-full p-3 text-left bg-gray-50 dark:bg-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600"
          >
            <p class="font-medium">Wyczyść stare sesje SECTRO</p>
            <p class="text-sm text-gray-600 dark:text-gray-400">Zakończ nieaktywne sesje</p>
          </button>
          
          <button
            @click="cleanup('empty_sessions')"
            class="w-full p-3 text-left bg-gray-50 dark:bg-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600"
          >
            <p class="font-medium">Usuń puste sesje</p>
            <p class="text-sm text-gray-600 dark:text-gray-400">Usuń sesje bez wyników</p>
          </button>
        </div>
        
        <div class="flex space-x-3 mt-6">
          <button
            @click="showCleanupModal = false"
            class="flex-1 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700"
          >
            Anuluj
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'

// Types
interface Zawodnik {
  nr_startowy: number
  imie: string
  nazwisko: string
  kategoria: string
  plec: string
  klub: string
  checked_in: boolean
  check_in_time?: string
}

interface Grupa {
  numer_grupy: number
  key: string
  nazwa: string
  kategoria: string
  plec: string
  zawodnicy: Zawodnik[]
  liczba_zawodnikow: number
  status: string
  sectro_session_id?: number
  estimated_time: number
}

interface QueueItem {
  nr_startowy: number
  imie: string
  nazwisko: string
  kategoria: string
  plec: string
  klub: string
  sectro_status: string
  session_id?: number
  session_name?: string
  source_type: string
  check_in_time: string
}

// State
const loading = ref(false)
const grupy = ref<Grupa[]>([])
const queue = ref<QueueItem[]>([])
const stats = ref<any>({})
const qrInput = ref('')
const lastResult = ref<any>(null)
const expandedGroups = reactive<Record<string, boolean>>({})
const showCleanupModal = ref(false)

// Methods
const refreshData = async () => {
  loading.value = true
  try {
    await Promise.all([
      loadGrupy(),
      loadQueue(),
      loadStats()
    ])
  } finally {
    loading.value = false
  }
}

const loadGrupy = async () => {
  try {
    const response = await fetch('/api/v2/grupy-startowe')
    const data = await response.json()
    if (data.success) {
      grupy.value = data.data.grupy
    }
  } catch (error) {
    console.error('Błąd ładowania grup:', error)
  }
}

const loadQueue = async () => {
  try {
    const response = await fetch('/api/v2/queue')
    const data = await response.json()
    if (data.success) {
      queue.value = data.data
    }
  } catch (error) {
    console.error('Błąd ładowania kolejki:', error)
  }
}

const loadStats = async () => {
  try {
    const response = await fetch('/api/v2/stats')
    const data = await response.json()
    if (data.success) {
      stats.value = data.data
    }
  } catch (error) {
    console.error('Błąd ładowania statystyk:', error)
  }
}

const handleCheckin = async () => {
  if (!qrInput.value) return
  
  try {
    const response = await fetch('/api/v2/checkin', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        nr_startowy: parseInt(qrInput.value) || undefined,
        qr_code: isNaN(parseInt(qrInput.value)) ? qrInput.value : undefined,
        action: 'checkin'
      })
    })
    
    const result = await response.json()
    lastResult.value = result
    
    if (result.success) {
      qrInput.value = ''
      await refreshData()
    }
  } catch (error) {
    console.error('Błąd meldowania:', error)
    lastResult.value = { success: false, message: 'Błąd połączenia z serwerem' }
  }
}

const handleCheckout = async () => {
  if (!qrInput.value) return
  
  try {
    const response = await fetch('/api/v2/checkin', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        nr_startowy: parseInt(qrInput.value) || undefined,
        qr_code: isNaN(parseInt(qrInput.value)) ? qrInput.value : undefined,
        action: 'checkout'
      })
    })
    
    const result = await response.json()
    lastResult.value = result
    
    if (result.success) {
      qrInput.value = ''
      await refreshData()
    }
  } catch (error) {
    console.error('Błąd wymeldowania:', error)
    lastResult.value = { success: false, message: 'Błąd połączenia z serwerem' }
  }
}

const toggleGrupa = async (grupa: Grupa) => {
  if (loading.value) return
  
  loading.value = true
  try {
    if (grupa.status === 'WAITING') {
      // Aktywuj grupę
      const response = await fetch('/api/v2/grupa/activate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          kategoria: grupa.kategoria,
          plec: grupa.plec,
          nazwa: grupa.nazwa
        })
      })
      
      const result = await response.json()
      lastResult.value = result
      
      if (result.success) {
        await refreshData()
      }
    } else if (grupa.status === 'ACTIVE') {
      // Deaktywuj grupę
      const response = await fetch('/api/v2/grupa/deactivate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          kategoria: grupa.kategoria,
          plec: grupa.plec
        })
      })
      
      const result = await response.json()
      lastResult.value = result
      
      if (result.success) {
        await refreshData()
      }
    }
  } catch (error) {
    console.error('Błąd toggle grupy:', error)
    lastResult.value = { success: false, message: 'Błąd połączenia z serwerem' }
  } finally {
    loading.value = false
  }
}

const cleanup = async (type: string) => {
  try {
    const response = await fetch('/api/v2/cleanup', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type })
    })
    
    const result = await response.json()
    lastResult.value = result
    
    if (result.success) {
      await refreshData()
    }
    
    showCleanupModal.value = false
  } catch (error) {
    console.error('Błąd czyszczenia:', error)
    lastResult.value = { success: false, message: 'Błąd połączenia z serwerem' }
  }
}

// UI Helper Functions
const getStatusClass = (status: string) => {
  switch (status) {
    case 'WAITING': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400'
    case 'ACTIVE': return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400'
    case 'TIMING': return 'bg-purple-100 text-purple-800 dark:bg-purple-900/20 dark:text-purple-400'
    case 'COMPLETED': return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400'
    default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400'
  }
}

const getStatusText = (status: string) => {
  switch (status) {
    case 'WAITING': return 'Oczekuje'
    case 'ACTIVE': return 'Aktywna'
    case 'TIMING': return 'Pomiary'
    case 'COMPLETED': return 'Zakończona'
    default: return status
  }
}

const getActionButtonClass = (status: string) => {
  switch (status) {
    case 'WAITING': return 'bg-green-600 text-white hover:bg-green-700'
    case 'ACTIVE': return 'bg-red-600 text-white hover:bg-red-700'
    case 'TIMING': return 'bg-gray-400 text-white cursor-not-allowed'
    default: return 'bg-gray-400 text-white cursor-not-allowed'
  }
}

const getActionButtonText = (status: string) => {
  switch (status) {
    case 'WAITING': return '▶️ Aktywuj'
    case 'ACTIVE': return '⏹️ Deaktywuj'
    case 'TIMING': return '⏱️ W trakcie'
    default: return 'Niedostępne'
  }
}

const getResultClass = (success: boolean) => {
  return success 
    ? 'bg-green-100 text-green-800 border border-green-200 dark:bg-green-900/20 dark:text-green-400 dark:border-green-800'
    : 'bg-red-100 text-red-800 border border-red-200 dark:bg-red-900/20 dark:text-red-400 dark:border-red-800'
}

const getQueuePositionClass = (index: number) => {
  if (index === 0) return 'bg-yellow-500 text-white'
  if (index === 1) return 'bg-gray-400 text-white'
  if (index === 2) return 'bg-orange-600 text-white'
  return 'bg-gray-300 text-gray-700'
}

const getSectroStatusClass = (status: string) => {
  switch (status) {
    case 'in_progress': return 'bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-400'
    case 'completed': return 'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400'
    default: return 'bg-gray-100 text-gray-800 dark:bg-gray-900/20 dark:text-gray-400'
  }
}

// Lifecycle
onMounted(() => {
  refreshData()
  
  // Auto-refresh co 5 sekund
  setInterval(refreshData, 5000)
})
</script>