<template>
  <div class="pwa-judge-view h-full bg-gradient-to-br from-green-50 to-emerald-100 dark:from-gray-900 dark:to-gray-800">
    <!-- Header -->
    <div class="bg-white dark:bg-gray-800 shadow-lg border-b border-gray-200 dark:border-gray-700">
      <div class="px-4 py-3">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-xl font-bold text-gray-900 dark:text-white">Panel Sędziego</h1>
            <p class="text-sm text-gray-600 dark:text-gray-400">Kontrola linii startu</p>
          </div>
          <div class="flex items-center space-x-2">
            <div class="flex items-center space-x-1 bg-green-100 dark:bg-green-900 px-2 py-1 rounded-full">
              <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span class="text-xs font-medium text-green-700 dark:text-green-300">Aktywny</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Stats -->
    <div class="p-4">
      <div class="grid grid-cols-3 gap-3 mb-6">
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-3">
          <div class="text-center">
            <div class="text-lg font-bold text-blue-600 dark:text-blue-400">{{ readyCount }}</div>
            <div class="text-xs text-gray-600 dark:text-gray-400">Gotowi</div>
          </div>
        </div>
        
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-3">
          <div class="text-center">
            <div class="text-lg font-bold text-yellow-600 dark:text-yellow-400">{{ timingCount }}</div>
            <div class="text-xs text-gray-600 dark:text-gray-400">W trakcie</div>
          </div>
        </div>

        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-3">
          <div class="text-center">
            <div class="text-lg font-bold text-green-600 dark:text-green-400">{{ finishedCount }}</div>
            <div class="text-xs text-gray-600 dark:text-gray-400">Ukończone</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Scanner Section -->
    <div class="px-4 pb-4 flex-1">
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 mb-6">
        <div class="text-center mb-4">
          <div class="mx-auto w-16 h-16 bg-green-100 dark:bg-green-900 rounded-full flex items-center justify-center mb-3">
            <ShieldCheckIcon class="h-8 w-8 text-green-600 dark:text-green-400" />
          </div>
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white">Weryfikacja Zawodnika</h2>
          <p class="text-sm text-gray-600 dark:text-gray-400">Skanuj QR przed startem</p>
        </div>
        
        <PWAQRScanner 
          :user-type="'judge'"
          :auto-start="true"
          @scan-success="handleVerification"
          @scan-error="handleScanError"
        />
      </div>

      <!-- Manual Controls -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 mb-6">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Kontrola manualna</h3>
        
        <div class="grid grid-cols-2 gap-3">
          <button 
            @click="startTimer"
            :disabled="!selectedAthlete"
            class="flex items-center justify-center space-x-2 bg-green-600 text-white p-3 rounded-lg disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            <PlayIcon class="h-5 w-5" />
            <span>START</span>
          </button>
          
          <button 
            @click="stopTimer"
            :disabled="!timingAthlete"
            class="flex items-center justify-center space-x-2 bg-red-600 text-white p-3 rounded-lg disabled:bg-gray-400 disabled:cursor-not-allowed"
          >
            <StopIcon class="h-5 w-5" />
            <span>STOP</span>
          </button>
        </div>

        <div class="mt-4 grid grid-cols-2 gap-3">
          <button 
            @click="markDNF"
            :disabled="!selectedAthlete"
            class="flex items-center justify-center space-x-2 bg-yellow-600 text-white p-2 rounded-lg disabled:bg-gray-400 disabled:cursor-not-allowed text-sm"
          >
            <ExclamationTriangleIcon class="h-4 w-4" />
            <span>DNF</span>
          </button>
          
          <button 
            @click="markDSQ"
            :disabled="!selectedAthlete"
            class="flex items-center justify-center space-x-2 bg-red-600 text-white p-2 rounded-lg disabled:bg-gray-400 disabled:cursor-not-allowed text-sm"
          >
            <XMarkIcon class="h-4 w-4" />
            <span>DSQ</span>
          </button>
        </div>
      </div>

      <!-- Selected Athlete -->
      <div v-if="selectedAthlete" class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 mb-6">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">Wybrany zawodnik</h3>
        <div class="flex items-center justify-between">
          <div>
            <p class="font-medium text-gray-900 dark:text-white">{{ selectedAthlete.imie }} {{ selectedAthlete.nazwisko }}</p>
            <p class="text-sm text-gray-500 dark:text-gray-400">#{{ selectedAthlete.nr_startowy }} · {{ selectedAthlete.kategoria }}</p>
          </div>
          <div class="text-right">
            <div :class="[
              'px-2 py-1 rounded-full text-xs font-medium',
              getStatusColor(selectedAthlete.status || 'WAITING')
            ]">
              {{ getStatusText(selectedAthlete.status || 'WAITING') }}
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4" v-if="recentActivity.length > 0">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">Ostatnie akcje</h3>
        <div class="space-y-2">
          <div 
            v-for="activity in recentActivity.slice(0, 5)" 
            :key="activity.id"
            class="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg"
          >
            <div class="flex items-center space-x-3">
              <div :class="[
                'w-8 h-8 rounded-full flex items-center justify-center',
                activity.type === 'start' ? 'bg-green-100 dark:bg-green-900' :
                activity.type === 'finish' ? 'bg-blue-100 dark:bg-blue-900' :
                'bg-yellow-100 dark:bg-yellow-900'
              ]">
                <PlayIcon v-if="activity.type === 'start'" class="h-4 w-4 text-green-600 dark:text-green-400" />
                <StopIcon v-else-if="activity.type === 'finish'" class="h-4 w-4 text-blue-600 dark:text-blue-400" />
                <ExclamationTriangleIcon v-else class="h-4 w-4 text-yellow-600 dark:text-yellow-400" />
              </div>
              <div>
                <p class="font-medium text-gray-900 dark:text-white">{{ activity.athlete_name }}</p>
                <p class="text-sm text-gray-500 dark:text-gray-400">{{ activity.action }}</p>
              </div>
            </div>
            <div class="text-right">
              <p class="text-xs text-gray-500 dark:text-gray-400">{{ formatTime(activity.timestamp) }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Messages -->
    <div v-if="message" class="fixed bottom-4 left-4 right-4 z-50">
      <div :class="[
        'p-4 rounded-lg shadow-lg',
        messageType === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
      ]">
        <div class="flex items-center">
          <CheckCircleIcon v-if="messageType === 'success'" class="h-5 w-5 mr-2" />
          <ExclamationTriangleIcon v-else class="h-5 w-5 mr-2" />
          <span>{{ message }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAthletesStore } from '../../stores/athletes'
