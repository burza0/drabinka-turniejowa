<template>
  <div class="p-4 sm:p-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6 space-y-4 sm:space-y-0">
      <div class="flex items-center space-x-3">
        <PrinterIcon class="h-8 w-8 text-indigo-600" />
        <h2 class="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">Drukowanie QR kodów</h2>
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

    <!-- Filtry i sortowanie -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-6 mb-6 transition-colors duration-200">
      <!-- Nagłówek sekcji -->
      <div class="flex items-center justify-between mb-6">
        <h3 class="text-lg sm:text-xl font-semibold text-gray-900 dark:text-white">Filtry i sortowanie</h3>
        <button 
          @click="clearAllFilters" 
          class="text-sm text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300 flex items-center space-x-1 transition-colors duration-200"
        >
          <span>🗑️</span>
          <span>Wyczyść wszystko</span>
        </button>
      </div>

      <!-- Pierwsza linia - główne filtry -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <!-- Filtr kategorii -->
        <div>
          <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
            <span class="flex items-center space-x-2">
              <span>🏆</span>
              <span>Kategoria</span>
            </span>
          </label>
          <select v-model="selectedKategoria" class="w-full rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-md focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 text-sm font-medium py-2.5 px-3 transition-all duration-200 hover:shadow-lg">
            <option value="">Wszystkie</option>
            <option v-for="kategoria in uniqueKategorie" :key="kategoria" :value="kategoria">
              {{ kategoria }} ({{ getKategoriaCount(kategoria) }})
            </option>
          </select>
        </div>

        <!-- Filtr klubu -->
        <div>
          <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
            <span class="flex items-center space-x-2">
              <span>🏢</span>
              <span>Klub</span>
            </span>
          </label>
          <select v-model="selectedKlub" class="w-full rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-md focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 text-sm font-medium py-2.5 px-3 transition-all duration-200 hover:shadow-lg">
            <option value="">Wszystkie</option>
            <option v-for="klub in uniqueKluby" :key="klub" :value="klub">
              {{ klub }} ({{ getKlubCount(klub) }})
            </option>
          </select>
        </div>

        <!-- Filtr QR kodów -->
        <div>
          <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
            <span class="flex items-center space-x-2">
              <span>📱</span>
              <span>Status QR</span>
            </span>
          </label>
          <select v-model="qrFilter" class="w-full rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-md focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 text-sm font-medium py-2.5 px-3 transition-all duration-200 hover:shadow-lg">
            <option value="">Wszystkie</option>
            <option value="with_qr">✅ Z QR kodami ({{ countStats.withQr }})</option>
            <option value="without_qr">❌ Bez QR kodów ({{ countStats.total - countStats.withQr }})</option>
          </select>
        </div>
      </div>

      <!-- Druga linia - sortowanie -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
        <!-- Sortowanie -->
        <div>
          <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
            <span class="flex items-center space-x-2">
              <span>🔄</span>
              <span>Sortowanie</span>
            </span>
          </label>
          <select v-model="sortBy" class="w-full rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-md focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500 text-sm font-medium py-2.5 px-3 transition-all duration-200 hover:shadow-lg">
            <option value="nr_startowy_asc">Nr startowy (rosnąco)</option>
            <option value="nr_startowy_desc">Nr startowy (malejąco)</option>
            <option value="nazwisko_asc">Nazwisko (A-Z)</option>
            <option value="nazwisko_desc">Nazwisko (Z-A)</option>
            <option value="kategoria_asc">Kategoria (A-Z)</option>
            <option value="klub_asc">Klub (A-Z)</option>
            <option value="qr_status">Status QR (najpierw bez QR)</option>
          </select>
        </div>
      </div>

      <!-- Trzecia linia - operacje grupowe -->
      <div class="border-t border-gray-200 dark:border-gray-700 pt-6">
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-4">
          <span class="flex items-center space-x-2">
            <span>⚡</span>
            <span>Operacje grupowe</span>
          </span>
        </label>
        <div class="flex flex-wrap gap-3">
          <button 
            @click="toggleAllFiltered" 
            :class="[
              'px-4 py-2 text-sm font-medium rounded-lg transition-all duration-200 flex items-center space-x-2',
              allFilteredSelected 
                ? 'bg-indigo-700 text-white shadow-inner border-2 border-indigo-800' 
                : 'bg-indigo-600 text-white hover:bg-indigo-700 border-2 border-transparent'
            ]"
          >
            <span>{{ allFilteredSelected ? '✅' : '☐' }}</span>
            <span>{{ allFilteredSelected ? 'Odznacz wszystkie' : 'Zaznacz wszystkie' }} ({{ filteredZawodnicy.length }})</span>
          </button>
          
          <button 
            @click="toggleByCategory" 
            :disabled="!selectedKategoria"
            :class="[
              'px-4 py-2 text-sm font-medium rounded-lg transition-all duration-200 flex items-center space-x-2 border-2',
              !selectedKategoria 
                ? 'bg-gray-300 dark:bg-gray-600 text-gray-500 dark:text-gray-400 cursor-not-allowed border-transparent'
                : categorySelected
                  ? 'bg-green-700 text-white shadow-inner border-green-800'
                  : 'bg-green-600 text-white hover:bg-green-700 border-transparent'
            ]"
          >
            <span>{{ !selectedKategoria ? '🏆' : categorySelected ? '✅' : '☐' }}</span>
            <span>
              {{ !selectedKategoria 
                ? 'Wybierz kategorię' 
                : categorySelected 
                  ? `Odznacz: ${selectedKategoria}` 
                  : `Zaznacz: ${selectedKategoria}` 
              }}
            </span>
          </button>
          
          <button 
            @click="toggleByClub" 
            :disabled="!selectedKlub"
            :class="[
              'px-4 py-2 text-sm font-medium rounded-lg transition-all duration-200 flex items-center space-x-2 border-2',
              !selectedKlub 
                ? 'bg-gray-300 dark:bg-gray-600 text-gray-500 dark:text-gray-400 cursor-not-allowed border-transparent'
                : clubSelected
                  ? 'bg-purple-700 text-white shadow-inner border-purple-800'
                  : 'bg-purple-600 text-white hover:bg-purple-700 border-transparent'
            ]"
          >
            <span>{{ !selectedKlub ? '🏢' : clubSelected ? '✅' : '☐' }}</span>
            <span>
              {{ !selectedKlub 
                ? 'Wybierz klub' 
                : clubSelected 
                  ? `Odznacz: ${selectedKlub}` 
                  : `Zaznacz: ${selectedKlub}` 
              }}
            </span>
          </button>
          
          <button 
            @click="toggleWithoutQr" 
            :class="[
              'px-4 py-2 text-sm font-medium rounded-lg transition-all duration-200 flex items-center space-x-2 border-2',
              filteredZawodnicy.filter(z => !z.qr_code).length === 0
                ? 'bg-gray-300 dark:bg-gray-600 text-gray-500 dark:text-gray-400 cursor-not-allowed border-transparent'
                : withoutQrSelected
                  ? 'bg-orange-700 text-white shadow-inner border-orange-800'
                  : 'bg-orange-600 text-white hover:bg-orange-700 border-transparent'
            ]"
            :disabled="filteredZawodnicy.filter(z => !z.qr_code).length === 0"
          >
            <span>{{ withoutQrSelected ? '✅' : '☐' }}</span>
            <span>{{ withoutQrSelected ? 'Odznacz bez QR' : 'Zaznacz bez QR' }} ({{ filteredZawodnicy.filter(z => !z.qr_code).length }})</span>
          </button>
          
          <button 
            @click="clearSelection" 
            :disabled="selectedZawodnicy.length === 0"
            :class="[
              'px-4 py-2 text-sm font-medium rounded-lg transition-all duration-200 flex items-center space-x-2 border-2 border-transparent',
              selectedZawodnicy.length > 0
                ? 'bg-gray-600 text-white hover:bg-gray-700'
                : 'bg-gray-300 dark:bg-gray-600 text-gray-500 dark:text-gray-400 cursor-not-allowed'
            ]"
          >
            <span>🗑️</span>
            <span>Wyczyść zaznaczenia ({{ selectedZawodnicy.length }})</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Statystyki -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <div class="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg border border-blue-200 dark:border-blue-800 transition-colors duration-200">
        <div class="text-2xl font-bold text-blue-600 dark:text-blue-400">{{ countStats.total }}</div>
        <div class="text-sm text-blue-700 dark:text-blue-300">Po filtrach</div>
      </div>
      <div class="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg border border-green-200 dark:border-green-800 transition-colors duration-200">
        <div class="text-2xl font-bold text-green-600 dark:text-green-400">{{ countStats.selected }}</div>
        <div class="text-sm text-green-700 dark:text-green-300">Zaznaczonych</div>
      </div>
      <div class="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg border border-purple-200 dark:border-purple-800 transition-colors duration-200">
        <div class="text-2xl font-bold text-purple-600 dark:text-purple-400">{{ countStats.withQr }}</div>
        <div class="text-sm text-purple-700 dark:text-purple-300">Z QR kodami</div>
      </div>
      <div class="bg-orange-50 dark:bg-orange-900/20 p-4 rounded-lg border border-orange-200 dark:border-orange-800 transition-colors duration-200">
        <div class="text-2xl font-bold text-orange-600 dark:text-orange-400">{{ countStats.generated }}</div>
        <div class="text-sm text-orange-700 dark:text-orange-300">Do druku</div>
      </div>
    </div>

    <!-- Lista zawodników -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 transition-colors duration-200">
      <div class="p-4 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-700 flex items-center justify-between transition-colors duration-200">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
          Lista zawodników ({{ filteredZawodnicy.length }})
        </h3>
        <div class="text-sm text-gray-600 dark:text-gray-400">
          Zaznaczono: {{ selectedZawodnicy.length }}
        </div>
      </div>
      
      <!-- Nagłówki kolumn - ukryte na mobile -->
      <div class="hidden md:grid grid-cols-6 gap-4 p-4 bg-gray-100 dark:bg-gray-700 text-sm font-medium text-gray-600 dark:text-gray-300 border-b border-gray-200 dark:border-gray-600 transition-colors duration-200">
        <div class="flex items-center">
          <input 
            type="checkbox" 
            :checked="selectedZawodnicy.length === filteredZawodnicy.length && filteredZawodnicy.length > 0"
            @change="toggleSelectAll"
            class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 dark:border-gray-600 rounded mr-3"
          >
          Nr startowy
        </div>
        <div>Imię i nazwisko</div>
        <div>Kategoria</div>
        <div>Klub</div>
        <div>Status QR</div>
        <div>Akcje</div>
      </div>
      
      <div class="max-h-96 overflow-y-auto">
        <div v-if="filteredZawodnicy.length === 0" class="p-8 text-center text-gray-500 dark:text-gray-400">
          <div class="text-4xl mb-2">🔍</div>
          <div class="text-lg font-medium mb-1">Brak zawodników</div>
          <div class="text-sm">Spróbuj zmienić kryteria filtrowania</div>
        </div>
        
        <!-- Mobile layout -->
        <div class="md:hidden">
          <div v-for="zawodnik in filteredZawodnicy" :key="zawodnik.nr_startowy" 
               class="p-4 border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-200">
            <div class="flex items-start space-x-3">
              <input 
                type="checkbox" 
                :checked="selectedZawodnicy.includes(zawodnik.nr_startowy)"
                @change="toggleZawodnik(zawodnik.nr_startowy)"
                class="h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-gray-300 dark:border-gray-600 rounded mt-1"
              >
              <div class="flex-1">
                <div class="flex items-center justify-between mb-2">
                  <div class="font-semibold text-lg text-gray-900 dark:text-white">
                    #{{ zawodnik.nr_startowy }}
                  </div>
                  <div class="flex items-center">
                    <div v-if="zawodnik.qr_code" class="flex items-center text-green-600 dark:text-green-400 bg-green-50 dark:bg-green-900/20 px-2 py-1 rounded-full text-xs font-medium">
                      <CheckCircleIcon class="h-3 w-3 mr-1" />
                      <span>QR</span>
                    </div>
                    <div v-else class="flex items-center text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/20 px-2 py-1 rounded-full text-xs font-medium">
                      <XCircleIcon class="h-3 w-3 mr-1" />
                      <span>Brak QR</span>
                    </div>
                  </div>
                </div>
                <div class="text-base font-medium text-gray-900 dark:text-white mb-2">
                  {{ zawodnik.imie }} {{ zawodnik.nazwisko }}
                </div>
                <div class="flex flex-wrap gap-2 text-sm">
                  <span class="bg-blue-100 dark:bg-blue-900/20 text-blue-800 dark:text-blue-200 px-2 py-1 rounded font-medium">{{ zawodnik.kategoria }}</span>
                  <span class="bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 px-2 py-1 rounded font-medium">{{ zawodnik.klub || '-' }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Desktop layout -->
        <div class="hidden md:block">
          <div v-for="zawodnik in filteredZawodnicy" :key="zawodnik.nr_startowy" 
               class="grid grid-cols-6 gap-4 p-4 border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 items-center text-sm transition-colors duration-200">
            <div class="flex items-center">
              <input 
                type="checkbox" 
                :checked="selectedZawodnicy.includes(zawodnik.nr_startowy)"
                @change="toggleZawodnik(zawodnik.nr_startowy)"
                class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 dark:border-gray-600 rounded mr-3"
              >
              <span class="font-medium text-gray-900 dark:text-white">#{{ zawodnik.nr_startowy }}</span>
            </div>
            <div class="font-medium text-gray-900 dark:text-white">{{ zawodnik.imie }} {{ zawodnik.nazwisko }}</div>
            <div class="text-gray-600 dark:text-gray-400">{{ zawodnik.kategoria }}</div>
            <div class="text-gray-600 dark:text-gray-400 truncate">{{ zawodnik.klub || '-' }}</div>
            <div class="flex items-center">
              <div v-if="zawodnik.qr_code" class="flex items-center text-green-600 dark:text-green-400">
                <CheckCircleIcon class="h-4 w-4 mr-1" />
                <span class="text-xs font-medium">Tak</span>
              </div>
              <div v-else class="flex items-center text-red-600 dark:text-red-400">
                <XCircleIcon class="h-4 w-4 mr-1" />
                <span class="text-xs font-medium">Nie</span>
              </div>
            </div>
            <div>
              <button 
                v-if="!zawodnik.qr_code"
                @click="generateSingleQr(zawodnik.nr_startowy)"
                class="text-xs bg-indigo-600 text-white px-3 py-1 rounded-md hover:bg-indigo-700 font-medium transition-colors duration-200"
              >
                Generuj QR
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Wygenerowane QR kody (podgląd) -->
    <div v-if="generatedQrCodes.length > 0" class="mt-6 bg-white rounded-lg shadow-sm border">
      <div class="p-4 border-b bg-gray-50 flex items-center justify-between">
        <h3 class="text-lg font-semibold text-gray-900">
          Wygenerowane QR kody ({{ generatedQrCodes.length }})
        </h3>
        <button 
          @click="clearGenerated" 
          class="text-sm text-red-600 hover:text-red-800"
        >
          Wyczyść
        </button>
      </div>
      
      <div class="p-4 grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4 max-h-80 overflow-y-auto">
        <div v-for="item in generatedQrCodes" :key="item.zawodnik.nr_startowy" 
             class="text-center p-2 border rounded">
          <img :src="item.qr_image" :alt="`QR ${item.zawodnik.nr_startowy}`" class="w-16 h-16 mx-auto mb-1">
          <div class="text-xs font-medium">{{ item.zawodnik.nr_startowy }}</div>
          <div class="text-xs text-gray-600">{{ item.zawodnik.imie }} {{ item.zawodnik.nazwisko }}</div>
        </div>
      </div>
    </div>

    <!-- Modal drukowania -->
    <div v-if="isPrintModalOpen" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-4xl w-full m-4 max-h-[90vh] overflow-y-auto">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold">Podgląd wydruku</h3>
          <button @click="isPrintModalOpen = false" class="text-gray-400 hover:text-gray-600">
            <XMarkIcon class="h-6 w-6" />
          </button>
        </div>
        
        <div class="mb-4 flex space-x-4">
          <button @click="doPrint" class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700">
            Drukuj teraz
          </button>
          <button @click="isPrintModalOpen = false" class="px-4 py-2 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400">
            Anuluj
          </button>
        </div>
        
        <!-- Podgląd naklejek -->
        <div id="printArea" class="print-content">
          <div class="sticker-grid">
            <div v-for="item in generatedQrCodes" :key="item.zawodnik.nr_startowy" class="sticker">
              <div class="sticker-header">
                <div class="nr-startowy">{{ item.zawodnik.nr_startowy }}</div>
                <div class="zawodnik-name">{{ item.zawodnik.imie }} {{ item.zawodnik.nazwisko }}</div>
              </div>
              <div class="qr-container">
                <img :src="item.qr_image" :alt="`QR ${item.zawodnik.nr_startowy}`" class="qr-code">
              </div>
              <div class="sticker-footer">
                <div class="kategoria">{{ item.zawodnik.kategoria }}</div>
                <div class="klub">{{ item.zawodnik.klub || '' }}</div>
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
import { 
  PrinterIcon, 
  QrCodeIcon, 
  CheckCircleIcon, 
  XCircleIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline'

// Interfaces
interface Zawodnik {
  nr_startowy: number
  imie: string
  nazwisko: string
  kategoria: string
  plec: string
  klub?: string
  qr_code?: string
}

interface QrCode {
  zawodnik: Zawodnik
  qr_code: string
  qr_image: string
}

// State
const zawodnicy = ref<Zawodnik[]>([])
const selectedZawodnicy = ref<number[]>([])
const generatedQrCodes = ref<QrCode[]>([])
const isLoading = ref(false)
const isGenerating = ref(false)
const isPrintModalOpen = ref(false)

// Filtry
const selectedKategoria = ref('')
const selectedKlub = ref('')
const qrFilter = ref('')
const sortBy = ref('nr_startowy_asc')

// Computed
const uniqueKategorie = computed(() => {
  return [...new Set(zawodnicy.value.map(z => z.kategoria))].sort()
})

const uniqueKluby = computed(() => {
  return [...new Set(zawodnicy.value.map(z => z.klub).filter(Boolean))].sort()
})

const filteredZawodnicy = computed(() => {
  let filtered = zawodnicy.value

  // Filtr kategorii
  if (selectedKategoria.value) {
    filtered = filtered.filter(z => z.kategoria === selectedKategoria.value)
  }

  // Filtr klubu
  if (selectedKlub.value) {
    filtered = filtered.filter(z => z.klub === selectedKlub.value)
  }

  // Filtr QR
  if (qrFilter.value === 'with_qr') {
    filtered = filtered.filter(z => z.qr_code)
  } else if (qrFilter.value === 'without_qr') {
    filtered = filtered.filter(z => !z.qr_code)
  }

  // Sortowanie
  if (sortBy.value === 'nr_startowy_asc') {
    filtered.sort((a, b) => a.nr_startowy - b.nr_startowy)
  } else if (sortBy.value === 'nr_startowy_desc') {
    filtered.sort((a, b) => b.nr_startowy - a.nr_startowy)
  } else if (sortBy.value === 'nazwisko_asc') {
    filtered.sort((a, b) => a.nazwisko.localeCompare(b.nazwisko))
  } else if (sortBy.value === 'nazwisko_desc') {
    filtered.sort((a, b) => b.nazwisko.localeCompare(a.nazwisko))
  }

  return filtered
})

// Computed do sprawdzania stanów zaznaczenia
const allFilteredSelected = computed(() => {
  if (filteredZawodnicy.value.length === 0) return false
  return filteredZawodnicy.value.every(z => selectedZawodnicy.value.includes(z.nr_startowy))
})

const categorySelected = computed(() => {
  if (!selectedKategoria.value) return false
  const categoryZawodnicy = filteredZawodnicy.value.filter(z => z.kategoria === selectedKategoria.value)
  return categoryZawodnicy.length > 0 && categoryZawodnicy.every(z => selectedZawodnicy.value.includes(z.nr_startowy))
})

const clubSelected = computed(() => {
  if (!selectedKlub.value) return false
  const clubZawodnicy = filteredZawodnicy.value.filter(z => z.klub === selectedKlub.value)
  return clubZawodnicy.length > 0 && clubZawodnicy.every(z => selectedZawodnicy.value.includes(z.nr_startowy))
})

const withoutQrSelected = computed(() => {
  const withoutQrZawodnicy = filteredZawodnicy.value.filter(z => !z.qr_code)
  return withoutQrZawodnicy.length > 0 && withoutQrZawodnicy.every(z => selectedZawodnicy.value.includes(z.nr_startowy))
})

const selectedZawodnicyWithQr = computed(() => {
  return selectedZawodnicy.value.filter(id => {
    const zawodnik = zawodnicy.value.find(z => z.nr_startowy === id)
    return zawodnik && zawodnik.qr_code
  })
})

const selectedZawodnicyWithoutQr = computed(() => {
  return selectedZawodnicy.value.filter(id => {
    const zawodnik = zawodnicy.value.find(z => z.nr_startowy === id)
    return zawodnik && !zawodnik.qr_code
  })
})

const countStats = computed(() => {
  const total = filteredZawodnicy.value.length
  const selected = selectedZawodnicy.value.filter(id => 
    filteredZawodnicy.value.some(z => z.nr_startowy === id)
  ).length
  const withQr = filteredZawodnicy.value.filter(z => z.qr_code).length
  const generated = generatedQrCodes.value.length

  return { total, selected, withQr, generated }
})

// Methods
const loadZawodnicy = async () => {
  isLoading.value = true
  try {
    const response = await fetch('/api/zawodnicy')
    if (response.ok) {
      zawodnicy.value = await response.json()
    }
  } catch (error) {
    console.error('Błąd podczas ładowania zawodników:', error)
  } finally {
    isLoading.value = false
  }
}

const toggleZawodnik = (nr_startowy: number) => {
  const index = selectedZawodnicy.value.indexOf(nr_startowy)
  if (index > -1) {
    selectedZawodnicy.value.splice(index, 1)
  } else {
    selectedZawodnicy.value.push(nr_startowy)
  }
}

const selectAllFiltered = () => {
  const filteredIds = filteredZawodnicy.value.map(z => z.nr_startowy)
  selectedZawodnicy.value = [...new Set([...selectedZawodnicy.value, ...filteredIds])]
}

const toggleAllFiltered = () => {
  if (allFilteredSelected.value) {
    // Odznacz wszystkie filtrowane
    const filteredIds = filteredZawodnicy.value.map(z => z.nr_startowy)
    selectedZawodnicy.value = selectedZawodnicy.value.filter(id => !filteredIds.includes(id))
  } else {
    // Zaznacz wszystkie filtrowane
    selectAllFiltered()
  }
}

const selectByCategory = () => {
  if (!selectedKategoria.value) {
    return // Przycisk jest wyłączony
  }
  const categoryZawodnicy = filteredZawodnicy.value
    .filter(z => z.kategoria === selectedKategoria.value)
    .map(z => z.nr_startowy)
  selectedZawodnicy.value = [...new Set([...selectedZawodnicy.value, ...categoryZawodnicy])]
}

const toggleByCategory = () => {
  if (!selectedKategoria.value) return
  
  if (categorySelected.value) {
    // Odznacz kategorię
    const categoryZawodnicy = filteredZawodnicy.value
      .filter(z => z.kategoria === selectedKategoria.value)
      .map(z => z.nr_startowy)
    selectedZawodnicy.value = selectedZawodnicy.value.filter(id => !categoryZawodnicy.includes(id))
  } else {
    // Zaznacz kategorię
    selectByCategory()
  }
}

const selectByClub = () => {
  if (!selectedKlub.value) {
    return // Przycisk jest wyłączony
  }
  const clubZawodnicy = filteredZawodnicy.value
    .filter(z => z.klub === selectedKlub.value)
    .map(z => z.nr_startowy)
  selectedZawodnicy.value = [...new Set([...selectedZawodnicy.value, ...clubZawodnicy])]
}

const toggleByClub = () => {
  if (!selectedKlub.value) return
  
  if (clubSelected.value) {
    // Odznacz klub
    const clubZawodnicy = filteredZawodnicy.value
      .filter(z => z.klub === selectedKlub.value)
      .map(z => z.nr_startowy)
    selectedZawodnicy.value = selectedZawodnicy.value.filter(id => !clubZawodnicy.includes(id))
  } else {
    // Zaznacz klub
    selectByClub()
  }
}

const selectWithoutQr = () => {
  const withoutQrZawodnicy = filteredZawodnicy.value
    .filter(z => !z.qr_code)
    .map(z => z.nr_startowy)
  selectedZawodnicy.value = [...new Set([...selectedZawodnicy.value, ...withoutQrZawodnicy])]
}

const toggleWithoutQr = () => {
  if (withoutQrSelected.value) {
    // Odznacz bez QR
    const withoutQrZawodnicy = filteredZawodnicy.value
      .filter(z => !z.qr_code)
      .map(z => z.nr_startowy)
    selectedZawodnicy.value = selectedZawodnicy.value.filter(id => !withoutQrZawodnicy.includes(id))
  } else {
    // Zaznacz bez QR
    selectWithoutQr()
  }
}

const clearSelection = () => {
  selectedZawodnicy.value = []
}

const generateSelected = async () => {
  if (selectedZawodnicyWithoutQr.value.length === 0) return
  
  isGenerating.value = true
  try {
    const response = await fetch('/api/qr/generate-bulk', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        zawodnicy_ids: selectedZawodnicyWithoutQr.value
      })
    })
    
    if (response.ok) {
      const data = await response.json()
      // Dodaj nowo wygenerowane QR kody do istniejących
      const existingIds = generatedQrCodes.value.map(qr => qr.zawodnik.nr_startowy)
      const newQrCodes = data.qr_codes.filter(qr => !existingIds.includes(qr.zawodnik.nr_startowy))
      generatedQrCodes.value = [...generatedQrCodes.value, ...newQrCodes]
      
      // Odśwież dane zawodników aby pobrać nowe QR kody
      await loadZawodnicy()
    } else {
      console.error('Błąd podczas generowania QR kodów')
    }
  } catch (error) {
    console.error('Błąd:', error)
  } finally {
    isGenerating.value = false
  }
}

