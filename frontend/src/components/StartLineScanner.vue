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
          <span :class="cameraActive ? 'text-green-600' : 'text-red-600'">
            {{ cameraActive ? '🟢 Aktywny' : '🔴 Nieaktywny' }}
          </span>
        </div>
        <button 
          @click="refreshAll"
          :disabled="loading"
          class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2 text-sm font-medium transition-colors duration-200"
        >
          <ArrowPathIcon class="h-5 w-5" :class="{ 'animate-spin': loading }" />
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
          <div v-if="syncing" class="animate-spin">
            <ArrowPathIcon class="h-4 w-4 text-orange-500" />
          </div>
        </div>
        <div class="text-sm text-orange-700 dark:text-orange-300">W kolejce</div>
      </div>
      
      <div class="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg border border-purple-200 dark:border-purple-800">
        <div class="flex items-center space-x-2">
          <div class="text-2xl font-bold text-purple-600 dark:text-purple-400">
            {{ aktualna_grupa ? aktualna_grupa.numer_grupy : '-' }}
          </div>
          <div v-if="syncing" class="animate-pulse">
            <div class="w-2 h-2 bg-purple-500 rounded-full"></div>
          </div>
        </div>
        <div class="text-sm text-purple-700 dark:text-purple-300">Aktywna grupa</div>
      </div>
    </div>

    <!-- Główny layout - dwie kolumny -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      
      <!-- Lewa kolumna: Zarządzanie grupami -->
      <div class="space-y-6">
        
        <!-- Aktywna grupa -->
        <div v-if="aktualna_grupa" class="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <UsersIcon class="h-6 w-6 text-green-600 dark:text-green-400" />
              <div>
                <h4 class="font-medium text-green-800 dark:text-green-200">{{ aktualna_grupa.nazwa }}</h4>
                <p class="text-sm text-green-700 dark:text-green-300">
                  {{ aktualna_grupa.liczba_zawodnikow }} zawodników
                </p>
              </div>
            </div>
            <button 
              @click="clearAktywnaGrupa" 
              class="text-green-600 hover:text-green-800 dark:text-green-400 dark:hover:text-green-200 p-1"
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
          
          <div v-if="loading" class="p-8 text-center text-gray-500 dark:text-gray-400">
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
                  :disabled="aktualna_grupa?.numer_grupy === grupa.numer_grupy"
                  :class="[
                    'px-3 py-1 rounded-md text-xs font-medium transition-colors duration-200',
                    aktualna_grupa?.numer_grupy === grupa.numer_grupy
                      ? 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 cursor-not-allowed'
                      : 'bg-blue-600 text-white hover:bg-blue-700'
                  ]"
                >
                  {{ aktualna_grupa?.numer_grupy === grupa.numer_grupy ? 'Aktywna' : 'Aktywuj' }}
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
              class="px-3 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 text-sm font-medium"
            >
              Wyczyść kolejkę
            </button>
            <button 
              @click="clearQueue('scanned')"
              class="px-3 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 text-sm font-medium"
            >
              Usuń skanowanych
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
                  :disabled="!manualQrCode || processing"
                  class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium text-sm"
                >
                  {{ processing ? '⏳' : 'Skanuj' }}
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
                Kolejka startowa ({{ aktualna_grupa ? aktualna_grupa.nazwa : `${kolejka_zawodnikow.length} zawodników` }})
              </h3>
              <div v-if="aktualna_grupa" class="text-sm text-gray-600 dark:text-gray-400">
                {{ kolejka_zawodnikow.length }} zawodników w kolejce
              </div>
            </div>
            <div class="flex items-center space-x-2">
              <div v-if="syncing" class="text-xs text-orange-600 dark:text-orange-400 flex items-center space-x-1">
                <ArrowPathIcon class="h-3 w-3 animate-spin" />
                <span>Sync...</span>
              </div>
            </div>
          </div>
          
          <div v-if="kolejka_zawodnikow.length === 0" class="p-8 text-center text-gray-500 dark:text-gray-400">
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
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { 
  QrCodeIcon, 
  UsersIcon,
  ArrowPathIcon,
  XMarkIcon,
  TrashIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  XCircleIcon
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

// State management - uproszczony
const grupy = ref<Grupa[]>([])
const aktualna_grupa = ref<Grupa | null>(null)
const kolejka_zawodnikow = ref<Zawodnik[]>([])
const selectedGrupa = ref<number | null>(null)
const manualQrCode = ref('')
const lastVerification = ref<VerificationResult | null>(null)
const loading = ref(false)
const processing = ref(false)
const syncing = ref(false)
const cameraActive = ref(true)
const apiVersion = ref('30.3.7') // Fallback version

// Auto-refresh WYŁĄCZONY - nie potrzebny
// let queueRefreshTimer: number | null = null
// const refreshInterval = ref(8000) // 8 sekund

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

// SIMPLIFIED: Direct API calls bez cache
const loadApiVersion = async () => {
  try {
    const response = await fetch('/api/version')
    if (response.ok) {
      const data = await response.json()
      if (data.version) {
        apiVersion.value = data.version
        console.log('✅ API Version:', data.version)
      }
    }
  } catch (error) {
    console.warn('⚠️ Nie można pobrać wersji API, używam fallback:', error)
  }
}

const loadGrupy = async () => {
  try {
    const response = await fetch('/api/grupy-startowe?' + Date.now()) // Force fresh data
    if (response.ok) {
      const data = await response.json()
      if (data.success) {
        grupy.value = data.grupy || []
        console.log('✅ Załadowano grupy:', grupy.value.length)
        return true
      }
    }
    console.error('❌ Błąd ładowania grup')
    return false
  } catch (error) {
    console.error('❌ Błąd ładowania grup:', error)
    return false
  }
}

const loadKolejka = async () => {
  try {
    // Timeout dla wolnych połączeń Heroku  
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), 15000) // 15 sekund timeout
    
    const response = await fetch('/api/start-queue?' + Date.now(), {
      signal: controller.signal
    })
    
    clearTimeout(timeoutId)
    
    if (response.ok) {
      const data = await response.json()
      if (data.success) {
        kolejka_zawodnikow.value = data.queue || []
        
        console.log('🔄 Kolejka załadowana:', {
          total: kolejka_zawodnikow.value.length,
          aktywna_grupa_backend: data.aktywna_grupa?.nazwa || 'null',
          aktywna_grupa_frontend: aktualna_grupa.value?.nazwa || 'null'
        })
        
        return true
      }
    }
    console.error('❌ Błąd ładowania kolejki')
    return false
  } catch (error) {
    if (error.name === 'AbortError') {
      console.error('⏱️ Timeout ładowania kolejki')
    } else {
      console.error('❌ Błąd ładowania kolejki:', error)
    }
    return false
  }
}

