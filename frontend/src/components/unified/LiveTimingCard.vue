<template>
  <div class="live-timing-card bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
    
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 bg-purple-100 dark:bg-purple-900/20 rounded-lg flex items-center justify-center">
          <svg class="w-5 h-5 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <div>
          <h2 class="text-xl font-bold text-gray-900 dark:text-white">SECTRO Live Timing</h2>
          <p class="text-sm text-gray-600 dark:text-gray-400">
            {{ session.kategoria }} {{ session.plec }} • {{ session.nazwa }}
          </p>
        </div>
      </div>
      
      <div class="flex items-center space-x-2">
        <div :class="getSessionStatusClass()" 
             class="px-3 py-1 rounded-full text-sm font-medium flex items-center space-x-2">
          <div class="w-2 h-2 rounded-full animate-pulse" 
               :class="session.status === 'active' ? 'bg-green-400' : 'bg-yellow-400'"></div>
          <span>{{ getSessionStatusText() }}</span>
        </div>
        
        <button 
          @click="refreshData"
          :disabled="loading"
          class="px-4 py-2 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg font-medium hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors duration-200"
        >
          <svg v-if="loading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="m4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Current Runner Dashboard -->
    <div v-if="currentRunner" class="mb-8">
      <div class="bg-gradient-to-br from-purple-500 to-blue-600 text-white rounded-xl p-6">
        <div class="flex items-center justify-between mb-4">
          <div>
            <div class="text-sm opacity-90">🏃 Aktualnie na trasie:</div>
            <div class="text-2xl font-bold">{{ currentRunner.imie }} {{ currentRunner.nazwisko }}</div>
            <div class="text-sm opacity-90">{{ currentRunner.klub }}</div>
          </div>
          
          <div class="text-right">
            <div class="text-3xl font-mono font-bold">
              {{ formatTime(currentRunner.current_time) }}
            </div>
            <div class="text-sm opacity-90">Czas biegu</div>
          </div>
        </div>
        
        <!-- Progress indicators -->
        <div class="flex items-center justify-between text-sm">
          <div class="flex items-center space-x-4">
            <div :class="currentRunner.start_time ? 'text-green-300' : 'text-white/50'"
                 class="flex items-center space-x-1">
              <div class="w-3 h-3 rounded-full" 
                   :class="currentRunner.start_time ? 'bg-green-300' : 'bg-white/50'"></div>
              <span>START</span>
            </div>
            
            <div class="flex-1 h-0.5 bg-white/30 mx-2 relative">
              <div v-if="currentRunner.start_time && !currentRunner.finish_time"
                   class="absolute left-0 top-0 h-full bg-green-300 animate-pulse"
                   style="width: 50%"></div>
            </div>
            
            <div :class="currentRunner.finish_time ? 'text-green-300' : 'text-white/50'"
                 class="flex items-center space-x-1">
              <div class="w-3 h-3 rounded-full" 
                   :class="currentRunner.finish_time ? 'bg-green-300' : 'bg-white/50'"></div>
              <span>FINISH</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Queue -->
    <div class="mb-8">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Kolejka startowa</h3>
      
      <div v-if="queue.length > 0" class="space-y-3">
        <div v-for="(athlete, index) in queue.slice(0, 10)" :key="athlete.nr_startowy"
             :class="getQueueItemClass(athlete, index)"
             class="p-4 rounded-lg border transition-all duration-200">
          
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <!-- Position -->
              <div :class="getPositionClass(index)"
                   class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold">
                {{ index + 1 }}
              </div>
              
              <!-- Athlete info -->
              <div>
                <div class="font-medium text-gray-900 dark:text-white">
                  {{ athlete.imie }} {{ athlete.nazwisko }} (#{{ athlete.nr_startowy }})
                </div>
                <div class="text-sm text-gray-600 dark:text-gray-400">
                  {{ athlete.klub }}
                </div>
              </div>
            </div>
            
            <!-- Status and timing -->
            <div class="text-right">
              <div :class="getStatusClass(athlete.unified_status)"
                   class="px-2 py-1 rounded-full text-xs font-medium mb-1">
                {{ getStatusText(athlete.unified_status) }}
              </div>
              
              <div v-if="athlete.final_time" class="text-sm font-mono font-semibold text-gray-900 dark:text-white">
                {{ formatTime(athlete.final_time) }}
              </div>
              <div v-else-if="athlete.current_time" class="text-sm font-mono text-blue-600 dark:text-blue-400">
                {{ formatTime(athlete.current_time) }}
              </div>
              <div v-else class="text-xs text-gray-500 dark:text-gray-400">
                Oczekuje
              </div>
            </div>
          </div>
        </div>
        
        <div v-if="queue.length > 10" class="text-center py-2 text-sm text-gray-500 dark:text-gray-400">
          ... i {{ queue.length - 10 }} więcej w kolejce
        </div>
      </div>
      
      <div v-else class="text-center py-8 text-gray-500 dark:text-gray-400">
        Brak zawodników w kolejce
      </div>
    </div>

    <!-- Manual Testing -->
    <div class="border-t border-gray-200 dark:border-gray-600 pt-6">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Manual Testing</h3>
      
      <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
        <div class="flex space-x-2 mb-4">
          <input 
            v-model="manualFrame"
            @keyup.enter="sendManualFrame"
            placeholder="Wpisz ramkę SECTRO (np. CZL1123456789)"
            class="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent text-sm"
          />
          <button 
            @click="sendManualFrame"
            :disabled="!manualFrame.trim()"
            class="px-4 py-2 bg-purple-600 disabled:bg-gray-400 text-white rounded-lg font-medium hover:bg-purple-700 transition-colors duration-200 text-sm"
          >
            Wyślij
          </button>
        </div>
        
        <div class="flex space-x-2">
          <button 
            @click="sendTestFrame('START')"
            class="px-3 py-1 bg-green-100 dark:bg-green-900/20 text-green-700 dark:text-green-400 rounded text-sm font-medium hover:bg-green-200 dark:hover:bg-green-900/40 transition-colors"
          >
            Test START
          </button>
          <button 
            @click="sendTestFrame('FINISH')"
            class="px-3 py-1 bg-blue-100 dark:bg-blue-900/20 text-blue-700 dark:text-blue-400 rounded text-sm font-medium hover:bg-blue-200 dark:hover:bg-blue-900/40 transition-colors"
          >
            Test FINISH
          </button>
          <button 
            @click="sendTestFrame('INVALID')"
            class="px-3 py-1 bg-red-100 dark:bg-red-900/20 text-red-700 dark:text-red-400 rounded text-sm font-medium hover:bg-red-200 dark:hover:bg-red-900/40 transition-colors"
          >
            Test Invalid
          </button>
        </div>
        
        <div v-if="lastTestResult" class="mt-3 p-2 rounded" 
             :class="lastTestResult.success ? 'bg-green-100 dark:bg-green-900/20 text-green-700 dark:text-green-400' : 'bg-red-100 dark:bg-red-900/20 text-red-700 dark:text-red-400'">
          <div class="text-xs font-medium">{{ lastTestResult.message }}</div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

// ===== PROPS & EMITS =====
const props = defineProps({
  session: {
    type: Object,
    required: true
  },
  queue: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['timing-started', 'measurement-recorded', 'refresh-requested'])

// ===== REACTIVE STATE =====
const manualFrame = ref('')
const lastTestResult = ref(null)
const currentTime = ref(0)
const timeInterval = ref(null)

// ===== COMPUTED PROPERTIES =====
const currentRunner = computed(() => {
  const running = props.queue.find(q => 
    q.unified_status === 'RUNNING' || q.unified_status === 'TIMING'
  )
  
  if (running && running.start_time) {
    const start = new Date(running.start_time).getTime()
    const now = running.finish_time ? new Date(running.finish_time).getTime() : Date.now()
    running.current_time = (now - start) / 1000
  }
  
  return running
})

// ===== STATUS METHODS =====
const getSessionStatusClass = () => {
  if (props.session.status === 'active') {
    return 'bg-green-100 dark:bg-green-900/20 text-green-600 dark:text-green-400'
  }
  return 'bg-yellow-100 dark:bg-yellow-900/20 text-yellow-600 dark:text-yellow-400'
}

const getSessionStatusText = () => {
  if (props.session.status === 'active') {
    return 'AKTYWNA'
  }
  return 'OCZEKUJE'
}

const getQueueItemClass = (athlete, index) => {
  if (athlete.unified_status === 'RUNNING' || athlete.unified_status === 'TIMING') {
    return 'bg-gradient-to-r from-purple-50 to-blue-50 dark:from-purple-900/20 dark:to-blue-900/20 border-purple-200 dark:border-purple-700'
  }
  if (athlete.unified_status === 'FINISHED') {
    return 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800'
  }
  if (index === 0) {
    return 'bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-700'
  }
  return 'bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700'
}

const getPositionClass = (index) => {
  if (index === 0) {
    return 'bg-blue-600 text-white'
  }
  if (index === 1) {
    return 'bg-blue-100 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400'
  }
  return 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400'
}

const getStatusClass = (status) => {
  switch (status) {
    case 'RUNNING':
    case 'TIMING':
      return 'bg-purple-100 dark:bg-purple-900/20 text-purple-600 dark:text-purple-400'
    case 'FINISHED':
      return 'bg-green-100 dark:bg-green-900/20 text-green-600 dark:text-green-400'
    case 'READY':
      return 'bg-blue-100 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400'
    default:
      return 'bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400'
  }
}

const getStatusText = (status) => {
  switch (status) {
    case 'RUNNING': return 'BIEGNIE'
    case 'TIMING': return 'TIMING'
    case 'FINISHED': return 'UKOŃCZONE'
    case 'READY': return 'GOTOWY'
    default: return 'OCZEKUJE'
  }
}

// ===== UTILITY METHODS =====
const formatTime = (seconds) => {
  if (!seconds || seconds < 0) return '00:00.00'
  
  const minutes = Math.floor(seconds / 60)
  const secs = seconds % 60
  
  return `${minutes.toString().padStart(2, '0')}:${secs.toFixed(2).padStart(5, '0')}`
}

// ===== MANUAL TESTING =====
const sendManualFrame = async () => {
  if (!manualFrame.value.trim()) return
  
  await processFrame(manualFrame.value.trim())
  manualFrame.value = ''
}

const sendTestFrame = async (type) => {
  const timestamp = Date.now().toString().slice(-9)
  let frame = ''
  
  switch (type) {
    case 'START':
      frame = `CZL1${timestamp}`
      break
    case 'FINISH':
      frame = `CZL2${timestamp}`
      break
    case 'INVALID':
      frame = `INVALID${timestamp}`
      break
  }
  
  await processFrame(frame)
}

const processFrame = async (frame) => {
  try {
    const response = await fetch('/api/unified/record-measurement', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        session_id: props.session.id,
        frame: frame
      })
    })
    
    const data = await response.json()
    
    lastTestResult.value = {
      success: data.success,
      message: data.message || data.error
    }
    
    if (data.success) {
      emit('measurement-recorded', data)
    }
    
    // Clear result after 5 seconds
    setTimeout(() => {
      lastTestResult.value = null
    }, 5000)
    
  } catch (error) {
    console.error('❌ Frame processing error:', error)
    lastTestResult.value = {
      success: false,
      message: 'Błąd połączenia z serwerem'
    }
  }
}

