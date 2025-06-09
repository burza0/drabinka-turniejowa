<template>
  <div class="p-4 sm:p-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6 space-y-4 sm:space-y-0">
      <div class="flex items-center space-x-3">
        <QrCodeIcon class="h-8 w-8 text-green-600" />
        <h2 class="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">Centrum Startu</h2>
        <span class="text-sm bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 px-2 py-1 rounded-full">
          v{{ apiVersion }}
        </span>
      </div>
      
      <div class="flex items-center space-x-3">
        <div class="text-sm text-gray-600 dark:text-gray-400">
          Scanner: 
          <span class="text-green-600">
            🟢 Aktywny
          </span>
        </div>
        <button 
          @click="syncAllData('manual')"
          :disabled="appState.loading"
          class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2 text-sm font-medium transition-colors duration-200"
        >
          <ArrowPathIcon class="h-5 w-5" :class="{ 'animate-spin': appState.loading }" />
          <span>Odśwież wszystko</span>
        </button>
      </div>
    </div>

    <!-- Stats Dashboard -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <div class="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg border border-blue-200 dark:border-blue-800">
        <div class="text-2xl font-bold text-blue-600 dark:text-blue-400">{{ totalGrup }}</div>
        <div class="text-sm text-blue-700 dark:text-blue-300">Grup startowych</div>
      </div>
      
      <div class="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg border border-green-200 dark:border-green-800">
        <div class="text-2xl font-bold text-green-600 dark:text-green-400">{{ zameldowaniZawodnicy }}</div>
        <div class="text-sm text-green-700 dark:text-green-300">Zameldowanych</div>
      </div>
      
      <div class="bg-orange-50 dark:bg-orange-900/20 p-4 rounded-lg border border-orange-200 dark:border-orange-800">
        <div class="flex items-center space-x-2">
          <div class="text-2xl font-bold text-orange-600 dark:text-orange-400">{{ kolejkaStatus.total }}</div>
          <div v-if="appState.loading" class="animate-spin">
            <ArrowPathIcon class="h-4 w-4 text-orange-500" />
          </div>
        </div>
        <div class="text-sm text-orange-700 dark:text-orange-300">W kolejce</div>
      </div>
      
      <div class="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg border border-purple-200 dark:border-purple-800">
        <div class="flex items-center space-x-2">
          <div class="text-2xl font-bold text-purple-600 dark:text-purple-400">
            {{ currentActiveGroup ? currentActiveGroup.numer_grupy : '-' }}
          </div>
          <div v-if="appState.activatingGroupId" class="animate-pulse">
            <div class="w-2 h-2 bg-purple-500 rounded-full"></div>
          </div>
          <div v-else-if="appState.syncingData" class="animate-spin">
            <ArrowPathIcon class="h-4 w-4 text-purple-500" />
          </div>
        </div>
        <div class="text-sm text-purple-700 dark:text-purple-300">
          Aktywna grupa
          <span v-if="appState.activatingGroupId" class="text-xs text-orange-600">(aktywuję...)</span>
          <span v-else-if="appState.syncingData" class="text-xs text-blue-600">(sync...)</span>
        </div>
      </div>
    </div>

    <!-- Główny layout - dwie kolumny -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      
      <!-- Lewa kolumna: Zarządzanie grupami -->
      <div class="space-y-6">
        
        <!-- Aktywna grupa -->
        <div v-if="currentActiveGroup" class="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
          <div class="flex items-center justify-between">
      <div class="flex items-center space-x-3">
              <UsersIcon class="h-6 w-6 text-green-600 dark:text-green-400" />
        <div>
                <h4 class="font-medium text-green-800 dark:text-green-200">
                  {{ currentActiveGroup.nazwa }}
                  <span v-if="appState.activatingGroupId" class="text-xs text-orange-600">(aktywuję...)</span>
                  <span v-else-if="appState.syncingData" class="text-xs text-blue-600">(sync...)</span>
          </h4>
                <p class="text-sm text-green-700 dark:text-green-300">
                  {{ currentActiveGroup.liczba_zawodnikow }} zawodników
          </p>
              </div>
        </div>
        <button 
          @click="clearAktywnaGrupa" 
              :disabled="appState.activatingGroupId"
              class="text-green-600 hover:text-green-800 dark:text-green-400 dark:hover:text-green-200 p-1 disabled:opacity-50 disabled:cursor-not-allowed"
        >
              <XMarkIcon class="h-5 w-5" />
        </button>
      </div>
    </div>

        <!-- Lista grup startowych -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
          <div class="p-4 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-700">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
              Grupy startowe ({{ totalGrup }})
            </h3>
          </div>
          
          <div v-if="appState.loading" class="p-8 text-center text-gray-500 dark:text-gray-400">
            <ArrowPathIcon class="h-8 w-8 animate-spin mx-auto mb-2" />
            <div>Ładowanie grup...</div>
          </div>
          
          <div v-else-if="grupy.length === 0" class="p-8 text-center text-gray-500 dark:text-gray-400">
            <div class="text-4xl mb-2">🏁</div>
            <div class="text-lg font-medium mb-1">Brak grup startowych</div>
            <div class="text-sm">Upewnij się że zawodnicy są zameldowani</div>
          </div>
          
          <div v-else class="divide-y divide-gray-200 dark:divide-gray-700 max-h-96 overflow-y-auto">
            <div v-for="grupa in grupy" :key="grupa.numer_grupy" 
                 class="p-4 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-200">
              
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-3">
                  <div class="w-8 h-8 bg-blue-100 dark:bg-blue-900 rounded-full flex items-center justify-center">
                    <span class="text-blue-600 dark:text-blue-400 font-bold text-sm">{{ grupa.numer_grupy }}</span>
                  </div>
                  <div>
                    <h4 class="font-medium text-gray-900 dark:text-white text-sm">{{ grupa.nazwa }}</h4>
                    <p class="text-xs text-gray-600 dark:text-gray-400">
                      {{ grupa.liczba_zawodnikow }} zawodników • ~{{ Math.round(grupa.estimated_time / 60) }} min
                    </p>
                  </div>
                </div>
                
                <button 
                  @click="setAktywnaGrupa(grupa)"
                  :disabled="getGroupButtonState(grupa).isDisabled"
                  :class="[
                    'inline-flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 shadow-sm border',
                    getGroupButtonState(grupa).isActive
                      ? 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800 text-green-800 dark:text-green-200 cursor-not-allowed'
                      : getGroupButtonState(grupa).isActivating
                      ? 'bg-orange-50 dark:bg-orange-900/20 border-orange-200 dark:border-orange-800 text-orange-800 dark:text-orange-200 cursor-not-allowed'
                      : 'bg-blue-600 border-blue-600 text-white hover:bg-blue-700 hover:border-blue-700 hover:shadow-md active:transform active:scale-95'
                  ]"
                >
                  <!-- Ikona stanu -->
                  <CheckCircleIcon v-if="getGroupButtonState(grupa).isActive" class="h-4 w-4" />
                  <ArrowPathIcon v-else-if="getGroupButtonState(grupa).isActivating" class="h-4 w-4 animate-spin" />
                  <PlayIcon v-else class="h-4 w-4" />
                  
                  <span>{{ getGroupButtonState(grupa).text }}</span>
                </button>
              </div>
              
              <!-- Rozwijane szczegóły -->
              <div v-if="selectedGrupa === grupa.numer_grupy" class="mt-3 pt-3 border-t border-gray-200 dark:border-gray-600">
                <div class="text-xs text-gray-600 dark:text-gray-400">
                  <strong>Zawodnicy:</strong> {{ grupa.numery_startowe }}
                </div>
              </div>
              
              <button 
                @click="toggleGrupaDetails(grupa.numer_grupy)"
                class="mt-2 text-xs text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-200"
              >
                {{ selectedGrupa === grupa.numer_grupy ? 'Ukryj szczegóły' : 'Pokaż szczegóły' }}
              </button>
            </div>
          </div>
        </div>

        <!-- Szybkie akcje -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4">
          <h4 class="font-medium text-gray-900 dark:text-white mb-3">Zarządzanie kolejką</h4>
          <div class="flex flex-wrap gap-2">
            <button 
              @click="clearQueue('all')"
              :disabled="appState.loading"
              class="px-3 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium flex items-center space-x-1"
            >
              <span v-if="appState.loading">🔄</span>
              <span>Usuń wszystkie grupy</span>
            </button>
            <button 
              @click="clearQueue('scanned')"
              :disabled="appState.loading"
              class="px-3 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium flex items-center space-x-1"
            >
              <span v-if="appState.loading">🔄</span>
              <span>Usuń skanowanych</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Prawa kolumna: QR Scanner i kolejka -->
      <div class="space-y-6">
        
        <!-- QR Scanner -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
      <div class="text-center">
            <div class="w-16 h-16 mx-auto mb-4 bg-green-100 dark:bg-green-900/20 rounded-full flex items-center justify-center">
              <QrCodeIcon class="h-8 w-8 text-green-600 dark:text-green-400" />
        </div>
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              QR Scanner
        </h3>
            <p class="text-gray-600 dark:text-gray-400 mb-4 text-sm">
              Zeskanuj QR kod lub wpisz numer startowy
        </p>
        
        <div class="max-w-md mx-auto">
          <div class="flex space-x-2">
            <input
              v-model="manualQrCode"
                  @keyup.enter="handleQRCode"
              type="text"
                  placeholder="QR kod lub nr startowy..."
                  class="flex-1 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 text-sm"
            />
            <button
                  @click="handleQRCode"
                  :disabled="!manualQrCode || appState.loading"
                  class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium text-sm"
                >
                  {{ appState.loading ? '⏳' : 'Skanuj' }}
            </button>
          </div>
        </div>
      </div>
    </div>

        <!-- Weryfikacja wyniku -->
    <div v-if="lastVerification" class="mb-6">
          <div :class="getVerificationClass(lastVerification.action)" class="rounded-lg p-4">
            <div class="flex items-start space-x-3">
            <div :class="getIconClass(lastVerification.action)">
                <component :is="getIconComponent(lastVerification.action)" class="h-6 w-6" />
          </div>
          <div class="flex-1">
                <h4 class="font-semibold mb-2" :class="getTextClass(lastVerification.action)">
              {{ lastVerification.komunikat }}
            </h4>
                <div class="text-sm opacity-90">
                  <strong>Nr:</strong> {{ lastVerification.zawodnik.nr_startowy }} • 
                  <strong>Imię:</strong> {{ lastVerification.zawodnik.imie }} {{ lastVerification.zawodnik.nazwisko }}
              </div>
                <div class="flex space-x-2 mt-3">
              <button
                v-if="lastVerification.action === 'AKCEPTUJ'"
                @click="confirmStart"
                    class="px-3 py-1 bg-white text-green-800 rounded-md hover:bg-green-50 text-sm font-medium border border-green-200"
                  >
                    ✅ Potwierdź
              </button>
              <button
                @click="clearVerification"
                    class="px-3 py-1 bg-white/20 hover:bg-white/30 rounded-md text-sm font-medium border border-white/30"
              >
                Wyczyść
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

        <!-- Kolejka startowa -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
      <div class="p-4 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-700 flex items-center justify-between">
            <div>
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                Kolejka startowa ({{ currentActiveGroup ? currentActiveGroup.nazwa : `${kolejka_zawodnikow.length} zawodników` }})
        </h3>
              <div v-if="currentActiveGroup" class="text-sm text-gray-600 dark:text-gray-400">
                {{ kolejka_zawodnikow.length }} zawodników w kolejce
                <span v-if="appState.syncingQueue" class="text-blue-600 dark:text-blue-400">• synchronizuję...</span>
                <span v-else-if="appState.syncingData" class="text-orange-600 dark:text-orange-400">• ładuję dane...</span>
              </div>
            </div>
            <div class="flex items-center space-x-2">
              <div v-if="appState.syncingQueue" class="text-xs text-blue-600 dark:text-blue-400 flex items-center space-x-1">
                <ArrowPathIcon class="h-3 w-3 animate-spin" />
                <span>Sync kolejki</span>
              </div>
              <div v-else-if="appState.syncingData" class="text-xs text-orange-600 dark:text-orange-400 flex items-center space-x-1">
                <ArrowPathIcon class="h-3 w-3 animate-spin" />
                <span>Sync danych</span>
              </div>
              <div v-else-if="appState.loading" class="text-xs text-orange-600 dark:text-orange-400 flex items-center space-x-1">
                <ArrowPathIcon class="h-3 w-3 animate-spin" />
                <span>Sync...</span>
              </div>
            </div>
          </div>
          
          <div v-if="appState.syncingQueue || appState.syncingData" class="p-6 text-center text-gray-500 dark:text-gray-400">
            <ArrowPathIcon class="h-8 w-8 animate-spin mx-auto mb-2 text-blue-500" />
            <div class="text-lg font-medium mb-1">
              <span v-if="appState.syncingQueue">Synchronizuję kolejkę...</span>
              <span v-else>Ładuję dane...</span>
            </div>
            <div class="text-sm">Aktualny stan może się zmienić</div>
      </div>
      
          <div v-else-if="kolejka_zawodnikow.length === 0" class="p-8 text-center text-gray-500 dark:text-gray-400">
        <div class="text-4xl mb-2">🏁</div>
        <div class="text-lg font-medium mb-1">Kolejka pusta</div>
            <div class="text-sm">Zawodnicy pojawią się po skanowaniu lub aktywacji grupy</div>
      </div>
      
          <div v-else class="divide-y divide-gray-200 dark:divide-gray-700 max-h-96 overflow-y-auto">
            <div v-for="(zawodnik, index) in kolejka_zawodnikow" :key="zawodnik.nr_startowy"
                 class="p-3 flex items-center justify-between hover:bg-gray-50 dark:hover:bg-gray-700">
              <div class="flex items-center space-x-3">
                <div class="w-6 h-6 bg-blue-100 dark:bg-blue-900 rounded-full flex items-center justify-center">
                  <span class="text-blue-600 dark:text-blue-400 font-bold text-xs">{{ index + 1 }}</span>
            </div>
            <div>
                  <p class="font-medium text-gray-900 dark:text-white text-sm">
                #{{ zawodnik.nr_startowy }} {{ zawodnik.imie }} {{ zawodnik.nazwisko }}
                    <span v-if="zawodnik.source_type === 'AKTYWNA_GRUPA'"
                          class="ml-2 px-2 py-0.5 text-xs rounded-full bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">
                      Grupa
                    </span>
                    <span v-else-if="zawodnik.source_type === 'SKANOWANY'"
                          class="ml-2 px-2 py-0.5 text-xs rounded-full bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200">
                      Skan
                    </span>
                    <span v-else-if="zawodnik.source_type === 'AKTYWNA_GRUPA_I_SKANOWANY'"
                          class="ml-2 px-2 py-0.5 text-xs rounded-full bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200">
                      Grupa+Skan
                    </span>
                  </p>
                  <p class="text-xs text-gray-500 dark:text-gray-400">
                    {{ zawodnik.kategoria }} {{ zawodnik.plec }} - {{ zawodnik.klub }}
              </p>
            </div>
          </div>
              
              <button
                @click="removeFromQueue(zawodnik)"
                class="p-1 text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-200 hover:bg-red-50 dark:hover:bg-red-900/20 rounded"
              >
                <TrashIcon class="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { 
  QrCodeIcon, 
  UsersIcon,
  ArrowPathIcon,
  XMarkIcon,
  TrashIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  XCircleIcon,
  PlayIcon
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