const loadAktywnaGrupa = async () => {
  try {
    const response = await fetch('/api/grupa-aktywna?' + Date.now()) // Force fresh data
    if (response.ok) {
      const data = await response.json()
      if (data.success && data.aktywna_grupa) {
        const grupaData = data.aktywna_grupa
        const grupa = grupy.value.find(g => 
          g.kategoria === grupaData.kategoria && g.plec === grupaData.plec
        )
        aktualna_grupa.value = grupa || null
        console.log('✅ Aktywna grupa z API:', aktualna_grupa.value?.nazwa || 'brak')
        return true
      } else {
        aktualna_grupa.value = null
        console.log('✅ Brak aktywnej grupy')
        return true
      }
    } else if (response.status === 404) {
      aktualna_grupa.value = null
      console.log('✅ Brak aktywnej grupy (404)')
      return true
    }
    return false
  } catch (error) {
    console.error('❌ Błąd ładowania aktywnej grupy:', error)
    return false
  }
}

// SIMPLIFIED: Manual refresh - tylko przez przycisk
const refreshAll = async () => {
  if (loading.value) return
  
  loading.value = true
  console.log('🔄 Odświeżanie wszystkich danych...')
  
  try {
    // Sequence: grupy → aktywna grupa → kolejka  
    const groupsLoaded = await loadGrupy()
    if (groupsLoaded) {
      await loadAktywnaGrupa()
      await loadKolejka()
    }
    console.log('✅ Odświeżanie zakończone')
    return groupsLoaded
  } finally {
    loading.value = false
  }
}

// OPTIMIZED: Aktywacja grupy z timeout handling dla Heroku
const setAktywnaGrupa = async (grupa: Grupa) => {
  if (!grupa || processing.value) return
  
  console.log('🎯 Aktywacja grupy:', grupa.nazwa)
  
  try {
    processing.value = true
    syncing.value = true
    
    // Timeout controller dla wolnych połączeń Heroku
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), 25000) // 25 sekund timeout
    
    const response = await fetch('/api/grupa-aktywna', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        numer_grupy: grupa.numer_grupy,
        kategoria: grupa.kategoria,
        plec: grupa.plec,
        nazwa: grupa.nazwa
      }),
      signal: controller.signal
    })
    
    clearTimeout(timeoutId)
    
    if (response.ok) {
      const result = await response.json()
      console.log('✅ Backend potwierdził aktywację:', result)
      
      // Immediate update
      aktualna_grupa.value = grupa
      
      // Force refresh kolejki po 2 sekundach (więcej czasu dla Heroku)
      setTimeout(async () => {
        console.log('🔄 Refreshing kolejka po aktywacji...')
        await loadKolejka()
        syncing.value = false
        console.log('✅ Grupa aktywowana:', grupa.nazwa)
      }, 2000)
      
      showSuccess(`✅ Aktywowano grupę: ${grupa.nazwa}`)
    } else if (response.status === 503) {
      syncing.value = false
      throw new Error('Serwer przeciążony - spróbuj ponownie za chwilę')
    } else {
      syncing.value = false
      const error = await response.text()
      console.error('❌ Backend odrzucił aktywację:', error)
      throw new Error(`Backend error: ${response.status}`)
    }
  } catch (error) {
    console.error('❌ Błąd aktywacji grupy:', error)
    syncing.value = false
    
    if (error.name === 'AbortError') {
      alert('⏱️ Operacja przekroczyła limit czasu. Heroku może być przeciążony. Spróbuj ponownie.')
    } else {
      alert(`Błąd aktywacji grupy: ${error.message}`)
    }
  } finally {
    processing.value = false
  }
}