const refreshData = () => {
  emit('refresh-requested')
}

// ===== LIFECYCLE =====
onMounted(() => {
  // Update timer every second for current runner
  timeInterval.value = setInterval(() => {
    if (currentRunner.value && currentRunner.value.start_time && !currentRunner.value.finish_time) {
      const start = new Date(currentRunner.value.start_time).getTime()
      const now = Date.now()
      currentRunner.value.current_time = (now - start) / 1000
    }
  }, 100) // Update every 100ms for smooth timing
})

onUnmounted(() => {
  if (timeInterval.value) {
    clearInterval(timeInterval.value)
  }
})
</script>

<style scoped>
/* Live timing animations */
.live-timing-card {
  transition: all 0.3s ease;
}

/* Pulse animation for active states */
@keyframes pulse-glow {
  0%, 100% { box-shadow: 0 0 0 0 rgba(139, 92, 246, 0.7); }
  50% { box-shadow: 0 0 0 10px rgba(139, 92, 246, 0); }
}

.animate-pulse-glow {
  animation: pulse-glow 2s infinite;
}

/* Timer font */
.font-mono {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
}

/* Smooth transitions for queue items */
.queue-item {
  transition: all 0.3s ease;
}

.queue-item:hover {
  transform: translateY(-1px);
}
</style> 