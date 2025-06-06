<template>
  <div class="space-y-6">
    <!-- Debug info -->
    <div class="bg-yellow-100 p-4 rounded mb-4 text-sm">
      <strong>🐛 Debug Info:</strong><br>
      Loading: {{ loading }}<br>
      Error: {{ error }}<br>
      Drabinka exists: {{ !!drabinka }}<br>
      Drabinka keys: {{ drabinka ? Object.keys(drabinka).join(', ') : 'brak' }}<br>
      Filtered keys: {{ Object.keys(filteredKategorieData).join(', ') }}
    </div>

    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6 space-y-4 sm:space-y-0">
      <div class="flex items-center space-x-3">
        <TrophyIcon class="h-8 w-8 text-yellow-600" />
        <h2 class="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">Drabinka Pucharowa SKATECROSS</h2>
      </div>
      <p class="text-sm text-gray-600 dark:text-gray-400">
        System turniejowy z grupami 4-osobowymi - do ćwierćfinałów awansuje maksymalnie 16 najlepszych zawodników
      </p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center h-64">
      <div class="animate-spin rounded-full h-32 w-32 border-b-2 border-indigo-500"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-50 border border-red-200 rounded-md p-4">
      <div class="flex">
        <ExclamationTriangleIcon class="h-5 w-5 text-red-400" />
        <div class="ml-3">
          <h3 class="text-sm font-medium text-red-800">Błąd ładowania drabinki</h3>
          <p class="mt-2 text-sm text-red-700">{{ error }}</p>
        </div>
      </div>
    </div>

    <!-- Drabinka Content -->
    <div v-else>
      <!-- Stats Cards -->
      <div class="grid grid-cols-2 md:grid-cols-2 lg:grid-cols-4 gap-4 lg:gap-6 mb-6">
        <StatsCard 
          title="Zawodnicy w turnieju" 
          :value="drabinka.podsumowanie?.łączna_liczba_zawodników || 0"
          :icon="UsersIcon"
          color="blue"
        />
        <StatsCard 
          title="W ćwierćfinałach" 
          :value="drabinka.podsumowanie?.w_ćwierćfinałach || 0"
          :icon="TrophyIcon"
          color="green"
        />
        <StatsCard 
          title="Mężczyźni" 
          :value="drabinka.podsumowanie?.podział_płeć?.mężczyźni || 0"
          :icon="UserIcon"
          color="purple"
        />
        <StatsCard 
          title="Kobiety" 
          :value="drabinka.podsumowanie?.podział_płeć?.kobiety || 0"
          :icon="UserIcon"
          color="red"
        />
      </div>

      <!-- Filtry i sortowanie -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-6 transition-colors duration-200 mb-6">
        <!-- Nagłówek sekcji -->
        <div class="flex items-center justify-between mb-6">
          <h3 class="text-lg sm:text-xl font-semibold text-gray-900 dark:text-white">Filtry i sortowanie</h3>
          <button 
            @click="clearAllFilters" 
            class="text-sm text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300 flex items-center space-x-1 transition-colors duration-200"
          >
            <span>🗑️</span>
            <span>Wyczyść filtry</span>
          </button>
        </div>

        <!-- Filtry w grid layout -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <!-- Filtr kategorii -->
          <div>
            <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
              <span class="flex items-center space-x-2">
                <span>🏆</span>
                <span>Kategoria</span>
              </span>
            </label>
            <select 
              v-model="drabinkaFilters.kategoria" 
              class="w-full rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-md focus:border-purple-500 focus:ring-2 focus:ring-purple-500 text-sm font-medium py-2.5 px-3 transition-all duration-200 hover:shadow-lg"
            >
              <option value="">Wszystkie</option>
              <option v-for="kategoria in uniqueKategorie" :key="kategoria" :value="kategoria">{{ kategoria }}</option>
            </select>
          </div>
          
          <!-- Filtr płci -->
          <div>
            <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
              <span class="flex items-center space-x-2">
                <span>👥</span>
                <span>Płeć</span>
              </span>
            </label>
            <select 
              v-model="drabinkaFilters.plec" 
              class="w-full rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-md focus:border-purple-500 focus:ring-2 focus:ring-purple-500 text-sm font-medium py-2.5 px-3 transition-all duration-200 hover:shadow-lg"
            >
              <option value="">Wszystkie</option>
              <option value="Mężczyźni">Mężczyźni</option>
              <option value="Kobiety">Kobiety</option>
            </select>
          </div>

          <!-- Filtr fazy turnieju -->
          <div>
            <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
              <span class="flex items-center space-x-2">
                <span>🎯</span>
                <span>Faza turnieju</span>
              </span>
            </label>
            <select 
              v-model="drabinkaFilters.faza" 
              class="w-full rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-md focus:border-purple-500 focus:ring-2 focus:ring-purple-500 text-sm font-medium py-2.5 px-3 transition-all duration-200 hover:shadow-lg"
            >
              <option value="">Wszystkie fazy</option>
              <option value="ćwierćfinały">Ćwierćfinały</option>
              <option value="półfinały">Półfinały</option>
              <option value="finał">Finał</option>
            </select>
          </div>
          
          <!-- Sortowanie -->
          <div>
            <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
              <span class="flex items-center space-x-2">
                <span>🔄</span>
                <span>Sortowanie</span>
              </span>
            </label>
            <select 
              v-model="drabinkaFilters.sortowanie" 
              class="w-full rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-md focus:border-purple-500 focus:ring-2 focus:ring-purple-500 text-sm font-medium py-2.5 px-3 transition-all duration-200 hover:shadow-lg"
            >
              <option value="kategoria_asc">Kategoria (A-Z)</option>
              <option value="kategoria_desc">Kategoria (Z-A)</option>
              <option value="zawodnikow_desc">Liczba zawodników (malejąco)</option>
              <option value="zawodnikow_asc">Liczba zawodników (rosnąco)</option>
            </select>
          </div>
        </div>

        <!-- Operacje grupowe -->
        <div class="border-t border-gray-200 dark:border-gray-700 pt-4">
          <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-3">
            <span class="flex items-center space-x-2">
              <span>⚡</span>
              <span>Operacje grupowe</span>
            </span>
          </label>
          <div class="flex flex-wrap gap-3">
            <button 
              @click="toggleAllCategories"
              :class="[
                'px-4 py-2 text-sm font-medium rounded-lg transition-all duration-200 flex items-center space-x-2 border-2',
                allCategoriesSelected 
                  ? 'bg-indigo-700 text-white shadow-inner border-indigo-800' 
                  : 'bg-indigo-600 text-white hover:bg-indigo-700 border-transparent'
              ]"
            >
              <span>{{ allCategoriesSelected ? '✅' : '☐' }}</span>
              <span>{{ allCategoriesSelected ? 'Odznacz wszystkie' : 'Zaznacz wszystkie' }} kategorie ({{ uniqueKategorie.length }})</span>
            </button>
            
            <button 
              @click="toggleGenders"
              :class="[
                'px-4 py-2 text-sm font-medium rounded-lg transition-all duration-200 flex items-center space-x-2 border-2',
                bothGendersSelected 
                  ? 'bg-green-700 text-white shadow-inner border-green-800'
                  : 'bg-green-600 text-white hover:bg-green-700 border-transparent'
              ]"
            >
              <span>{{ bothGendersSelected ? '✅' : '☐' }}</span>
              <span>{{ bothGendersSelected ? 'Tylko jedna płeć' : 'Obie płcie' }}</span>
            </button>
            
            <button 
              @click="showFinalsOnly"
              :class="[
                'px-4 py-2 text-sm font-medium rounded-lg transition-all duration-200 flex items-center space-x-2 border-2',
                drabinkaFilters.faza === 'finał'
                  ? 'bg-yellow-700 text-white shadow-inner border-yellow-800'
                  : 'bg-yellow-600 text-white hover:bg-yellow-700 border-transparent'
              ]"
            >
              <span>🏆</span>
              <span>{{ drabinkaFilters.faza === 'finał' ? 'Pokaż wszystkie' : 'Tylko finały' }}</span>
            </button>
            
            <button 
              @click="clearAllFilters"
              class="px-4 py-2 text-sm font-medium rounded-lg transition-all duration-200 flex items-center space-x-2 border-2 border-transparent bg-gray-600 text-white hover:bg-gray-700"
            >
              <span>🗑️</span>
              <span>Wyczyść filtry</span>
            </button>
          </div>
        </div>

        <!-- Statystyki filtrów -->
        <div class="mt-4 flex justify-between items-center text-sm text-gray-500 dark:text-gray-400 border-t border-gray-200 dark:border-gray-700 pt-4">
          <div>
            Wyświetlane kategorie: {{ Object.keys(filteredKategorieData).length }} z {{ Object.keys(kategorieData).length }}
          </div>
          <div>
            Łączna liczba zawodników: {{ totalContestants }}
          </div>
        </div>
      </div>

      <!-- Kategorie -->
      <div class="space-y-8">
        <div v-for="(kategoria, kategoriaName) in filteredKategorieData" :key="kategoriaName" class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
          <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-6">🏆 {{ kategoriaName }}</h3>
          
          <!-- Płcie w kategorii -->
          <div class="space-y-8">
            <div v-for="(plecData, plecName) in kategoria" :key="plecName" 
                 v-show="selectedPlcie.length === 0 || selectedPlcie.includes(String(plecName)) || drabinkaFilters.plec === '' || drabinkaFilters.plec === String(plecName)"
                 class="border-l-4 border-indigo-500 pl-4">
              <h4 class="text-lg font-medium text-gray-800 dark:text-gray-200 mb-4">{{ String(plecName) === 'Mężczyźni' ? '👨 Mężczyźni' : '👩 Kobiety' }}</h4>
              
              <!-- Statystyki -->
              <div v-if="plecData.statystyki" class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4 mb-4">
                <div class="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <span class="font-medium text-gray-700 dark:text-gray-300">Łącznie:</span>
                    <span class="ml-1 text-gray-900 dark:text-white">{{ plecData.statystyki.łącznie_zawodników }}</span>
                  </div>
                  <div>
                    <span class="font-medium text-gray-700 dark:text-gray-300">W ćwierćfinałach:</span>
                    <span class="ml-1 text-gray-900 dark:text-white">{{ plecData.statystyki.w_ćwierćfinałach }}</span>
                  </div>
                </div>
              </div>

              <!-- Ćwierćfinały -->
              <div v-if="plecData.ćwierćfinały?.length > 0 && (!drabinkaFilters.faza || drabinkaFilters.faza === 'ćwierćfinały')" class="mb-6">
                <h5 class="font-medium text-gray-700 dark:text-gray-300 mb-3">🥇 Ćwierćfinały</h5>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  <div v-for="grupa in plecData.ćwierćfinały" :key="grupa.grupa" class="border border-gray-200 dark:border-gray-600 rounded-lg p-3">
                    <div class="text-xs font-medium text-gray-500 dark:text-gray-400 mb-2">Grupa {{ grupa.grupa }} (awansuje {{ grupa.awansują }})</div>
                    <div class="space-y-1">
                      <div v-for="(zawodnik, index) in grupa.zawodnicy" :key="zawodnik.nr_startowy" 
                           :class="[
                             'text-sm p-2 rounded',
                             index < grupa.awansują ? 'bg-green-50 dark:bg-green-900/20 text-green-800 dark:text-green-200 font-medium' : 'bg-gray-50 dark:bg-gray-700 text-gray-600 dark:text-gray-300'
                           ]">
                        {{ zawodnik.nr_startowy }}. {{ zawodnik.imie }} {{ zawodnik.nazwisko }}
                        <div class="text-xs">{{ formatTime(zawodnik.czas_przejazdu_s) }}</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Półfinały -->
              <div v-if="plecData.półfinały?.length > 0 && (!drabinkaFilters.faza || drabinkaFilters.faza === 'półfinały')" class="mb-6">
                <h5 class="font-medium text-gray-700 dark:text-gray-300 mb-3">🥈 Półfinały</h5>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div v-for="grupa in plecData.półfinały" :key="grupa.grupa" class="border border-gray-200 dark:border-gray-600 rounded-lg p-3">
                    <div class="text-xs font-medium text-gray-500 dark:text-gray-400 mb-2">Grupa {{ grupa.grupa }} (awansuje {{ grupa.awansują }})</div>
                    <div class="space-y-1">
                      <div v-for="(zawodnik, index) in grupa.zawodnicy" :key="zawodnik.nr_startowy" 
                           :class="[
                             'text-sm p-2 rounded',
                             index < grupa.awansują ? 'bg-yellow-50 dark:bg-yellow-900/20 text-yellow-800 dark:text-yellow-200 font-medium' : 'bg-gray-50 dark:bg-gray-700 text-gray-600 dark:text-gray-300'
                           ]">
                        {{ zawodnik.nr_startowy }}. {{ zawodnik.imie }} {{ zawodnik.nazwisko }}
                        <div class="text-xs">{{ formatTime(zawodnik.czas_przejazdu_s) }}</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Finał -->
              <div v-if="plecData.finał?.length > 0 && (!drabinkaFilters.faza || drabinkaFilters.faza === 'finał')" class="mb-6">
                <h5 class="font-medium text-gray-700 dark:text-gray-300 mb-3">🏆 Finał</h5>
                <div class="border-2 border-yellow-300 dark:border-yellow-600 rounded-lg p-4 bg-yellow-50 dark:bg-yellow-900/20">
                  <div v-for="grupa in plecData.finał" :key="grupa.grupa">
                    <div class="space-y-2">
                      <div v-for="(zawodnik, index) in grupa.zawodnicy" :key="zawodnik.nr_startowy" 
                           :class="[
                             'text-sm p-3 rounded font-medium',
                             index === 0 ? 'bg-yellow-200 dark:bg-yellow-800 text-yellow-900 dark:text-yellow-100' : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
                           ]">
                        <span v-if="index === 0">🥇</span>
                        <span v-else-if="index === 1">🥈</span>
                        <span v-else-if="index === 2">🥉</span>
                        <span v-else>{{ index + 1 }}.</span>
                        {{ zawodnik.nr_startowy }}. {{ zawodnik.imie }} {{ zawodnik.nazwisko }}
                        <div class="text-xs">{{ formatTime(zawodnik.czas_przejazdu_s) }}</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Brak zawodników -->
              <div v-if="!plecData.ćwierćfinały?.length && !plecData.półfinały?.length && !plecData.finał?.length" 
                   class="text-center py-8 text-gray-500 dark:text-gray-400">
                <TrophyIcon class="h-12 w-12 mx-auto mb-3 text-gray-300 dark:text-gray-600" />
                <p>Brak zawodników w tej kategorii</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { ExclamationTriangleIcon, TrophyIcon, UsersIcon, UserIcon } from '@heroicons/vue/24/outline'
