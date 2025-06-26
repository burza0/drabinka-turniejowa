import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

interface OfflineAction {
  id: string
  type: 'scan' | 'checkin' | 'manual-checkin'
  data: any
  timestamp: number
  endpoint: string
  method: string
}

interface NetworkState {
  isOnline: boolean
  lastSync: number | null
  syncInProgress: boolean
}

export const useOfflineStore = defineStore('offline', () => {
  // State
  const queue = ref<OfflineAction[]>([])
  const networkState = ref<NetworkState>({
    isOnline: navigator.onLine,
    lastSync: null,
    syncInProgress: false
  })

  // Getters
  const queueCount = computed(() => queue.value.length)
  const hasPendingActions = computed(() => queue.value.length > 0)
  const isOnline = computed(() => networkState.value.isOnline)

  // Actions
  const addToQueue = (action: Omit<OfflineAction, 'id' | 'timestamp'>) => {
    const queueItem: OfflineAction = {
      ...action,
      id: `offline-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      timestamp: Date.now()
    }
    
    queue.value.push(queueItem)
    console.log('📥 Added to offline queue:', queueItem.type, queueItem.data)
    
    // Zapisz w localStorage jako backup
    localStorage.setItem('skatecross-offline-queue', JSON.stringify(queue.value))
    
    // Spróbuj sync natychmiast jeśli online
    if (networkState.value.isOnline && !networkState.value.syncInProgress) {
      syncQueue()
    }
  }

  const removeFromQueue = (id: string) => {
    const index = queue.value.findIndex(item => item.id === id)
    if (index !== -1) {
      queue.value.splice(index, 1)
      localStorage.setItem('skatecross-offline-queue', JSON.stringify(queue.value))
    }
  }

  const clearQueue = () => {
    queue.value = []
    localStorage.removeItem('skatecross-offline-queue')
  }

  const syncQueue = async () => {
    if (networkState.value.syncInProgress || !networkState.value.isOnline) {
      return
    }

    networkState.value.syncInProgress = true
    console.log('🔄 Starting offline queue sync...')

    const itemsToSync = [...queue.value] // Copy array
    let successCount = 0

    for (const item of itemsToSync) {
      try {
        const response = await fetch(item.endpoint, {
          method: item.method,
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(item.data)
        })

        if (response.ok) {
          removeFromQueue(item.id)
          successCount++
          console.log('✅ Offline action synced:', item.type)
        } else {
          console.log('❌ Failed to sync offline action:', item.type, response.status)
        }
      } catch (error) {
        console.log('❌ Network error syncing offline action:', item.type, error)
        break // Stop syncing if network issues
      }
    }

    networkState.value.syncInProgress = false
    networkState.value.lastSync = Date.now()
    
    console.log(`🔄 Offline sync completed: ${successCount}/${itemsToSync.length} items synced`)
  }

  const setOnlineStatus = (online: boolean) => {
    const wasOffline = !networkState.value.isOnline
    networkState.value.isOnline = online
    
    if (online && wasOffline && queue.value.length > 0) {
      console.log('🌐 Back online - starting queue sync')
      syncQueue()
    }
  }

  const loadQueueFromStorage = () => {
    const stored = localStorage.getItem('skatecross-offline-queue')
    if (stored) {
      try {
        queue.value = JSON.parse(stored)
        console.log(`📦 Loaded ${queue.value.length} items from offline queue`)
      } catch (error) {
        console.error('Error loading offline queue from storage:', error)
        clearQueue()
      }
    }
  }

  // Initialize
  loadQueueFromStorage()

  // Listen to online/offline events
  window.addEventListener('online', () => setOnlineStatus(true))
  window.addEventListener('offline', () => setOnlineStatus(false))

  return {
    // State
    queue: computed(() => queue.value),
    networkState: computed(() => networkState.value),
    
    // Getters
    queueCount,
    hasPendingActions,
    isOnline,
    
    // Actions
    addToQueue,
    removeFromQueue,
    clearQueue,
    syncQueue,
    setOnlineStatus,
    loadQueueFromStorage
  }
}) 