interface Zawodnik {
  nr_startowy: number
  imie: string
  nazwisko: string
  kategoria: string
  plec: string
  klub: string
  ostatni_skan?: string
  czas_przejazdu_s?: number
  status?: string
  source_type: string
}

interface VerificationResult {
  success: boolean
  action: 'AKCEPTUJ' | 'OSTRZEZENIE' | 'ODRZUC'
  issues: string[]
  zawodnik: any
  komunikat: string
}

// State management - CENTRALIZED
const appState = ref({
  loading: false,
  error: null,
  lastUpdate: null,
  optimisticActiveGroupId: null,
  syncingData: false,
  syncingQueue: false,
  activatingGroupId: null
})

const grupy = ref<Grupa[]>([])
const aktualna_grupa = ref<Grupa | null>(null)
const kolejka_zawodnikow = ref<Zawodnik[]>([])
const selectedGrupa = ref<number | null>(null)
const manualQrCode = ref('')
const lastVerification = ref<VerificationResult | null>(null)
const apiVersion = ref('32.0.0')

// NOWY: Stan statusów grup z backendu
const grupyStatuses = ref<Record<string, { is_active: boolean; count: number }>>({})

// Computed properties
const totalZawodnikow = computed(() => {
  return grupy.value.reduce((sum, g) => sum + g.liczba_zawodnikow, 0)
})