import StatsCard from './StatsCard.vue'

// Types
interface DrabinkaResponse {
  [key: string]: any
}

// Reactive data
const drabinka = ref<DrabinkaResponse | null>(null)
const loading = ref(true)
const error = ref<string | null>(null)

// Nowy system filtrów z dropdown'ami
const drabinkaFilters = ref({
  kategoria: '',
  plec: '',
  faza: '',
  sortowanie: 'kategoria_asc'
})

// Stary system filtrów - zachowuję dla kompatybilności
const selectedKategorie = ref<string[]>([])
const selectedPlcie = ref<string[]>([])

// Computed
const kategorieData = computed(() => {
  if (!drabinka.value) return {}
  
  const { podsumowanie, ...kategorie } = drabinka.value
  return kategorie
})

const uniqueKategorie = computed(() => {
  return Object.keys(kategorieData.value).sort()
})

const filteredKategorieData = computed(() => {
  if (!drabinka.value) {
    return {}
  }
  
  const { podsumowanie, ...kategorie } = drabinka.value
  let filtered: any = {}
  
  // Filtrowanie po kategorii (nowy system)
  if (drabinkaFilters.value.kategoria) {
    if (kategorie[drabinkaFilters.value.kategoria]) {
      filtered[drabinkaFilters.value.kategoria] = kategorie[drabinkaFilters.value.kategoria]
    }
  } else {
    // Stary system filtrów - kategorie
    for (const [kategoriaName, kategoria] of Object.entries(kategorie)) {
      if (selectedKategorie.value.length === 0 || selectedKategorie.value.includes(kategoriaName)) {
        filtered[kategoriaName] = kategoria
      }
    }
  }
  
  // Filtrowanie po płci
  if (drabinkaFilters.value.plec || selectedPlcie.value.length > 0) {
    const targetGender = drabinkaFilters.value.plec || (selectedPlcie.value.length === 1 ? selectedPlcie.value[0] : '')
    
    if (targetGender) {
      const newFiltered: any = {}
      for (const [kategoriaName, kategoria] of Object.entries(filtered)) {
        const filteredKategoria: any = {}
        for (const [plecName, plecData] of Object.entries(kategoria as any)) {
          if (plecName === targetGender) {
            filteredKategoria[plecName] = plecData
          }
        }
        if (Object.keys(filteredKategoria).length > 0) {
          newFiltered[kategoriaName] = filteredKategoria
        }
      }
      filtered = newFiltered
    }
  }
  
  // Filtrowanie po fazie turnieju
  if (drabinkaFilters.value.faza) {
    const targetPhase = drabinkaFilters.value.faza
    const newFiltered: any = {}
    
    for (const [kategoriaName, kategoria] of Object.entries(filtered)) {
      const filteredKategoria: any = {}
      for (const [plecName, plecData] of Object.entries(kategoria as any)) {
        const filteredPlecData: any = { ...plecData }
        
        // Usuwanie niewłaściwych faz
        if (targetPhase === 'ćwierćfinały') {
          delete filteredPlecData.półfinały
          delete filteredPlecData.finał
        } else if (targetPhase === 'półfinały') {
          delete filteredPlecData.ćwierćfinały
          delete filteredPlecData.finał
        } else if (targetPhase === 'finał') {
          delete filteredPlecData.ćwierćfinały
          delete filteredPlecData.półfinały
        }
        
        // Sprawdzanie czy zostały jakieś dane
        const hasData = filteredPlecData[targetPhase]?.length > 0
        if (hasData) {
          filteredKategoria[plecName] = filteredPlecData
        }
      }
      if (Object.keys(filteredKategoria).length > 0) {
        newFiltered[kategoriaName] = filteredKategoria
      }
    }
    filtered = newFiltered
  }
  
  // Sortowanie
  const sortedKeys = Object.keys(filtered).sort((a, b) => {
    switch (drabinkaFilters.value.sortowanie) {
      case 'kategoria_desc':
        return b.localeCompare(a)
      case 'zawodnikow_desc':
        return getTotalContestants(filtered[b]) - getTotalContestants(filtered[a])
      case 'zawodnikow_asc':
        return getTotalContestants(filtered[a]) - getTotalContestants(filtered[b])
      default: // kategoria_asc
        return a.localeCompare(b)
    }
  })
  
  const sortedFiltered: any = {}
  sortedKeys.forEach(key => {
    sortedFiltered[key] = filtered[key]
  })
  
  return sortedFiltered
})

