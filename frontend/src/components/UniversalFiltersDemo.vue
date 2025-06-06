<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          🔧 Universal Filter System - Demo
        </h1>
        <p class="text-gray-600 dark:text-gray-300 mb-4">
          Demonstracja zaawansowanego systemu filtrów dla wersji 31
        </p>
        <div class="flex justify-center space-x-4">
          <span class="bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-3 py-1 rounded-full text-sm">
            Layout: Advanced
          </span>
          <span class="bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 px-3 py-1 rounded-full text-sm">
            Group Operations: Enabled
          </span>
          <span class="bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200 px-3 py-1 rounded-full text-sm">
            Custom Filters: QR Status
          </span>
        </div>
      </div>

      <!-- Universal Filter System Demo -->
      <div class="mb-8">
        <UniversalFilterSystem
          v-model="filters"
          :config="demoConfig"
          :data="demoData"
          @filtersChange="handleFiltersChange"
          @groupOperation="handleGroupOperation"
          @clearFilters="handleClearFilters"
        />
      </div>

      <!-- Results Preview -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          📊 Wyniki filtrowania
        </h3>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div class="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
            <div class="text-2xl font-bold text-blue-600 dark:text-blue-400">{{ mockResults.total }}</div>
            <div class="text-sm text-blue-700 dark:text-blue-300">Łącznie pozycji</div>
          </div>
          <div class="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg">
            <div class="text-2xl font-bold text-green-600 dark:text-green-400">{{ mockResults.filtered }}</div>
            <div class="text-sm text-green-700 dark:text-green-300">Po filtrach</div>
          </div>
          <div class="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg">
            <div class="text-2xl font-bold text-purple-600 dark:text-purple-400">{{ mockResults.selected }}</div>
            <div class="text-sm text-purple-700 dark:text-purple-300">Zaznaczonych</div>
          </div>
        </div>

        <!-- Current Filters Display -->
        <div class="border-t border-gray-200 dark:border-gray-700 pt-4">
          <h4 class="font-medium text-gray-900 dark:text-white mb-2">Aktywne filtry:</h4>
          <div class="bg-gray-50 dark:bg-gray-900 p-3 rounded-lg">
            <pre class="text-sm text-gray-700 dark:text-gray-300">{{ JSON.stringify(filters, null, 2) }}</pre>
          </div>
        </div>

        <!-- Last Operation Display -->
        <div v-if="lastOperation" class="border-t border-gray-200 dark:border-gray-700 pt-4 mt-4">
          <h4 class="font-medium text-gray-900 dark:text-white mb-2">Ostatnia operacja grupowa:</h4>
          <div class="bg-yellow-50 dark:bg-yellow-900/20 p-3 rounded-lg">
            <pre class="text-sm text-yellow-700 dark:text-yellow-300">{{ JSON.stringify(lastOperation, null, 2) }}</pre>
          </div>
        </div>
      </div>

      <!-- Documentation -->
      <div class="mt-8 bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          📚 Dokumentacja konfiguracji
        </h3>
        
        <div class="space-y-4">
          <div>
            <h4 class="font-medium text-gray-900 dark:text-white mb-2">Layout: Advanced</h4>
            <p class="text-sm text-gray-600 dark:text-gray-400">
              Zawiera 3 poziomy: Main Filters, Sorting, Group Operations z zaawansowanymi funkcjami.
            </p>
          </div>
          
          <div>
            <h4 class="font-medium text-gray-900 dark:text-white mb-2">Custom Filters</h4>
            <p class="text-sm text-gray-600 dark:text-gray-400">
              Filtr QR Status z opcjami: Wszystkie, Z QR kodami, Bez QR kodów - ze zliczaniem elementów.
            </p>
          </div>
          
          <div>
            <h4 class="font-medium text-gray-900 dark:text-white mb-2">Group Operations</h4>
            <p class="text-sm text-gray-600 dark:text-gray-400">
              Dynamiczne przyciski: Toggle All, Toggle by Category, Toggle by Club, Toggle Without QR.
            </p>
          </div>
          
          <div>
            <h4 class="font-medium text-gray-900 dark:text-white mb-2">Theme</h4>
            <p class="text-sm text-gray-600 dark:text-gray-400">
              Focus Color: Indigo, Border Style: Thick, Spacing: Normal.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, reactive } from 'vue'
import UniversalFilterSystem from './UniversalFilterSystem.vue'
import { useUniversalFilters, type FilterState } from '../composables/useUniversalFilters'

// Demo setup
const { qrPrintConfig, createFilterData, generateStats } = useUniversalFilters()
const lastOperation = ref<any>(null)

// Mock data
const mockCategories = ['Open Women', 'Open Men', 'Junior Women', 'Junior Men', 'Master Women', 'Master Men']
const mockClubs = ['SKC Kraków', 'RC Warszawa', 'Gdańsk Roller', 'Wrocław Speed', 'Poznań Racing']

// Generate mock stats
const mockStats = {
  category_Open_Women: 15,
  category_Open_Men: 22,
  category_Junior_Women: 8,
  category_Junior_Men: 12,
  category_Master_Women: 6,
  category_Master_Men: 9,
  club_SKC_Kraków: 18,
  club_RC_Warszawa: 16,
  club_Gdańsk_Roller: 14,
  club_Wrocław_Speed: 12,
  club_Poznań_Racing: 12,
  withQr: 45,
  withoutQr: 27
}

// Configuration
const demoConfig = computed(() => qrPrintConfig.value)

const demoData = computed(() => createFilterData(
  mockCategories,
  mockClubs,
  'qr',
  mockStats
))

// State
const filters = reactive<FilterState>({
  search: '',
  category: '',
  club: '',
  gender: '',
  sorting: 'nr_startowy_asc',
  qr_status: ''
})

// Mock results based on filters
const mockResults = computed(() => {
  let total = 72
  let filtered = total
  
  // Simulate filtering
  if (filters.category) filtered = Math.floor(filtered * 0.7)
  if (filters.club) filtered = Math.floor(filtered * 0.6)
  if (filters.gender) filtered = Math.floor(filtered * 0.5)
  if (filters.qr_status) filtered = Math.floor(filtered * 0.8)
  if (filters.search) filtered = Math.floor(filtered * 0.4)
  
  return {
    total,
    filtered,
    selected: Math.floor(filtered * 0.3)
  }
})

// Methods
const handleFiltersChange = (newFilters: FilterState) => {
  console.log('🔄 Filters changed:', newFilters)
}

const handleGroupOperation = (operation: string, data?: any) => {
  console.log('⚡ Group operation:', operation, data)
  lastOperation.value = {
    operation,
    data,
    timestamp: new Date().toLocaleTimeString()
  }
}

const handleClearFilters = () => {
  console.log('🗑️ Filters cleared')
  lastOperation.value = {
    operation: 'clear_filters',
    timestamp: new Date().toLocaleTimeString()
  }
}
</script> 