const totalGrup = computed(() => grupy.value.length)

const zameldowaniZawodnicy = computed(() => {
  return grupy.value.reduce((sum, g) => sum + g.liczba_zawodnikow, 0)
})

const kolejkaStatus = computed(() => {
  const total = kolejka_zawodnikow.value.length
  const skanowani = kolejka_zawodnikow.value.filter(z => z.source_type === 'SKANOWANY').length
  const aktywnaGrupa = kolejka_zawodnikow.value.filter(z => z.source_type === 'AKTYWNA_GRUPA').length
  
  return { total, skanowani, aktywnaGrupa }
})

// TOGGLE: Aktywacja/Deaktywacja grupy z systemem toggle
const setAktywnaGrupa = async (grupa: Grupa) => {
  if (!grupa || appState.value.activatingGroupId) return
  
  const groupKey = `${grupa.kategoria}_${grupa.plec}`
  const isCurrentlyActive = grupyStatuses.value[groupKey]?.is_active || false
  const action = isCurrentlyActive ? 'deaktywacja' : 'aktywacja'
  
  console.log(`🎯 ${action} grupy:`, grupa.nazwa, { currentlyActive: isCurrentlyActive })
  
  // OPTYMISTIC UPDATE: Od razu zaktualizuj UI
  appState.value.activatingGroupId = grupa.numer_grupy
  appState.value.error = null
  
  // Optymistyczna aktualizacja statusu
  if (grupyStatuses.value[groupKey]) {
    grupyStatuses.value[groupKey].is_active = !isCurrentlyActive
  }
  
  try {
    const response = await fetch('/api/grupa-aktywna', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        kategoria: grupa.kategoria,
        plec: grupa.plec,
        nazwa: grupa.nazwa
      })
    })
    
    if (!response.ok) {
      const errorText = await response.text()
      throw new Error(`Backend error: ${response.status} - ${errorText}`)
    }
    
    const result = await response.json()
    console.log(`✅ ${result.action === 'added' ? 'Dodano' : 'Usunięto'} grupę:`, grupa.nazwa)
    
    // Synchronizuj dane w tle
    setTimeout(async () => {
      appState.value.syncingData = true
      try {
        await syncAllData('po toggle grupy')
      } finally {
        appState.value.syncingData = false
      }
    }, 300)
    
  } catch (error) {
    console.error('❌ Błąd toggle grupy:', error)
    
    // ROLLBACK: Cofnij optymistyczną zmianę
    if (grupyStatuses.value[groupKey]) {
      grupyStatuses.value[groupKey].is_active = isCurrentlyActive
    }
    
    appState.value.error = error.message
    console.error(`Błąd: ${error.message}`)
  } finally {
    appState.value.activatingGroupId = null
  }
}