import { useOfflineStore } from '../../stores/offline'
import { 
  ShieldCheckIcon, 
  PlayIcon, 
  StopIcon,
  ExclamationTriangleIcon,
  XMarkIcon,
  CheckCircleIcon
} from '@heroicons/vue/24/outline'
import PWAQRScanner from '../PWAQRScanner.vue'

const athletesStore = useAthletesStore()
const offlineStore = useOfflineStore()

const message = ref('')
const messageType = ref<'success' | 'error'>('success')
const selectedAthlete = ref<any>(null)
const timingAthlete = ref<any>(null)
const recentActivity = ref<any[]>([])

const readyCount = computed(() => 
  athletesStore.allAthletes.filter((a: any) => a.checked_in && !a.status).length
)

const timingCount = computed(() => 
  athletesStore.allAthletes.filter((a: any) => a.status === 'TIMING').length
)

const finishedCount = computed(() => 
  athletesStore.allAthletes.filter((a: any) => a.status === 'FINISHED').length
)

const handleVerification = async (qrData: string) => {
  try {
    const nrStartowy = parseInt(qrData)
    
    if (isNaN(nrStartowy)) {
      showMessage('Nieprawidłowy kod QR', 'error')
      return
    }

    const athlete = athletesStore.allAthletes.find((a: any) => a.nr_startowy === nrStartowy)
    
    if (!athlete) {
      showMessage(`Nie znaleziono zawodnika #${nrStartowy}`, 'error')
      return
    }

    if (!athlete.checked_in) {
      showMessage(`Zawodnik #${nrStartowy} nie jest zameldowany`, 'error')
      return
    }

    selectedAthlete.value = athlete
    showMessage(`✅ Zweryfikowano: ${athlete.imie} ${athlete.nazwisko}`, 'success')
    
    // Haptic feedback
    if ('vibrate' in navigator) {
      navigator.vibrate(100)
    }
    
  } catch (error) {
    console.error('Verification error:', error)
    showMessage('Błąd podczas weryfikacji', 'error')
  }
}

