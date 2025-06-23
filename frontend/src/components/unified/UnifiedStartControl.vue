<template>
  <div class="unified-start-control min-h-screen bg-gray-50 dark:bg-gray-900 p-6">
    
    <!-- Header with current workflow phase -->
    <div class="mb-8">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <div class="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <div>
            <h1 class="text-3xl font-bold text-gray-900 dark:text-white">🚀 Unified Start Control</h1>
            <p class="text-gray-600 dark:text-gray-400">Centrum Startu + SECTRO Live Timing</p>
          </div>
        </div>
        
        <div class="text-right">
          <div class="text-sm text-gray-500 dark:text-gray-400">Faza workflow:</div>
          <div class="text-lg font-semibold" :class="getPhaseClass()">
            {{ currentPhase }}
          </div>
        </div>
      </div>
      
      <!-- Workflow progress -->
      <div class="mt-4 flex items-center space-x-2">
        <div v-for="(step, index) in workflowSteps" :key="index" 
             class="flex items-center">
          <div :class="getStepClass(index)" 
               class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold">
            {{ index + 1 }}
          </div>
          <div v-if="index < workflowSteps.length - 1" 
               :class="getArrowClass(index)"
               class="w-8 h-0.5 mx-2">
          </div>
        </div>
      </div>
      <div class="mt-2 flex space-x-10">
        <div v-for="(step, index) in workflowSteps" :key="index" 
             :class="getStepTextClass(index)"
             class="text-xs font-medium">
          {{ step }}
        </div>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
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
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Grupy gotowe</p>
            <p class="text-2xl font-bold text-blue-600 dark:text-blue-400">{{ readyGroups }}</p>
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
            <p class="text-sm font-medium text-gray-600 dark:text-gray-400">W kolejce</p>
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

    <!-- Dynamic content based on workflow phase -->
    <div class="space-y-8">
      
      <!-- PHASE 1: QR Scanner - Always visible -->
      <QRScannerCard 
        @athlete-registered="onAthleteRegistered"
        @refresh-requested="refreshData"
      />
      
      <!-- PHASE 2: Start Groups - Show when athletes registered -->
      <StartGroupsCard 
        v-if="hasRegisteredAthletes"
        :groups="groups"
        :loading="loading"
        @group-activated="onGroupActivated"
        @group-deactivated="onGroupDeactivated"
        @refresh-requested="refreshData"
      />
      
      <!-- PHASE 3: Live Timing - Show when group active -->
      <LiveTimingCard
        v-if="activeSession"
        :session="activeSession"
        :queue="queue"
        :loading="loading"
        @timing-started="onTimingStarted"
        @measurement-recorded="onMeasurementRecorded"
        @refresh-requested="refreshData"
      />
      
      <!-- PHASE 4: Results - Show when there are results -->
      <ResultsCard
        v-if="activeSession && hasResults"
        :session-id="activeSession.id"
        :loading="loading"
        @refresh-requested="refreshData"
      />
      
    </div>
    
    <!-- Global refresh button -->
    <div class="fixed bottom-8 right-8">
      <button 
        @click="refreshData"
        :disabled="loading"
        class="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white p-4 rounded-full shadow-lg transition-all duration-200"
      >
        <svg v-if="loading" class="w-6 h-6 animate-spin" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="m4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
      </button>
    </div>
    
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import QRScannerCard from './QRScannerCard.vue'
import StartGroupsCard from './StartGroupsCard.vue'
import LiveTimingCard from './LiveTimingCard.vue'
import ResultsCard from './ResultsCard.vue'

// ===== REACTIVE STATE =====
const loading = ref(false)
const groups = ref([])
const queue = ref([])
const activeSession = ref(null)
const stats = ref({})
const refreshInterval = ref(null)

// ===== WORKFLOW CONSTANTS =====
const workflowSteps = ['Rejestracja', 'Grupy', 'Timing', 'Wyniki']

// ===== COMPUTED PROPERTIES =====
const hasRegisteredAthletes = computed(() => 
  groups.value.some(g => g.liczba_zawodnikow > 0)
)

const readyGroups = computed(() => 
  groups.value.filter(g => g.liczba_zawodnikow > 0).length
)

const hasResults = computed(() => 
  queue.value.some(q => q.unified_status === 'FINISHED' || q.unified_status === 'TIMING')
)

const currentPhase = computed(() => {
  if (activeSession.value && hasResults.value) return '4. Wyniki'
  if (activeSession.value) return '3. Live Timing'
  if (hasRegisteredAthletes.value) return '2. Grupy Startowe'
  return '1. Rejestracja Zawodników'
})

