<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
    <!-- Header -->
    <header class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700 transition-colors duration-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- Main Header Row -->
        <div class="flex justify-between items-center h-16">
          <!-- Logo/Brand -->
          <div class="flex items-center flex-shrink-0">
            <h1 class="text-lg sm:text-xl font-semibold text-gray-900 dark:text-white transition-colors duration-200">
              <span class="hidden sm:inline">SKATECROSS Dashboard</span>
              <span class="sm:hidden">SKATECROSS</span>
              <span v-if="isAdmin" class="ml-1 sm:ml-2 inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200">
                🔧
                <span class="hidden sm:inline ml-1">ADMIN</span>
              </span>
            </h1>
          </div>
          
          <!-- Search Bar - Desktop tylko w headerze -->
          <div class="hidden sm:block flex-1 max-w-lg mx-8">
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <MagnifyingGlassIcon class="h-5 w-5 text-gray-400" />
              </div>
              <input 
                type="text" 
                class="block w-full pl-10 pr-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg leading-5 bg-white dark:bg-gray-700 placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white focus:outline-none focus:placeholder-gray-400 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-sm transition-colors duration-200 shadow-sm"
                placeholder="Szukaj zawodników..."
                v-model="searchTerm"
              />
            </div>
          </div>
          
          <!-- Header Icons - Compact on mobile -->
          <div class="flex items-center space-x-2 sm:space-x-4">
            <!-- Admin Toggle - More compact on mobile -->
            <div class="flex items-center space-x-1 sm:space-x-2">
              <label class="text-xs sm:text-sm text-gray-600 dark:text-gray-300 hidden sm:inline">Admin:</label>
              <button
                @click="toggleAdminMode"
                :class="[
                  'relative inline-flex h-5 w-9 sm:h-6 sm:w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2',
                  isAdmin ? 'bg-indigo-600' : 'bg-gray-200 dark:bg-gray-600'
                ]"
              >
                <span
                  :class="[
                    'pointer-events-none inline-block h-4 w-4 sm:h-5 sm:w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                    isAdmin ? 'translate-x-4 sm:translate-x-5' : 'translate-x-0'
                  ]"
                />
              </button>
            </div>
            
            <button class="p-1 sm:p-2 text-gray-400 dark:text-gray-300 hover:text-gray-500 dark:hover:text-gray-200">
              <GlobeAltIcon class="h-5 w-5 sm:h-6 sm:w-6" />
            </button>
            <button 
              @click="toggleDarkMode"
              class="p-1 sm:p-2 text-gray-400 dark:text-gray-300 hover:text-gray-500 dark:hover:text-gray-200 transition-colors duration-200"
              :title="isDarkMode ? 'Przełącz na tryb jasny' : 'Przełącz na tryb ciemny'"
            >
              <SunIcon v-if="isDarkMode" class="h-5 w-5 sm:h-6 sm:w-6" />
              <MoonIcon v-else class="h-5 w-5 sm:h-6 sm:w-6" />
            </button>
            
            <!-- User Avatar -->
            <div class="w-7 h-7 sm:w-8 sm:h-8 bg-indigo-500 rounded-full flex items-center justify-center">
              <span class="text-white text-xs sm:text-sm font-medium">{{ isAdmin ? 'A' : 'U' }}</span>
            </div>
          </div>
        </div>
        
        <!-- Search Bar - Below header on mobile -->
        <div class="pb-4 sm:hidden">
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <MagnifyingGlassIcon class="h-4 w-4 text-gray-400" />
            </div>
            <input 
              type="text" 
              class="block w-full pl-9 pr-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md leading-5 bg-white dark:bg-gray-700 placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 text-sm transition-colors duration-200"
              placeholder="Szukaj zawodników..."
              v-model="searchTerm"
            />
          </div>
        </div>
      </div>
    </header>

    <!-- Navigation Tabs -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="border-b border-gray-200 dark:border-gray-700">
        <nav class="-mb-px flex flex-wrap gap-x-4 gap-y-2 sm:space-x-8 sm:gap-y-0" aria-label="Tabs">
          <button
            v-for="tab in filteredTabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="[
              activeTab === tab.id
                ? 'border-indigo-500 text-indigo-600 dark:text-indigo-400'
                : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:border-gray-300 dark:hover:border-gray-600',
              'whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm transition-colors duration-200 flex items-center'
            ]"
          >
            <component :is="tab.icon" class="h-4 w-4 sm:h-5 sm:w-5 mr-1 sm:mr-2" />
            <span class="text-xs sm:text-sm">{{ tab.name }}</span>
          </button>
        </nav>
      </div>
    </div>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- Lista Zawodników -->
      <div v-if="activeTab === 'zawodnicy'">
        <!-- Header -->
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6 space-y-4 sm:space-y-0">
          <div class="flex items-center space-x-3">
            <ListBulletIcon class="h-8 w-8 text-blue-600" />
            <h2 class="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">Lista zawodników</h2>
          </div>
        </div>
        
        <!-- Stats Cards -->
        <div class="grid grid-cols-2 md:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6 mb-6">
          <StatsCard 
            title="Wszyscy zawodnicy" 
            :value="stats.total"
            :icon="UsersIcon"
            color="blue"
          />
          <StatsCard 
            title="Ukończyli" 
            :value="stats.finished"
            :icon="CheckCircleIcon"
            color="green"
          />
          <StatsCard 
            title="DNF/DSQ" 
            :value="stats.dnfDsq"
            :icon="XCircleIcon"
            color="red"
          />
          <StatsCard 
            title="Rekord toru" 
            :value="stats.recordTime"
            :icon="ClockIcon"
            color="purple"
            :subtitle="stats.recordHolder !== '-' ? `Rekord: ${stats.recordHolder}` : ''"
          />
        </div>

        <!-- Table -->
        <div class="bg-white dark:bg-gray-800 shadow rounded-lg transition-colors duration-200">
          <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
            <!-- Filtry -->
            <div class="space-y-4">
              <!-- Filtr Kluby -->
              <div class="mb-6 border-b border-gray-200 dark:border-gray-700 pb-4">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                  Kluby <span class="text-xs text-gray-500">({{ filters.kluby.length }} wybranych)</span>
                </label>
                <div class="flex flex-wrap gap-2">
                  <button
                    v-for="klub in uniqueKluby"
                    :key="klub"
                    @click="toggleFilter('kluby', klub)"
                    :class="[
                      'px-3 py-2 rounded-full text-sm font-medium transition-colors duration-200',
                      filters.kluby.includes(klub)
                        ? 'bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 border-2 border-blue-300 dark:border-blue-600'
                        : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 border-2 border-transparent hover:bg-gray-200 dark:hover:bg-gray-600'
                    ]"
                  >
                    {{ klub }}
                  </button>
                </div>
              </div>
              <!-- Wrapper filtrów -->
              <div class="border-b border-gray-200 dark:border-gray-700 pb-2 mb-4">
                <!-- Kategorie w jednym rzędzie -->
                <div class="flex flex-col items-start w-full mb-4">
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                    Kategorie <span class="text-xs text-gray-500">({{ filters.kategorie.length }} wybranych)</span>
                  </label>
                  <div class="flex flex-wrap gap-2 w-full">
                    <button
                      v-for="kategoria in uniqueKategorie"
                      :key="kategoria"
                      @click="toggleFilter('kategorie', kategoria)"
                      class="px-4 py-2 rounded-full text-sm font-medium transition-colors duration-200 text-center"
                      :class="[
                        filters.kategorie.includes(kategoria)
                          ? 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 border-2 border-green-300 dark:border-green-600'
                          : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 border-2 border-transparent hover:bg-gray-200 dark:hover:bg-gray-600'
                      ]"
                    >
                      {{ kategoria }}
                    </button>
                  </div>
                </div>
                <!-- Płeć i statusy w jednym rzędzie -->
                <div class="flex flex-wrap gap-2 w-full">
                  <button
                    @click="toggleFilter('plcie', 'M')"
                    class="px-4 py-2 rounded-full text-sm font-medium transition-colors duration-200 text-center"
                    :class="[
                      filters.plcie.includes('M')
                        ? 'bg-indigo-100 dark:bg-indigo-900 text-indigo-800 dark:text-indigo-200 border-2 border-indigo-300 dark:border-indigo-600'
                        : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 border-2 border-transparent hover:bg-gray-200 dark:hover:bg-gray-600'
                    ]"
                  >
                    👨 Mężczyźni
                  </button>
                  <button
                    @click="toggleFilter('plcie', 'K')"
                    class="px-4 py-2 rounded-full text-sm font-medium transition-colors duration-200 text-center"
                    :class="[
                      filters.plcie.includes('K')
                        ? 'bg-pink-100 dark:bg-pink-900 text-pink-800 dark:text-pink-200 border-2 border-pink-300 dark:border-pink-600'
                        : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 border-2 border-transparent hover:bg-gray-200 dark:hover:bg-gray-600'
                    ]"
                  >
                    👩 Kobiety
                  </button>
                  <button
                    @click="toggleFilter('statusy', 'FINISHED')"
                    class="px-4 py-2 rounded-full text-sm font-medium transition-colors duration-200 text-center"
                    :class="[
                      filters.statusy.includes('FINISHED')
                        ? 'bg-emerald-100 dark:bg-emerald-900 text-emerald-800 dark:text-emerald-200 border-2 border-emerald-300 dark:border-emerald-600'
                        : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 border-2 border-transparent hover:bg-gray-200 dark:hover:bg-gray-600'
                    ]"
                  >
                    ✅ Ukończone
                  </button>
                  <button
                    @click="toggleFilter('statusy', 'DNF')"
                    class="px-4 py-2 rounded-full text-sm font-medium transition-colors duration-200 text-center"
                    :class="[
                      filters.statusy.includes('DNF')
                        ? 'bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200 border-2 border-yellow-300 dark:border-yellow-600'
                        : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 border-2 border-transparent hover:bg-gray-200 dark:hover:bg-gray-600'
                    ]"
                  >
                    ⚠️ DNF
                  </button>
                  <button
                    @click="toggleFilter('statusy', 'DSQ')"
                    class="px-4 py-2 rounded-full text-sm font-medium transition-colors duration-200 text-center"
                    :class="[
                      filters.statusy.includes('DSQ')
                        ? 'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200 border-2 border-red-300 dark:border-red-600'
                        : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 border-2 border-transparent hover:bg-gray-200 dark:hover:bg-gray-600'
                    ]"
                  >
                    ❌ DSQ
                  </button>
                </div>
              </div>
            </div>
            
            <!-- Szybkie akcje filtrowania -->
            <div class="flex flex-wrap gap-2 pt-4 border-t border-gray-200 dark:border-gray-700">
              <button 
                @click="selectAllClubs"
                class="px-4 py-2 text-sm bg-blue-500 text-white rounded-full hover:bg-blue-600 transition-colors duration-200"
              >
                Wszystkie kluby
              </button>
              <button 
                @click="selectAllCategories"
                class="px-4 py-2 text-sm bg-green-500 text-white rounded-full hover:bg-green-600 transition-colors duration-200"
              >
                Wszystkie kategorie
              </button>
              <button 
                @click="selectFinishedOnly"
                class="px-4 py-2 text-sm bg-emerald-500 text-white rounded-full hover:bg-emerald-600 transition-colors duration-200"
              >
                Tylko ukończone
              </button>
              <button 
                @click="clearFilters"
                class="px-4 py-2 text-sm bg-gray-500 text-white rounded-full hover:bg-gray-600 transition-colors duration-200"
              >
                🗑️ Wyczyść wszystko
              </button>
            </div>
          </div>
          
          <!-- Card Layout for Mobile -->
          <div class="md:hidden p-4 space-y-4">
            <ZawodnikCard 
              v-for="zawodnik in filteredZawodnicy" 
              :key="zawodnik.nr_startowy"
              :zawodnik="zawodnik"
              :isAdmin="isAdmin"
              @edit="openEditModal"
            />
          </div>
          
          <!-- Table Layout for Desktop -->
          <div class="hidden md:block overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead class="bg-gray-50 dark:bg-gray-700">
                <tr>
                  <th class="px-6 py-3 text-left text-sm font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Nr startowy
                  </th>
                  <th class="px-6 py-3 text-left text-sm font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Klub
                  </th>
                  <th class="px-6 py-3 text-left text-sm font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Zawodnik
                  </th>
                  <th class="px-6 py-3 text-left text-sm font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Kategoria
                  </th>
                  <th class="px-6 py-3 text-left text-sm font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Status
                  </th>
                  <th class="px-6 py-3 text-left text-sm font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Czas
                  </th>
                  <th v-if="isAdmin" class="px-6 py-3 text-left text-sm font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Akcje
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                <tr v-for="zawodnik in filteredZawodnicy" :key="zawodnik.nr_startowy">
                  <td class="px-6 py-4 whitespace-nowrap text-base font-medium text-gray-900 dark:text-white">
                    {{ zawodnik.nr_startowy }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-base text-gray-600 dark:text-gray-300">
                    {{ zawodnik.klub }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-base font-medium text-gray-900 dark:text-white">
                      {{ zawodnik.imie }} {{ zawodnik.nazwisko }}
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-base text-gray-600 dark:text-gray-300">
                    {{ zawodnik.kategoria }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <StatusBadge :status="zawodnik.status" />
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-base font-medium text-gray-900 dark:text-white">
                    {{ zawodnik.czas_przejazdu_s ? formatTime(zawodnik.czas_przejazdu_s) : '-' }}
                  </td>
                  <td v-if="isAdmin" class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div class="flex flex-col space-y-2">
                      <button 
                        @click="openEditModal(zawodnik)"
                        class="inline-flex items-center justify-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 dark:bg-indigo-900 text-indigo-800 dark:text-indigo-200 hover:bg-indigo-200 dark:hover:bg-indigo-800 transition-colors duration-200"
                      >
                        <PencilIcon class="h-3 w-3 mr-1" />
                        Edytuj
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Drabinka Pucharowa -->
      <div v-if="activeTab === 'drabinka'">
        <DrabinkaPucharowa />
      </div>

      <!-- Rankingi -->
      <div v-if="activeTab === 'rankingi'">
        <Rankingi />
      </div>

      <!-- Grupy Startowe -->
      <div v-if="activeTab === 'grupy-startowe'">
        <GrupyStartowe />
      </div>

      <!-- Start Line Scanner -->
      <div v-if="activeTab === 'start-line'">
        <StartLineScanner />
      </div>

      <!-- QR Admin Dashboard -->
      <div v-if="activeTab === 'qr-dashboard'">
        <QrAdminDashboard />
      </div>

      <!-- QR Print -->
      <div v-if="activeTab === 'qr-print'">
        <QrPrint />
      </div>
    </main>

    <!-- Edit Modal -->
    <EditZawodnikModal 
      :show="showEditModal"
      :zawodnik="selectedZawodnik"
      @close="closeEditModal"
      @updated="handleZawodnikUpdated"
      @deleted="handleZawodnikDeleted"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { 
  MagnifyingGlassIcon, 
  GlobeAltIcon, 
  SunIcon, 
  MoonIcon,
  UsersIcon,
  CheckCircleIcon,
  XCircleIcon,
  ClockIcon,
  TrophyIcon,
  ChartBarIcon,
  ListBulletIcon,
  PencilIcon,
  TrashIcon,
  PlusIcon,
  QrCodeIcon,
  ArrowPathIcon,
  ArrowDownTrayIcon,
  DevicePhoneMobileIcon,
  ExclamationTriangleIcon,
  WrenchScrewdriverIcon,
  DocumentTextIcon,
  UserGroupIcon,
  PrinterIcon
} from '@heroicons/vue/24/outline'
import StatsCard from './components/StatsCard.vue'
import StatusBadge from './components/StatusBadge.vue'
import ZawodnikCard from './components/ZawodnikCard.vue'
import DrabinkaPucharowa from './components/DrabinkaPucharowa.vue'
import EditZawodnikModal from './components/EditZawodnikModal.vue'
import Rankingi from './components/Rankingi.vue'
import QrAdminDashboard from './components/QrAdminDashboard.vue'
import QrPrint from './components/QrPrint.vue'
import GrupyStartowe from './components/GrupyStartowe.vue'
import StartLineScanner from './components/StartLineScanner.vue'

// Types
interface Zawodnik {
  nr_startowy: number
  imie: string
  nazwisko: string
  kategoria: string
  plec: string
  klub: string
  czas_przejazdu_s: number | null
  status: string
}

interface Stats {
  total: number
  finished: number
  dnfDsq: number
  recordTime: string
  recordHolder: string
}

// Reactive variables
const zawodnicy = ref<Zawodnik[]>([])
const searchTerm = ref('')
const isAdmin = ref(false)
const isDarkMode = ref(false)
const loading = ref(true)
const error = ref<string | null>(null)
const showEditModal = ref(false)
const selectedZawodnik = ref<Zawodnik | null>(null)
const activeTab = ref('zawodnicy')
const filters = ref({
  kluby: [],
  kategorie: [],
  plcie: [],
  statusy: []
})

// Tabs configuration
const tabs = [
  { id: 'zawodnicy', name: 'Zawodnicy', icon: UsersIcon, adminOnly: false },
  { id: 'drabinka', name: 'Drabinka', icon: TrophyIcon, adminOnly: false },
  { id: 'rankingi', name: 'Rankingi', icon: ListBulletIcon, adminOnly: false },
  { id: 'grupy-startowe', name: 'Grupy Startowe', icon: UsersIcon, adminOnly: true },
  { id: 'start-line', name: 'Linia Startu', icon: QrCodeIcon, adminOnly: true },
  { id: 'qr-print', name: 'Drukowanie QR', icon: PrinterIcon, adminOnly: true },
  { id: 'qr-dashboard', name: 'QR Dashboard', icon: QrCodeIcon, adminOnly: true }
]

// Computed
const filteredZawodnicy = computed(() => {
  let result = zawodnicy.value
  
  // Filtrowanie tekstowe
  if (searchTerm.value) {
    const term = searchTerm.value.toLowerCase()
    result = result.filter(z => 
      z.imie.toLowerCase().includes(term) ||
      z.nazwisko.toLowerCase().includes(term) ||
      z.kategoria.toLowerCase().includes(term) ||
      z.nr_startowy.toString().includes(term) ||
      z.klub.toLowerCase().includes(term)
    )
  }
  
  // Filtrowanie po klubie
  if (filters.value.kluby.length > 0) {
    result = result.filter(z => filters.value.kluby.includes(z.klub))
  }
  
  // Filtrowanie po kategorii
  if (filters.value.kategorie.length > 0) {
    result = result.filter(z => filters.value.kategorie.includes(z.kategoria))
  }
  
  // Filtrowanie po płci
  if (filters.value.plcie.length > 0) {
    result = result.filter(z => filters.value.plcie.includes(z.plec))
  }
  
  // Filtrowanie po statusie
  if (filters.value.statusy.length > 0) {
    result = result.filter(z => filters.value.statusy.includes(z.status))
  }
  
  return result
})

const stats = computed((): Stats => {
  const total = zawodnicy.value.length
  const finished = zawodnicy.value.filter(z => z.status === 'FINISHED').length
  const dnfDsq = zawodnicy.value.filter(z => z.status === 'DNF' || z.status === 'DSQ').length
  
  const finishedContestants = zawodnicy.value.filter(z => z.status === 'FINISHED' && z.czas_przejazdu_s)
  
  let recordTime = '-'
  let recordHolder = '-'
  
  if (finishedContestants.length > 0) {
    const bestContestant = finishedContestants.reduce((best, current) => 
      current.czas_przejazdu_s! < best.czas_przejazdu_s! ? current : best
    )
    recordTime = formatTime(bestContestant.czas_przejazdu_s!)
    recordHolder = `${bestContestant.imie} ${bestContestant.nazwisko}`
  }

  return { total, finished, dnfDsq, recordTime, recordHolder }
})

const uniqueKluby = computed(() => {
  return [...new Set(zawodnicy.value.map(z => z.klub))]
})

const uniqueKategorie = computed(() => {
  return [...new Set(zawodnicy.value.map(z => z.kategoria))]
})

const filteredTabs = computed(() => {
  return tabs.filter(tab => !tab.adminOnly || isAdmin.value)
})

// Methods
const formatTime = (seconds: number): string => {
  const mins = Math.floor(seconds / 60)
  const secs = (seconds % 60).toFixed(2)
  return `${mins}:${secs.padStart(5, '0')}`
}

const fetchZawodnicy = async () => {
  try {
    loading.value = true
    const response = await axios.get<Zawodnik[]>('/api/zawodnicy')
    zawodnicy.value = response.data
  } catch (error) {
    console.error('Błąd podczas pobierania zawodników:', error)
  } finally {
    loading.value = false
  }
}

const clearFilters = () => {
  filters.value = {
    kluby: [],
    kategorie: [],
    plcie: [],
    statusy: []
  }
}

const selectAllClubs = () => {
  filters.value.kluby = [...uniqueKluby.value]
}

const selectAllCategories = () => {
  filters.value.kategorie = [...uniqueKategorie.value]
}

const selectFinishedOnly = () => {
  filters.value.statusy = ['FINISHED']
}

const toggleFilter = (filterType: keyof typeof filters.value, value: string) => {
  const currentFilter = filters.value[filterType]
  if (currentFilter.includes(value)) {
    filters.value[filterType] = currentFilter.filter(v => v !== value)
  } else {
    filters.value[filterType] = [...currentFilter, value]
  }
}

const toggleAdminMode = () => {
  isAdmin.value = !isAdmin.value
}

const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value
  // Aplikuj dark mode do dokumentu
  if (isDarkMode.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}

// Modal functions
const openEditModal = (zawodnik: Zawodnik) => {
  selectedZawodnik.value = zawodnik
  showEditModal.value = true
}

const closeEditModal = () => {
  showEditModal.value = false
  selectedZawodnik.value = null
}

const handleZawodnikUpdated = () => {
  // Refresh data after update
  fetchZawodnicy()
}

const handleZawodnikDeleted = () => {
  // Refresh data after delete
  fetchZawodnicy()
}

const openAddModal = () => {
  selectedZawodnik.value = null
  showEditModal.value = true
}

// Lifecycle
onMounted(() => {
  fetchZawodnicy()
})
</script>

<style>
/* Custom styles if needed */
</style>

