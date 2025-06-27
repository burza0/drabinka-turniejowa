<template>
  <div class="pwa-qr-scanner">
    <!-- Scanner Container -->
    <div class="relative bg-black rounded-lg overflow-hidden shadow-2xl">
      <!-- Video Element -->
      <video
        ref="videoElement"
        class="w-full h-64 md:h-80 object-cover"
        :class="{ 'mirror': cameraState.facingMode === 'user' }"
        autoplay
        muted
        playsinline
      />
      
      <!-- Scanner Overlay -->
      <div class="absolute inset-0 pointer-events-none">
        <!-- Scan Frame -->
        <div class="absolute inset-4 border-2 border-white/30 rounded-lg">
          <div class="absolute top-0 left-0 w-6 h-6 border-t-4 border-l-4 border-blue-400 rounded-tl-lg"></div>
          <div class="absolute top-0 right-0 w-6 h-6 border-t-4 border-r-4 border-blue-400 rounded-tr-lg"></div>
          <div class="absolute bottom-0 left-0 w-6 h-6 border-b-4 border-l-4 border-blue-400 rounded-bl-lg"></div>
          <div class="absolute bottom-0 right-0 w-6 h-6 border-b-4 border-r-4 border-blue-400 rounded-br-lg"></div>
        </div>
        
        <!-- Scanning Line Animation -->
        <div 
          v-if="isScanning"
          class="absolute left-6 right-6 h-0.5 bg-gradient-to-r from-transparent via-blue-400 to-transparent scanning-line"
        />
        
        <!-- Status Messages -->
        <div class="absolute top-4 left-4 right-4">
          <div 
            v-if="showError"
            class="bg-red-500/90 text-white px-3 py-2 rounded-lg text-sm backdrop-blur-sm"
          >
            <div>❌ {{ showError }}</div>
            <div v-if="isDevelopment" class="text-xs mt-1 opacity-75">
              {{ debugInfo.protocol }} | {{ debugInfo.secure }} | {{ debugInfo.mediaDevices }}
            </div>
            <div v-if="!debugInfo.secure" class="text-xs mt-2 bg-yellow-500/20 p-2 rounded border border-yellow-400/30">
              🔒 <strong>Rozwiązanie:</strong> Użyj HTTPS adresu z tego urządzenia
            </div>
          </div>
          
          <div 
            v-else-if="!cameraState.hasPermission"
            class="bg-yellow-500/90 text-white px-3 py-2 rounded-lg text-sm backdrop-blur-sm"
          >
            📷 Wymagane uprawnienia do kamery
          </div>
          
          <div 
            v-else-if="cameraLoading"
            class="bg-blue-500/90 text-white px-3 py-2 rounded-lg text-sm backdrop-blur-sm"
          >
            🔄 Inicjalizacja kamery...
          </div>
          
          <div 
            v-else-if="isScanning"
            class="bg-green-500/90 text-white px-3 py-2 rounded-lg text-sm backdrop-blur-sm"
          >
            📱 Skanowanie... Przyłóż kod QR do ramki
          </div>
        </div>
        
        <!-- Last Scan Result -->
        <div 
          v-if="lastScan && showLastResult"
          class="absolute bottom-4 left-4 right-4"
        >
          <div 
            class="px-4 py-3 rounded-lg backdrop-blur-sm border"
            :class="lastScan.success 
              ? 'bg-green-500/90 text-white border-green-400' 
              : 'bg-red-500/90 text-white border-red-400'
            "
          >
            <div class="flex items-center justify-between">
              <div class="flex-1">
                <div class="font-medium">
                  {{ lastScan.success ? '✅ Zeskanowano' : '❌ Błąd' }}
                </div>
                <div class="text-sm opacity-90">
                  {{ lastScan.success ? formatAthleteInfo(lastScan.athleteData) : lastScan.error }}
                </div>
              </div>
              <button 
                @click="hideLastResult"
                class="ml-2 p-1 hover:bg-white/20 rounded"
              >
                <XMarkIcon class="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Controls -->
    <div class="mt-4 flex flex-wrap gap-3 justify-center">
      <!-- Camera Controls -->
      <div class="flex justify-center space-x-3">
        <button
          v-if="!isScanning"
          @click="startScanning"
          :disabled="cameraLoading"
          class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2 text-sm font-medium"
        >
          <PlayIcon v-if="!cameraLoading" class="h-4 w-4" />
          <ArrowPathIcon v-else class="h-4 w-4 animate-spin" />
          <span>{{ cameraLoading ? 'Ładowanie...' : 'Włącz kamerę' }}</span>
        </button>
        
        <button
          v-else
          @click="stopScanning"
          class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 flex items-center space-x-2 text-sm font-medium"
        >
          <StopIcon class="h-4 w-4" />
          <span>Wyłącz kamerę</span>
        </button>
      </div>
      
      <!-- Switch Camera -->
      <!-- TYMCZASOWO WYŁĄCZONE - uprościmy później -->
      
      <!-- Camera Permission -->
      <!-- TYMCZASOWO WYŁĄCZONE - uprościmy później -->
      
      <!-- Diagnostic Test Button -->
      <!-- TYMCZASOWO WYŁĄCZONE - uprościmy później -->
      
      <!-- Browser Settings Help -->
      <button
        v-if="showError"
        @click="openBrowserSettings"
        class="px-4 py-3 bg-gray-500 hover:bg-gray-600 text-white rounded-lg transition-all text-sm"
      >
        🔧 Pomoc z uprawnieniami
      </button>
    </div>
    
    <!-- Manual Input Fallback -->
    <div class="mt-6 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
      <h3 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
        📝 Ręczne wprowadzenie
      </h3>
      <div class="flex space-x-2">
        <input
          v-model="manualInput"
          @keyup.enter="handleManualInput"
          type="text"
          placeholder="Wpisz kod QR lub numer startowy..."
          class="flex-1 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
        />
        <button
          @click="handleManualInput"
          :disabled="!manualInput.trim()"
          class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg disabled:bg-gray-300 disabled:text-gray-500 transition-all"
        >
          ✓
        </button>
      </div>
    </div>
    
    <!-- Recent Scans -->
    <div v-if="recentScans.length > 0" class="mt-6">
      <h3 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
        📱 Ostatnie skany ({{ recentScans.length }})
      </h3>
      <div class="space-y-2 max-h-64 overflow-y-auto">
        <div
          v-for="scan in recentScans.slice(0, 5)"
          :key="scan.id"
          class="flex items-center justify-between p-3 rounded-lg border"
          :class="scan.success 
            ? 'bg-green-50 border-green-200 dark:bg-green-900/20 dark:border-green-800' 
            : 'bg-red-50 border-red-200 dark:bg-red-900/20 dark:border-red-800'
          "
        >
          <div class="flex-1">
            <div class="text-sm font-medium">
              {{ scan.success ? '✅' : '❌' }} 
              {{ scan.success ? formatAthleteInfo(scan.athleteData) : 'Błąd' }}
            </div>
            <div class="text-xs text-gray-500 dark:text-gray-400">
              {{ formatTime(scan.timestamp) }} • {{ scan.qrCode }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { useAthletesStore } from '../stores/athletes'
import { useOfflineStore } from '../stores/offline'
import { useUserStore } from '../stores/user'
import QrScanner from 'qr-scanner'
import { 
  PlayIcon, 
  StopIcon, 
  ArrowPathIcon, 
  XMarkIcon 
} from '@heroicons/vue/24/outline'

// Props
interface Props {
  onScan?: (qrCode: string, athleteData?: any) => void
  onError?: (error: string) => void
  autoStart?: boolean
  showHistory?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  autoStart: false,
  showHistory: true
})

