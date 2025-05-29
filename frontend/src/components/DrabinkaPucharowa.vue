<template>
  <div>
    <!-- Header -->
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-gray-900">Drabinka Pucharowa SKATECROSS</h2>
      <p class="mt-1 text-sm text-gray-600">
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
    <div v-else-if="drabinka">
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

      <!-- Filtry -->
      <div class="bg-white shadow rounded-lg p-4 mb-6">
        <h3 class="text-lg font-medium text-gray-900 mb-4">🔍 Filtry</h3>
        
        <div class="space-y-4">
          <!-- Filtry w formie chip/tag buttons -->
          
          <!-- Filtr Kategorie -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
              Kategorie <span class="text-xs text-gray-500">({{ selectedKategorie.length }} wybranych)</span>
            </label>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="kategoria in uniqueKategorie"
                :key="kategoria"
                @click="toggleKategoria(kategoria)"
                :class="[
                  'px-3 py-2 rounded-full text-sm font-medium transition-colors duration-200',
                  selectedKategorie.includes(kategoria)
                    ? 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 border-2 border-green-300 dark:border-green-600'
                    : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 border-2 border-transparent hover:bg-gray-200 dark:hover:bg-gray-600'
                ]"
              >
                {{ kategoria }}
              </button>
            </div>
          </div>
          
          <!-- Filtr Płeć -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
              Płeć <span class="text-xs text-gray-500">({{ selectedPlcie.length }} wybranych)</span>
            </label>
            <div class="flex flex-wrap gap-2">
              <button
                @click="togglePlec('Mężczyźni')"
                :class="[
                  'px-4 py-2 rounded-full text-sm font-medium transition-colors duration-200',
                  selectedPlcie.includes('Mężczyźni')
                    ? 'bg-indigo-100 dark:bg-indigo-900 text-indigo-800 dark:text-indigo-200 border-2 border-indigo-300 dark:border-indigo-600'
                    : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 border-2 border-transparent hover:bg-gray-200 dark:hover:bg-gray-600'
                ]"
              >
                👨 Mężczyźni
              </button>
              <button
                @click="togglePlec('Kobiety')"
                :class="[
                  'px-4 py-2 rounded-full text-sm font-medium transition-colors duration-200',
                  selectedPlcie.includes('Kobiety')
                    ? 'bg-pink-100 dark:bg-pink-900 text-pink-800 dark:text-pink-200 border-2 border-pink-300 dark:border-pink-600'
                    : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 border-2 border-transparent hover:bg-gray-200 dark:hover:bg-gray-600'
                ]"
              >
                👩 Kobiety
              </button>
            </div>
          </div>
          
          <!-- Szybkie akcje filtrowania -->
          <div class="flex flex-wrap gap-2 pt-4 border-t border-gray-200 dark:border-gray-700">
            <button 
              @click="selectAllCategories"
              class="px-4 py-2 text-sm bg-green-500 text-white rounded-full hover:bg-green-600 transition-colors duration-200"
            >
              Wszystkie kategorie
            </button>
            <button 
              @click="selectAllGenders"
              class="px-4 py-2 text-sm bg-indigo-500 text-white rounded-full hover:bg-indigo-600 transition-colors duration-200"
            >
              Obie płcie
            </button>
            <button 
              @click="clearFilters"
              class="px-4 py-2 text-sm bg-gray-500 text-white rounded-full hover:bg-gray-600 transition-colors duration-200"
            >
              🗑️ Wyczyść wszystko
            </button>
          </div>
        </div>
        
        <!-- Licznik przefiltrowanych wyników -->
        <div class="mt-4 flex justify-between items-center text-sm text-gray-500 dark:text-gray-400">
          <div>
            Wyświetlane kategorie: {{ Object.keys(filteredKategorieData).length }} z {{ Object.keys(kategorieData).length }}
          </div>
        </div>
      </div>

      <!-- Kategorie -->
      <div class="space-y-8">
        <div v-for="(kategoria, kategoriaName) in filteredKategorieData" :key="kategoriaName" class="bg-white shadow rounded-lg p-6">
          <h3 class="text-xl font-semibold text-gray-900 mb-6">🏆 {{ kategoriaName }}</h3>
          
          <!-- Płcie w kategorii -->
          <div class="space-y-8">
            <div v-for="(plecData, plecName) in kategoria" :key="plecName" 
                 v-show="selectedPlcie.length === 0 || selectedPlcie.includes(String(plecName))"
                 class="border-l-4 border-indigo-500 pl-4">
              <h4 class="text-lg font-medium text-gray-800 mb-4">{{ String(plecName) === 'Mężczyźni' ? '👨 Mężczyźni' : '👩 Kobiety' }}</h4>
              
              <!-- Statystyki -->
              <div v-if="plecData.statystyki" class="bg-gray-50 rounded-lg p-4 mb-4">
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                  <div>
                    <span class="font-medium">Łącznie:</span>
                    <span class="ml-1">{{ plecData.statystyki.łącznie_zawodników }}</span>
                  </div>
                  <div>
                    <span class="font-medium">W ćwierćfinałach:</span>
                    <span class="ml-1">{{ plecData.statystyki.w_ćwierćfinałach }}</span>
                  </div>
                  <div>
                    <span class="font-medium">Odpadło:</span>
                    <span class="ml-1">{{ plecData.statystyki.odpadło }}</span>
                  </div>
                  <div>
                    <span class="font-medium">Grup finałowych:</span>
                    <span class="ml-1">{{ plecData.statystyki.grup_finał }}</span>
                  </div>
                </div>
              </div>

              <!-- Ćwierćfinały -->
              <div v-if="plecData.ćwierćfinały?.length > 0" class="mb-6">
                <h5 class="font-medium text-gray-700 mb-3">🥇 Ćwierćfinały</h5>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  <div v-for="grupa in plecData.ćwierćfinały" :key="grupa.grupa" class="border border-gray-200 rounded-lg p-3">
                    <div class="text-xs font-medium text-gray-500 mb-2">Grupa {{ grupa.grupa }} (awansuje {{ grupa.awansują }})</div>
                    <div class="space-y-1">
                      <div v-for="(zawodnik, index) in grupa.zawodnicy" :key="zawodnik.nr_startowy" 
                           :class="[
                             'text-sm p-2 rounded',
                             index < grupa.awansują ? 'bg-green-50 text-green-800 font-medium' : 'bg-gray-50 text-gray-600'
                           ]">
                        {{ zawodnik.nr_startowy }}. {{ zawodnik.imie }} {{ zawodnik.nazwisko }}
                        <div class="text-xs">{{ formatTime(zawodnik.czas_przejazdu_s) }}</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Półfinały -->
              <div v-if="plecData.półfinały?.length > 0" class="mb-6">
                <h5 class="font-medium text-gray-700 mb-3">🥈 Półfinały</h5>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div v-for="grupa in plecData.półfinały" :key="grupa.grupa" class="border border-gray-200 rounded-lg p-3">
                    <div class="text-xs font-medium text-gray-500 mb-2">Grupa {{ grupa.grupa }} (awansuje {{ grupa.awansują }})</div>
                    <div class="space-y-1">
                      <div v-for="(zawodnik, index) in grupa.zawodnicy" :key="zawodnik.nr_startowy" 
                           :class="[
                             'text-sm p-2 rounded',
                             index < grupa.awansują ? 'bg-yellow-50 text-yellow-800 font-medium' : 'bg-gray-50 text-gray-600'
                           ]">
                        {{ zawodnik.nr_startowy }}. {{ zawodnik.imie }} {{ zawodnik.nazwisko }}
                        <div class="text-xs">{{ formatTime(zawodnik.czas_przejazdu_s) }}</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Finał -->
              <div v-if="plecData.finał?.length > 0" class="mb-6">
                <h5 class="font-medium text-gray-700 mb-3">🏆 Finał</h5>
                <div class="border-2 border-yellow-300 rounded-lg p-4 bg-yellow-50">
                  <div v-for="grupa in plecData.finał" :key="grupa.grupa">
                    <div class="space-y-2">
                      <div v-for="(zawodnik, index) in grupa.zawodnicy" :key="zawodnik.nr_startowy" 
                           :class="[
                             'text-sm p-3 rounded font-medium',
                             index === 0 ? 'bg-yellow-200 text-yellow-900' : 'bg-gray-100 text-gray-700'
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
                   class="text-center py-8 text-gray-500">
                <TrophyIcon class="h-12 w-12 mx-auto mb-3 text-gray-300" />
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