// IMPROVED: Clear z optymistyczną aktualizacją
const clearAktywnaGrupa = async () => {
  if (appState.value.activatingGroupId) return
  
  console.log('🧹 Czyszczenie aktywnej grupy...')
  
  // OPTYMISTIC UPDATE
  const previousGroup = aktualna_grupa.value
  aktualna_grupa.value = null
  appState.value.optimisticActiveGroupId = null
  appState.value.activatingGroupId = -1  // Specjalna wartość dla czyszczenia
  
  try {
    const response = await fetch('/api/grupa-aktywna', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ clear: true })
    })
    
    if (!response.ok) throw new Error('Błąd czyszczenia grupy')
    
    // Synchronizuj w tle
    setTimeout(async () => {
      appState.value.syncingData = true
      try {
        await syncAllData('po wyczyszczeniu grupy')
      } finally {
        appState.value.syncingData = false
      }
    }, 500)
    
    console.log('🧹 Wyczyszczono aktywną grupę')
    
  } catch (error) {
    console.error('❌ Błąd czyszczenia grupy:', error)
    // ROLLBACK
    aktualna_grupa.value = previousGroup
    appState.value.optimisticActiveGroupId = previousGroup?.numer_grupy || null
    appState.value.error = error.message
    console.error(`Błąd: ${error.message}`)
  } finally {
    appState.value.activatingGroupId = null
  }
}