// Stores
const athletesStore = useAthletesStore()
const offlineStore = useOfflineStore()
const userStore = useUserStore()

// Refs
const videoElement = ref<HTMLVideoElement>()
let qrScanner: QrScanner | null = null

// PROSTE LOCAL STATE zamiast skomplikowanych store'ów
const isScanning = ref(false)
const showError = ref<string | null>(null)
const showCamera = ref(false)
const cameraLoading = ref(false)

// Local state
const manualInput = ref('')
const showLastResult = ref(false)
const lastScan = ref<any>(null)
const recentScans = ref<any[]>([])

// Camera state
const cameraState = ref({
  hasPermission: false,
  facingMode: 'environment'
})

// UPROSZCZONE COMPUTED - bez store dependencies
const canScan = computed(() => !cameraLoading.value && !showError.value)

// Methods
const initializeScanner = async () => {
  if (!videoElement.value) {
    console.error('❌ Video element not available')
    return
  }

  try {
    console.log('🔍 Initializing QR Scanner...')
    
    // PROSTE SPRAWDZENIE - jak w starym skanerze
    if (!QrScanner.hasCamera()) {
      console.error('❌ No camera available')
      showError.value = 'Nie znaleziono kamery na urządzeniu'
      return
    }

    console.log('📷 Camera support confirmed - creating scanner...')

    // BEZPOŚREDNIE TWORZENIE SKANERA - UPROSZCZONA konfiguracja bez problematycznych ograniczeń  
    qrScanner = new QrScanner(
      videoElement.value,
      (result) => {
        console.log('🎯 QR detected:', result.data)
        handleQRCode(result.data)
      },
      {
        // MINIMALNE USTAWIENIA - bez problematycznych constraints
        highlightScanRegion: true,
        highlightCodeOutline: true,
        // USUWAM preferredCamera - może powodować OverconstrainedError
        returnDetailedScanResult: true
      }
    )

    console.log('✅ QR Scanner created successfully')
    cameraState.value.hasPermission = true

    // Auto-start if enabled
    if (props.autoStart) {
      console.log('🚀 Auto-starting scanner...')
      await startScanning()
    }

  } catch (error) {
    console.error('❌ Failed to initialize QR scanner:', error)
    
    let errorMessage = 'Nie udało się zainicjalizować skanera'
    
    if (error instanceof Error) {
      if (error.name === 'NotAllowedError') {
        errorMessage = 'Odmówiono dostępu do kamery. Sprawdź uprawnienia w przeglądarce.'
      } else if (error.name === 'NotFoundError') {
        errorMessage = 'Nie znaleziono kamery na urządzeniu.'
      } else if (error.name === 'NotSupportedError') {
        errorMessage = 'Kamera nie jest obsługiwana w tej przeglądarce.'
      } else if (error.name === 'NotReadableError') {
        errorMessage = 'Kamera jest używana przez inną aplikację.'
      } else if (error.name === 'OverconstrainedError') {
        errorMessage = 'Problemy z ustawieniami kamery. Spróbuj ponownie.'
      } else {
        errorMessage = `Błąd kamery: ${error.message}`
      }
    }
    
    // PROSTY ERROR HANDLING zamiast store
    showError.value = errorMessage
    cameraState.value.hasPermission = false
  }
}

