<template>
  <div>
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6 space-y-4 sm:space-y-0">
      <div class="flex items-center space-x-3">
        <ChartBarIcon class="h-8 w-8 text-purple-600 dark:text-purple-400" />
        <h2 class="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">Rankingi SKATECROSS</h2>
      </div>
      <div class="flex items-center space-x-4">
        <select 
          v-model="selectedSeason" 
          class="rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
        >
          <option value="2025">Sezon 2025</option>
          <option value="2024">Sezon 2024</option>
        </select>
        <button 
          @click="refreshRankings"
          :disabled="loading"
          class="inline-flex items-center px-3 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-purple-600 hover:bg-purple-700 disabled:opacity-50"
        >
          <ArrowPathIcon :class="['h-4 w-4 mr-2', loading ? 'animate-spin' : '']" />
          Odśwież
        </button>
      </div>
    </div>

    <!-- Tabs Navigation -->
    <div class="border-b border-gray-200 dark:border-gray-700 mb-6">
      <nav class="-mb-px flex space-x-8 overflow-x-auto">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="[
            'whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm flex items-center space-x-2',
            activeTab === tab.id
              ? 'border-purple-500 text-purple-600 dark:text-purple-400'
              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
          ]"
        >
          <component :is="tab.icon" class="h-5 w-5" />
          <span>{{ tab.name }}</span>
          <span v-if="tab.count" class="ml-2 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 py-0.5 px-2 rounded-full text-xs">
            {{ tab.count }}
          </span>
        </button>
      </nav>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-12">
      <div class="text-center">
        <ArrowPathIcon class="h-8 w-8 text-purple-500 animate-spin mx-auto mb-4" />
        <p class="text-gray-600 dark:text-gray-400">Ładowanie rankingów...</p>
      </div>
    </div>

    <!-- Tab Content -->
    <div v-else>
      <!-- Klasyfikacja Indywidualna -->
      <div v-if="activeTab === 'individual'" class="space-y-6">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">Klasyfikacja Indywidualna</h3>
          <select 
            v-model="selectedCategory" 
            class="rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700"
          >
            <option value="">Wszystkie kategorie</option>
            <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
          </select>
        </div>
        
        <div class="bg-white dark:bg-gray-800 shadow rounded-lg overflow-hidden">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead class="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Pozycja</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Zawodnik</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Klub</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Kategoria</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Punkty</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Zawody</th>
              </tr>
            </thead>
            <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              <tr v-if="filteredIndividualRanking.length === 0">
                <td colspan="6" class="px-6 py-12 text-center text-gray-500 dark:text-gray-400">
                  Brak danych rankingowych dla wybranej kategorii
                </td>
              </tr>
              <tr v-for="(rider, index) in filteredIndividualRanking" :key="rider.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                  <span v-if="index === 0">🥇</span>
                  <span v-else-if="index === 1">🥈</span>
                  <span v-else-if="index === 2">🥉</span>
                  <span v-else>{{ index + 1 }}</span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm font-medium text-gray-900 dark:text-white">{{ rider.imie }} {{ rider.nazwisko }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{{ rider.klub }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{{ rider.kategoria }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-purple-600 dark:text-purple-400">{{ rider.punkty }} pkt</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{{ rider.liczba_zawodow }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Klasyfikacja Generalna -->
      <div v-if="activeTab === 'general'" class="space-y-6">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">Klasyfikacja Generalna (n-2)</h3>
          <div class="text-sm text-gray-600 dark:text-gray-400">
            <span class="font-medium">Zasada n-2:</span> Najlepsze wyniki minus 2 najsłabsze
          </div>
        </div>
        
        <div class="bg-white dark:bg-gray-800 shadow rounded-lg overflow-hidden">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead class="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Pozycja</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Zawodnik</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Kategoria</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Punkty końcowe</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Uczestnictwa</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Odrzucone</th>
              </tr>
            </thead>
            <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              <tr v-if="generalRanking.length === 0">
                <td colspan="6" class="px-6 py-12 text-center text-gray-500 dark:text-gray-400">
                  Brak danych rankingu generalnego
                </td>
              </tr>
              <tr v-for="(rider, index) in generalRanking" :key="rider.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                  <span v-if="index === 0">🏆</span>
                  <span v-else>{{ index + 1 }}</span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm font-medium text-gray-900 dark:text-white">{{ rider.imie }} {{ rider.nazwisko }}</div>
                  <div class="text-sm text-gray-500 dark:text-gray-400">{{ rider.klub }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{{ rider.kategoria }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-green-600 dark:text-green-400">{{ rider.punkty_koncowe }} pkt</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{{ rider.uczestnictwa }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-red-500 dark:text-red-400">{{ rider.odrzucone || 0 }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Klasyfikacja Klubowa - Suma -->
      <div v-if="activeTab === 'clubs-total'" class="space-y-6">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">Klasyfikacja Klubowa - Suma Punktów</h3>
          <div class="text-sm text-gray-600 dark:text-gray-400">
            Wszystkie punkty zawodników klubu
          </div>
        </div>
        
        <div class="bg-white dark:bg-gray-800 shadow rounded-lg overflow-hidden">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead class="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Pozycja</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Klub</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Łączne punkty</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Zawodnicy</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Średnia</th>
              </tr>
            </thead>
            <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              <tr v-if="clubRankingTotal.length === 0">
                <td colspan="5" class="px-6 py-12 text-center text-gray-500 dark:text-gray-400">
                  Brak danych rankingu klubowego
                </td>
              </tr>
              <tr v-for="(club, index) in clubRankingTotal" :key="club.klub" class="hover:bg-gray-50 dark:hover:bg-gray-700">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                  <span v-if="index === 0">🏆</span>
                  <span v-else-if="index === 1">🥈</span>
                  <span v-else-if="index === 2">🥉</span>
                  <span v-else>{{ index + 1 }}</span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">{{ club.klub }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-blue-600 dark:text-blue-400">{{ club.laczne_punkty }} pkt</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{{ club.liczba_zawodnikow }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{{ club.srednia.toFixed(1) }} pkt</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Klasyfikacja Klubowa - Top 3 -->
      <div v-if="activeTab === 'clubs-top3'" class="space-y-6">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">Klasyfikacja Klubowa - Top 3</h3>
          <div class="text-sm text-gray-600 dark:text-gray-400">
            3 najlepszych zawodników z każdej kategorii
          </div>
        </div>
        
        <div class="bg-white dark:bg-gray-800 shadow rounded-lg overflow-hidden">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead class="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Pozycja</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Klub</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Punkty Top 3</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Kategorie</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Balance</th>
              </tr>
            </thead>
            <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              <tr v-if="clubRankingTop3.length === 0">
                <td colspan="5" class="px-6 py-12 text-center text-gray-500 dark:text-gray-400">
                  Brak danych rankingu klubowego Top 3
                </td>
              </tr>
              <tr v-for="(club, index) in clubRankingTop3" :key="club.klub" class="hover:bg-gray-50 dark:hover:bg-gray-700">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">{{ index + 1 }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">{{ club.klub }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-green-600 dark:text-green-400">{{ club.punkty_top3 }} pkt</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{{ club.aktywne_kategorie }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{{ club.balance }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Klasyfikacja Medalowa -->
      <div v-if="activeTab === 'medals'" class="space-y-6">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">Klasyfikacja Medalowa</h3>
          <div class="text-sm text-gray-600 dark:text-gray-400">
            Złote, srebrne i brązowe medale
          </div>
        </div>
        
        <div class="bg-white dark:bg-gray-800 shadow rounded-lg overflow-hidden">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead class="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Pozycja</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Klub</th>
                <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">🥇 Złote</th>
                <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">🥈 Srebrne</th>
                <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">🥉 Brązowe</th>
                <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Łącznie</th>
              </tr>
            </thead>
            <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              <tr v-if="medalRanking.length === 0">
                <td colspan="6" class="px-6 py-12 text-center text-gray-500 dark:text-gray-400">
                  Brak danych medalowych
                </td>
              </tr>
              <tr v-for="(club, index) in medalRanking" :key="club.klub" class="hover:bg-gray-50 dark:hover:bg-gray-700">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">{{ index + 1 }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">{{ club.klub }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-center text-sm font-bold text-yellow-600">{{ club.zlote }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-center text-sm font-bold text-gray-400">{{ club.srebrne }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-center text-sm font-bold text-yellow-700">{{ club.brazowe }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-center text-sm font-bold text-purple-600">{{ club.lacznie }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="!loading && isEmpty" class="text-center py-12">
      <ChartBarIcon class="h-16 w-16 text-gray-300 mx-auto mb-4" />
      <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">Brak danych rankingowych</h3>
      <p class="text-gray-600 dark:text-gray-400 mb-6">
        Rankingi będą dostępne po zakończeniu pierwszych zawodów w sezonie.
      </p>
      <button 
        @click="refreshRankings"
        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-purple-600 hover:bg-purple-700"
      >
        <ArrowPathIcon class="h-4 w-4 mr-2" />
        Sprawdź ponownie
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { 
  ChartBarIcon, 
  TrophyIcon, 
  UsersIcon, 
  BuildingOfficeIcon,
  CalendarIcon,
  ArrowPathIcon,
  StarIcon
} from '@heroicons/vue/24/outline'

// State
const loading = ref(false)
const selectedSeason = ref('2025')
const selectedCategory = ref('')
const activeTab = ref('individual')

// Data
const individualRanking = ref([])
const generalRanking = ref([])
const clubRankingTotal = ref([])
const clubRankingTop3 = ref([])
const medalRanking = ref([])
const categories = ref(['Junior D', 'Junior C', 'Junior B', 'Junior A', 'Senior', 'Master'])

// Tabs configuration
const tabs = computed(() => [
  {
    id: 'individual',
    name: 'Indywidualna',
    icon: UsersIcon,
    count: individualRanking.value.length
  },
  {
    id: 'general',
    name: 'Generalna (n-2)',
    icon: TrophyIcon,
    count: generalRanking.value.length
  },
  {
    id: 'clubs-total',
    name: 'Klubowa - Suma',
    icon: BuildingOfficeIcon,
    count: clubRankingTotal.value.length
  },
  {
    id: 'clubs-top3',
    name: 'Klubowa - Top 3',
    icon: BuildingOfficeIcon,
    count: clubRankingTop3.value.length
  },
  {
    id: 'medals',
    name: 'Medalowa',
    icon: StarIcon,
    count: medalRanking.value.length
  }
])

// Computed
const filteredIndividualRanking = computed(() => {
  if (!selectedCategory.value) return individualRanking.value
  return individualRanking.value.filter(rider => rider.kategoria === selectedCategory.value)
})

const isEmpty = computed(() => {
  return individualRanking.value.length === 0 && 
         generalRanking.value.length === 0 && 
         clubRankingTotal.value.length === 0 && 
         medalRanking.value.length === 0
})

// Methods
const refreshRankings = async () => {
  loading.value = true
  try {
    // Fetch all ranking data from API
    await Promise.all([
      fetchIndividualRanking(),
      fetchGeneralRanking(),
      fetchClubRankings(),
      fetchMedalRanking()
    ])
  } catch (error) {
    console.error('Error fetching rankings:', error)
  } finally {
    loading.value = false
  }
}

const fetchIndividualRanking = async () => {
  try {
    const response = await fetch(`/api/rankings/individual?season=${selectedSeason.value}`)
    if (response.ok) {
      individualRanking.value = await response.json()
    }
  } catch (error) {
    console.log('Individual ranking endpoint not ready yet')
    individualRanking.value = []
  }
}

const fetchGeneralRanking = async () => {
  try {
    const response = await fetch(`/api/rankings/general?season=${selectedSeason.value}`)
    if (response.ok) {
      generalRanking.value = await response.json()
    }
  } catch (error) {
    console.log('General ranking endpoint not ready yet')
    generalRanking.value = []
  }
}

const fetchClubRankings = async () => {
  try {
    const [totalResponse, top3Response] = await Promise.all([
      fetch(`/api/rankings/clubs/total?season=${selectedSeason.value}`),
      fetch(`/api/rankings/clubs/top3?season=${selectedSeason.value}`)
    ])
    
    if (totalResponse.ok) {
      clubRankingTotal.value = await totalResponse.json()
    }
    if (top3Response.ok) {
      clubRankingTop3.value = await top3Response.json()
    }
  } catch (error) {
    console.log('Club rankings endpoints not ready yet')
    clubRankingTotal.value = []
    clubRankingTop3.value = []
  }
}

const fetchMedalRanking = async () => {
  try {
    const response = await fetch(`/api/rankings/medals?season=${selectedSeason.value}`)
    if (response.ok) {
      medalRanking.value = await response.json()
    }
  } catch (error) {
    console.log('Medal ranking endpoint not ready yet')
    medalRanking.value = []
  }
}

// Lifecycle
onMounted(() => {
  refreshRankings()
})
</script>

<style scoped>
/* Custom styles for placeholder */
</style> 