const printSelected = async () => {
  if (selectedZawodnicyWithQr.value.length === 0) return
  
  isGenerating.value = true
  try {
    // Znajdź zawodników z QR kodami
    const zawodnicyWithQr = selectedZawodnicyWithQr.value.map(id => {
      return zawodnicy.value.find(z => z.nr_startowy === id)
    }).filter(Boolean)
    
    // Wygeneruj obrazy QR kodów
    const qrPromises = zawodnicyWithQr.map(async (zawodnik) => {
      if (!zawodnik.qr_code) return null
      
      // Generuj obraz QR kodu po stronie klienta
      const qr = await import('qrcode')
      const qrDataUrl = await qr.toDataURL(zawodnik.qr_code, {
        width: 200,
        margin: 2,
        color: {
          dark: '#000000',
          light: '#FFFFFF'
        }
      })
      
      return {
        zawodnik: zawodnik,
        qr_code: zawodnik.qr_code,
        qr_image: qrDataUrl
      }
    })
    
    const qrResults = await Promise.all(qrPromises)
    const validQrCodes = qrResults.filter(Boolean)
    
    // Zastąp wygenerowane QR kody nowymi
    generatedQrCodes.value = validQrCodes
    
    // Otwórz modal drukowania
    isPrintModalOpen.value = true
    
  } catch (error) {
    console.error('Błąd podczas przygotowywania QR kodów do druku:', error)
  } finally {
    isGenerating.value = false
  }
}