const startScanning = async () => {
  if (!qrScanner) {
    console.error('❌ Scanner not initialized')
    return
  }

  try {
    cameraLoading.value = true
    showError.value = null

    // PROSTE URUCHOMIENIE - jak w starym skanerze
    await qrScanner.start()
    
    isScanning.value = true
    showCamera.value = true
    console.log('📱 Scanning started')
    
    // Haptic feedback if enabled
    if (userStore.currentUser?.preferences?.hapticFeedback && 'vibrate' in navigator) {
      navigator.vibrate(50)
    }
  } catch (error) {
    console.error('Failed to start scanning:', error)
    
    let errorMessage = 'Nie udało się uruchomić skanera'
    if (error instanceof Error) {
      if (error.name === 'NotAllowedError') {
        errorMessage = 'Odmówiono dostępu do kamery. Sprawdź uprawnienia w przeglądarce.'
      } else if (error.name === 'NotFoundError') {
        errorMessage = 'Nie znaleziono kamery na urządzeniu.'
      } else if (error.name === 'OverconstrainedError') {
        errorMessage = 'Problemy z konfiguracją kamery. Spróbuj ponownie.'
      } else {
        errorMessage = `Błąd kamery: ${error.message}`
      }
    }
    
    showError.value = errorMessage
    isScanning.value = false
  } finally {
    cameraLoading.value = false
  }
}