// Computed properties dla operacji grupowych
const allCategoriesSelected = computed(() => 
  selectedKategorie.value.length === uniqueKategorie.value.length
)

const bothGendersSelected = computed(() => 
  selectedPlcie.value.length === 2 || drabinkaFilters.value.plec === ''
)

const totalContestants = computed(() => {
  let total = 0
  for (const kategoria of Object.values(filteredKategorieData.value)) {
    total += getTotalContestants(kategoria)
  }
  return total
})

// Helper function
const getTotalContestants = (kategoria: any): number => {
  let count = 0
  for (const plecData of Object.values(kategoria)) {
    if (typeof plecData === 'object' && plecData !== null) {
      // Sprawdzamy wszystkie fazy
      const phases = ['ćwierćfinały', 'półfinały', 'finał']
      for (const phase of phases) {
        if ((plecData as any)[phase]?.length > 0) {
          for (const grupa of (plecData as any)[phase]) {
            count += grupa.zawodnicy?.length || 0
          }
        }
      }
    }
  }
  return count
}

// Methods
const formatTime = (seconds: number | null): string => {
  if (!seconds) return '-'
  const mins = Math.floor(seconds / 60)
  const secs = (seconds % 60).toFixed(2)
  return `${mins}:${secs.padStart(5, '0')}`
}

