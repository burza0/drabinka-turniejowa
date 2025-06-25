<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
    <div class="flex justify-between items-center mb-4">
      <h3 class="text-lg font-bold text-gray-900 dark:text-white">Live Results</h3>
      
      <div class="flex items-center space-x-4">
        <button 
          @click="refreshResults"
          class="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm flex items-center space-x-1"
        >
          <span>🔄</span>
          <span>Odśwież</span>
        </button>
        
        <div class="text-sm text-gray-500 dark:text-gray-400">
          Wyników: {{ results.length }}
        </div>
      </div>
    </div>
    
    <!-- Results Table -->
    <div class="overflow-x-auto">
      <table class="min-w-full">
        <thead class="bg-gray-50 dark:bg-gray-700">
          <tr>
            <th class="px-4 py-2 text-left text-sm font-medium text-gray-500 dark:text-gray-300">Pozycja</th>
            <th class="px-4 py-2 text-left text-sm font-medium text-gray-500 dark:text-gray-300">Nr</th>
            <th class="px-4 py-2 text-left text-sm font-medium text-gray-500 dark:text-gray-300">Zawodnik</th>
            <th class="px-4 py-2 text-left text-sm font-medium text-gray-500 dark:text-gray-300">Kategoria</th>
            <th class="px-4 py-2 text-left text-sm font-medium text-gray-500 dark:text-gray-300">Klub</th>
            <th class="px-4 py-2 text-left text-sm font-medium text-gray-500 dark:text-gray-300">Start</th>
            <th class="px-4 py-2 text-left text-sm font-medium text-gray-500 dark:text-gray-300">Finish</th>
            <th class="px-4 py-2 text-left text-sm font-medium text-gray-500 dark:text-gray-300">Czas</th>
            <th class="px-4 py-2 text-left text-sm font-medium text-gray-500 dark:text-gray-300">Status</th>
          </tr>
        </thead>
        <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
          <tr 
            v-for="(result, index) in sortedResults" 
            :key="result.nr_startowy"
            :class="[
              'hover:bg-gray-50 dark:hover:bg-gray-700',
              result.status === 'completed' ? '' : 'opacity-75'
            ]"
          >
            <td class="px-4 py-2 whitespace-nowrap">
              <span :class="[
                'inline-flex items-center justify-center w-8 h-8 rounded-full text-sm font-bold',
                index === 0 ? 'bg-yellow-400 text-yellow-900' :
                index === 1 ? 'bg-gray-300 text-gray-900' :
                index === 2 ? 'bg-orange-400 text-orange-900' :
                'bg-gray-100 text-gray-600'
              ]">
                {{ index + 1 }}
              </span>
            </td>
            
            <td class="px-4 py-2 whitespace-nowrap">
              <span class="text-base font-bold text-gray-900 dark:text-white">
                {{ result.nr_startowy }}
              </span>
            </td>
            
            <td class="px-4 py-2 whitespace-nowrap">
              <div class="text-base font-medium text-gray-900 dark:text-white">
                {{ result.imie }} {{ result.nazwisko }}
              </div>
            </td>
            
            <td class="px-4 py-2 whitespace-nowrap text-sm text-gray-600 dark:text-gray-300">
              {{ result.kategoria }} {{ result.plec }}
            </td>
            
            <td class="px-4 py-2 whitespace-nowrap text-sm text-gray-600 dark:text-gray-300">
              {{ result.klub }}
            </td>
            
            <td class="px-4 py-2 whitespace-nowrap text-sm font-mono text-gray-600 dark:text-gray-300">
              {{ result.start_time ? formatSectroTime(result.start_time) : '-' }}
            </td>
            
            <td class="px-4 py-2 whitespace-nowrap text-sm font-mono text-gray-600 dark:text-gray-300">
              {{ result.finish_time ? formatSectroTime(result.finish_time) : '-' }}
            </td>
            
            <td class="px-4 py-2 whitespace-nowrap">
              <span :class="[
                'text-lg font-bold font-mono',
                result.total_time ? 'text-green-600 dark:text-green-400' : 'text-gray-400'
              ]">
                {{ result.total_time ? formatRaceTime(result.total_time) : '--:--' }}
              </span>
            </td>
            
            <td class="px-4 py-2 whitespace-nowrap">
              <StatusBadge :status="result.status" />
            </td>
          </tr>
        </tbody>
      </table>
      
      <!-- No Results -->
      <div v-if="results.length === 0" class="text-center py-8 text-gray-500 dark:text-gray-400">
        <div class="text-4xl mb-2">🏁</div>
        <div>Brak wyników</div>
        <div class="text-sm">Wyniki pojawią się po pierwszych przejażdzkach</div>
      </div>
    </div>
    
    <!-- Statistics -->
    <div v-if="results.length > 0" class="mt-6 pt-4 border-t border-gray-200 dark:border-gray-600">
      <div class="grid grid-cols-1 sm:grid-cols-4 gap-4 text-center">
        <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded">
          <div class="text-lg font-bold text-gray-900 dark:text-white">{{ completedCount }}</div>
          <div class="text-sm text-gray-500 dark:text-gray-400">Ukończone</div>
        </div>
        
        <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded">
          <div class="text-lg font-bold text-green-600">{{ bestTime }}</div>
          <div class="text-sm text-gray-500 dark:text-gray-400">Najlepszy czas</div>
        </div>
        
        <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded">
          <div class="text-lg font-bold text-blue-600">{{ averageTime }}</div>
          <div class="text-sm text-gray-500 dark:text-gray-400">Średni czas</div>
        </div>
        
        <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded">
          <div class="text-lg font-bold text-purple-600">{{ lastUpdateTime }}</div>
          <div class="text-sm text-gray-500 dark:text-gray-400">Ostatnia aktualizacja</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import StatusBadge from '../StatusBadge.vue'

