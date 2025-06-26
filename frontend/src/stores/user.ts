import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export type UserType = 'office' | 'judge' | 'athlete' | 'trainer' | 'admin'

export interface UserProfile {
  type: UserType
  id?: string
  name?: string
  permissions: string[]
  preferences: {
    hapticFeedback: boolean
    soundFeedback: boolean
    autoScan: boolean
    scanDelay: number
  }
}

const USER_TYPE_CONFIG = {
  office: {
    label: 'Biuro Obsługi',
    icon: '👥',
    description: 'Meldowanie zawodników, skaner QR',
    permissions: ['scan', 'checkin', 'view-athletes', 'manual-checkin'],
    defaultView: '/scanner'
  },
  judge: {
    label: 'Sędzia Linii Startu',
    icon: '🏁',
    description: 'Kontrola startu, weryfikacja zawodników',
    permissions: ['scan', 'verify', 'view-athletes', 'start-control'],
    defaultView: '/start-line'
  },
  athlete: {
    label: 'Zawodnik',
    icon: '🏃‍♂️',
    description: 'Sprawdzanie własnych wyników',
    permissions: ['view-own-results', 'self-scan'],
    defaultView: '/athlete'
  },
  trainer: {
    label: 'Trener',
    icon: '🥇',
    description: 'Śledzenie podopiecznych, statystyki',
    permissions: ['scan', 'view-athletes', 'view-stats', 'export-data'],
    defaultView: '/trainer'
  },
  admin: {
    label: 'Administrator',
    icon: '⚙️',
    description: 'Pełny dostęp do systemu',
    permissions: ['*'],
    defaultView: '/admin'
  }
}

export const useUserStore = defineStore('user', () => {
  // State
  const currentUser = ref<UserProfile | null>(null)
  const isAuthenticated = ref(false)

  // Getters
  const userType = computed(() => currentUser.value?.type)
  const userConfig = computed(() => 
    currentUser.value ? USER_TYPE_CONFIG[currentUser.value.type] : null
  )
  const hasPermission = computed(() => (permission: string) => {
    if (!currentUser.value) return false
    
    const permissions = currentUser.value.permissions
    return permissions.includes('*') || permissions.includes(permission)
  })

  const canScan = computed(() => hasPermission.value('scan'))
  const canCheckin = computed(() => hasPermission.value('checkin'))
  const canViewAthletes = computed(() => hasPermission.value('view-athletes'))
  const canManualCheckin = computed(() => hasPermission.value('manual-checkin'))

  // Actions
  const setUserType = (type: UserType, profile?: Partial<UserProfile>) => {
    const config = USER_TYPE_CONFIG[type]
    
    currentUser.value = {
      type,
      permissions: config.permissions,
      preferences: {
        hapticFeedback: true,
        soundFeedback: true,
        autoScan: type === 'office' || type === 'judge',
        scanDelay: type === 'office' ? 500 : 1000
      },
      ...profile
    }
    
    isAuthenticated.value = true
    
    // Zapisz w localStorage
    localStorage.setItem('skatecross-user-profile', JSON.stringify(currentUser.value))
    
    console.log(`👤 User type set to: ${config.label}`)
    return currentUser.value
  }

  const updatePreferences = (preferences: Partial<UserProfile['preferences']>) => {
    if (!currentUser.value) return
    
    currentUser.value.preferences = {
      ...currentUser.value.preferences,
      ...preferences
    }
    
    localStorage.setItem('skatecross-user-profile', JSON.stringify(currentUser.value))
  }

  const logout = () => {
    currentUser.value = null
    isAuthenticated.value = false
    localStorage.removeItem('skatecross-user-profile')
    console.log('👤 User logged out')
  }

  const loadUserFromStorage = () => {
    const stored = localStorage.getItem('skatecross-user-profile')
    if (stored) {
      try {
        const profile = JSON.parse(stored)
        currentUser.value = profile
        isAuthenticated.value = true
        console.log(`👤 Loaded user profile: ${profile.type}`)
      } catch (error) {
        console.error('Error loading user profile:', error)
        logout()
      }
    }
  }

  // Auto-detection based on URL params or user choice
  const autoDetectUserType = (): UserType | null => {
    const params = new URLSearchParams(window.location.search)
    const typeParam = params.get('user_type') as UserType
    
    if (typeParam && typeParam in USER_TYPE_CONFIG) {
      return typeParam
    }
    
    // Check for specific routes
    const path = window.location.pathname
    if (path.includes('/scanner')) return 'office'
    if (path.includes('/start-line')) return 'judge'
    if (path.includes('/athlete')) return 'athlete'
    if (path.includes('/trainer')) return 'trainer'
    if (path.includes('/admin')) return 'admin'
    
    return null
  }

  // Initialize
  loadUserFromStorage()
  
  // Auto-detect if no user is set
  if (!currentUser.value) {
    const detectedType = autoDetectUserType()
    if (detectedType) {
      setUserType(detectedType)
    }
  }

  return {
    // State
    currentUser: computed(() => currentUser.value),
    isAuthenticated: computed(() => isAuthenticated.value),
    
    // Getters
    userType,
    userConfig,
    hasPermission,
    canScan,
    canCheckin,
    canViewAthletes,
    canManualCheckin,
    
    // Actions
    setUserType,
    updatePreferences,
    logout,
    loadUserFromStorage,
    autoDetectUserType,
    
    // Config
    USER_TYPE_CONFIG
  }
}) 