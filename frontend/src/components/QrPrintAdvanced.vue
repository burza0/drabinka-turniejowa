<template>
  <div class="p-4 sm:p-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6 space-y-4 sm:space-y-0">
      <div class="flex items-center space-x-3">
        <PrinterIcon class="h-8 w-8 text-indigo-600" />
        <h2 class="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">
          Drukowanie QR kodów (Advanced)
        </h2>
        <span class="text-xs bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-2 py-1 rounded-full">
          Universal Filters v31
        </span>
      </div>
      
      <div class="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-3">
        <button 
          @click="generateSelected" 
          :disabled="selectedZawodnicyWithoutQr.length === 0 || isGenerating"
          class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2 text-sm font-medium transition-colors duration-200"
        >
          <QrCodeIcon class="h-5 w-5" />
          <span>Generuj QR ({{ selectedZawodnicyWithoutQr.length }})</span>
        </button>
        
        <button 
          @click="printSelected" 
          :disabled="selectedZawodnicyWithQr.length === 0 || isGenerating"
          class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center space-x-2 text-sm font-medium transition-colors duration-200"
        >
          <PrinterIcon class="h-5 w-5" />
          <span>Drukuj ({{ selectedZawodnicyWithQr.length }})</span>
        </button>
      </div>
    </div>

    <!-- Universal Filter System -->
    <UniversalFilterSystem
      v-model="filters"
      :config="filterConfig"
      :data="filterData"
      @filtersChange="handleFiltersChange"
      @groupOperation="handleGroupOperation"
      @clearFilters="handleClearFilters"
      class="mb-6"
    />

    <!-- Stats Summary -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <div class="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg border border-blue-200 dark:border-blue-800">
        <div class="text-2xl font-bold text-blue-600 dark:text-blue-400">{{ filteredZawodnicy.length }}</div>
        <div class="text-sm text-blue-700 dark:text-blue-300">Zawodników (po filtrach)</div>
      </div>
      
      <div class="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg border border-green-200 dark:border-green-800">
        <div class="text-2xl font-bold text-green-600 dark:text-green-400">{{ countStats.withQr }}</div>
        <div class="text-sm text-green-700 dark:text-green-300">Z QR kodami</div>
      </div>
      
      <div class="bg-orange-50 dark:bg-orange-900/20 p-4 rounded-lg border border-orange-200 dark:border-orange-800">
        <div class="text-2xl font-bold text-orange-600 dark:text-orange-400">{{ countStats.withoutQr }}</div>
        <div class="text-sm text-orange-700 dark:text-orange-300">Bez QR kodów</div>
      </div>
      
      <div class="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg border border-purple-200 dark:border-purple-800">
        <div class="text-2xl font-bold text-purple-600 dark:text-purple-400">{{ selectedZawodnicy.length }}</div>
        <div class="text-sm text-purple-700 dark:text-purple-300">Zaznaczonych</div>
      </div>
    </div>

    <!-- Table -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead class="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                <input 
                  type="checkbox" 
                  :checked="allFilteredSelected"
                  @change="toggleAllFiltered"
                  class="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                />
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Nr
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Zawodnik
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Kategoria
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Klub
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                QR Status
              </th>
            </tr>
          </thead>
          <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            <tr 
              v-for="zawodnik in filteredZawodnicy" 
              :key="zawodnik.id"
              :class="[
                'hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-200',
                selectedZawodnicy.includes(zawodnik.id) ? 'bg-indigo-50 dark:bg-indigo-900/20' : ''
              ]"
            >
              <td class="px-6 py-4 whitespace-nowrap">
                <input 
                  type="checkbox" 
                  :checked="selectedZawodnicy.includes(zawodnik.id)"
                  @change="toggleZawodnik(zawodnik.id)"
                  class="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                />
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                {{ zawodnik.nr_startowy }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium text-gray-900 dark:text-white">
                  {{ zawodnik.imie }} {{ zawodnik.nazwisko }}
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                {{ zawodnik.kategoria }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                {{ zawodnik.klub }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span 
                  :class="[
                    'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                    zawodnik.qr_code
                      ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                      : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
                  ]"
                >
                  {{ zawodnik.qr_code ? '✅ Wygenerowany' : '❌ Brak QR' }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Debug Panel -->
    <div v-if="showDebug" class="mt-6 p-4 bg-gray-100 dark:bg-gray-800 rounded-lg">
      <details>
        <summary class="font-medium cursor-pointer">🐛 Debug Information</summary>
        <pre class="mt-2 text-xs overflow-auto">{{ debugInfo }}</pre>
      </details>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, reactive, onMounted } from 'vue'
import { PrinterIcon, QrCodeIcon } from '@heroicons/vue/24/outline'
import UniversalFilterSystem from './UniversalFilterSystem.vue'
import { useUniversalFilters, type FilterState } from '../composables/useUniversalFilters'

// Mock data - w rzeczywistej aplikacji pobieramy z API
const zawodnicy = ref([
  { id: 1, nr_startowy: 101, imie: 'Anna', nazwisko: 'Kowalska', kategoria: 'Open Women', klub: 'SKC Kraków', qr_code: null, plec: 'K' },
  { id: 2, nr_startowy: 102, imie: 'Piotr', nazwisko: 'Nowak', kategoria: 'Open Men', klub: 'RC Warszawa', qr_code: 'QR123', plec: 'M' },
  { id: 3, nr_startowy: 103, imie: 'Marta', nazwisko: 'Wiśniewska', kategoria: 'Open Women', klub: 'SKC Kraków', qr_code: null, plec: 'K' },
  { id: 4, nr_startowy: 104, imie: 'Tomasz', nazwisko: 'Zieliński', kategoria: 'Junior Men', klub: 'Gdańsk Roller', qr_code: 'QR124', plec: 'M' },
  { id: 5, nr_startowy: 105, imie: 'Karolina', nazwisko: 'Mazur', kategoria: 'Junior Women', klub: 'RC Warszawa', qr_code: null, plec: 'K' },
])

// State
const selectedZawodnicy = ref<number[]>([])
const isGenerating = ref(false)
const showDebug = ref(true)

// Universal filters setup
const { qrPrintConfig, createFilterData, generateStats } = useUniversalFilters()

const filters = reactive<FilterState>({
  search: '',
  category: '',
  club: '',
  gender: '',
  sorting: 'nr_startowy_asc',
  qr_status: ''
})

// Computed properties
const uniqueKategorie = computed(() => [...new Set(zawodnicy.value.map(z => z.kategoria))])
const uniqueKluby = computed(() => [...new Set(zawodnicy.value.map(z => z.klub))])

const countStats = computed(() => {
  const withQr = zawodnicy.value.filter(z => z.qr_code).length
  const withoutQr = zawodnicy.value.length - withQr
  return { 
    total: zawodnicy.value.length,
    withQr,
    withoutQr 
  }
})

const stats = computed(() => {
  const baseStats = generateStats(zawodnicy.value, {
    categoryKey: 'kategoria',
    clubKey: 'klub'
  })
  
  return {
    ...baseStats,
    withQr: countStats.value.withQr,
    withoutQr: countStats.value.withoutQr
  }
})

const filterConfig = computed(() => qrPrintConfig.value)

const filterData = computed(() => createFilterData(
  uniqueKategorie.value,
  uniqueKluby.value,
  'qr',
  stats.value
))

const filteredZawodnicy = computed(() => {
  let filtered = [...zawodnicy.value]
  
  // Search filter
  if (filters.search) {
    const searchTerm = filters.search.toLowerCase()
    filtered = filtered.filter(z => 
      z.imie.toLowerCase().includes(searchTerm) ||
      z.nazwisko.toLowerCase().includes(searchTerm) ||
      z.nr_startowy.toString().includes(searchTerm)
    )
  }
  
  // Category filter
  if (filters.category) {
    filtered = filtered.filter(z => z.kategoria === filters.category)
  }
  
  // Club filter
  if (filters.club) {
    filtered = filtered.filter(z => z.klub === filters.club)
  }
  
  // Gender filter
  if (filters.gender) {
    filtered = filtered.filter(z => z.plec === filters.gender)
  }
  
  // QR status filter
  if (filters.qr_status === 'with_qr') {
    filtered = filtered.filter(z => z.qr_code)
  } else if (filters.qr_status === 'without_qr') {
    filtered = filtered.filter(z => !z.qr_code)
  }
  
  // Sorting
  filtered.sort((a, b) => {
    switch (filters.sorting) {
      case 'nr_startowy_asc':
        return a.nr_startowy - b.nr_startowy
      case 'nr_startowy_desc':
        return b.nr_startowy - a.nr_startowy
      case 'nazwisko_asc':
        return a.nazwisko.localeCompare(b.nazwisko)
      case 'nazwisko_desc':
        return b.nazwisko.localeCompare(a.nazwisko)
      case 'kategoria_asc':
        return a.kategoria.localeCompare(b.kategoria)
      case 'klub_asc':
        return a.klub.localeCompare(b.klub)
      case 'qr_status':
        return (a.qr_code ? 1 : 0) - (b.qr_code ? 1 : 0)
      default:
        return 0
    }
  })
  
  return filtered
})

const selectedZawodnicyWithQr = computed(() => 
  selectedZawodnicy.value.filter(id => {
    const zawodnik = zawodnicy.value.find(z => z.id === id)
    return zawodnik?.qr_code
  })
)

const selectedZawodnicyWithoutQr = computed(() => 
  selectedZawodnicy.value.filter(id => {
    const zawodnik = zawodnicy.value.find(z => z.id === id)
    return !zawodnik?.qr_code
  })
)

const allFilteredSelected = computed(() => 
  filteredZawodnicy.value.length > 0 && 
  filteredZawodnicy.value.every(z => selectedZawodnicy.value.includes(z.id))
)

const debugInfo = computed(() => ({
  filters: filters,
  selectedCount: selectedZawodnicy.value.length,
  filteredCount: filteredZawodnicy.value.length,
  stats: countStats.value,
  filterConfig: filterConfig.value,
  filterData: filterData.value
}))

// Methods
const handleFiltersChange = (newFilters: FilterState) => {
  Object.assign(filters, newFilters)
}

const handleGroupOperation = (operation: string, data?: any) => {
  console.log('Group operation:', operation, data)
  
  switch (operation) {
    case 'toggle_all':
      toggleAllFiltered()
      break
      
    case 'toggle_by_category':
      if (filters.category) {
        const categoryZawodnicy = filteredZawodnicy.value
          .filter(z => z.kategoria === filters.category)
          .map(z => z.id)
        
        const allCategorySelected = categoryZawodnicy.every(id => selectedZawodnicy.value.includes(id))
        
        if (allCategorySelected) {
          // Odznacz kategorię
          selectedZawodnicy.value = selectedZawodnicy.value.filter(id => !categoryZawodnicy.includes(id))
        } else {
          // Zaznacz kategorię
          categoryZawodnicy.forEach(id => {
            if (!selectedZawodnicy.value.includes(id)) {
              selectedZawodnicy.value.push(id)
            }
          })
        }
      }
      break
      
    case 'toggle_by_club':
      if (filters.club) {
        const clubZawodnicy = filteredZawodnicy.value
          .filter(z => z.klub === filters.club)
          .map(z => z.id)
        
        const allClubSelected = clubZawodnicy.every(id => selectedZawodnicy.value.includes(id))
        
        if (allClubSelected) {
          selectedZawodnicy.value = selectedZawodnicy.value.filter(id => !clubZawodnicy.includes(id))
        } else {
          clubZawodnicy.forEach(id => {
            if (!selectedZawodnicy.value.includes(id)) {
              selectedZawodnicy.value.push(id)
            }
          })
        }
      }
      break
      
    case 'toggle_without_qr':
      const withoutQrZawodnicy = filteredZawodnicy.value
        .filter(z => !z.qr_code)
        .map(z => z.id)
      
      const allWithoutQrSelected = withoutQrZawodnicy.every(id => selectedZawodnicy.value.includes(id))
      
      if (allWithoutQrSelected) {
        selectedZawodnicy.value = selectedZawodnicy.value.filter(id => !withoutQrZawodnicy.includes(id))
      } else {
        withoutQrZawodnicy.forEach(id => {
          if (!selectedZawodnicy.value.includes(id)) {
            selectedZawodnicy.value.push(id)
          }
        })
      }
      break
  }
}

const handleClearFilters = () => {
  filters.search = ''
  filters.category = ''
  filters.club = ''
  filters.gender = ''
  filters.qr_status = ''
  // Keep sorting as is
}

const toggleAllFiltered = () => {
  if (allFilteredSelected.value) {
    // Odznacz wszystkie przefiltrowane
    const filteredIds = filteredZawodnicy.value.map(z => z.id)
    selectedZawodnicy.value = selectedZawodnicy.value.filter(id => !filteredIds.includes(id))
  } else {
    // Zaznacz wszystkie przefiltrowane
    filteredZawodnicy.value.forEach(z => {
      if (!selectedZawodnicy.value.includes(z.id)) {
        selectedZawodnicy.value.push(z.id)
      }
    })
  }
}

const toggleZawodnik = (id: number) => {
  const index = selectedZawodnicy.value.indexOf(id)
  if (index > -1) {
    selectedZawodnicy.value.splice(index, 1)
  } else {
    selectedZawodnicy.value.push(id)
  }
}

const generateSelected = () => {
  isGenerating.value = true
  console.log('Generating QR codes for:', selectedZawodnicyWithoutQr.value)
  
  // Simulate API call
  setTimeout(() => {
    selectedZawodnicyWithoutQr.value.forEach(id => {
      const zawodnik = zawodnicy.value.find(z => z.id === id)
      if (zawodnik) {
        zawodnik.qr_code = `QR${Date.now()}_${id}`
      }
    })
    isGenerating.value = false
  }, 2000)
}

const printSelected = () => {
  console.log('Printing QR codes for:', selectedZawodnicyWithQr.value)
  // Implement printing logic
}

onMounted(() => {
  console.log('QrPrintAdvanced mounted with Universal Filter System')
})
</script> 