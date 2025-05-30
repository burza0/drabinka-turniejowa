<template>
  <div class="p-4 sm:p-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6 space-y-4 sm:space-y-0">
      <div class="flex items-center space-x-3">
        <QrCodeIcon class="h-8 w-8 text-green-600" />
        <h2 class="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">Linia Startu</h2>
      </div>
      
      <div class="flex items-center space-x-3">
        <div class="text-sm text-gray-600 dark:text-gray-400">
          Scanner status: 
          <span :class="isScanning ? 'text-green-600' : 'text-red-600'">
            {{ isScanning ? '🟢 Aktywny' : '🔴 Nieaktywny' }}
          </span>
        </div>
      </div>
    </div>

    <!-- Aktywna grupa info -->
    <div v-if="aktywnaCategoriaInfo" class="mb-6 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
      <div class="flex items-center space-x-3">
        <UsersIcon class="h-6 w-6 text-blue-600 dark:text-blue-400" />
        <div>
          <h4 class="font-medium text-blue-800 dark:text-blue-200">
            Oczekiwana grupa: {{ aktywnaCategoriaInfo }}
          </h4>
          <p class="text-sm text-blue-700 dark:text-blue-300">
            Weryfikacja będzie sprawdzać czy zawodnik pasuje do tej grupy
          </p>
        </div>
        <button 
          @click="clearAktywnaGrupa" 
          class="ml-auto text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-200"
        >
          ✕
        </button>
      </div>
    </div>

    <!-- QR Scanner Area -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6 mb-6">
      <div class="text-center">
        <div class="w-24 h-24 mx-auto mb-4 bg-green-100 dark:bg-green-900/20 rounded-full flex items-center justify-center">
          <QrCodeIcon class="h-12 w-12 text-green-600 dark:text-green-400" />
        </div>
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
          Zeskanuj QR kod zawodnika
        </h3>
        <p class="text-gray-600 dark:text-gray-400 mb-4">
          Użyj czytnika QR kodów lub wpisz kod ręcznie
        </p>
        
        <!-- Manual QR Input -->
        <div class="max-w-md mx-auto">
          <div class="flex space-x-2">
            <input
              v-model="manualQrCode"
              @keyup.enter="verifyQrCode"
              type="text"
              placeholder="Wpisz kod QR lub zeskanuj..."
              class="flex-1 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
            />
            <button
              @click="verifyQrCode"
              :disabled="!manualQrCode || isVerifying"
              class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
            >
              {{ isVerifying ? '⏳' : 'Sprawdź' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Verification Result -->
    <div v-if="lastVerification" class="mb-6">
      <div :class="getVerificationClass(lastVerification.action)" class="rounded-lg p-6">
        <div class="flex items-start space-x-4">
          <!-- Icon -->
          <div class="flex-shrink-0">
            <div :class="getIconClass(lastVerification.action)">
              <component :is="getIconComponent(lastVerification.action)" class="h-8 w-8" />
            </div>
          </div>
          
          <!-- Content -->
          <div class="flex-1">
            <h4 class="text-lg font-semibold mb-2" :class="getTextClass(lastVerification.action)">
              {{ lastVerification.komunikat }}
            </h4>
            
            <!-- Zawodnik info -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div>
                <p class="text-sm opacity-90">
                  <strong>Nr:</strong> {{ lastVerification.zawodnik.nr_startowy }}
                </p>
                <p class="text-sm opacity-90">
                  <strong>Imię:</strong> {{ lastVerification.zawodnik.imie }} {{ lastVerification.zawodnik.nazwisko }}
                </p>
              </div>
              <div>
                <p class="text-sm opacity-90">
                  <strong>Kategoria:</strong> {{ lastVerification.zawodnik.kategoria }} {{ lastVerification.zawodnik.plec === 'M' ? 'M' : 'K' }}
                </p>
                <p class="text-sm opacity-90">
                  <strong>Klub:</strong> {{ lastVerification.zawodnik.klub || '-' }}
                </p>
              </div>
            </div>
            
            <!-- Issues -->
            <div v-if="lastVerification.issues && lastVerification.issues.length > 0" class="mb-4">
              <h5 class="font-medium mb-2" :class="getTextClass(lastVerification.action)">Uwagi:</h5>
              <ul class="space-y-1">
                <li v-for="issue in lastVerification.issues" :key="issue" class="text-sm opacity-90">
                  {{ issue }}
                </li>
              </ul>
            </div>
            
            <!-- Actions -->
            <div class="flex space-x-3">
              <button
                v-if="lastVerification.action === 'AKCEPTUJ'"
                @click="confirmStart"
                class="px-4 py-2 bg-white text-green-800 rounded-lg hover:bg-green-50 font-medium border border-green-200"
              >
                ✅ Potwierdź start
              </button>
              <button
                v-if="lastVerification.action === 'OSTRZEZENIE'"
                @click="confirmStart"
                class="px-4 py-2 bg-white text-orange-800 rounded-lg hover:bg-orange-50 font-medium border border-orange-200"
              >
                ⚠️ Pozwól startować
              </button>
              <button
                @click="clearVerification"
                class="px-4 py-2 bg-white/20 hover:bg-white/30 rounded-lg font-medium border border-white/30"
              >
                Wyczyść
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Start Queue -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
      <div class="p-4 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-700 flex items-center justify-between">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
          Kolejka startowa ({{ startQueue.length }})
        </h3>
        <button
          @click="loadStartQueue"
          class="text-sm text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-200"
        >
          🔄 Odśwież
        </button>
      </div>
      
      <div v-if="startQueue.length === 0" class="p-8 text-center text-gray-500 dark:text-gray-400">
        <div class="text-4xl mb-2">🏁</div>
        <div class="text-lg font-medium mb-1">Kolejka pusta</div>
        <div class="text-sm">Zawodnicy pojawią się tutaj po zeskanowaniu QR</div>
      </div>
      
      <div v-else class="divide-y divide-gray-200 dark:divide-gray-700">
        <div v-for="(zawodnik, index) in startQueue" :key="zawodnik.nr_startowy"
             class="p-4 flex items-center justify-between hover:bg-gray-50 dark:hover:bg-gray-700">
          <div class="flex items-center space-x-4">
            <div class="w-8 h-8 bg-blue-100 dark:bg-blue-900 rounded-full flex items-center justify-center">
              <span class="text-blue-600 dark:text-blue-400 font-bold text-sm">{{ index + 1 }}</span>
            </div>
            <div>
              <p class="font-medium text-gray-900 dark:text-white">
                #{{ zawodnik.nr_startowy }} {{ zawodnik.imie }} {{ zawodnik.nazwisko }}
                <!-- Badge for source type -->
                <span v-if="zawodnik.source_type === 'AKTYWNA_GRUPA'"
                      class="ml-2 px-2 py-1 text-xs rounded-full bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">
                  Aktywna grupa
                </span>
                <span v-else-if="zawodnik.source_type === 'SKANOWANY'"
                      class="ml-2 px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200">
                  Skanowany
                </span>
                <span v-else-if="zawodnik.source_type === 'AKTYWNA_GRUPA_I_SKANOWANY'"
                      class="ml-2 px-2 py-1 text-xs rounded-full bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200">
                  Grupa + Skan
                </span>
              </p>
              <p class="text-sm text-gray-500 dark:text-gray-400">{{ zawodnik.kategoria }} {{ zawodnik.plec }} - {{ zawodnik.klub }}</p>
              <p v-if="zawodnik.ostatni_skan" class="text-xs text-gray-400 dark:text-gray-500">
                Skan: {{ formatDate(zawodnik.ostatni_skan) }}
              </p>
            </div>
          </div>
          
          <div class="flex items-center space-x-2">
            <!-- Status badge -->
            <span v-if="zawodnik.czas_przejazdu_s" 
                  class="px-2 py-1 text-xs rounded-full bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200">
              {{ zawodnik.czas_przejazdu_s }}s
            </span>
            
            <!-- Remove button - dla wszystkich zawodników w kolejce -->
            <button
              @click="removeFromQueue(zawodnik.nr_startowy, zawodnik.imie, zawodnik.nazwisko, zawodnik.source_type)"
              :class="getRemoveButtonClass(zawodnik.source_type)"
              :title="getRemoveButtonTitle(zawodnik.source_type)"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { 
  QrCodeIcon, 
  UsersIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  XCircleIcon
} from '@heroicons/vue/24/outline'

// Interfaces
interface Zawodnik {
  nr_startowy: number
  imie: string
  nazwisko: string
  kategoria: string
  plec: string
  klub: string
  checked_in: boolean
  ma_wynik: boolean
  status: string
  source_type: string
}

interface VerificationResult {
  success: boolean
  action: 'AKCEPTUJ' | 'OSTRZEZENIE' | 'ODRZUC'
  issues: string[]
  zawodnik: Zawodnik
  komunikat: string
}

interface QueueItem {
  nr_startowy: number
  imie: string
  nazwisko: string
  kategoria: string
  plec: string
  klub: string
  ostatni_skan: string
  czas_przejazdu_s: number | null
  status: string
  source_type: string
}

// State
const manualQrCode = ref('')
const isScanning = ref(false)
const isVerifying = ref(false)
const lastVerification = ref<VerificationResult | null>(null)
const startQueue = ref<QueueItem[]>([])
const aktywnaCategoriaInfo = ref<string | null>(null)

// Methods
const verifyQrCode = async () => {
  if (!manualQrCode.value) return
  
  isVerifying.value = true
  try {
    const response = await fetch('/api/start-line-verify', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        qr_code: manualQrCode.value,
        kategoria: getAktywnaKategoria(),
        plec: getAktywnaPlec(),
        device_id: 'start-line-scanner'
      })
    })
    
    if (response.ok) {
      const data = await response.json()
      lastVerification.value = data
      manualQrCode.value = '' // Clear input
      await loadStartQueue() // Refresh queue
    } else {
      const error = await response.json()
      lastVerification.value = {
        success: false,
        action: 'ODRZUC',
        issues: [error.error || 'Nieznany błąd'],
        zawodnik: {} as Zawodnik,
        komunikat: '❌ Błąd weryfikacji'
      }
    }
  } catch (error) {
    console.error('Błąd:', error)
    lastVerification.value = {
      success: false,
      action: 'ODRZUC', 
      issues: ['Błąd połączenia z serwerem'],
      zawodnik: {} as Zawodnik,
      komunikat: '❌ Błąd połączenia'
    }
  } finally {
    isVerifying.value = false
  }
}