// IMPROVED: Sync z lepszymi loading states
const syncAllData = async (reason = 'manual') => {
  console.log(`🔄 Synchronizacja danych: ${reason}`)
  
  // Różne loading states dla różnych powodów
  if (reason === 'manual') {
    if (appState.value.loading) return
    appState.value.loading = true
  } else if (reason.includes('kolejka') || reason.includes('queue')) {
    appState.value.syncingQueue = true
  } else {
    appState.value.syncingData = true
  }
  
  appState.value.error = null
  
  try {
    // 1. API Version (tylko raz przy starcie)
    if (!apiVersion.value || apiVersion.value === '32.0.0') {
      try {
        const versionResponse = await fetch('/api/version')
        if (versionResponse.ok) {
          const versionData = await versionResponse.json()
          apiVersion.value = versionData.version || '32.0.0'
        }
      } catch (e) {
        console.warn('⚠️ Nie można pobrać wersji API')
      }
    }
    
    // 2. Grupy startowe
    const grupyResponse = await fetch(`/api/grupy-startowe?_t=${Date.now()}`)
    if (!grupyResponse.ok) throw new Error('Błąd ładowania grup')
    const grupyData = await grupyResponse.json()
    grupy.value = grupyData.grupy || []
    
    // 3. Aktywna grupa - ZAWSZE ładuj z backend (cache-busting)
    {
      try {
        const aktywnaResponse = await fetch(`/api/grupa-aktywna?_t=${Date.now()}`)
        if (aktywnaResponse.ok) {
          const aktywnaData = await aktywnaResponse.json()
          if (aktywnaData.success && aktywnaData.aktywna_grupa) {
            const grupaData = aktywnaData.aktywna_grupa
            aktualna_grupa.value = grupy.value.find(g => 
              g.kategoria === grupaData.kategoria && g.plec === grupaData.plec
            ) || null
          } else {
            aktualna_grupa.value = null
          }
        } else {
          aktualna_grupa.value = null
        }
      } catch (e) {
        console.warn('⚠️ Błąd ładowania aktywnej grupy:', e)
        if (!appState.value.optimisticActiveGroupId) {
          aktualna_grupa.value = null
        }
      }
    }
    
    // 4. Statusy grup (dla przycisków toggle)
    try {
      const statusyResponse = await fetch(`/api/start-queue/all-group-statuses?_t=${Date.now()}`)
      if (statusyResponse.ok) {
        const statusyData = await statusyResponse.json()
        grupyStatuses.value = statusyData.statuses || {}
      }
    } catch (e) {
      console.warn('⚠️ Błąd ładowania statusów grup:', e)
    }

    // 5. Kolejka startowa
    const kolejkaResponse = await fetch(`/api/start-queue?_t=${Date.now()}`)
    if (!kolejkaResponse.ok) throw new Error('Błąd ładowania kolejki')
    const kolejkaData = await kolejkaResponse.json()
    kolejka_zawodnikow.value = kolejkaData.queue || []
    
    appState.value.lastUpdate = new Date()
    console.log('✅ Synchronizacja zakończona:', {
      grupy: grupy.value.length,
      aktualna_grupa: aktualna_grupa.value?.nazwa || `ID:${appState.value.optimisticActiveGroupId}` || 'brak',
      kolejka: kolejka_zawodnikow.value.length
    })
    
  } catch (error) {
    console.error('❌ Błąd synchronizacji:', error)
    appState.value.error = error.message
  } finally {
    // Wyczyść wszystkie loading states
    if (reason === 'manual') {
      appState.value.loading = false
    }
    appState.value.syncingData = false
    appState.value.syncingQueue = false
  }
}

