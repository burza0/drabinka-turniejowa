<template>
  <div class="results-card bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
    
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 bg-green-100 dark:bg-green-900/20 rounded-lg flex items-center justify-center">
          <svg class="w-5 h-5 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
          </svg>
        </div>
        <div>
          <h2 class="text-xl font-bold text-gray-900 dark:text-white">Wyniki</h2>
          <p class="text-sm text-gray-600 dark:text-gray-400">Ranking i analiza sesji</p>
        </div>
      </div>
      
      <div class="flex items-center space-x-2">
        <button 
          @click="exportResults"
          class="px-4 py-2 bg-green-100 dark:bg-green-900/20 text-green-700 dark:text-green-400 rounded-lg font-medium hover:bg-green-200 dark:hover:bg-green-900/40 transition-colors duration-200"
        >
          📊 Eksport
        </button>
        
        <button 
          @click="refreshResults"
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

    <!-- Stats Summary -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
      <div class="bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900/20 dark:to-blue-800/20 rounded-lg p-4 border border-blue-200 dark:border-blue-800">
        <div class="flex items-center justify-between">
          <div>
            <div class="text-sm font-medium text-blue-600 dark:text-blue-400">Ukończone</div>
            <div class="text-2xl font-bold text-blue-900 dark:text-blue-100">{{ finishedCount }}</div>
          </div>
          <div class="w-10 h-10 bg-blue-200 dark:bg-blue-800 rounded-lg flex items-center justify-center">
            <svg class="w-5 h-5 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-gradient-to-br from-green-50 to-green-100 dark:from-green-900/20 dark:to-green-800/20 rounded-lg p-4 border border-green-200 dark:border-green-800">
        <div class="flex items-center justify-between">
          <div>
            <div class="text-sm font-medium text-green-600 dark:text-green-400">Najlepszy czas</div>
            <div class="text-2xl font-bold text-green-900 dark:text-green-100">{{ bestTime }}</div>
          </div>
          <div class="w-10 h-10 bg-green-200 dark:bg-green-800 rounded-lg flex items-center justify-center">
            <svg class="w-5 h-5 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-900/20 dark:to-purple-800/20 rounded-lg p-4 border border-purple-200 dark:border-purple-800">
        <div class="flex items-center justify-between">
          <div>
            <div class="text-sm font-medium text-purple-600 dark:text-purple-400">Średni czas</div>
            <div class="text-2xl font-bold text-purple-900 dark:text-purple-100">{{ averageTime }}</div>
          </div>
          <div class="w-10 h-10 bg-purple-200 dark:bg-purple-800 rounded-lg flex items-center justify-center">
            <svg class="w-5 h-5 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
        </div>
      </div>

      <div class="bg-gradient-to-br from-orange-50 to-orange-100 dark:from-orange-900/20 dark:to-orange-800/20 rounded-lg p-4 border border-orange-200 dark:border-orange-800">
        <div class="flex items-center justify-between">
          <div>
            <div class="text-sm font-medium text-orange-600 dark:text-orange-400">W kolejce</div>
            <div class="text-2xl font-bold text-orange-900 dark:text-orange-100">{{ pendingCount }}</div>
          </div>
          <div class="w-10 h-10 bg-orange-200 dark:bg-orange-800 rounded-lg flex items-center justify-center">
            <svg class="w-5 h-5 text-orange-600 dark:text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Results Table -->
    <div class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
      
      <!-- Table Header -->
      <div class="bg-gray-50 dark:bg-gray-700 px-6 py-3 border-b border-gray-200 dark:border-gray-600">
        <div class="grid grid-cols-12 gap-4 text-sm font-medium text-gray-600 dark:text-gray-400">
          <div class="col-span-1">Poz.</div>
          <div class="col-span-4">Zawodnik</div>
          <div class="col-span-3">Klub</div>
          <div class="col-span-2">Czas</div>
          <div class="col-span-2">Status</div>
        </div>
      </div>

      <!-- Table Body -->
      <div v-if="sortedResults.length > 0" class="divide-y divide-gray-200 dark:divide-gray-600">
        <div v-for="(result, index) in sortedResults" :key="result.nr_startowy"
             :class="getResultRowClass(result, index)"
             class="px-6 py-4 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-150">
          
          <div class="grid grid-cols-12 gap-4 items-center">
            
            <!-- Position -->
            <div class="col-span-1">
              <div :class="getPositionClass(index)"
                   class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold">
                {{ result.position || '-' }}
              </div>
            </div>

            <!-- Athlete -->
            <div class="col-span-4">
              <div class="flex items-center space-x-3">
                <div class="flex-1">
                  <div class="font-semibold text-gray-900 dark:text-white">
                    {{ result.imie }} {{ result.nazwisko }}
                  </div>
                  <div class="text-sm text-gray-600 dark:text-gray-400">
                    ID: {{ result.nr_startowy }}
                  </div>
                </div>
                
                <!-- Medal icons -->
                <div v-if="result.position === 1" class="text-yellow-500">🥇</div>
                <div v-else-if="result.position === 2" class="text-gray-400">🥈</div>
                <div v-else-if="result.position === 3" class="text-amber-600">🥉</div>
              </div>
            </div>

            <!-- Club -->
            <div class="col-span-3">
              <div class="text-sm text-gray-900 dark:text-white">
                {{ result.klub || 'Brak klubu' }}
              </div>
            </div>

            <!-- Time -->
            <div class="col-span-2">
              <div v-if="result.total_time" class="text-lg font-mono font-bold text-gray-900 dark:text-white">
                {{ formatTime(result.total_time) }}
              </div>
              <div v-else-if="result.current_time" class="text-lg font-mono text-blue-600 dark:text-blue-400">
                {{ formatTime(result.current_time) }}
              </div>
              <div v-else class="text-sm text-gray-500 dark:text-gray-400">
                -:--.--
              </div>
              
              <!-- Timing details -->
              <div v-if="result.start_time || result.finish_time" class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                <div v-if="result.start_time">Start: {{ formatTimestamp(result.start_time) }}</div>
                <div v-if="result.finish_time">Finish: {{ formatTimestamp(result.finish_time) }}</div>
              </div>
            </div>

            <!-- Status -->
            <div class="col-span-2">
              <!-- Time diff from leader -->
              <div v-if="result.position > 1 && result.total_time && bestTimeSeconds" 
                   class="text-xs text-gray-500 dark:text-gray-400">
                +{{ formatTime(result.total_time - bestTimeSeconds) }}
              </div>
              
              <!-- Debug info - sprawdźmy co się wyświetla -->
              <div class="text-xs text-gray-400 mt-1">
                Status: {{ result.unified_status }}
              </div>
            </div>

          </div>
        </div>
      </div>

      <!-- Empty state -->
      <div v-else class="px-6 py-12 text-center">
        <svg class="w-12 h-12 text-gray-400 dark:text-gray-600 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
        </svg>
        <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">Brak wyników</h3>
        <p class="text-gray-600 dark:text-gray-400">
          Wyniki pojawią się po ukończeniu biegu przez zawodników
        </p>
      </div>

    </div>

  </div>
