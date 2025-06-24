<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
    <!-- Dashboard Header -->
    <div class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between">
          <div class="flex items-center space-x-4">
            <div class="p-3 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-xl">
              <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z" />
              </svg>
            </div>
            <div>
              <h1 class="text-2xl lg:text-3xl font-bold text-gray-900 dark:text-white">
                🎯 SKATECROSS QR Dashboard
              </h1>
              <p class="text-gray-600 dark:text-gray-400 text-sm lg:text-base">
                Zarządzanie systemem QR turnieju SKATECROSS
              </p>
            </div>
          </div>
          
          <!-- Real-time Stats -->
          <div class="mt-4 lg:mt-0 grid grid-cols-3 gap-4">
            <div class="text-center">
              <div class="text-xl lg:text-2xl font-bold text-indigo-600 dark:text-indigo-400">{{ stats.totalZawodnicy }}</div>
              <div class="text-xs text-gray-500 dark:text-gray-400">👤 Zawodnicy</div>
            </div>
            <div class="text-center">
              <div class="text-xl lg:text-2xl font-bold text-green-600 dark:text-green-400">{{ stats.qrGenerated }}</div>
              <div class="text-xs text-gray-500 dark:text-gray-400">🔲 Kody QR</div>
            </div>
            <div class="text-center">
              <div class="text-xl lg:text-2xl font-bold text-purple-600 dark:text-purple-400">{{ stats.checkedIn }}</div>
              <div class="text-xs text-gray-500 dark:text-gray-400">✅ Zameldowani</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Dashboard Grid -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      
      <!-- Quick Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <EnhancedStatsCard 
          title="Łączna liczba zawodników" 
          :value="stats.totalZawodnicy"
          icon="👥"
          color="blue"
          :subtitle="`${stats.activeCategories} kategorii aktywnych`"
          :progress="(stats.checkedIn / stats.totalZawodnicy) * 100"
          :trend="stats.totalZawodnicy > 0 ? 'up' : 'neutral'"
          actionLabel="Zobacz wszystkich"
          @action="navigateTo('zawodnicy')"
        />
        
        <EnhancedStatsCard 
          title="Kody QR wygenerowane" 
          :value="stats.qrGenerated"
          icon="🔲"
          color="purple"
          :subtitle="`${Math.round((stats.qrGenerated / stats.totalZawodnicy) * 100)}% pokrycie`"
          :progress="(stats.qrGenerated / stats.totalZawodnicy) * 100"
          :trend="stats.qrGenerated > 0 ? 'up' : 'neutral'"
          actionLabel="Generuj QR"
          @action="navigateTo('qr-print')"
        />
        
        <EnhancedStatsCard 
          title="Zameldowani zawodnicy" 
          :value="stats.checkedIn"
          icon="✅"
          color="green"
          :subtitle="`${Math.round((stats.checkedIn / stats.totalZawodnicy) * 100)}% zameldowanych`"
          :progress="(stats.checkedIn / stats.totalZawodnicy) * 100"
          :trend="stats.checkedIn > 0 ? 'up' : 'neutral'"
          actionLabel="Centrum startu"
          @action="navigateTo('start-line')"
        />
        
        <EnhancedStatsCard 
          title="Aktywne kategorie" 
          :value="stats.activeCategories"
          icon="🏆"
          color="yellow"
          :subtitle="`${stats.clubsCount} klubów uczestniczy`"
          :progress="100"
          trend="neutral"
          actionLabel="Zobacz rankingi"
          @action="navigateTo('rankingi')"
        />
      </div>

      <!-- Top Section: Visualization -->
      <div class="mb-8">
        <div class="relative overflow-hidden rounded-3xl bg-white dark:bg-gray-800 shadow-xl">
          <div class="absolute inset-0 bg-gradient-to-r from-indigo-600 via-purple-600 to-blue-600 opacity-90"></div>
          <div class="relative px-8 py-12 text-center">
            <div class="flex items-center justify-center mb-4">
              <svg class="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
            <h2 class="text-3xl lg:text-4xl font-bold text-white mb-2">📊 Visualization</h2>
            <p class="text-indigo-100 text-lg">Dane turnieju prezentowane w przejrzysty sposób</p>
            <div class="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
              <div class="bg-white bg-opacity-20 rounded-lg p-3">
                <div class="text-2xl font-bold">{{ progressStats.qrProgress }}%</div>
                <div class="text-indigo-100">QR Coverage</div>
              </div>
              <div class="bg-white bg-opacity-20 rounded-lg p-3">
                <div class="text-2xl font-bold">{{ progressStats.checkinProgress }}%</div>
                <div class="text-indigo-100">Check-in Rate</div>
              </div>
              <div class="bg-white bg-opacity-20 rounded-lg p-3">
                <div class="text-2xl font-bold">{{ progressStats.readiness }}%</div>
                <div class="text-indigo-100">Tournament Ready</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Middle Row: Three Main Tiles -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <!-- Zawodnicy Management -->
        <div @click="navigateTo('zawodnicy')" class="group cursor-pointer transform hover:scale-105 transition-all duration-300">
          <div class="relative overflow-hidden rounded-3xl bg-gradient-to-br from-purple-500 to-purple-700 shadow-xl hover:shadow-2xl">
            <div class="absolute inset-0 bg-black opacity-0 group-hover:opacity-10 transition-opacity duration-300"></div>
            <div class="relative px-8 py-12 text-center">
              <div class="flex items-center justify-center mb-6">
                <svg class="w-16 h-16 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
                </svg>
              </div>
              <h3 class="text-2xl font-bold text-white mb-3">👤 Management</h3>
              <p class="text-purple-100 text-sm mb-4">Zarządzanie zawodnikami</p>
              <div class="text-lg font-semibold text-white">{{ stats.totalZawodnicy }} zawodników</div>
            </div>
          </div>
        </div>

        <!-- QR System -->
        <div @click="navigateTo('qr-dashboard')" class="group cursor-pointer transform hover:scale-105 transition-all duration-300">
          <div class="relative overflow-hidden rounded-3xl bg-gradient-to-br from-blue-500 to-cyan-600 shadow-xl hover:shadow-2xl">
            <div class="absolute inset-0 bg-black opacity-0 group-hover:opacity-10 transition-opacity duration-300"></div>
            <div class="relative px-8 py-12 text-center">
              <div class="flex items-center justify-center mb-6">
                <svg class="w-16 h-16 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h.01M5 8h2a1 1 0 001-1V5a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1zm12 0h2a1 1 0 001-1V5a1 1 0 00-1-1h-2a1 1 0 00-1 1v2a1 1 0 001 1zM5 20h2a1 1 0 001-1v-2a1 1 0 00-1-1H5a1 1 0 00-1 1v2a1 1 0 001 1z" />
                </svg>
              </div>
              <h3 class="text-2xl font-bold text-white mb-1">🔲 QR System</h3>
              <h3 class="text-xl font-semibold text-white mb-3">Solutions</h3>
              <p class="text-blue-100 text-sm mb-4">Admin Dashboard QR</p>
              <div class="text-lg font-semibold text-white">{{ stats.qrGenerated }} kodów QR</div>
            </div>
          </div>
        </div>

        <!-- Start Line Management -->
        <div @click="navigateTo('start-line')" class="group cursor-pointer transform hover:scale-105 transition-all duration-300">
          <div class="relative overflow-hidden rounded-3xl bg-gradient-to-br from-green-500 to-emerald-600 shadow-xl hover:shadow-2xl">
            <div class="absolute inset-0 bg-black opacity-0 group-hover:opacity-10 transition-opacity duration-300"></div>
            <div class="relative px-8 py-12 text-center">
              <div class="flex items-center justify-center mb-6">
                <svg class="w-16 h-16 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 class="text-xl font-bold text-white mb-1">🏁 Start Line</h3>
              <h3 class="text-xl font-bold text-white mb-1">Response</h3>
              <h3 class="text-xl font-bold text-white mb-3">Management</h3>
              <p class="text-green-100 text-sm mb-4">Centrum startu i skaner</p>
              <div class="text-lg font-semibold text-white">{{ stats.checkedIn }} zameldowanych</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Analytics Row -->
      <div class="mb-8">
        <div @click="navigateTo('rankingi')" class="group cursor-pointer transform hover:scale-105 transition-all duration-300">
          <div class="relative overflow-hidden rounded-3xl bg-gradient-to-r from-orange-500 to-red-600 shadow-xl hover:shadow-2xl">
            <div class="absolute inset-0 bg-black opacity-0 group-hover:opacity-10 transition-opacity duration-300"></div>
            <div class="relative px-8 py-16 text-center">
              <div class="flex items-center justify-center mb-6">
                <svg class="w-16 h-16 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h2 class="text-3xl lg:text-4xl font-bold text-white mb-3">📊 Key Analytics</h2>
              <p class="text-orange-100 text-lg mb-6">Rankingi i statystyki turnieju</p>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <div class="bg-white bg-opacity-20 rounded-lg p-3">
                  <div class="text-xl font-bold">{{ stats.activeCategories }}</div>
                  <div class="text-orange-100">Kategorie</div>
                </div>
                <div class="bg-white bg-opacity-20 rounded-lg p-3">
                  <div class="text-xl font-bold">{{ stats.clubsCount }}</div>
                  <div class="text-orange-100">Kluby</div>
                </div>
                <div class="bg-white bg-opacity-20 rounded-lg p-3">
                  <div class="text-xl font-bold">{{ progressStats.readiness }}%</div>
                  <div class="text-orange-100">Gotowość</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- QR Print System -->
      <div class="mb-8">
        <div @click="navigateTo('qr-print')" class="group cursor-pointer transform hover:scale-105 transition-all duration-300">
          <div class="relative overflow-hidden rounded-3xl bg-gradient-to-r from-yellow-500 to-orange-500 shadow-xl hover:shadow-2xl">
            <div class="absolute inset-0 bg-black opacity-0 group-hover:opacity-10 transition-opacity duration-300"></div>
            <div class="relative px-8 py-16 text-center">
              <div class="flex items-center justify-center mb-6">
                <svg class="w-16 h-16 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z" />
                </svg>
              </div>
              <h2 class="text-2xl lg:text-3xl font-bold text-white mb-3">Building blocks: QR Print System</h2>
              <p class="text-yellow-100 text-lg mb-6">System generowania i druku kodów QR</p>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div class="bg-white bg-opacity-20 rounded-lg p-3">
                  <div class="text-xl font-bold">{{ stats.qrGenerated }}/{{ stats.totalZawodnicy }}</div>
                  <div class="text-yellow-100">QR Generated</div>
                </div>
                <div class="bg-white bg-opacity-20 rounded-lg p-3">
                  <div class="text-xl font-bold">{{ progressStats.qrProgress }}%</div>
                  <div class="text-yellow-100">Coverage</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Activity Feed -->
      <div class="bg-white dark:bg-gray-800 rounded-3xl shadow-xl p-8">
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-xl font-bold text-gray-900 dark:text-white flex items-center">
            <span class="mr-2">📈</span>
            Ostatnia aktywność turnieju
          </h3>
          <button 
            @click="refreshData"
            :disabled="loading"
            class="text-indigo-600 dark:text-indigo-400 hover:text-indigo-700 dark:hover:text-indigo-300 text-sm font-medium disabled:opacity-50 flex items-center"
          >
            <svg v-if="loading" class="animate-spin -ml-1 mr-2 h-4 w-4 text-indigo-600" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="m4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ loading ? 'Ładowanie...' : 'Odśwież' }}
          </button>
        </div>
        
        <div v-if="recentActivities.length > 0" class="space-y-4">
          <div v-for="activity in recentActivities" :key="activity.id" 
               class="flex items-center space-x-4 p-4 bg-gray-50 dark:bg-gray-700 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors duration-200">
            <div :class="['p-2 rounded-lg', activity.color]">
              <span class="text-white text-lg">{{ activity.icon }}</span>
            </div>
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-900 dark:text-white">{{ activity.title }}</p>
              <p class="text-xs text-gray-500 dark:text-gray-400">{{ activity.description }}</p>
            </div>
            <div class="text-xs text-gray-400 dark:text-gray-500">
              {{ activity.time }}
            </div>
          </div>
        </div>
        
        <div v-else class="text-center py-8">
          <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <h3 class="mt-2 text-sm font-medium text-gray-900 dark:text-white">Brak aktywności</h3>
          <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Rozpocznij turniej, aby zobaczyć aktywność</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import EnhancedStatsCard from './EnhancedStatsCard.vue'