// OPTIMIZED: Clear aktywnej grupy
const clearAktywnaGrupa = async () => {
  if (processing.value) return
  
  console.log('🧹 Czyszczenie aktywnej grupy...')
  
  try {
    processing.value = true
    syncing.value = true
    
    const response = await fetch('/api/grupa-aktywna', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ clear: true })
    })
    
    if (response.ok) {
      aktualna_grupa.value = null
      
      // Force refresh kolejki
      setTimeout(async () => {
        await loadKolejka()
        syncing.value = false
        console.log('✅ Grupa wyczyszczona')
      }, 500)
      
      showSuccess('🧹 Wyczyszczono aktywną grupę')
    }
  } catch (error) {
    console.error('❌ Błąd czyszczenia grupy:', error)
    syncing.value = false
  } finally {
    processing.value = false
  }
}

const handleQRCode = async () => {
  if (!manualQrCode.value) return
  
  processing.value = true
  try {
    const response = await fetch('/api/start-line-verify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        qr_code: manualQrCode.value,
        kategoria: aktualna_grupa.value?.kategoria,
        plec: aktualna_grupa.value?.plec,
        device_id: 'start-line-scanner-v30.3'
      })
    })
    
    if (response.ok) {
      const data = await response.json()
      lastVerification.value = data
      manualQrCode.value = ''
      await loadKolejka()
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
    console.error('Błąd:', error)
    lastVerification.value = {
      success: false,
      action: 'ODRZUC',
      issues: ['Błąd połączenia z serwerem'],
      zawodnik: {},
      komunikat: '❌ Błąd połączenia'
    }
  } finally {
    processing.value = false
  }
}

const removeFromQueue = async (zawodnik: Zawodnik) => {
  const confirmMessage = `Czy na pewno chcesz usunąć zawodnika #${zawodnik.nr_startowy} ${zawodnik.imie} ${zawodnik.nazwisko} z kolejki?`
  
  if (!confirm(confirmMessage)) return
  
  try {
    const response = await fetch(`/api/start-queue/remove/${zawodnik.nr_startowy}`, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' }
    })
    
    if (response.ok) {
      await loadKolejka()
      showSuccess(`Usunięto zawodnika #${zawodnik.nr_startowy} z kolejki`)
    } else {
      const error = await response.json()
      alert(`Błąd: ${error.message}`)
    }
  } catch (error) {
    console.error('Błąd usuwania:', error)
    alert('Błąd połączenia z serwerem')
  }
}

const clearQueue = async (type: 'all' | 'scanned') => {
  const confirmMessage = type === 'all' 
    ? 'Czy na pewno chcesz wyczyścić całą kolejkę startową?'
    : 'Czy na pewno chcesz usunąć wszystkich skanowanych zawodników z kolejki?'
  
  if (!confirm(confirmMessage)) return
  
  try {
    const response = await fetch('/api/start-queue/clear', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type })
    })
    
    if (response.ok) {
      await loadKolejka()
      showSuccess(`Wyczyszczono kolejkę: ${type}`)
    }
  } catch (error) {
    console.error('Błąd czyszczenia kolejki:', error)
  }
}

const toggleGrupaDetails = (numer_grupy: number) => {
  if (selectedGrupa.value === numer_grupy) {
    selectedGrupa.value = null
  } else {
    selectedGrupa.value = numer_grupy
  }
}

const confirmStart = () => {
  clearVerification()
}

const clearVerification = () => {
  lastVerification.value = null
}

const showSuccess = (message: string) => {
  // Tu można dodać toast notification
  console.log(`✅ ${message}`)
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

// Lifecycle
onMounted(async () => {
  await loadApiVersion()
  await refreshAll()
})

onUnmounted(() => {
  // Auto-refresh WYŁĄCZONY - nie potrzebny
  // stopQueueAutoRefresh()
})
</script> 