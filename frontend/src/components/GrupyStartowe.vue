<template>
  <div class="p-4 sm:p-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6 space-y-4 sm:space-y-0">
      <div class="flex items-center space-x-3">
        <UsersIcon class="h-8 w-8 text-blue-600" />
        <h2 class="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">Grupy Startowe</h2>
      </div>
      
      <div class="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-3">
        <button 
          @click="loadGrupy"
          :disabled="isLoading"
          class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2 text-sm font-medium transition-colors duration-200"
        >
          <ArrowPathIcon class="h-5 w-5" :class="{ 'animate-spin': isLoading }" />
          <span>Odśwież grupy</span>
        </button>
      </div>
    </div>

    <!-- Statystyki -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <div class="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg border border-blue-200 dark:border-blue-800 transition-colors duration-200">
        <div class="text-2xl font-bold text-blue-600 dark:text-blue-400">{{ stats.totalGrup }}</div>
        <div class="text-sm text-blue-700 dark:text-blue-300">Grup startowych</div>
      </div>
      <div class="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg border border-green-200 dark:border-green-800 transition-colors duration-200">
        <div class="text-2xl font-bold text-green-600 dark:text-green-400">{{ stats.totalZawodnikow }}</div>
        <div class="text-sm text-green-700 dark:text-green-300">Zameldowanych</div>
      </div>
      <div class="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg border border-purple-200 dark:border-purple-800 transition-colors duration-200">
        <div class="text-2xl font-bold text-purple-600 dark:text-purple-400">{{ Math.round(stats.estimatedTimeMin) }}</div>
        <div class="text-sm text-purple-700 dark:text-purple-300">Minut (szacunkowo)</div>
      </div>
      <div class="bg-orange-50 dark:bg-orange-900/20 p-4 rounded-lg border border-orange-200 dark:border-orange-800 transition-colors duration-200">
        <div class="text-2xl font-bold text-orange-600 dark:text-orange-400">{{ aktywnaNazwa || 'Brak' }}</div>
        <div class="text-sm text-orange-700 dark:text-orange-300">Aktywna grupa</div>
      </div>
    </div>

    <!-- Lista grup -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 transition-colors duration-200">
      <div class="p-4 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-700 flex items-center justify-between transition-colors duration-200">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
          Lista grup startowych ({{ grupy.length }})
        </h3>
      </div>
      
      <div v-if="isLoading" class="p-8 text-center text-gray-500 dark:text-gray-400">
        <ArrowPathIcon class="h-8 w-8 animate-spin mx-auto mb-2" />
        <div>Ładowanie grup startowych...</div>
      </div>
      
      <div v-else-if="grupy.length === 0" class="p-8 text-center text-gray-500 dark:text-gray-400">
        <div class="text-4xl mb-2">🏁</div>
        <div class="text-lg font-medium mb-1">Brak grup startowych</div>
        <div class="text-sm">Upewnij się że zawodnicy są zameldowani</div>
      </div>
      
      <div v-else class="divide-y divide-gray-200 dark:divide-gray-700">
        <div v-for="grupa in grupy" :key="grupa.numer_grupy" 
             class="p-4 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-200">
          
          <!-- Header grupy -->
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-3">
            <div class="flex items-center space-x-3 mb-2 sm:mb-0">
              <div class="flex-shrink-0">
                <div class="w-10 h-10 bg-blue-100 dark:bg-blue-900 rounded-full flex items-center justify-center">
                  <span class="text-blue-600 dark:text-blue-400 font-bold">{{ grupa.numer_grupy }}</span>
                </div>
              </div>
              <div>
                <h4 class="font-semibold text-gray-900 dark:text-white">{{ grupa.nazwa }}</h4>
                <p class="text-sm text-gray-600 dark:text-gray-400">
                  {{ grupa.liczba_zawodnikow }} zawodników • ~{{ Math.round(grupa.estimated_time / 60) }} min
                </p>
              </div>
            </div>
            
            <div class="flex items-center space-x-2">
              <!-- Status badge -->
              <span 
                :class="[
                  'px-2 py-1 rounded-full text-xs font-medium',
                  getStatusClass(grupa.status)
                ]"
              >
                {{ getStatusText(grupa.status) }}
              </span>
              
              <!-- Akcje -->
              <button 
                @click="setAktywnaGrupa(grupa)"
                :disabled="activeGrupa?.numer_grupy === grupa.numer_grupy"
                :class="[
                  'px-3 py-1 rounded-md text-sm font-medium transition-colors duration-200',
                  activeGrupa?.numer_grupy === grupa.numer_grupy
                    ? 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 cursor-not-allowed'
                    : 'bg-blue-600 text-white hover:bg-blue-700'
                ]"
              >
                {{ activeGrupa?.numer_grupy === grupa.numer_grupy ? 'Aktywna' : 'Aktywuj' }}
              </button>
              
              <button 
                @click="toggleGrupaDetails(grupa.numer_grupy)"
                class="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
              >
                <ChevronDownIcon 
                  class="h-5 w-5 transition-transform duration-200"
                  :class="{ 'rotate-180': expandedGrupy.includes(grupa.numer_grupy) }"
                />
              </button>
            </div>
          </div>
          
          <!-- Szczegóły grupy (rozwijane) -->
          <div v-if="expandedGrupy.includes(grupa.numer_grupy)" class="mt-4 bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
            <h5 class="font-medium text-gray-900 dark:text-white mb-3">Lista zawodników:</h5>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm">
              <div v-for="(zawodnik, index) in parseZawodnicy(grupa.lista_zawodnikow)" :key="index"
                   class="flex items-center space-x-2 text-gray-700 dark:text-gray-300">
                <span class="w-6 text-right">{{ index + 1 }}.</span>
                <span>{{ zawodnik }}</span>
              </div>
            </div>
            
            <!-- Numery startowe -->
            <div class="mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
              <span class="text-sm font-medium text-blue-800 dark:text-blue-200">
                Numery startowe: {{ grupa.numery_startowe }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Aktywna grupa info -->
    <div v-if="activeGrupa" class="mt-6 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
      <div class="flex items-center space-x-3">
        <div class="flex-shrink-0">
          <CheckCircleIcon class="h-6 w-6 text-green-600 dark:text-green-400" />
        </div>
        <div>
          <h4 class="font-medium text-green-800 dark:text-green-200">Aktywna grupa: {{ activeGrupa.nazwa }}</h4>
          <p class="text-sm text-green-700 dark:text-green-300">
            {{ activeGrupa.liczba_zawodnikow }} zawodników • {{ activeGrupa.kategoria }} {{ activeGrupa.plec === 'M' ? 'Mężczyźni' : 'Kobiety' }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { 
  UsersIcon, 
  ArrowPathIcon,
  ChevronDownIcon,
  CheckCircleIcon
} from '@heroicons/vue/24/outline'

// Interfaces
interface Grupa {
  numer_grupy: number
  nazwa: string
  kategoria: string
  plec: string
  liczba_zawodnikow: number
  lista_zawodnikow: string
  numery_startowe: string
  estimated_time: number
  status: string
}

// State
const grupy = ref<Grupa[]>([])
const activeGrupa = ref<Grupa | null>(null)
const expandedGrupy = ref<number[]>([])
const isLoading = ref(false)

// Computed
const stats = computed(() => {
  const totalGrup = grupy.value.length
  const totalZawodnikow = grupy.value.reduce((sum, g) => sum + g.liczba_zawodnikow, 0)
  const estimatedTimeMin = grupy.value.reduce((sum, g) => sum + g.estimated_time, 0) / 60
  
  return { totalGrup, totalZawodnikow, estimatedTimeMin }
})

const aktywnaNazwa = computed(() => {
  return activeGrupa.value ? `Grupa ${activeGrupa.value.numer_grupy}` : null
})

// Methods
const loadGrupy = async () => {
  isLoading.value = true
  try {
    const response = await fetch('/api/grupy-startowe')
    if (response.ok) {
      const data = await response.json()
      grupy.value = data.grupy || []
    } else {
      console.error('Błąd podczas ładowania grup')
    }
  } catch (error) {
    console.error('Błąd:', error)
  } finally {
    isLoading.value = false
  }
}

const setAktywnaGrupa = async (grupa: Grupa) => {
  try {
    const response = await fetch('/api/grupa-aktywna', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        numer_grupy: grupa.numer_grupy,
        kategoria: grupa.kategoria,
        plec: grupa.plec
      })
    })
    
    if (response.ok) {
      activeGrupa.value = grupa
    } else {
      console.error('Błąd podczas ustawiania aktywnej grupy')
    }
  } catch (error) {
    console.error('Błąd:', error)
  }
}

const toggleGrupaDetails = (numer: number) => {
  const index = expandedGrupy.value.indexOf(numer)
  if (index > -1) {
    expandedGrupy.value.splice(index, 1)
  } else {
    expandedGrupy.value.push(numer)
  }
}

const parseZawodnicy = (listaString: string) => {
  if (!listaString) return []
  return listaString.split('\n').filter(Boolean)
}

const getStatusClass = (status: string) => {
  switch (status) {
    case 'AKTYWNA': return 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200'
    case 'UKONCZONA': return 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200'
    default: return 'bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200'
  }
}

const getStatusText = (status: string) => {
  switch (status) {
    case 'AKTYWNA': return '🏃 Aktywna'
    case 'UKONCZONA': return '✅ Ukończona'
    default: return '⏳ Oczekuje'
  }
}

// Lifecycle
onMounted(() => {
  loadGrupy()
})
</script> 