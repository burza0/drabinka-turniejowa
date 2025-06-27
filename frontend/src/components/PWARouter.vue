<template>
  <div class="pwa-router h-screen bg-gray-100 dark:bg-gray-900">
    <!-- User Type Selection Screen -->
    <div v-if="!currentUserType" class="h-full flex flex-col">
      <!-- Header -->
      <div class="bg-white dark:bg-gray-800 shadow-lg">
        <div class="px-6 py-4">
          <div class="flex items-center justify-between">
            <div>
              <h1 class="text-2xl font-bold text-gray-900 dark:text-white">SKATECROSS PWA</h1>
              <p class="text-sm text-gray-600 dark:text-gray-400">Wybierz typ użytkownika</p>
            </div>
            <div class="flex items-center space-x-2">
              <div class="flex items-center space-x-1 bg-green-100 dark:bg-green-900 px-2 py-1 rounded-full">
                <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span class="text-xs font-medium text-green-700 dark:text-green-300">v37.0</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- User Type Cards -->
      <div class="flex-1 p-6 space-y-4">
        <div 
          v-for="userType in userTypes" 
          :key="userType.id"
          @click="selectUserType(userType.id)"
          class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 cursor-pointer transform transition-all duration-200 hover:scale-105 hover:shadow-xl active:scale-95"
        >
          <div class="flex items-center space-x-4">
            <div :class="[
              'p-4 rounded-xl',
              userType.bgColor
            ]">
              <component :is="userType.icon" :class="[
                'h-8 w-8',
                userType.iconColor
              ]" />
            </div>
            <div class="flex-1">
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white">{{ userType.name }}</h3>
              <p class="text-sm text-gray-600 dark:text-gray-400">{{ userType.description }}</p>
              <div class="mt-2 flex flex-wrap gap-2">
                <span 
                  v-for="feature in userType.features" 
                  :key="feature"
                  class="px-2 py-1 bg-gray-100 dark:bg-gray-700 text-xs text-gray-600 dark:text-gray-300 rounded-full"
                >
                  {{ feature }}
                </span>
              </div>
            </div>
            <div class="text-gray-400">
              <ChevronRightIcon class="h-6 w-6" />
            </div>
          </div>
        </div>
      </div>

      <!-- Footer -->
      <div class="p-4 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700">
        <div class="text-center">
          <p class="text-xs text-gray-500 dark:text-gray-400">
            SKATECROSS v37.0 - Progressive Web App
          </p>
          <div class="mt-2 flex items-center justify-center space-x-4">
            <div class="flex items-center space-x-1">
              <div :class="[
                'w-2 h-2 rounded-full',
                networkStatus ? 'bg-green-500' : 'bg-red-500'
              ]"></div>
              <span class="text-xs text-gray-500 dark:text-gray-400">
                {{ networkStatus ? 'Online' : 'Offline' }}
              </span>
            </div>
            <div v-if="offlineQueue > 0" class="flex items-center space-x-1">
              <ClockIcon class="w-3 h-3 text-yellow-500" />
              <span class="text-xs text-yellow-600 dark:text-yellow-400">
                {{ offlineQueue }} w kolejce
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Selected User View -->
    <div v-else class="h-full flex flex-col">
      <!-- Top Navigation -->
      <div class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
        <div class="px-4 py-2">
          <div class="flex items-center justify-between">
            <button 
              @click="goBack"
              class="flex items-center space-x-2 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white"
            >
              <ArrowLeftIcon class="h-5 w-5" />
              <span class="text-sm">Zmień typ</span>
            </button>
            
            <div class="flex items-center space-x-2">
              <div :class="[
                'w-8 h-8 rounded-lg flex items-center justify-center',
                getCurrentUserType()?.bgColor || 'bg-gray-100'
              ]">
                <component :is="getCurrentUserType()?.icon" :class="[
                  'h-4 w-4',
                  getCurrentUserType()?.iconColor || 'text-gray-600'
                ]" />
              </div>
              <span class="text-sm font-medium text-gray-900 dark:text-white">
                {{ getCurrentUserType()?.name }}
              </span>
            </div>

            <!-- Install Button -->
            <button 
              v-if="showInstallPrompt"
              @click="installPWA"
              class="flex items-center space-x-1 bg-blue-600 text-white px-3 py-1 rounded-lg text-sm hover:bg-blue-700"
            >
              <ArrowDownTrayIcon class="h-4 w-4" />
              <span>Zainstaluj</span>
            </button>
          </div>
        </div>
      </div>

      <!-- View Content -->
      <div class="flex-1 overflow-hidden">
        <OfficeView v-if="currentUserType === 'office'" />
        <JudgeView v-if="currentUserType === 'judge'" />
        <PWAQRScanner v-if="currentUserType === 'athlete'" :user-type="'athlete'" :auto-start="true" />
        <PWAQRScanner v-if="currentUserType === 'trainer'" :user-type="'trainer'" :auto-start="true" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '../stores/user'