// Emits
const emit = defineEmits(['navigate'])

// Data
const stats = ref({
  totalZawodnicy: 0,
  qrGenerated: 0,
  checkedIn: 0,
  activeCategories: 0,
  clubsCount: 0
})

const loading = ref(false)

const recentActivities = ref([
  {
    id: 1,
    title: 'System QR aktywny',
    description: 'Dashboard gotowy do pracy',
    time: 'Teraz',
    icon: '🔲',
    color: 'bg-blue-500'
  }
])

// Computed
const progressStats = computed(() => ({
  qrProgress: stats.value.totalZawodnicy > 0 ? Math.round((stats.value.qrGenerated / stats.value.totalZawodnicy) * 100) : 0,
  checkinProgress: stats.value.totalZawodnicy > 0 ? Math.round((stats.value.checkedIn / stats.value.totalZawodnicy) * 100) : 0,
  readiness: stats.value.totalZawodnicy > 0 ? Math.round(((stats.value.checkedIn + stats.value.qrGenerated) / (stats.value.totalZawodnicy * 2)) * 100) : 0
}))

// Methods
const navigateTo = (section: string) => {
  emit('navigate', section)
}

const loadStats = async () => {
  try {
    loading.value = true
    
    // Pobierz dane wszystkich zawodników (nie tylko 50)
    const zawodnicyResponse = await axios.get('/api/zawodnicy?limit=1000')
    const zawodnicy = zawodnicyResponse.data.data || []
    console.log(`📊 Dashboard: Załadowano ${zawodnicy.length} zawodników`)
    
    // Oblicz statystyki
    stats.value.totalZawodnicy = zawodnicy.length
    stats.value.qrGenerated = zawodnicy.filter((z: any) => z.qr_code).length
    stats.value.checkedIn = zawodnicy.filter((z: any) => z.checked_in).length
    
    // Unikalne kategorie
    const categories = [...new Set(zawodnicy.map((z: any) => z.kategoria).filter(Boolean))]
    stats.value.activeCategories = categories.length
    
    // Unikalne kluby
    const clubs = [...new Set(zawodnicy.map((z: any) => z.klub).filter(Boolean))]
    stats.value.clubsCount = clubs.length
    
    // Aktualizuj aktywności
    updateActivities()
    
  } catch (error) {
    console.error('Błąd ładowania statystyk:', error)
    // Symulacja danych w przypadku błędu
    stats.value = {
      totalZawodnicy: 8,
      qrGenerated: 6,
      checkedIn: 4,
      activeCategories: 4,
      clubsCount: 3
    }
  } finally {
    loading.value = false
  }
}

