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
            <span v-if="sessions.length === 1">
              {{ sessions[0].kategoria }} {{ sessions[0].plec }} • {{ sessions[0].nazwa }}
            </span>
            <span v-else>
              {{ sessions.length }} aktywnych grup: {{ activeGroupNames }}
            </span>
          </p>
        </div>
      </div>
      
      <div class="flex items-center space-x-2">
        <div :class="getSessionStatusClass()" 
             class="px-3 py-1 rounded-full text-sm font-medium flex items-center space-x-2">
          <div class="w-2 h-2 rounded-full animate-pulse" 
               :class="sessions.some(s => s.status === 'active') ? 'bg-green-400' : 'bg-yellow-400'"></div>
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

    <!-- Queue with Inline Actions -->
    <div class="mb-8">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
        Kolejka startowa z kontrolą
        <span class="text-sm font-normal text-gray-500 dark:text-gray-400 ml-2">
          ({{ queue.length }} zawodników)
        </span>
      </h3>
      
      <div v-if="queue.length > 0" class="space-y-3">
        <div v-for="(athlete, index) in queue.slice(0, 15)" :key="athlete.nr_startowy"
             :class="getQueueItemClass(athlete, index)"
             class="p-4 rounded-lg border transition-all duration-200">
          
          <!-- Main row - athlete info + status -->
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center space-x-3">
              <!-- Position -->
              <div :class="getPositionClass(index)"
                   class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold">
                {{ index + 1 }}
              </div>
              
              <!-- Athlete info -->
              <div>
                <div class="font-medium text-gray-900 dark:text-white">
                  {{ athlete.imie }} {{ athlete.nazwisko }} 
                  <span class="text-gray-500 dark:text-gray-400">(#{{ athlete.nr_startowy }})</span>
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
              
              <div v-if="athlete.total_time" class="text-sm font-mono font-semibold text-gray-900 dark:text-white">
                ✅ {{ formatTime(athlete.total_time) }}
              </div>
              <div v-else-if="athlete.start_time && !athlete.finish_time" class="text-sm font-mono text-blue-600 dark:text-blue-400">
                ⏱️ {{ formatTime(getRealtimeCurrentTime(athlete)) }}
              </div>
            </div>
          </div>
          
          <!-- Action row - SECTRO input + contextual buttons -->
          <div class="flex items-center justify-between space-x-3 pt-2 border-t border-gray-100 dark:border-gray-700">
            
            <!-- SECTRO Input -->
            <div class="flex items-center space-x-2 flex-1">
              <span class="text-xs text-gray-500 dark:text-gray-400 font-medium">SECTRO:</span>
              <input 
                v-model="sectroFrames[athlete.nr_startowy]"
                @keyup.enter="sendManualFrameForAthlete(athlete.nr_startowy)"
                placeholder="CZL1123456789..."
                class="flex-1 max-w-48 px-2 py-1 text-xs border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-1 focus:ring-purple-500 focus:border-transparent"
              />
              <button 
                @click="sendManualFrameForAthlete(athlete.nr_startowy)"
                :disabled="!sectroFrames[athlete.nr_startowy]?.trim()"
                class="px-2 py-1 bg-purple-100 dark:bg-purple-900/20 text-purple-700 dark:text-purple-400 rounded text-xs font-medium hover:bg-purple-200 dark:hover:bg-purple-900/40 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Wyślij
              </button>
            </div>
            
            <!-- Contextual Action Buttons -->
            <div class="flex items-center space-x-1">
              
              <!-- READY status buttons -->
              <template v-if="athlete.unified_status === 'READY' || athlete.unified_status === 'REGISTERED'">
                <button 
                  @click="performAction(athlete, 'START')"
                  class="px-3 py-1 bg-green-100 dark:bg-green-900/20 text-green-700 dark:text-green-400 rounded text-xs font-medium hover:bg-green-200 dark:hover:bg-green-900/40 transition-colors"
                >
                  🚀 START
                </button>
                <button 
                  @click="performAction(athlete, 'INVALID')"
                  class="px-3 py-1 bg-red-100 dark:bg-red-900/20 text-red-700 dark:text-red-400 rounded text-xs font-medium hover:bg-red-200 dark:hover:bg-red-900/40 transition-colors"
                >
                  ❌ INVALID
                </button>
              </template>
              
              <!-- TIMING/RUNNING status buttons -->
              <template v-else-if="athlete.unified_status === 'TIMING' || athlete.unified_status === 'RUNNING'">
                <button 
                  @click="performAction(athlete, 'FINISH')"
                  class="px-3 py-1 bg-blue-100 dark:bg-blue-900/20 text-blue-700 dark:text-blue-400 rounded text-xs font-medium hover:bg-blue-200 dark:hover:bg-blue-900/40 transition-colors"
                >
                  🏁 FINISH
                </button>
                <button 
                  @click="performAction(athlete, 'STOP')"
                  class="px-3 py-1 bg-yellow-100 dark:bg-yellow-900/20 text-yellow-700 dark:text-yellow-400 rounded text-xs font-medium hover:bg-yellow-200 dark:hover:bg-yellow-900/40 transition-colors"
                >
                  ⏹️ STOP
                </button>
                <button 
                  @click="performAction(athlete, 'INVALID')"
                  class="px-3 py-1 bg-red-100 dark:bg-red-900/20 text-red-700 dark:text-red-400 rounded text-xs font-medium hover:bg-red-200 dark:hover:bg-red-900/40 transition-colors"
                >
                  ❌ INVALID
                </button>
              </template>
              
              <!-- FINISHED status buttons -->
              <template v-else-if="athlete.unified_status === 'FINISHED'">
                <button 
                  @click="performAction(athlete, 'RESET')"
                  class="px-3 py-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded text-xs font-medium hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
                >
                  🔄 RESET
                </button>
                <button 
                  @click="performAction(athlete, 'INVALID')"
                  class="px-3 py-1 bg-red-100 dark:bg-red-900/20 text-red-700 dark:text-red-400 rounded text-xs font-medium hover:bg-red-200 dark:hover:bg-red-900/40 transition-colors"
                >
                  ❌ INVALID
                </button>
              </template>
              
              <!-- Default actions for other statuses -->
              <template v-else>
                <button 
                  @click="performAction(athlete, 'START')"
                  class="px-3 py-1 bg-green-100 dark:bg-green-900/20 text-green-700 dark:text-green-400 rounded text-xs font-medium hover:bg-green-200 dark:hover:bg-green-900/40 transition-colors"
                >
                  🚀 START
                </button>
              </template>
              
            </div>
          </div>
          
          <!-- Result feedback for this athlete -->
          <div v-if="actionResults[athlete.nr_startowy]" 
               class="mt-2 p-2 rounded text-xs"
               :class="actionResults[athlete.nr_startowy].success ? 'bg-green-100 dark:bg-green-900/20 text-green-700 dark:text-green-400' : 'bg-red-100 dark:bg-red-900/20 text-red-700 dark:text-red-400">
            {{ actionResults[athlete.nr_startowy].message }}
          </div>
          
        </div>
        
        <div v-if="queue.length > 15" class="text-center py-2 text-sm text-gray-500 dark:text-gray-400">
          ... i {{ queue.length - 15 }} więcej w kolejce
        </div>
      </div>
      
      <div v-else class="text-center py-8 text-gray-500 dark:text-gray-400">
        Brak zawodników w kolejce
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

// ===== PROPS & EMITS =====
const props = defineProps({
  sessions: {
    type: Array,
    required: true,
    default: () => []
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
const sectroFrames = ref({})  // Map nr_startowy -> sectro frame input
const actionResults = ref({})  // Map nr_startowy -> last action result  
const timeInterval = ref(null)
const realtimeCurrentTime = ref(0)  // Reactive timer for current runner

// ===== COMPUTED PROPERTIES =====
const activeGroupNames = computed(() => {
  return props.sessions.map(s => `${s.kategoria} ${s.plec}`).join(', ')
})

const currentRunner = computed(() => {
  // Szukaj aktywnie biegnącego zawodnika
  const running = props.queue.find(q => 
    q.unified_status === 'RUNNING' || q.unified_status === 'TIMING'
  )
  
  if (running) {
    return {
      ...running,
      current_time: getRealtimeCurrentTime(running)
    }
  }
  
  // Jeśli nie ma aktywnie biegnącego, szukaj ostatniego z start_time (ale bez finish_time)
  const started = props.queue.find(q => 
    q.start_time && !q.finish_time
  )
  
  if (started) {
    return {
      ...started,
      current_time: getRealtimeCurrentTime(started)
    }
  }
  
  return null
})

// Helper function to get real-time current time
const getRealtimeCurrentTime = (athlete) => {
  if (!athlete.start_time) return 0
  
  // Use reactive timer to force re-computation
  const _ = realtimeCurrentTime.value
  
  const start = new Date(athlete.start_time).getTime()
  const end = athlete.finish_time ? new Date(athlete.finish_time).getTime() : Date.now()
  return Math.max(0, (end - start) / 1000)
}

// ===== STATUS METHODS =====
const getSessionStatusClass = () => {
  const allActive = props.sessions.every(s => s.status === 'active')
  if (allActive && props.sessions.length > 0) {
    return 'bg-green-100 dark:bg-green-900/20 text-green-600 dark:text-green-400'
  }
  return 'bg-yellow-100 dark:bg-yellow-900/20 text-yellow-600 dark:text-yellow-400'
}

const getSessionStatusText = () => {
  if (props.sessions.length === 0) return 'BRAK SESJI'
  
  const activeCount = props.sessions.filter(s => s.status === 'active').length
  if (activeCount === props.sessions.length) {
    return `${activeCount} AKTYWNA${activeCount > 1 ? 'E' : ''}`
  }
  return `${activeCount}/${props.sessions.length} AKTYWNE`
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

// ===== NEW INLINE ACTIONS =====
const sendManualFrameForAthlete = async (nr_startowy) => {
  const frame = sectroFrames.value[nr_startowy]
  if (!frame?.trim()) return
  
  await processFrameForAthlete(frame.trim(), nr_startowy)
  sectroFrames.value[nr_startowy] = ''
}

const performAction = async (athlete, actionType) => {
  console.log(`🎯 Performing action "${actionType}" for athlete #${athlete.nr_startowy}`)
  
  // Generate appropriate frame for action
  const now = new Date()
  const hours = now.getHours().toString().padStart(2, '0')
  const minutes = now.getMinutes().toString().padStart(2, '0')
  const seconds = now.getSeconds().toString().padStart(2, '0')
  const milliseconds = now.getMilliseconds().toString().padStart(3, '0')
  const sectroTimestamp = `${hours}${minutes}${seconds}${milliseconds}`
  
  let frame = ''
  
  switch (actionType) {
    case 'START':
      frame = `CZL1${sectroTimestamp}`  // Input 1 = START
      break
    case 'FINISH':
      frame = `CZL4${sectroTimestamp}`  // Input 4 = FINISH
      break
    case 'STOP':
      frame = `CZL2${sectroTimestamp}`  // Input 2 = STOP (intermediate)
      break
    case 'INVALID':
      frame = `INVALID${sectroTimestamp}`
      break
    case 'RESET':
      // Reset requires special handling - clear athlete data
      frame = `RESET${sectroTimestamp}`
      break
  }
  
  await processFrameForAthlete(frame, athlete.nr_startowy)
}

const processFrameForAthlete = async (frame, nr_startowy) => {
  try {
    const response = await fetch('/api/unified/record-measurement', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        session_id: props.sessions[0]?.id,
        raw_frame: frame,
        nr_startowy: nr_startowy
      })
    })
    
    const data = await response.json()
    
    actionResults.value[nr_startowy] = {
      success: data.success,
      message: data.message || data.error
    }
    
    if (data.success) {
      emit('measurement-recorded', data)
    }
    
    // Clear result after 3 seconds
    setTimeout(() => {
      if (actionResults.value[nr_startowy]) {
        delete actionResults.value[nr_startowy]
      }
    }, 3000)
    
  } catch (error) {
    console.error('❌ Frame processing error:', error)
    actionResults.value[nr_startowy] = {
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
  // Reactive timer - force computed property re-calculation every second for smooth timing
  timeInterval.value = setInterval(() => {
    realtimeCurrentTime.value = Date.now()
  }, 1000)
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