const loadStartQueue = async () => {
  try {
    const response = await fetch('/api/start-queue')
    if (response.ok) {
      const data = await response.json()
      startQueue.value = data.queue || []
    }
  } catch (error) {
    console.error('Błąd podczas ładowania kolejki:', error)
  }
}

const confirmStart = () => {
  // Tutaj można dodać logikę potwierdzenia startu
  // np. zapisanie do dodatkowej tabeli lub wysłanie sygnału do systemu pomiaru czasu
  clearVerification()
}

const clearVerification = () => {
  lastVerification.value = null
}

const clearAktywnaGrupa = () => {
  aktywnaCategoriaInfo.value = null
}

const getAktywnaKategoria = () => {
  // Można rozszerzyć o pobieranie z localStorage lub API
  return null
}

const getAktywnaPlec = () => {
  // Można rozszerzyć o pobieranie z localStorage lub API  
  return null
}

const formatTime = (timestamp: string) => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  return date.toLocaleTimeString('pl-PL', { 
    hour: '2-digit', 
    minute: '2-digit',
    second: '2-digit'
  })
}

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
    case 'AKCEPTUJ': return 'w-12 h-12 bg-green-600 rounded-full flex items-center justify-center text-white'
    case 'OSTRZEZENIE': return 'w-12 h-12 bg-orange-600 rounded-full flex items-center justify-center text-white'
    case 'ODRZUC': return 'w-12 h-12 bg-red-600 rounded-full flex items-center justify-center text-white'
    default: return 'w-12 h-12 bg-gray-600 rounded-full flex items-center justify-center text-white'
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