const doPrint = () => {
  window.print()
  isPrintModalOpen.value = false
}

const clearGenerated = () => {
  generatedQrCodes.value = []
}

const clearAllFilters = () => {
  selectedKategoria.value = ''
  selectedKlub.value = ''
  qrFilter.value = ''
  sortBy.value = 'nr_startowy_asc'
  selectedZawodnicy.value = []
}

const toggleSelectAll = () => {
  if (selectedZawodnicy.value.length === filteredZawodnicy.value.length && filteredZawodnicy.value.length > 0) {
    // Odznacz wszystkie z filtrowanych
    const filteredIds = filteredZawodnicy.value.map(z => z.nr_startowy)
    selectedZawodnicy.value = selectedZawodnicy.value.filter(id => !filteredIds.includes(id))
  } else {
    // Zaznacz wszystkie filtrowane
    selectAllFiltered()
  }
}

const generateSingleQr = async (nr_startowy: number) => {
  isGenerating.value = true
  try {
    const response = await fetch('/api/qr/generate-bulk', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        zawodnicy_ids: [nr_startowy]
      })
    })
    
    if (response.ok) {
      const data = await response.json()
      generatedQrCodes.value = [...generatedQrCodes.value, ...data.qr_codes]
      
      // Odśwież dane zawodników
      await loadZawodnicy()
    } else {
      console.error('Błąd podczas generowania QR kodu')
    }
  } catch (error) {
    console.error('Błąd:', error)
  } finally {
    isGenerating.value = false
  }
}