// ===== WORKFLOW STYLING METHODS =====
const getPhaseClass = () => {
  const phase = currentPhase.value
  if (phase.includes('Wyniki')) return 'text-green-600 dark:text-green-400'
  if (phase.includes('Timing')) return 'text-purple-600 dark:text-purple-400'
  if (phase.includes('Grupy')) return 'text-blue-600 dark:text-blue-400'
  return 'text-gray-600 dark:text-gray-400'
}

const getStepClass = (index) => {
  const currentStep = getCurrentStepIndex()
  if (index < currentStep) return 'bg-green-500 text-white'
  if (index === currentStep) return 'bg-blue-500 text-white'
  return 'bg-gray-300 dark:bg-gray-600 text-gray-600 dark:text-gray-400'
}

const getArrowClass = (index) => {
  const currentStep = getCurrentStepIndex()
  if (index < currentStep) return 'bg-green-500'
  return 'bg-gray-300 dark:bg-gray-600'
}

const getStepTextClass = (index) => {
  const currentStep = getCurrentStepIndex()
  if (index < currentStep) return 'text-green-600 dark:text-green-400'
  if (index === currentStep) return 'text-blue-600 dark:text-blue-400'
  return 'text-gray-500 dark:text-gray-400'
}

const getCurrentStepIndex = () => {
  if (activeSession.value && hasResults.value) return 3  // Wyniki
  if (activeSession.value) return 2                      // Timing
  if (hasRegisteredAthletes.value) return 1              // Grupy
  return 0                                               // Rejestracja
}

// ===== API METHODS =====
const refreshData = async () => {
  loading.value = true
  try {
    const response = await fetch('/api/unified/dashboard-data')
    const data = await response.json()
    
    if (data.success) {
      groups.value = data.groups || []
      queue.value = data.queue || []
      activeSession.value = data.activeSession
      stats.value = data.stats || {}
      
      console.log('✅ Unified dashboard data refreshed:', {
        groups: groups.value.length,
        queue: queue.value.length,
        activeSession: activeSession.value?.id || 'none',
        currentPhase: currentPhase.value
      })
    } else {
      console.error('❌ Error refreshing unified data:', data.error)
    }
  } catch (error) {
    console.error('❌ Network error refreshing unified data:', error)
  } finally {
    loading.value = false
  }
}

// ===== EVENT HANDLERS =====
const onAthleteRegistered = async (data) => {
  console.log('🏃 Athlete registered:', data)
  await refreshData()
  
  // Auto-scroll to groups if first registration
  if (groups.value.length === 1) {
    setTimeout(() => {
      const groupsCard = document.querySelector('.start-groups-card')
      if (groupsCard) {
        groupsCard.scrollIntoView({ behavior: 'smooth' })
      }
    }, 500)
  }
}

const onGroupActivated = async (data) => {
  console.log('🏁 Group activated:', data)
  await refreshData()
  
  // Auto-scroll to live timing
  setTimeout(() => {
    const timingCard = document.querySelector('.live-timing-card')
    if (timingCard) {
      timingCard.scrollIntoView({ behavior: 'smooth' })
    }
  }, 500)
}

const onGroupDeactivated = async (data) => {
  console.log('⏹️ Group deactivated:', data)
  await refreshData()
}

const onTimingStarted = async (data) => {
  console.log('⏱️ Timing started:', data)
  await refreshData()
}

const onMeasurementRecorded = async (data) => {
  console.log('📊 Measurement recorded:', data)
  await refreshData()
  
  // Auto-scroll to results if first result
  if (hasResults.value) {
    setTimeout(() => {
      const resultsCard = document.querySelector('.results-card')
      if (resultsCard) {
        resultsCard.scrollIntoView({ behavior: 'smooth' })
      }
    }, 500)
  }
}

// ===== LIFECYCLE =====
onMounted(() => {
  refreshData()
  // Auto-refresh every 10 seconds
  refreshInterval.value = setInterval(refreshData, 10000)
})

onUnmounted(() => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
  }
})
</script>

<style scoped>
.unified-start-control {
  transition: all 0.3s ease;
}

/* Smooth transitions for workflow steps */
.workflow-step {
  transition: all 0.3s ease;
}

/* Card animations */
.card-enter-active, .card-leave-active {
  transition: all 0.5s ease;
}

.card-enter-from, .card-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

/* Scrollbar styling */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style> 