// SIMPLIFIED: QR Code handling
const handleQRCode = async () => {
  if (!manualQrCode.value || appState.value.loading) return
  
  appState.value.loading = true
  try {
    const response = await fetch('/api/start-line-verify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        qr_code: manualQrCode.value,
        kategoria: aktualna_grupa.value?.kategoria,
        plec: aktualna_grupa.value?.plec,
        device_id: 'start-line-scanner-v30.4'
      })
    })
    
    if (response.ok) {
      const data = await response.json()
      lastVerification.value = data
      manualQrCode.value = ''
      await syncAllData('po skanie QR')
    } else {
      const error = await response.json()
      lastVerification.value = {
        success: false,
        action: 'ODRZUC',
        issues: [error.error || 'Nieznany błąd'],
        zawodnik: {},
        komunikat: '❌ Błąd weryfikacji'
      }
    }
  } catch (error) {
    console.error('Błąd QR:', error)
    lastVerification.value = {
      success: false,
      action: 'ODRZUC', 
      issues: ['Błąd połączenia z serwerem'],
      zawodnik: {},
      komunikat: '❌ Błąd połączenia'
    }
  } finally {
    appState.value.loading = false
  }
}

// IMPROVED: Remove z optymistyczną aktualizacją
const removeFromQueue = async (zawodnik: Zawodnik) => {
  
  // if (!confirm(...)) return  // USUNIĘTO DIALOG
  
  // OPTYMISTIC UPDATE: Od razu usuń z lokalnej listy
  const originalQueue = [...kolejka_zawodnikow.value]
  kolejka_zawodnikow.value = kolejka_zawodnikow.value.filter(z => z.nr_startowy !== zawodnik.nr_startowy)
  
  try {
    const response = await fetch(`/api/start-queue/remove/${zawodnik.nr_startowy}`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' }
    })
    
    if (response.ok) {
      // Synchronizuj w tle dla pewności
      setTimeout(async () => {
        appState.value.syncingQueue = true
        try {
          const kolejkaResponse = await fetch(`/api/start-queue?_t=${Date.now()}`)
          if (kolejkaResponse.ok) {
            const kolejkaData = await kolejkaResponse.json()
            kolejka_zawodnikow.value = kolejkaData.queue || []
          }
        } finally {
          appState.value.syncingQueue = false
        }
      }, 1000)
      
      console.log(`Usunięto zawodnika #${zawodnik.nr_startowy} z kolejki`)
    } else {
      const error = await response.json()
      throw new Error(error.message || 'Błąd usuwania')
    }
  } catch (error) {
    console.error('Błąd usuwania:', error)
    // ROLLBACK: Przywróć oryginalną kolejkę
    kolejka_zawodnikow.value = originalQueue
    console.error(`Błąd: ${error.message}`)
  }
}