const stopScanning = () => {
  if (qrScanner) {
    qrScanner.stop()
    isScanning.value = false
    console.log('📱 Scanning stopped')
  }
}

const toggleScanning = async () => {
  if (isScanning.value) {
    stopScanning()
  } else {
    await startScanning()
  }
}

const switchCamera = async () => {
  if (!qrScanner) return
  
  const wasScanning = isScanning.value
  
  // Stop current scanning
  if (wasScanning) {
    stopScanning()
  }
  
  // Switch camera mode
  cameraState.value.facingMode = cameraState.value.facingMode === 'user' ? 'environment' : 'user'
  
  // Recreate scanner with new camera
  if (qrScanner) {
    qrScanner.destroy()
  }
  await nextTick()
  await initializeScanner()
  
  // Resume scanning if it was active
  if (wasScanning) {
    await startScanning()
  }
}

const addScanResult = (qrCode: string, success: boolean, athleteData?: any, error?: string) => {
  const scanResult = {
    id: Date.now(),
    qrCode,
    success,
    athleteData,
    error,
    timestamp: Date.now()
  }
  
  lastScan.value = scanResult
  recentScans.value.unshift(scanResult)
  
  // Keep only last 10 scans
  if (recentScans.value.length > 10) {
    recentScans.value = recentScans.value.slice(0, 10)
  }
  
  return scanResult
}

const handleQRCode = async (qrCode: string) => {
  console.log('📱 QR Code detected:', qrCode)
  
  try {
    // Find athlete by QR code
    const athlete = athletesStore.findAthleteByQR(qrCode)
    
    if (athlete) {
      // Success - athlete found
      addScanResult(qrCode, true, athlete)
      
      // Show result temporarily
      showLastResult.value = true
      setTimeout(() => {
        showLastResult.value = false
      }, 3000)
      
      // Call parent callback
      props.onScan?.(qrCode, athlete)
      
      // Process check-in if user has permission
      if (userStore.canCheckin) {
        await processCheckin(athlete)
      }
      
      // Haptic & sound feedback
      if (userStore.currentUser?.preferences?.hapticFeedback && 'vibrate' in navigator) {
        navigator.vibrate([50, 50, 50])
      }
      
      if (userStore.currentUser?.preferences?.soundFeedback) {
        // Play success sound (could be implemented)
        console.log('🔊 Success sound')
      }
      
    } else {
      // Error - athlete not found
      const error = `Nie znaleziono zawodnika z kodem: ${qrCode}`
      addScanResult(qrCode, false, undefined, error)
      
      showLastResult.value = true
      setTimeout(() => {
        showLastResult.value = false
      }, 3000)
      
      props.onError?.(error)
      
      // Error feedback
      if (userStore.currentUser?.preferences?.hapticFeedback && 'vibrate' in navigator) {
        navigator.vibrate([100, 100, 100])
      }
    }
    
  } catch (error) {
    console.error('Error processing QR code:', error)
    const errorMsg = 'Błąd przetwarzania kodu QR'
    addScanResult(qrCode, false, undefined, errorMsg)
    props.onError?.(errorMsg)
  }
  
  // Brief pause before next scan (debouncing)
  const delay = userStore.currentUser?.preferences?.scanDelay || 1000
  setTimeout(() => {
    // Scanner automatically continues
  }, delay)
}

const handleManualInput = () => {
  const input = manualInput.value.trim()
  if (!input) return
  
  // Try as QR code first, then as number
  handleQRCode(input)
  manualInput.value = ''
}