</template>

<script setup>
import { computed } from 'vue'

// ===== PROPS & EMITS =====
const props = defineProps({
  sessionId: {
    type: Number,
    required: true
  },
  results: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['refresh-requested'])

// ===== REACTIVE STATE =====
// results jest teraz w props - nie potrzebujemy lokalnej zmiennej

// ===== COMPUTED PROPERTIES =====
const sortedResults = computed(() => {
  // Sortuj i przypisz pozycje
  const finished = props.results
    .filter(r => r.unified_status === 'FINISHED' && r.total_time)
    .sort((a, b) => a.total_time - b.total_time)
    .map((r, index) => ({ ...r, position: index + 1 }))
  
  const pending = props.results
    .filter(r => r.unified_status !== 'FINISHED' || !r.total_time)
    .map(r => ({ ...r, position: null }))
  
  return [...finished, ...pending]
})

const finishedResults = computed(() => 
  sortedResults.value.filter(r => r.unified_status === 'FINISHED' && r.total_time)
)

const finishedCount = computed(() => finishedResults.value.length)

const pendingCount = computed(() => 
  sortedResults.value.filter(r => r.unified_status !== 'FINISHED').length
)

const bestTimeSeconds = computed(() => {
  const finished = finishedResults.value
  if (finished.length === 0) return null
  return Math.min(...finished.map(r => r.total_time))
})

const bestTime = computed(() => {
  if (!bestTimeSeconds.value) return '--:--'
  return formatTime(bestTimeSeconds.value)
})

const averageTime = computed(() => {
  const finished = finishedResults.value
  if (finished.length === 0) return '--:--'
  
  const sum = finished.reduce((acc, r) => acc + r.total_time, 0)
  const avg = sum / finished.length
  return formatTime(avg)
})

// ===== STYLING METHODS =====
const getResultRowClass = (result, index) => {
  if (result.unified_status === 'RUNNING' || result.unified_status === 'TIMING') {
    return 'bg-purple-50 dark:bg-purple-900/10'
  }
  if (result.position === 1) {
    return 'bg-yellow-50 dark:bg-yellow-900/10'
  }
  if (result.position === 2) {
    return 'bg-gray-50 dark:bg-gray-800'
  }
  if (result.position === 3) {
    return 'bg-amber-50 dark:bg-amber-900/10'
  }
  return 'bg-white dark:bg-gray-800'
}

const getPositionClass = (index) => {
  const result = sortedResults.value[index]
  
  if (result.position === 1) {
    return 'bg-yellow-500 text-white'
  }
  if (result.position === 2) {
    return 'bg-gray-400 text-white'
  }
  if (result.position === 3) {
    return 'bg-amber-600 text-white'
  }
  if (result.total_time) {
    return 'bg-blue-100 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400'
  }
  return 'bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400'
}

const getStatusClass = (status) => {
  switch (status) {
    case 'FINISHED':
      return 'bg-green-100 dark:bg-green-900/20 text-green-600 dark:text-green-400'
    case 'RUNNING':
    case 'TIMING':
      return 'bg-purple-100 dark:bg-purple-900/20 text-purple-600 dark:text-purple-400'
    case 'READY':
      return 'bg-blue-100 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400'
    default:
      return 'bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400'
  }
}

const getStatusText = (status) => {
  switch (status) {
    case 'FINISHED': return 'UKOŃCZONE'
    case 'RUNNING': return 'BIEGNIE'
    case 'TIMING': return 'TIMING'
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

const formatTimestamp = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString('pl-PL', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

// ===== ACTION METHODS =====
const refreshResults = async () => {
  // Dane są teraz przekazywane przez props - wystarczy emit do nadrzędnego komponentu
  emit('refresh-requested')
}

const exportResults = () => {
  // Generate CSV export
  const headers = ['Pozycja', 'Zawodnik', 'Klub', 'Czas', 'Start', 'Finish', 'Status']
  const csvRows = [headers.join(',')]
  
  sortedResults.value.forEach(result => {
    const row = [
      result.position || '',
      `"${result.imie} ${result.nazwisko}"`,
      `"${result.klub || ''}"`,
      result.total_time ? formatTime(result.total_time) : '',
      result.start_time ? formatTimestamp(result.start_time) : '',
      result.finish_time ? formatTimestamp(result.finish_time) : '',
      getStatusText(result.unified_status)
    ]
    csvRows.push(row.join(','))
  })
  
  const csv = csvRows.join('\n')
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  
  if (link.download !== undefined) {
    const url = URL.createObjectURL(blob)
    link.setAttribute('href', url)
    link.setAttribute('download', `wyniki_sesja_${props.sessionId}_${new Date().toISOString().slice(0, 10)}.csv`)
    link.style.visibility = 'hidden'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }
}

// ===== LIFECYCLE =====
// Dane są teraz przekazywane przez props - nie potrzebujemy onMounted
</script>

<style scoped>
/* Results table styling */
.results-card {
  transition: all 0.3s ease;
}

/* Podium effects */
.position-1 {
  position: relative;
}

.position-1::before {
  content: '👑';
  position: absolute;
  top: -8px;
  right: -8px;
  font-size: 16px;
}

/* Smooth transitions */
.hover\:bg-gray-50:hover {
  background-color: rgba(249, 250, 251, 0.8);
}

/* Table responsiveness */
@media (max-width: 768px) {
  .grid-cols-12 {
    grid-template-columns: repeat(6, 1fr);
  }
  
  .col-span-4 {
    grid-column: span 3;
  }
  
  .col-span-3 {
    display: none;
  }
}

/* Font for times */
.font-mono {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
}
</style> 