const removeFromQueue = async (nr_startowy: number, imie: string, nazwisko: string, source_type: string) => {
  // Różne komunikaty w zależności od typu zawodnika
  let confirmMessage = ''
  let warningMessage = ''
  
  if (source_type === 'AKTYWNA_GRUPA') {
    confirmMessage = `Zawodnik #${nr_startowy} ${imie} ${nazwisko} jest z aktywnej grupy.\nUsunięcie go może być tymczasowe - pojawi się ponownie przy odświeżeniu.\nCzy kontynuować?`
    warningMessage = 'Uwaga: Zawodnik z aktywnej grupy'
  } else if (source_type === 'AKTYWNA_GRUPA_I_SKANOWANY') {
    confirmMessage = `Czy na pewno chcesz usunąć zawodnika #${nr_startowy} ${imie} ${nazwisko} z kolejki?\nZostanie usunięty checkpoint skanu, ale zawodnik pozostanie w aktywnej grupie.`
    warningMessage = 'Usunięcie checkpointu skanowania'
  } else {
    confirmMessage = `Czy na pewno chcesz usunąć zawodnika #${nr_startowy} ${imie} ${nazwisko} z kolejki startowej?`
    warningMessage = 'Usunięcie z kolejki'
  }
  
  // Potwierdzenie
  if (!confirm(confirmMessage)) {
    return
  }
  
  try {
    const response = await fetch(`/api/start-queue/remove/${nr_startowy}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    
    if (response.ok) {
      const data = await response.json()
      
      // Pokaż komunikat sukcesu
      console.log(`✅ ${data.message}`)
      // Tu można dodać toast notification
      
      // Odśwież kolejkę
      await loadStartQueue()
    } else {
      const error = await response.json()
      console.error('❌ Błąd podczas usuwania zawodnika:', error.message)
      alert(`Błąd: ${error.message}`)
    }
  } catch (error) {
    console.error('❌ Błąd sieci:', error)
    alert('Błąd połączenia z serwerem')
  }
}

const getRemoveButtonClass = (source_type: string) => {
  const baseClass = 'p-1 rounded hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors'
  
  if (source_type === 'AKTYWNA_GRUPA') {
    return `${baseClass} text-orange-600 hover:text-orange-800 dark:text-orange-400 dark:hover:text-orange-200`
  } else if (source_type === 'AKTYWNA_GRUPA_I_SKANOWANY') {
    return `${baseClass} text-purple-600 hover:text-purple-800 dark:text-purple-400 dark:hover:text-purple-200`
  } else {
    return `${baseClass} text-red-600 hover:text-red-800 dark:text-red-400 dark:hover:text-red-200`
  }
}

const getRemoveButtonTitle = (source_type: string) => {
  if (source_type === 'AKTYWNA_GRUPA') {
    return 'Ukryj zawodnika z aktywnej grupy (można przywrócić)'
  } else if (source_type === 'AKTYWNA_GRUPA_I_SKANOWANY') {
    return 'Usuń checkpoint skanowania (zostanie w aktywnej grupie)'
  } else {
    return 'Usuń zawodnika z kolejki startowej'
  }
}

// Auto-refresh queue every 5 seconds
let queueRefreshInterval: number

onMounted(() => {
  loadStartQueue()
  queueRefreshInterval = setInterval(loadStartQueue, 5000)
  isScanning.value = true
})

onUnmounted(() => {
  if (queueRefreshInterval) {
    clearInterval(queueRefreshInterval)
  }
  isScanning.value = false
})
</script> 