// Nowe metody dla nowego systemu filtrów
const clearAllFilters = () => {
  drabinkaFilters.value = {
    kategoria: '',
    plec: '',
    faza: '',
    sortowanie: 'kategoria_asc'
  }
  selectedKategorie.value = []
  selectedPlcie.value = []
}

const toggleAllCategories = () => {
  if (allCategoriesSelected.value) {
    selectedKategorie.value = []
    drabinkaFilters.value.kategoria = ''
  } else {
    selectedKategorie.value = [...uniqueKategorie.value]
    drabinkaFilters.value.kategoria = ''
  }
}

const toggleGenders = () => {
  if (bothGendersSelected.value) {
    selectedPlcie.value = ['Mężczyźni']
    drabinkaFilters.value.plec = 'Mężczyźni'
  } else {
    selectedPlcie.value = ['Mężczyźni', 'Kobiety']
    drabinkaFilters.value.plec = ''
  }
}

const showFinalsOnly = () => {
  if (drabinkaFilters.value.faza === 'finał') {
    drabinkaFilters.value.faza = ''
  } else {
    drabinkaFilters.value.faza = 'finał'
  }
}

// Stare metody dla kompatybilności
const toggleKategoria = (kategoria: string) => {
  const index = selectedKategorie.value.indexOf(kategoria)
  if (index > -1) {
    selectedKategorie.value.splice(index, 1)
  } else {
    selectedKategorie.value.push(kategoria)
  }
  // Resetuj nowy filtr gdy używamy starego
  drabinkaFilters.value.kategoria = ''
}

const togglePlec = (plec: string) => {
  const index = selectedPlcie.value.indexOf(plec)
  if (index > -1) {
    selectedPlcie.value.splice(index, 1)
  } else {
    selectedPlcie.value.push(plec)
  }
  // Resetuj nowy filtr gdy używamy starego
  drabinkaFilters.value.plec = ''
}

const selectAllCategories = () => {
  selectedKategorie.value = uniqueKategorie.value
  drabinkaFilters.value.kategoria = ''
}

const selectAllGenders = () => {
  selectedPlcie.value = ['Mężczyźni', 'Kobiety']
  drabinkaFilters.value.plec = ''
}

const clearFilters = () => {
  selectedKategorie.value = []
  selectedPlcie.value = []
  clearAllFilters()
}

const fetchDrabinka = async () => {
  try {
    loading.value = true
    error.value = null
    
    const response = await axios.get<DrabinkaResponse>('/api/drabinka')
    drabinka.value = response.data
  } catch (err) {
    error.value = 'Nie udało się załadować drabinki turniejowej'
  } finally {
    loading.value = false
  }
}

// Lifecycle
onMounted(() => {
  fetchDrabinka()
})
</script>

<style scoped>
/* Custom animations for tournament bracket */
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style> 