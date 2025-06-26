import { createPinia } from 'pinia'

export const pinia = createPinia()

// Export wszystkich stores
export { useOfflineStore } from './offline'
export { useScannerStore } from './scanner'
export { useUserStore } from './user'
export { useAthletesStore } from './athletes' 