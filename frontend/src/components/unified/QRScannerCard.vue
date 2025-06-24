<template>
  <div class="qr-scanner-card bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
    
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 bg-blue-100 dark:bg-blue-900/20 rounded-lg flex items-center justify-center">
          <svg class="w-5 h-5 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h2M4 4h5m0 0v5m0 0h5M4 20h5m0 0v-5m0 0h5M20 4h-5m0 0v5m0 0h-5" />
          </svg>
        </div>
        <div>
          <h2 class="text-xl font-bold text-gray-900 dark:text-white">QR Scanner</h2>
          <p class="text-sm text-gray-600 dark:text-gray-400">Skanuj QR zawodników do meldowania</p>
        </div>
      </div>
      
      <div class="flex items-center space-x-2">
        <button 
          @click="toggleCamera"
          :class="cameraActive ? 'bg-red-100 text-red-600 dark:bg-red-900/20 dark:text-red-400' : 'bg-green-100 text-green-600 dark:bg-green-900/20 dark:text-green-400'"
          class="px-4 py-2 rounded-lg font-medium transition-colors duration-200"
        >
          {{ cameraActive ? '⏹️ Stop' : '📹 Start' }}
        </button>
        
        <button 
          @click="manualScan"
          class="px-4 py-2 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg font-medium hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors duration-200"
        >
          ⌨️ Manual
        </button>
      </div>
    </div>

    <!-- Camera Scanner -->
    <div v-if="cameraActive" class="mb-6">
      <div class="relative w-full max-w-md mx-auto">
        <video ref="videoElement" autoplay class="w-full h-64 bg-black rounded-lg border-2 border-gray-300 dark:border-gray-600"></video>
        <canvas ref="canvasElement" class="hidden"></canvas>
        
        <!-- Scanner overlay -->
        <div class="absolute inset-0 flex items-center justify-center pointer-events-none">
          <div class="w-48 h-48 border-2 border-blue-500 rounded-lg relative">
            <!-- Corner decorations -->
            <div class="absolute top-0 left-0 w-8 h-8 border-t-4 border-l-4 border-blue-500 rounded-tl-lg"></div>
            <div class="absolute top-0 right-0 w-8 h-8 border-t-4 border-r-4 border-blue-500 rounded-tr-lg"></div>
            <div class="absolute bottom-0 left-0 w-8 h-8 border-b-4 border-l-4 border-blue-500 rounded-bl-lg"></div>
            <div class="absolute bottom-0 right-0 w-8 h-8 border-b-4 border-r-4 border-blue-500 rounded-br-lg"></div>
          </div>
        </div>
        
        <!-- Scanning status -->
        <div class="absolute bottom-2 left-2 bg-black/50 text-white px-2 py-1 rounded text-sm">
          {{ scanStatus }}
        </div>
      </div>
    </div>

    <!-- Manual Input -->
    <div v-if="showManualInput" class="mb-6">
      <div class="flex space-x-2">
        <input 
          v-model="manualCode"
          @keyup.enter="submitManualCode"
          placeholder="Wpisz kod QR lub ID zawodnika..."
          class="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        <button 
          @click="submitManualCode"
          :disabled="!manualCode.trim()"
          class="px-6 py-2 bg-blue-600 disabled:bg-gray-400 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors duration-200"
        >
          Skanuj
        </button>
      </div>
    </div>

    <!-- Recent Scans -->
    <div v-if="recentScans.length > 0" class="space-y-3">
      <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Ostatnie skany</h3>
      
      <div class="space-y-2 max-h-48 overflow-y-auto">
        <div v-for="scan in recentScans" :key="scan.id" 
             :class="scan.success ? 'border-green-200 bg-green-50 dark:border-green-800 dark:bg-green-900/20' : 'border-red-200 bg-red-50 dark:border-red-800 dark:bg-red-900/20'"
             class="p-3 rounded-lg border">
          
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div :class="scan.success ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'">
                {{ scan.success ? '✅' : '❌' }}
              </div>
              
              <div>
                <div class="font-medium text-gray-900 dark:text-white">
                  {{ scan.athleteName || scan.qrCode }}
                </div>
                <div :class="scan.success ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'"
                     class="text-sm">
                  {{ scan.message }}
                </div>
              </div>
            </div>
            
            <div class="text-right">
              <div class="text-xs text-gray-500 dark:text-gray-400">
                {{ formatTime(scan.timestamp) }}
              </div>
              <div v-if="scan.success" class="text-xs font-medium text-blue-600 dark:text-blue-400">
                {{ scan.status }}
              </div>
            </div>
          </div>
          
        </div>
      </div>
    </div>

    <!-- Instructions -->
    <div v-if="!cameraActive && recentScans.length === 0" class="text-center py-8">
      <svg class="w-16 h-16 text-gray-400 dark:text-gray-600 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M12 4v1m6 11h2m-6 0h-2v4m0-11v3m0 0h.01M12 12h4.01M16 20h4M4 12h4m12 0h2M4 4h5m0 0v5m0 0h5M4 20h5m0 0v-5m0 0h5M20 4h-5m0 0v5m0 0h-5" />
      </svg>
      <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">Rozpocznij skanowanie</h3>
      <p class="text-gray-600 dark:text-gray-400 mb-4">
        Kliknij "Start" aby włączyć kamerę lub "Manual" aby wprowadzić kod ręcznie
      </p>
      <div class="text-sm text-gray-500 dark:text-gray-400">
        💡 Skanowanie automatycznie melduje/wymeldowuje zawodników
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