const updateActivities = () => {
  const activities = []
  
  if (stats.value.totalZawodnicy > 0) {
    activities.push({
      id: Date.now(),
      title: `${stats.value.totalZawodnicy} zawodników zarejestrowanych`,
      description: `${stats.value.activeCategories} kategorii, ${stats.value.clubsCount} klubów`,
      time: '5 min temu',
      icon: '👥',
      color: 'bg-blue-500'
    })
  }
  
  if (stats.value.qrGenerated > 0) {
    activities.push({
      id: Date.now() + 1,
      title: `${stats.value.qrGenerated} kodów QR wygenerowanych`,
      description: `${progressStats.value.qrProgress}% pokrycie QR`,
      time: '10 min temu',
      icon: '🔲',
      color: 'bg-purple-500'
    })
  }
  
  if (stats.value.checkedIn > 0) {
    activities.push({
      id: Date.now() + 2,
      title: `${stats.value.checkedIn} zawodników zameldowanych`,
      description: `${progressStats.value.checkinProgress}% gotowości do startu`,
      time: '15 min temu',
      icon: '✅',
      color: 'bg-green-500'
    })
  }
  
  recentActivities.value = activities
}

const refreshData = () => {
  loadStats()
}

// Lifecycle
onMounted(() => {
  loadStats()
  
  // Auto-refresh co 30 sekund
  setInterval(loadStats, 30000)
})
</script>

<style scoped>
.gradient-bg {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.card-hover {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.card-hover:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}
</style> 