// Filtry - domyślnie odznaczone (puste) - tak jak w Lista zawodników
const selectedKategorie = ref<string[]>([])
const selectedPlcie = ref<string[]>([])

// Computed
const kategorieData = computed(() => {
  if (!drabinka.value) return {}
  
  const { podsumowanie, ...kategorie } = drabinka.value
  return kategorie
})

const allKategorie = computed(() => {
  return Object.keys(kategorieData.value).sort()
})

const filteredKategorieData = computed(() => {
  if (!drabinka.value) return {}
  
  const { podsumowanie, ...kategorie } = drabinka.value
  const filtered: any = {}
  
  for (const [kategoriaName, kategoria] of Object.entries(kategorie)) {
    if (selectedKategorie.value.length === 0 || selectedKategorie.value.includes(kategoriaName)) {
      filtered[kategoriaName] = kategoria
    }
  }
  
  return filtered
})

const uniqueKategorie = computed(() => {
  return Object.keys(kategorieData.value).sort()
})

// Methods
const formatTime = (seconds: number | null): string => {
  if (!seconds) return '-'
  const mins = Math.floor(seconds / 60)
  const secs = (seconds % 60).toFixed(2)
  return `${mins}:${secs.padStart(5, '0')}`
}

// Filter methods
const toggleKategoria = (kategoria: string) => {
  const index = selectedKategorie.value.indexOf(kategoria)
  if (index > -1) {
    selectedKategorie.value.splice(index, 1)
  } else {
    selectedKategorie.value.push(kategoria)
  }
}

const togglePlec = (plec: string) => {
  const index = selectedPlcie.value.indexOf(plec)
  if (index > -1) {
    selectedPlcie.value.splice(index, 1)
  } else {
    selectedPlcie.value.push(plec)
  }
}

const selectAllCategories = () => {
  selectedKategorie.value = allKategorie.value
}

const selectAllGenders = () => {
  selectedPlcie.value = ['Mężczyźni', 'Kobiety']
}

const clearFilters = () => {
  selectedKategorie.value = []
  selectedPlcie.value = []
}

const fetchDrabinka = async () => {
  try {
    loading.value = true
    error.value = null
    
    const response = await axios.get<DrabinkaResponse>('/api/drabinka')
    drabinka.value = response.data
  } catch (err) {
    console.error('Błąd podczas pobierania drabinki:', err)
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