// Props
const props = defineProps({
  sessionId: {
    type: Number,
    required: true
  },
  results: {
    type: Array,
    default: () => []
  }
})

// Reactive data
const internalResults = ref([])
const loading = ref(false)
const lastUpdateTime = ref('--:--')

// Computed
const sortedResults = computed(() => {
  const completed = internalResults.value
    .filter(r => r.status === 'completed' && r.total_time)
    .sort((a, b) => a.total_time - b.total_time)
  
  const incomplete = internalResults.value
    .filter(r => r.status !== 'completed' || !r.total_time)
    .sort((a, b) => (a.start_time || 0) - (b.start_time || 0))
  
  return [...completed, ...incomplete]
})

const completedCount = computed(() => {
  return internalResults.value.filter(r => r.status === 'completed' && r.total_time).length
})

const bestTime = computed(() => {
  const completed = internalResults.value.filter(r => r.status === 'completed' && r.total_time)
  if (completed.length === 0) return '--:--'
  
  const best = Math.min(...completed.map(r => r.total_time))
  return formatRaceTime(best)
})

const averageTime = computed(() => {
  const completed = internalResults.value.filter(r => r.status === 'completed' && r.total_time)
  if (completed.length === 0) return '--:--'
  
  const avg = completed.reduce((sum, r) => sum + r.total_time, 0) / completed.length
  return formatRaceTime(avg)
})

// Methods
const formatRaceTime = (seconds) => {
  if (!seconds || seconds <= 0) return '--:--'
  
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = (seconds % 60).toFixed(3)
  return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.padStart(6, '0')}`
}

const formatSectroTime = (sectroTime) => {
  if (!sectroTime) return '--:--'
  
  // Convert seconds since midnight to HH:MM:SS format
  const hours = Math.floor(sectroTime / 3600)
  const minutes = Math.floor((sectroTime % 3600) / 60)
  const seconds = Math.floor(sectroTime % 60)
  const milliseconds = Math.floor((sectroTime % 1) * 1000)
  
  return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}.${milliseconds.toString().padStart(3, '0')}`
}

const refreshResults = async () => {
  if (!props.sessionId) return
  
  loading.value = true
  
  try {
    const response = await axios.get(`/api/sectro/sessions/${props.sessionId}/results`)
    
    if (response.data.success) {
      internalResults.value = response.data.results
      lastUpdateTime.value = new Date().toLocaleTimeString('pl-PL')
      console.log('✅ Wyniki odświeżone:', response.data.results.length)
    }
  } catch (error) {
    console.error('❌ Błąd odświeżania wyników:', error)
  } finally {
    loading.value = false
  }
}

// Watch for prop changes
const updateFromProps = () => {
  if (props.results && props.results.length > 0) {
    internalResults.value = [...props.results]
    lastUpdateTime.value = new Date().toLocaleTimeString('pl-PL')
  }
}

// Auto-refresh
let refreshInterval
onMounted(() => {
  updateFromProps()
  refreshResults()
  
  // Auto-refresh every 5 seconds
  refreshInterval = setInterval(() => {
    refreshResults()
  }, 5000)
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})

// Watch for external updates
import { watch } from 'vue'
watch(() => props.results, updateFromProps, { deep: true })
</script> 