const startTimer = () => {
  if (!selectedAthlete.value) return
  
  timingAthlete.value = selectedAthlete.value
  selectedAthlete.value.status = 'TIMING'
  
  // Queue action for backend
  offlineStore.addToQueue({
    type: 'scan',
    data: {
      nr_startowy: selectedAthlete.value.nr_startowy,
      action: 'start',
      timestamp: new Date().toISOString()
    },
    endpoint: '/api/unified/start-timer',
    method: 'POST'
  })

  addActivity('start', selectedAthlete.value, 'Timer wystartowany')
  showMessage(`⏱️ Timer wystartowany dla ${selectedAthlete.value.imie} ${selectedAthlete.value.nazwisko}`, 'success')
}

const stopTimer = () => {
  if (!timingAthlete.value) return
  
  timingAthlete.value.status = 'FINISHED'
  
  // Queue action for backend
  offlineStore.addToQueue({
    type: 'scan',
    data: {
      nr_startowy: timingAthlete.value.nr_startowy,
      action: 'finish',
      timestamp: new Date().toISOString()
    },
    endpoint: '/api/unified/stop-timer',
    method: 'POST'
  })

  addActivity('finish', timingAthlete.value, 'Timer zatrzymany')
  showMessage(`🏁 Timer zatrzymany dla ${timingAthlete.value.imie} ${timingAthlete.value.nazwisko}`, 'success')
  
  timingAthlete.value = null
  selectedAthlete.value = null
}

const markDNF = () => {
  if (!selectedAthlete.value) return
  
  selectedAthlete.value.status = 'DNF'
  
  offlineStore.addToQueue({
    type: 'scan',
    data: {
      nr_startowy: selectedAthlete.value.nr_startowy,
      action: 'dnf',
      timestamp: new Date().toISOString()
    },
    endpoint: '/api/unified/mark-dnf',
    method: 'POST'
  })

  addActivity('dnf', selectedAthlete.value, 'Oznaczono DNF')
  showMessage(`⚠️ DNF: ${selectedAthlete.value.imie} ${selectedAthlete.value.nazwisko}`, 'success')
  
  selectedAthlete.value = null
}

const markDSQ = () => {
  if (!selectedAthlete.value) return
  
  selectedAthlete.value.status = 'DSQ'
  
  offlineStore.addToQueue({
    type: 'scan',
    data: {
      nr_startowy: selectedAthlete.value.nr_startowy,
      action: 'dsq',
      timestamp: new Date().toISOString()
    },
    endpoint: '/api/unified/mark-dsq',
    method: 'POST'
  })

  addActivity('dsq', selectedAthlete.value, 'Oznaczono DSQ')
  showMessage(`❌ DSQ: ${selectedAthlete.value.imie} ${selectedAthlete.value.nazwisko}`, 'success')
  
  selectedAthlete.value = null
}

const addActivity = (type: string, athlete: any, action: string) => {
  recentActivity.value.unshift({
    id: Date.now(),
    type,
    athlete_name: `${athlete.imie} ${athlete.nazwisko}`,
    action,
    timestamp: new Date().toISOString()
  })
}

const getStatusColor = (status: string) => {
  switch (status) {
    case 'TIMING': return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300'
    case 'FINISHED': return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300'
    case 'DNF': return 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-300'
    case 'DSQ': return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'
    default: return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300'
  }
}

const getStatusText = (status: string) => {
  switch (status) {
    case 'TIMING': return 'W trakcie'
    case 'FINISHED': return 'Ukończone'
    case 'DNF': return 'DNF'
    case 'DSQ': return 'DSQ'
    default: return 'Gotowy'
  }
}

const handleScanError = (error: string) => {
  showMessage(error, 'error')
}

const showMessage = (text: string, type: 'success' | 'error') => {
  message.value = text
  messageType.value = type
  setTimeout(() => {
    message.value = ''
  }, 3000)
}

const formatTime = (timestamp: string) => {
  return new Date(timestamp).toLocaleTimeString('pl-PL', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(async () => {
  await athletesStore.fetchAthletes()
})
</script> 