const processCheckin = async (athlete: any) => {
  if (athlete.checked_in) {
    console.log('👤 Athlete already checked in:', athlete.nr_startowy)
    return
  }
  
  try {
    const checkinData = {
      qr_code: athlete.qr_code,
      nr_startowy: athlete.nr_startowy,
      device_id: `pwa-scanner-${userStore.userType}`,
      checkpoint_name: 'check-in'
    }
    
    if (offlineStore.isOnline) {
      // Online - send immediately
      const response = await fetch('/api/unified/scan-qr', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(checkinData)
      })
      
      if (response.ok) {
        const result = await response.json()
        athletesStore.updateAthlete({ 
          ...athlete, 
          checked_in: true, 
          check_in_time: new Date().toISOString() 
        })
        console.log('✅ Check-in successful:', result)
      }
    } else {
      // Offline - add to queue
      offlineStore.addToQueue({
        type: 'checkin',
        data: checkinData,
        endpoint: '/api/unified/scan-qr',
        method: 'POST'
      })
      
      // Optimistic update
      athletesStore.updateAthlete({ 
        ...athlete, 
        checked_in: true, 
        check_in_time: new Date().toISOString() 
      })
      
      console.log('📥 Check-in queued for offline sync')
    }
    
  } catch (error) {
    console.error('Check-in error:', error)
  }
}

const hideLastResult = () => {
  showLastResult.value = false
}

// TYMCZASOWO UPROSZCZONE FUNKCJE
const requestPermissions = async () => {
  // Próba reinicjalizacji skanera
  await initializeScanner()
}

const testCameraAccess = async () => {
  console.log('🧪 Testing camera access manually...')
  showError.value = null
  await initializeScanner()
}

const openBrowserSettings = () => {
  const url = window.location.protocol + '//' + window.location.host
  alert(`🔧 Uprawnienia kamery:

1. Chrome: Kliknij ikonę 🔒 w pasku adresu → Uprawnienia witryny → Kamera: Zezwalaj
2. Safari: Ustawienia → Prywatność i bezpieczeństwo → Kamera → Zezwalaj dla ${url}
3. Firefox: Kliknij ikonę 🛡️ w pasku adresu → Połączenie zabezpieczone → Uprawnienia

WAŻNE: Odśwież stronę po zmianie uprawnień!`)
}

const isDevelopment = computed(() => {
  return import.meta.env.DEV || window.location.hostname === 'localhost'
})

const debugInfo = computed(() => {
  return {
    protocol: window.location.protocol === 'https:' ? '🔒 HTTPS' : '🌐 HTTP',
    secure: window.isSecureContext ? '✅ Secure' : '❌ Not Secure',
    mediaDevices: navigator.mediaDevices ? '✅ MediaDevices' : '❌ No MediaDevices'
  }
})

// Utility functions
const formatAthleteInfo = (athlete: any) => {
  if (!athlete) return 'Brak danych'
  return `#${athlete.nr_startowy} ${athlete.imie} ${athlete.nazwisko}`
}

const formatTime = (timestamp: number) => {
  return new Date(timestamp).toLocaleTimeString('pl-PL', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

// Lifecycle
onMounted(async () => {
  // Load athletes if not already loaded
  if (athletesStore.allAthletes.length === 0) {
    try {
      await athletesStore.fetchAthletes()
    } catch (error) {
      console.warn('Could not load athletes:', error)
    }
  }
  
  // Initialize scanner
  await nextTick()
  await initializeScanner()
})

onUnmounted(() => {
  if (qrScanner) {
    qrScanner.destroy()
  }
})
</script>

<style scoped>
.mirror {
  transform: scaleX(-1);
}

.scanning-line {
  animation: scan 2s linear infinite;
  top: 2rem;
}

@keyframes scan {
  0% {
    top: 1.5rem;
    opacity: 1;
  }
  50% {
    opacity: 0.8;
  }
  100% {
    top: calc(100% - 1.5rem);
    opacity: 1;
  }
}

.pwa-qr-scanner {
  max-width: 500px;
  margin: 0 auto;
}

@media (max-width: 640px) {
  .pwa-qr-scanner {
    margin: 0;
  }
}
</style> 