const getKategoriaCount = (kategoria: string) => {
  return filteredZawodnicy.value.filter(z => z.kategoria === kategoria).length
}

const getKlubCount = (klub: string) => {
  return filteredZawodnicy.value.filter(z => z.klub === klub).length
}

// Lifecycle
onMounted(() => {
  loadZawodnicy()
})
</script>

<style scoped>
/* Podstawowe style */
.sticker-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 10px;
  padding: 20px;
}

.sticker {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 10px;
  text-align: center;
  background: white;
  page-break-inside: avoid;
}

.sticker-header {
  margin-bottom: 8px;
}

.nr-startowy {
  font-size: 18px;
  font-weight: bold;
  color: #1f2937;
}

.zawodnik-name {
  font-size: 12px;
  color: #6b7280;
  margin-top: 2px;
}

.qr-container {
  margin: 8px 0;
}

.qr-code {
  width: 80px;
  height: 80px;
  margin: 0 auto;
}

.sticker-footer {
  margin-top: 8px;
  font-size: 10px;
  color: #9ca3af;
}

.kategoria {
  font-weight: 500;
}

.klub {
  margin-top: 2px;
}

/* Style do drukowania */
@media print {
  body * {
    visibility: hidden;
  }
  
  .print-content,
  .print-content * {
    visibility: visible;
  }
  
  .print-content {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
  }
  
  .sticker-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 5px;
    padding: 10px;
  }
  
  .sticker {
    border: 1px solid #000;
    margin: 0;
    padding: 5px;
    font-size: 10px;
  }
  
  .nr-startowy {
    font-size: 14px;
  }
  
  .zawodnik-name {
    font-size: 8px;
  }
  
  .qr-code {
    width: 60px;
    height: 60px;
  }
  
  .kategoria,
  .klub {
    font-size: 8px;
  }
}
</style> 