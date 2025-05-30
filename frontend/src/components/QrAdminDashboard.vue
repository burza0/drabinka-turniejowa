<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
      <div class="flex justify-between items-center mb-4">
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white flex items-center">
          <QrCodeIcon class="h-8 w-8 mr-3 text-indigo-600" />
          QR Admin Dashboard
        </h1>
        <div class="flex space-x-2">
          <button
            @click="refreshData"
            :disabled="loading"
            class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 flex items-center"
          >
            <ArrowPathIcon class="h-4 w-4 mr-2" :class="{ 'animate-spin': loading }" />
            Odśwież
          </button>
          <button
            @click="exportData"
            class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 flex items-center"
          >
            <ArrowDownTrayIcon class="h-4 w-4 mr-2" />
            Eksport CSV
          </button>
        </div>
      </div>
      
      <!-- Quick Status -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
          <div class="text-2xl font-bold text-blue-600 dark:text-blue-400">
            {{ basicStats.total_zawodnikow || 0 }}
          </div>
          <div class="text-sm text-blue-700 dark:text-blue-300">Wszyscy zawodnicy</div>
        </div>
        <div class="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg">
          <div class="text-2xl font-bold text-green-600 dark:text-green-400">
            {{ basicStats.z_qr_kodami || 0 }}
          </div>
          <div class="text-sm text-green-700 dark:text-green-300">Z QR kodami</div>
        </div>
        <div class="bg-orange-50 dark:bg-orange-900/20 p-4 rounded-lg">
          <div class="text-2xl font-bold text-orange-600 dark:text-orange-400">
            {{ basicStats.zameldowanych || 0 }}
          </div>
          <div class="text-sm text-orange-700 dark:text-orange-300">Zameldowanych</div>
        </div>
        <div class="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg">
          <div class="text-2xl font-bold text-purple-600 dark:text-purple-400">
            {{ basicStats.procent_zameldowanych || 0 }}%
          </div>
          <div class="text-sm text-purple-700 dark:text-purple-300">% zameldowanych</div>
        </div>
      </div>
    </div>

    <!-- Warnings/Issues -->
    <div v-if="issues.length > 0" class="bg-yellow-50 dark:bg-yellow-900/20 border-l-4 border-yellow-400 p-4 rounded-lg">
      <div class="flex">
        <ExclamationTriangleIcon class="h-5 w-5 text-yellow-400" />
        <div class="ml-3">
          <h3 class="text-sm font-medium text-yellow-800 dark:text-yellow-200">
            Wykryto problemy ({{ issues.length }})
          </h3>
          <div class="mt-2 text-sm text-yellow-700 dark:text-yellow-300">
            <ul class="list-disc list-inside space-y-1">
              <li v-for="issue in issues" :key="issue.type">
                {{ issue.title }}: {{ issue.count }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Live Feed -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Recent Activity -->
      <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
        <h2 class="text-lg font-medium text-gray-900 dark:text-white mb-4 flex items-center">
          <ClockIcon class="h-5 w-5 mr-2 text-gray-500" />
          Ostatnia aktywność
          <span class="ml-2 text-xs bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded-full">
            {{ recentCheckpoints.length }}
          </span>
        </h2>
        <div class="space-y-3 max-h-80 overflow-y-auto">
          <div 
            v-for="checkpoint in recentCheckpoints.slice(0, 10)" 
            :key="`${checkpoint.nr_startowy}-${checkpoint.scan_time}`"
            class="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg"
          >
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-indigo-100 dark:bg-indigo-900 rounded-full flex items-center justify-center">
                <span class="text-sm font-medium text-indigo-600 dark:text-indigo-400">
                  {{ checkpoint.nr_startowy }}
                </span>
              </div>
              <div>
                <div class="text-sm font-medium text-gray-900 dark:text-white">
                  {{ checkpoint.imie }} {{ checkpoint.nazwisko }}
                </div>
                <div class="text-xs text-gray-500 dark:text-gray-400">
                  {{ checkpoint.kategoria }} • {{ formatCheckpointName(checkpoint.checkpoint_name) }}
                </div>
              </div>
            </div>
            <div class="text-right">
              <div class="text-xs text-gray-500 dark:text-gray-400">
                {{ formatTime(checkpoint.scan_time) }}
              </div>
              <div class="text-xs text-gray-400 dark:text-gray-500">
                {{ checkpoint.device_id }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Active Devices -->
      <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
        <h2 class="text-lg font-medium text-gray-900 dark:text-white mb-4 flex items-center">
          <DevicePhoneMobileIcon class="h-5 w-5 mr-2 text-gray-500" />
          Aktywne urządzenia
          <span class="ml-2 text-xs bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded-full">
            {{ deviceActivity.length }}
          </span>
        </h2>
        <div class="space-y-3">
          <div 
            v-for="device in deviceActivity" 
            :key="device.device_id"
            class="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg"
          >
            <div class="flex items-center space-x-3">
              <div class="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
              <div>
                <div class="text-sm font-medium text-gray-900 dark:text-white">
                  {{ device.device_id }}
                </div>
                <div class="text-xs text-gray-500 dark:text-gray-400">
                  {{ device.total_scans }} skanów • {{ device.unique_zawodnicy }} zawodników
                </div>
              </div>
            </div>
            <div class="text-right">
              <div class="text-xs text-gray-500 dark:text-gray-400">
                {{ formatTime(device.last_activity) }}
              </div>
              <div class="flex space-x-1 text-xs">
                <span class="bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-2 py-1 rounded">
                  {{ device.check_ins }} check-in
                </span>
                <span class="bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 px-2 py-1 rounded">
                  {{ device.results }} wyniki
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Category Statistics -->
    <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
      <h2 class="text-lg font-medium text-gray-900 dark:text-white mb-4 flex items-center">
        <ChartBarIcon class="h-5 w-5 mr-2 text-gray-500" />
        Statystyki według kategorii
      </h2>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead class="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Kategoria
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Łącznie
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Zameldowanych
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Z wynikami
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Postęp
              </th>
            </tr>
          </thead>
          <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-for="category in categoryStats" :key="category.kategoria">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                {{ category.kategoria }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                {{ category.total }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                {{ category.zameldowanych }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                {{ category.z_wynikami }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="w-16 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div 
                      class="bg-indigo-600 h-2 rounded-full transition-all duration-300"
                      :style="{ width: `${Math.round((category.z_wynikami / category.total) * 100)}%` }"
                    ></div>
                  </div>
                  <span class="ml-2 text-sm text-gray-500 dark:text-gray-300">
                    {{ Math.round((category.z_wynikami / category.total) * 100) }}%
                  </span>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Hourly Progress Chart -->
    <div v-if="hourlyProgress.length > 0" class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
      <h2 class="text-lg font-medium text-gray-900 dark:text-white mb-4 flex items-center">
        <ChartBarIcon class="h-5 w-5 mr-2 text-gray-500" />
        Postęp w ciągu dnia
      </h2>
      <div class="space-y-2">
        <div 
          v-for="hour in hourlyProgress" 
          :key="hour.hour"
          class="flex items-center space-x-4"
        >
          <div class="text-sm font-medium text-gray-600 dark:text-gray-300 w-20">
            {{ formatHour(hour.hour) }}
          </div>
          <div class="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-4 relative">
            <div 
              class="bg-blue-500 h-full rounded-full transition-all duration-300"
              :style="{ width: `${Math.min((hour.check_ins / maxHourlyActivity) * 100, 100)}%` }"
            ></div>
            <div 
              class="bg-green-500 h-full rounded-full absolute top-0 transition-all duration-300"
              :style="{ 
                width: `${Math.min((hour.results / maxHourlyActivity) * 100, 100)}%`,
                left: `${Math.min((hour.check_ins / maxHourlyActivity) * 100, 100)}%`
              }"
            ></div>
          </div>
          <div class="text-sm text-gray-500 dark:text-gray-400 w-24 text-right">
            {{ hour.check_ins }} / {{ hour.results }}
          </div>
        </div>
      </div>
      <div class="flex items-center space-x-4 mt-4 text-xs text-gray-500">
        <div class="flex items-center">
          <div class="w-3 h-3 bg-blue-500 rounded-full mr-2"></div>
          Check-ins
        </div>
        <div class="flex items-center">
          <div class="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
          Wyniki
        </div>
      </div>
    </div>

    <!-- Działania diagnostyczne -->
    <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
      <h2 class="text-lg font-medium text-gray-900 dark:text-white mb-4 flex items-center">
        <WrenchScrewdriverIcon class="h-5 w-5 mr-2 text-gray-500" />
        Narzędzia diagnostyczne
      </h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <button
          @click="generateMissingQR"
          class="p-4 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg hover:border-indigo-400 transition-colors"
        >
          <QrCodeIcon class="h-8 w-8 mx-auto text-gray-400 mb-2" />
          <div class="text-sm font-medium text-gray-600 dark:text-gray-300">
            Generuj brakujące QR
          </div>
          <div class="text-xs text-gray-500">
            {{ basicStats.bez_qr_kodow }} zawodników
          </div>
        </button>
        
        <button
          @click="resetAllCheckIns"
          class="p-4 border-2 border-dashed border-red-300 dark:border-red-600 rounded-lg hover:border-red-400 transition-colors"
        >
          <ArrowPathIcon class="h-8 w-8 mx-auto text-red-400 mb-2" />
          <div class="text-sm font-medium text-red-600 dark:text-red-300">
            Reset check-inów
          </div>
          <div class="text-xs text-red-500">
            Usuń wszystkie meldunki
          </div>
        </button>
        
        <button
          @click="viewSystemLogs"
          class="p-4 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg hover:border-indigo-400 transition-colors"
        >
          <DocumentTextIcon class="h-8 w-8 mx-auto text-gray-400 mb-2" />
          <div class="text-sm font-medium text-gray-600 dark:text-gray-300">
            Logi systemu
          </div>
          <div class="text-xs text-gray-500">
            Ostatnie wydarzenia
          </div>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
import {
  QrCodeIcon,
  ArrowPathIcon,
  ArrowDownTrayIcon,
  ClockIcon,
  DevicePhoneMobileIcon,
  ChartBarIcon,
  ExclamationTriangleIcon,
  WrenchScrewdriverIcon,
  DocumentTextIcon
} from '@heroicons/vue/24/outline'

// Types
interface BasicStats {
  total_zawodnikow: number
  z_qr_kodami: number
  zameldowanych: number
  bez_qr_kodow: number
  procent_zameldowanych: number
}

interface RecentCheckpoint {
  nr_startowy: number
  imie: string
  nazwisko: string
  kategoria: string
  checkpoint_name: string
  scan_time: string
  device_id: string
}

interface DeviceActivity {
  device_id: string
  total_scans: number
  last_activity: string
  unique_zawodnicy: number
  check_ins: number
  results: number
}

interface CategoryStats {
  kategoria: string
  total: number
  zameldowanych: number
  z_wynikami: number
}

interface HourlyProgress {
  hour: string
  scans: number
  check_ins: number
  results: number
}

interface Issue {
  type: string
  title: string
  count: number
  details: any[]
}

// Reactive state
const loading = ref(false)
const basicStats = ref<BasicStats>({
  total_zawodnikow: 0,
  z_qr_kodami: 0,
  zameldowanych: 0,
  bez_qr_kodow: 0,
  procent_zameldowanych: 0
})
const recentCheckpoints = ref<RecentCheckpoint[]>([])
const deviceActivity = ref<DeviceActivity[]>([])
const categoryStats = ref<CategoryStats[]>([])
const hourlyProgress = ref<HourlyProgress[]>([])
const issues = ref<Issue[]>([])

// Auto refresh interval
let refreshInterval: NodeJS.Timeout | null = null

// Computed
const maxHourlyActivity = computed(() => {
  if (hourlyProgress.value.length === 0) return 1
  return Math.max(...hourlyProgress.value.map(h => Math.max(h.check_ins, h.results)))
})

// Methods
const fetchDashboardData = async () => {
  try {
    loading.value = true
    const response = await axios.get('/api/qr/dashboard')
    
    if (response.data.success) {
      basicStats.value = response.data.basic_stats
      recentCheckpoints.value = response.data.recent_checkpoints
      deviceActivity.value = response.data.device_activity
      categoryStats.value = response.data.category_stats
      hourlyProgress.value = response.data.hourly_progress
      issues.value = response.data.issues
    }
  } catch (error) {
    console.error('Błąd podczas pobierania danych dashboard:', error)
  } finally {
    loading.value = false
  }
}

const refreshData = () => {
  fetchDashboardData()
}

const exportData = async () => {
  try {
    window.open('/api/qr/export', '_blank')
  } catch (error) {
    console.error('Błąd podczas eksportu:', error)
  }
}

const generateMissingQR = async () => {
  // TODO: Implement bulk QR generation
  alert('Funkcja w przygotowaniu')
}

const resetAllCheckIns = async () => {
  if (confirm('Czy na pewno chcesz zresetować wszystkie check-iny? Ta operacja jest nieodwracalna.')) {
    // TODO: Implement reset
    alert('Funkcja w przygotowaniu')
  }
}

const viewSystemLogs = () => {
  // TODO: Implement system logs viewer
  alert('Funkcja w przygotowaniu')
}

const formatTime = (timeString: string) => {
  const date = new Date(timeString)
  return date.toLocaleTimeString('pl-PL', { 
    hour: '2-digit', 
    minute: '2-digit',
    second: '2-digit'
  })
}

const formatHour = (hourString: string) => {
  const date = new Date(hourString)
  return date.toLocaleTimeString('pl-PL', { 
    hour: '2-digit', 
    minute: '2-digit'
  })
}

const formatCheckpointName = (name: string) => {
  const names: Record<string, string> = {
    'check-in': 'Zameldowanie',
    'finish': 'Meta',
    'verify': 'Weryfikacja'
  }
  return names[name] || name
}

// Lifecycle
onMounted(() => {
  fetchDashboardData()
  // Auto refresh every 10 seconds
  refreshInterval = setInterval(fetchDashboardData, 10000)
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})
</script> 