// ===== PROPS & EMITS =====
const emit = defineEmits(['athlete-registered', 'refresh-requested'])

// ===== REACTIVE STATE =====
const cameraActive = ref(false)
const showManualInput = ref(false)
const manualCode = ref('')
const scanStatus = ref('Gotowy do skanowania...')
const recentScans = ref([])
const videoElement = ref(null)
const canvasElement = ref(null)
const scanInterval = ref(null)

// ===== CAMERA METHODS =====
const toggleCamera = async () => {
  if (cameraActive.value) {
    stopCamera()
  } else {
    await startCamera()
  }
}

const startCamera = async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ 
      video: { 
        facingMode: 'environment',
        width: { ideal: 1280 },
        height: { ideal: 720 }
      } 
    })
    
    if (videoElement.value) {
      videoElement.value.srcObject = stream
      cameraActive.value = true
      showManualInput.value = false
      scanStatus.value = 'Skanowanie aktywne...'
      
      // Start scanning loop
      scanInterval.value = setInterval(scanFrame, 500)
    }
  } catch (error) {
    console.error('❌ Camera error:', error)
    scanStatus.value = 'Błąd kamery'
    // Fallback to manual input
    showManualInput.value = true
  }
}

const stopCamera = () => {
  if (videoElement.value && videoElement.value.srcObject) {
    const tracks = videoElement.value.srcObject.getTracks()
    tracks.forEach(track => track.stop())
    videoElement.value.srcObject = null
  }
  
  cameraActive.value = false
  scanStatus.value = 'Kamera zatrzymana'
  
  if (scanInterval.value) {
    clearInterval(scanInterval.value)
    scanInterval.value = null
  }
}

// ===== QR SCANNING =====
const scanFrame = () => {
  if (!videoElement.value || !canvasElement.value) return
  
  const video = videoElement.value
  const canvas = canvasElement.value
  const context = canvas.getContext('2d')
  
  if (video.readyState === video.HAVE_ENOUGH_DATA) {
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight
    context.drawImage(video, 0, 0, canvas.width, canvas.height)
    
    const imageData = context.getImageData(0, 0, canvas.width, canvas.height)
    
    try {
      // Simulate QR detection (in real app use jsQR library)
      // For demo, we'll trigger on spacebar press
      // const code = jsQR(imageData.data, imageData.width, imageData.height)
      // if (code) {
      //   processQRCode(code.data)
      // }
    } catch (error) {
      console.error('QR scan error:', error)
    }
  }
}