// ENHANCED: Clear queue - usuwa wszystkie grupy z kolejki
const clearQueue = async (type: 'all' | 'scanned') => {
  console.log(`🧹 Czyszczenie kolejki: ${type}`)
  
  // OPTYMISTIC UPDATE: Od razu wyczyść lokalny stan
  const originalQueue = [...kolejka_zawodnikow.value]
  const originalStatuses = { ...grupyStatuses.value }
  
  if (type === 'all') {
    // Wyczyść wszystko
    kolejka_zawodnikow.value = []
    // Ustaw wszystkie grupy jako nieaktywne
    Object.keys(grupyStatuses.value).forEach(key => {
      if (grupyStatuses.value[key]) {
        grupyStatuses.value[key].is_active = false
        grupyStatuses.value[key].count = 0
      }
    })
  } else if (type === 'scanned') {
    // Usuń tylko skanowanych
    kolejka_zawodnikow.value = kolejka_zawodnikow.value.filter(z => z.source_type !== 'SKANOWANY')
  }
  
  appState.value.loading = true
  try {
    const response = await fetch('/api/start-queue/clear', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type })
    })
    
    if (response.ok) {
      const result = await response.json()
      console.log(`✅ ${result.message}`)
      
      // Synchronizuj dane w tle żeby potwierdzić zmiany
      setTimeout(async () => {
        appState.value.syncingData = true
        try {
          await syncAllData('po czyszczeniu kolejki')
        } finally {
          appState.value.syncingData = false
        }
      }, 500)
    } else {
      throw new Error('Błąd czyszczenia kolejki')
    }
  } catch (error) {
    console.error('❌ Błąd czyszczenia kolejki:', error)
    
    // ROLLBACK: Przywróć oryginalny stan
    kolejka_zawodnikow.value = originalQueue
    grupyStatuses.value = originalStatuses
    
    console.error(`Błąd: ${error.message}`)
  } finally {
    appState.value.loading = false
  }
}