import { useOfflineStore } from '../stores/offline'
import { 
  BuildingOfficeIcon,
  ShieldCheckIcon,
  UserIcon,
  AcademicCapIcon,
  ChevronRightIcon,
  ArrowLeftIcon,
  ClockIcon,
  ArrowDownTrayIcon
} from '@heroicons/vue/24/outline'
import OfficeView from './PWAViews/OfficeView.vue'
import JudgeView from './PWAViews/JudgeView.vue'
import PWAQRScanner from './PWAQRScanner.vue'

const userStore = useUserStore()
const offlineStore = useOfflineStore()

const currentUserType = ref<string | null>(null)
const showInstallPrompt = ref(false)
const deferredPrompt = ref<any>(null)

const userTypes = [
  {
    id: 'office',
    name: 'Biuro Obsługi',
    description: 'Meldowanie zawodników, rejestracja uczestników',
    icon: BuildingOfficeIcon,
    bgColor: 'bg-blue-100 dark:bg-blue-900',
    iconColor: 'text-blue-600 dark:text-blue-400',
    features: ['Skaner QR', 'Meldowanie', 'Lista zawodników']
  },
  {
    id: 'judge',
    name: 'Sędzia',
    description: 'Kontrola linii startu, weryfikacja, timing',
    icon: ShieldCheckIcon,
    bgColor: 'bg-green-100 dark:bg-green-900',
    iconColor: 'text-green-600 dark:text-green-400',
    features: ['Weryfikacja', 'Timer', 'DNF/DSQ']
  },
  {
    id: 'athlete',
    name: 'Zawodnik',
    description: 'Sprawdzanie wyników, self-scan',
    icon: UserIcon,
    bgColor: 'bg-purple-100 dark:bg-purple-900',
    iconColor: 'text-purple-600 dark:text-purple-400',
    features: ['Moje wyniki', 'QR weryfikacja', 'Statystyki']
  },
  {
    id: 'trainer',
    name: 'Trener',
    description: 'Śledzenie podopiecznych, statystyki klubu',
    icon: AcademicCapIcon,
    bgColor: 'bg-orange-100 dark:bg-orange-900',
    iconColor: 'text-orange-600 dark:text-orange-400',
    features: ['Podopieczni', 'Statystyki klubu', 'Wyniki']
  }
]

const networkStatus = computed(() => offlineStore.isOnline)
const offlineQueue = computed(() => offlineStore.queueCount)

const selectUserType = (type: string) => {
  currentUserType.value = type
  userStore.setUserType(type as any)
  
  // Save to localStorage for persistence
  localStorage.setItem('skatecross-user-type', type)
}

const goBack = () => {
  currentUserType.value = null
  localStorage.removeItem('skatecross-user-type')
}

const getCurrentUserType = () => {
  return userTypes.find(type => type.id === currentUserType.value)
}

const installPWA = async () => {
  if (deferredPrompt.value) {
    deferredPrompt.value.prompt()
    const { outcome } = await deferredPrompt.value.userChoice
    
    if (outcome === 'accepted') {
      console.log('🎉 PWA installed successfully')
    }
    
    deferredPrompt.value = null
    showInstallPrompt.value = false
  }
}

// PWA Install Events
onMounted(() => {
  // Restore user type from localStorage
  const savedUserType = localStorage.getItem('skatecross-user-type')
  if (savedUserType) {
    currentUserType.value = savedUserType
    userStore.setUserType(savedUserType as any)
  }

  // Listen for PWA install prompt
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault()
    deferredPrompt.value = e
    showInstallPrompt.value = true
  })

  // Listen for PWA install
  window.addEventListener('appinstalled', () => {
    showInstallPrompt.value = false
    console.log('✅ PWA installed')
  })
})
</script> 