// ===== MANUAL INPUT =====
const manualScan = () => {
  showManualInput.value = !showManualInput.value
  if (showManualInput.value) {
    stopCamera()
  }
}

const submitManualCode = () => {
  if (manualCode.value.trim()) {
    processQRCode(manualCode.value.trim())
    manualCode.value = ''
  }
}

// ===== QR PROCESSING =====
const processQRCode = async (qrCode) => {
  console.log('🔍 Processing QR code:', qrCode)
  
  try {
    const response = await fetch('/api/unified/register-athlete', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ identifier: qrCode })
    })
    
    const data = await response.json()
    
    const scanResult = {
      id: Date.now(),
      qrCode: qrCode,
      timestamp: new Date(),
      success: data.success,
      message: data.message,
      athleteName: data.athlete ? `${data.athlete.imie} ${data.athlete.nazwisko}` : null,
      status: data.athlete?.status
    }
    
    // Add to recent scans (keep last 10)
    recentScans.value.unshift(scanResult)
    if (recentScans.value.length > 10) {
      recentScans.value.pop()
    }
    
    if (data.success) {
      scanStatus.value = `✅ ${data.message}`
      emit('athlete-registered', data)
      
      // Audio feedback
      playBeep(true)
      
      // Reset status after 3 seconds
      setTimeout(() => {
        scanStatus.value = 'Skanowanie aktywne...'
      }, 3000)
    } else {
      scanStatus.value = `❌ ${data.message}`
      playBeep(false)
      
      setTimeout(() => {
        scanStatus.value = 'Skanowanie aktywne...'
      }, 3000)
    }
    
  } catch (error) {
    console.error('❌ QR processing error:', error)
    
    const scanResult = {
      id: Date.now(),
      qrCode: qrCode,
      timestamp: new Date(),
      success: false,
      message: 'Błąd połączenia z serwerem'
    }
    
    recentScans.value.unshift(scanResult)
    if (recentScans.value.length > 10) {
      recentScans.value.pop()
    }
    
    scanStatus.value = '❌ Błąd połączenia'
    playBeep(false)
  }
}

// ===== UTILITIES =====
const formatTime = (timestamp) => {
  return new Date(timestamp).toLocaleTimeString('pl-PL', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

const playBeep = (success) => {
  // Audio feedback
  const audioContext = new (window.AudioContext || window.webkitAudioContext)()
  const oscillator = audioContext.createOscillator()
  const gainNode = audioContext.createGain()
  
  oscillator.connect(gainNode)
  gainNode.connect(audioContext.destination)
  
  oscillator.frequency.value = success ? 800 : 400
  oscillator.type = 'square'
  
  gainNode.gain.setValueAtTime(0.3, audioContext.currentTime)
  gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1)
  
  oscillator.start(audioContext.currentTime)
  oscillator.stop(audioContext.currentTime + 0.1)
}

// ===== KEYBOARD SHORTCUTS =====
const handleKeyPress = (event) => {
  // Spacebar for quick scan simulation
  if (event.code === 'Space' && cameraActive.value) {
    event.preventDefault()
    // Simulate QR code for testing
    const testQR = `TEST_${Date.now()}`
    processQRCode(testQR)
  }
}

// ===== LIFECYCLE =====
onMounted(() => {
  document.addEventListener('keydown', handleKeyPress)
})

onUnmounted(() => {
  stopCamera()
  document.removeEventListener('keydown', handleKeyPress)
})
</script>

<style scoped>
/* Camera video styling */
video {
  object-fit: cover;
}

/* Smooth transitions */
.qr-scanner-card {
  transition: all 0.3s ease;
}

/* Scan overlay animation */
@keyframes scan-line {
  0% { transform: translateY(-100%); }
  100% { transform: translateY(100%); }
}

.scanning::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, #3b82f6, transparent);
  animation: scan-line 2s infinite;
}
</style> 