// Helper functions
const toggleGrupaDetails = (numer_grupy: number) => {
  selectedGrupa.value = selectedGrupa.value === numer_grupy ? null : numer_grupy
}

const confirmStart = () => {
  lastVerification.value = null
}

const clearVerification = () => {
  lastVerification.value = null
}

const showSuccess = (message: string) => {
  console.log(`✅ ${message}`)
  // Tu można dodać toast notification
}

const showError = (message: string) => {
  console.error(`❌ ${message}`)
  // Tu można dodać toast notification
}

// Verification UI helpers
const getVerificationClass = (action: string) => {
  switch (action) {
    case 'AKCEPTUJ': return 'bg-green-100 dark:bg-green-900/20 border border-green-200 dark:border-green-800'
    case 'OSTRZEZENIE': return 'bg-orange-100 dark:bg-orange-900/20 border border-orange-200 dark:border-orange-800'
    case 'ODRZUC': return 'bg-red-100 dark:bg-red-900/20 border border-red-200 dark:border-red-800'
    default: return 'bg-gray-100 dark:bg-gray-700 border border-gray-200 dark:border-gray-600'
  }
}

const getIconClass = (action: string) => {
  switch (action) {
    case 'AKCEPTUJ': return 'w-8 h-8 bg-green-600 rounded-full flex items-center justify-center text-white'
    case 'OSTRZEZENIE': return 'w-8 h-8 bg-orange-600 rounded-full flex items-center justify-center text-white'
    case 'ODRZUC': return 'w-8 h-8 bg-red-600 rounded-full flex items-center justify-center text-white'
    default: return 'w-8 h-8 bg-gray-600 rounded-full flex items-center justify-center text-white'
  }
}

const getTextClass = (action: string) => {
  switch (action) {
    case 'AKCEPTUJ': return 'text-green-800 dark:text-green-200'
    case 'OSTRZEZENIE': return 'text-orange-800 dark:text-orange-200'
    case 'ODRZUC': return 'text-red-800 dark:text-red-200'
    default: return 'text-gray-800 dark:text-gray-200'
  }
}

const getIconComponent = (action: string) => {
  switch (action) {
    case 'AKCEPTUJ': return CheckCircleIcon
    case 'OSTRZEZENIE': return ExclamationTriangleIcon
    case 'ODRZUC': return XCircleIcon
    default: return QrCodeIcon
  }
}

// Computed: Aktywna grupa z optymistyczną aktualizacją
const currentActiveGroup = computed(() => {
  // Jeśli mamy optymistyczną aktywną grupę, znajdź ją w liście grup
  if (appState.value.optimisticActiveGroupId) {
    return grupy.value.find(g => g.numer_grupy === appState.value.optimisticActiveGroupId) || aktualna_grupa.value
  }
  return aktualna_grupa.value
})

// TOGGLE: Helper do sprawdzania stanu przycisku grupy na podstawie statusów z backendu
const getGroupButtonState = (grupa: Grupa) => {
  const groupKey = `${grupa.kategoria}_${grupa.plec}`
  const isActive = grupyStatuses.value[groupKey]?.is_active || false
  const isActivating = appState.value.activatingGroupId === grupa.numer_grupy
  const isAnyActivating = appState.value.activatingGroupId !== null
  
  return {
    isActive: isActive && !isActivating,
    isActivating: isActivating,
    isDisabled: isAnyActivating,
    text: isActivating ? 'Przetwarzam...' : isActive ? 'Aktywna' : 'Aktywuj',
    showSpinner: isActivating
  }
}

// Lifecycle
onMounted(async () => {
  await syncAllData('inicjalizacja')
})

onUnmounted(() => {
  // Cleanup jeśli potrzebny
})
</script> 