import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import QrScanner from 'qr-scanner'

interface ScanResult {
  id: string
  qrCode: string
  timestamp: number
  success: boolean
  athleteData?: any
  error?: string
}

interface CameraState {
  isActive: boolean
  isLoading: boolean
  error: string | null
  facingMode: 'user' | 'environment'
  hasPermission: boolean
  availableCameras: QrScanner.Camera[]
  currentCameraId?: string
}

export const useScannerStore = defineStore('scanner', () => {
  // State
  const cameraState = ref<CameraState>({
    isActive: false,
    isLoading: false,
    error: null,
    facingMode: 'environment', // Tylna kamera domyślnie
    hasPermission: false,
    availableCameras: [],
    currentCameraId: undefined
  })

  const scanHistory = ref<ScanResult[]>([])
  const lastScan = ref<ScanResult | null>(null)
  const isScanning = ref(false)

  // Getters
  const canScan = computed(() => 
    cameraState.value.hasPermission && 
    !cameraState.value.isLoading && 
    !cameraState.value.error
  )

  const recentScans = computed(() => 
    scanHistory.value
      .sort((a, b) => b.timestamp - a.timestamp)
      .slice(0, 10)
  )

  const successfulScans = computed(() => 
    scanHistory.value.filter(scan => scan.success)
  )

  const errorScans = computed(() => 
    scanHistory.value.filter(scan => !scan.success)
  )

  // Actions
  const requestCameraPermission = async (): Promise<boolean> => {
    try {
      cameraState.value.isLoading = true
      cameraState.value.error = null

      console.log('🔐 Checking camera support...')
      
      // Check if running on secure context (required for camera)
      if (!window.isSecureContext) {
        console.error('❌ Not a secure context! Camera requires HTTPS or localhost')
        cameraState.value.error = 'Kamera wymaga HTTPS lub localhost'
        return false
      }

      // Check if navigator.mediaDevices is available
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        console.error('❌ MediaDevices API not available')
        cameraState.value.error = 'API kamery niedostępne'
        return false
      }

      // Sprawdź czy QrScanner jest obsługiwany
      console.log('📷 Checking QrScanner camera support...')
      const hasCamera = await QrScanner.hasCamera()
      console.log('📷 QrScanner hasCamera result:', hasCamera)
      
      if (!hasCamera) {
        cameraState.value.error = 'Urządzenie nie ma kamery lub jest niedostępna'
        return false
      }

      // Test basic camera access
      console.log('🔐 Testing basic camera access...')
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ 
          video: { facingMode: 'environment' } 
        })
        stream.getTracks().forEach(track => track.stop()) // Stop immediately after test
        console.log('✅ Basic camera access successful')
      } catch (testError) {
        console.error('❌ Basic camera access failed:', testError)
        throw testError
      }

      // Pobierz dostępne kamery
      console.log('📷 Listing available cameras...')
      const cameras = await QrScanner.listCameras(true)
      console.log('📷 Available cameras:', cameras.map(c => ({ id: c.id, label: c.label })))
      cameraState.value.availableCameras = cameras

      if (cameras.length === 0) {
        cameraState.value.error = 'Nie znaleziono dostępnych kamer'
        return false
      }

      // Wybierz odpowiednią kamerę (preferuj tylną)
      const preferredCamera = cameras.find(camera => 
        camera.label.toLowerCase().includes('back') ||
        camera.label.toLowerCase().includes('rear') ||
        camera.label.toLowerCase().includes('environment')
      ) || cameras[0]

      console.log('📷 Selected camera:', preferredCamera.label)

      if (preferredCamera) {
        cameraState.value.currentCameraId = preferredCamera.id
      }

      cameraState.value.hasPermission = true
      console.log('✅ Camera permission granted successfully!')
      
      return true
    } catch (error) {
      console.error('❌ Camera permission error:', error)
      
      let errorMessage = 'Brak dostępu do kamery'
      
      if (error instanceof Error) {
        if (error.name === 'NotAllowedError') {
          errorMessage = 'Odmówiono dostępu do kamery. Kliknij ikonę kamery w pasku adresu i zezwól.'
        } else if (error.name === 'NotFoundError') {
          errorMessage = 'Nie znaleziono kamery na urządzeniu'
        } else if (error.name === 'NotSupportedError') {
          errorMessage = 'Kamera nie jest obsługiwana'
        } else if (error.name === 'NotReadableError') {
          errorMessage = 'Kamera jest używana przez inną aplikację'
        } else {
          errorMessage = `Błąd kamery: ${error.message}`
        }
      }
      
      cameraState.value.error = errorMessage
      cameraState.value.hasPermission = false
      return false
    } finally {
      cameraState.value.isLoading = false
    }
  }

  const switchCamera = async () => {
    if (cameraState.value.availableCameras.length <= 1) return

    const currentIndex = cameraState.value.availableCameras.findIndex(
      camera => camera.id === cameraState.value.currentCameraId
    )
    
    const nextIndex = (currentIndex + 1) % cameraState.value.availableCameras.length
    const nextCamera = cameraState.value.availableCameras[nextIndex]
    
    cameraState.value.currentCameraId = nextCamera.id
    console.log('🔄 Switched to camera:', nextCamera.label)
  }

  const addScanResult = (qrCode: string, success: boolean, athleteData?: any, error?: string) => {
    const scanResult: ScanResult = {
      id: `scan-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      qrCode,
      timestamp: Date.now(),
      success,
      athleteData,
      error
    }

    scanHistory.value.unshift(scanResult) // Dodaj na początek
    lastScan.value = scanResult

    // Ogranicz historię do 100 ostatnich skanów
    if (scanHistory.value.length > 100) {
      scanHistory.value = scanHistory.value.slice(0, 100)
    }

    // Zapisz historię w localStorage
    localStorage.setItem('skatecross-scan-history', JSON.stringify(scanHistory.value))

    console.log('📱 Scan result added:', {
      qrCode,
      success,
      timestamp: new Date(scanResult.timestamp).toLocaleTimeString()
    })

    return scanResult
  }

  const clearScanHistory = () => {
    scanHistory.value = []
    lastScan.value = null
    localStorage.removeItem('skatecross-scan-history')
  }

  const loadScanHistoryFromStorage = () => {
    const stored = localStorage.getItem('skatecross-scan-history')
    if (stored) {
      try {
        const history = JSON.parse(stored)
        scanHistory.value = history
        if (history.length > 0) {
          lastScan.value = history[0]
        }
        console.log(`📦 Loaded ${history.length} scan history items`)
      } catch (error) {
        console.error('Error loading scan history:', error)
        clearScanHistory()
      }
    }
  }

  const startScanning = () => {
    if (!cameraState.value.hasPermission) {
      console.warn('Cannot start scanning - no camera permission')
      return false
    }
    
    cameraState.value.isActive = true
    isScanning.value = true
    console.log('📷 Scanner started')
    return true
  }

  const stopScanning = () => {
    cameraState.value.isActive = false
    isScanning.value = false
    console.log('📷 Scanner stopped')
  }

  const setCameraError = (error: string | null) => {
    cameraState.value.error = error
  }

  const setLoadingState = (loading: boolean) => {
    cameraState.value.isLoading = loading
  }

  // Initialize
  loadScanHistoryFromStorage()

  return {
    // State
    cameraState: computed(() => cameraState.value),
    scanHistory: computed(() => scanHistory.value),
    lastScan: computed(() => lastScan.value),
    isScanning: computed(() => isScanning.value),

    // Getters
    canScan,
    recentScans,
    successfulScans,
    errorScans,

    // Actions
    requestCameraPermission,
    switchCamera,
    addScanResult,
    clearScanHistory,
    loadScanHistoryFromStorage,
    startScanning,
    stopScanning,
    setCameraError,
    setLoadingState
  }
}) 