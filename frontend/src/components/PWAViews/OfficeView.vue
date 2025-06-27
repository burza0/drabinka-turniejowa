<template>
  <div class="pwa-office-view h-full bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
    <!-- Header -->
    <div class="bg-white dark:bg-gray-800 shadow-lg border-b border-gray-200 dark:border-gray-700">
      <div class="px-4 py-3">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-xl font-bold text-gray-900 dark:text-white">Biuro Obsługi</h1>
            <p class="text-sm text-gray-600 dark:text-gray-400">Meldowanie zawodników</p>
          </div>
          <div class="flex items-center space-x-2">
            <div class="flex items-center space-x-1 bg-green-100 dark:bg-green-900 px-2 py-1 rounded-full">
              <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span class="text-xs font-medium text-green-700 dark:text-green-300">Online</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Stats -->
    <div class="p-4">
      <div class="grid grid-cols-2 gap-4 mb-6">
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-4">
          <div class="flex items-center">
            <div class="p-2 bg-blue-100 dark:bg-blue-900 rounded-lg">
              <UsersIcon class="h-6 w-6 text-blue-600 dark:text-blue-400" />
            </div>
            <div class="ml-3">
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Zameldowani</p>
              <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ checkedInCount }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-4">
          <div class="flex items-center">
            <div class="p-2 bg-yellow-100 dark:bg-yellow-900 rounded-lg">
              <ClockIcon class="h-6 w-6 text-yellow-600 dark:text-yellow-400" />
            </div>
            <div class="ml-3">
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Oczekujący</p>
              <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ waitingCount }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Scanner Section -->
    <div class="px-4 pb-4 flex-1">
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 mb-6">
        <div class="text-center mb-4">
          <div class="mx-auto w-16 h-16 bg-blue-100 dark:bg-blue-900 rounded-full flex items-center justify-center mb-3">
            <QrCodeIcon class="h-8 w-8 text-blue-600 dark:text-blue-400" />
          </div>
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white">Skanuj QR Zawodnika</h2>
          <p class="text-sm text-gray-600 dark:text-gray-400">Przyłóż QR kod do kamery</p>
        </div>
        
        <PWAQRScanner 
          :user-type="'office'"
          :auto-start="true"
          @scan-success="handleCheckIn"
          @scan-error="handleScanError"
        />
      </div>

      <!-- Recent Check-ins -->
      <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4" v-if="recentCheckIns.length > 0">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-3">Ostatnie meldunki</h3>
        <div class="space-y-2">
          <div 
            v-for="checkIn in recentCheckIns.slice(0, 5)" 
            :key="checkIn.nr_startowy"
            class="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg"
          >
            <div class="flex items-center space-x-3">
              <div class="w-8 h-8 bg-green-100 dark:bg-green-900 rounded-full flex items-center justify-center">
                <CheckCircleIcon class="h-5 w-5 text-green-600 dark:text-green-400" />
              </div>
              <div>
                <p class="font-medium text-gray-900 dark:text-white">{{ checkIn.imie }} {{ checkIn.nazwisko }}</p>
                <p class="text-sm text-gray-500 dark:text-gray-400">#{{ checkIn.nr_startowy }} · {{ checkIn.kategoria }}</p>
              </div>
            </div>
            <div class="text-right">
              <p class="text-xs text-gray-500 dark:text-gray-400">{{ formatTime(checkIn.check_in_time) }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Success/Error Messages -->
    <div v-if="message" class="fixed bottom-4 left-4 right-4 z-50">
      <div :class="[
        'p-4 rounded-lg shadow-lg',
        messageType === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
      ]">
        <div class="flex items-center">
          <CheckCircleIcon v-if="messageType === 'success'" class="h-5 w-5 mr-2" />
          <ExclamationTriangleIcon v-else class="h-5 w-5 mr-2" />
          <span>{{ message }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAthletesStore } from '../../stores/athletes'
import { useOfflineStore } from '../../stores/offline'
import { 
  UsersIcon, 
  ClockIcon, 
  QrCodeIcon, 
  CheckCircleIcon,
  ExclamationTriangleIcon 
} from '@heroicons/vue/24/outline'
import PWAQRScanner from '../PWAQRScanner.vue'

const athletesStore = useAthletesStore()
const offlineStore = useOfflineStore()

const message = ref('')
const messageType = ref<'success' | 'error'>('success')
const recentCheckIns = ref<any[]>([])

const checkedInCount = computed(() => 
  athletesStore.allAthletes.filter((a: any) => a.checked_in).length
)

const waitingCount = computed(() => 
  athletesStore.allAthletes.filter((a: any) => !a.checked_in).length
)

const handleCheckIn = async (qrData: string) => {
  try {
    // Parse QR data to get athlete number
    const nrStartowy = parseInt(qrData)
    
    if (isNaN(nrStartowy)) {
      showMessage('Nieprawidłowy kod QR', 'error')
      return
    }

    // Find athlete
    const athlete = athletesStore.allAthletes.find((a: any) => a.nr_startowy === nrStartowy)
    
    if (!athlete) {
      showMessage(`Nie znaleziono zawodnika #${nrStartowy}`, 'error')
      return
    }

    if (athlete.checked_in) {
      showMessage(`${athlete.imie} ${athlete.nazwisko} już zameldowany`, 'error')
      return
    }

    // Perform check-in (with offline support)
    offlineStore.addToQueue({
      type: 'checkin',
      data: {
        nr_startowy: nrStartowy,
        timestamp: new Date().toISOString()
      },
      endpoint: '/api/unified/scan-qr',
      method: 'POST'
    })
    const success = true

    if (success) {
      // Update local state optimistically
      athlete.checked_in = true
      athlete.check_in_time = new Date().toISOString()
      
      // Add to recent check-ins
      recentCheckIns.value.unshift({
        ...athlete,
        check_in_time: new Date().toISOString()
      })

      showMessage(`✅ ${athlete.imie} ${athlete.nazwisko} zameldowany!`, 'success')
      
      // Haptic feedback if available
      if ('vibrate' in navigator) {
        navigator.vibrate(200)
      }
    }
    
  } catch (error) {
    console.error('Check-in error:', error)
    showMessage('Błąd podczas meldowania', 'error')
  }
}

const handleScanError = (error: string) => {
  showMessage(error, 'error')
}

const showMessage = (text: string, type: 'success' | 'error') => {
  message.value = text
  messageType.value = type
  setTimeout(() => {
    message.value = ''
  }, 3000)
}

const formatTime = (timestamp: string) => {
  return new Date(timestamp).toLocaleTimeString('pl-PL', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(async () => {
  await athletesStore.fetchAthletes()
})
</script> 