<template>
  <div class="start-groups-card bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
    
    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 bg-blue-100 dark:bg-blue-900/20 rounded-lg flex items-center justify-center">
          <svg class="w-5 h-5 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
        </div>
        <div>
          <h2 class="text-xl font-bold text-gray-900 dark:text-white">Grupy Startowe</h2>
          <p class="text-sm text-gray-600 dark:text-gray-400">Zarządzanie grupami i aktywacja SECTRO</p>
        </div>
      </div>
      
      <div class="flex items-center space-x-2">
        <button 
          @click="refreshGroups"
          :disabled="loading"
          class="px-4 py-2 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg font-medium hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors duration-200"
        >
          <svg v-if="loading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="m4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span class="ml-2">Odśwież</span>
        </button>
      </div>
    </div>

    <!-- Groups Grid -->
    <div v-if="groups.length > 0" class="space-y-4">
      
      <!-- Active group banner -->
      <div v-if="activeGroup" class="bg-gradient-to-r from-purple-500 to-blue-600 text-white rounded-xl p-4 mb-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <div class="w-8 h-8 bg-white/20 rounded-lg flex items-center justify-center">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div>
              <div class="font-semibold">🎯 Aktywna grupa</div>
              <div class="text-sm opacity-90">{{ activeGroup.kategoria_nazwa }} {{ activeGroup.plec }} • {{ activeGroup.liczba_zawodnikow }} zawodników</div>
            </div>
          </div>
          
          <button 
            @click="deactivateGroup(activeGroup)"
            class="px-4 py-2 bg-white/20 hover:bg-white/30 rounded-lg font-medium transition-colors duration-200"
          >
            ⏹️ Zakończ
          </button>
        </div>
      </div>

      <!-- Groups list -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="group in groups" :key="group.id" 
             :class="getGroupCardClass(group)"
             class="p-4 rounded-xl border transition-all duration-200 hover:shadow-md">
          
          <!-- Group header -->
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center space-x-2">
              <div :class="getGroupIconClass(group)" 
                   class="w-8 h-8 rounded-lg flex items-center justify-center text-xs font-bold">
                {{ group.kategoria_skrot }}
              </div>
              <div>
                <div class="font-semibold text-gray-900 dark:text-white">
                  {{ group.kategoria_nazwa }}
                </div>
                <div class="text-sm text-gray-600 dark:text-gray-400">
                  {{ group.plec }}
                </div>
              </div>
            </div>
            
            <div :class="getStatusBadgeClass(group)" 
                 class="px-2 py-1 rounded-full text-xs font-medium">
              {{ getStatusText(group) }}
            </div>
          </div>

          <!-- Athletes count -->
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center space-x-2">
              <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197m13.5-9a2.5 2.5 0 11-5 0 2.5 2.5 0 015 0z" />
              </svg>
              <span class="text-sm text-gray-600 dark:text-gray-400">Zawodnicy:</span>
            </div>
            <span class="font-semibold text-gray-900 dark:text-white">
              {{ group.liczba_zawodnikow }}
            </span>
          </div>

          <!-- Action button -->
          <div class="space-y-2">
            <button 
              v-if="!group.is_active && group.liczba_zawodnikow > 0"
              @click="activateGroup(group)"
              :disabled="loading || !!activeGroup"
              class="w-full px-4 py-2 bg-blue-600 disabled:bg-gray-400 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors duration-200 flex items-center justify-center space-x-2"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1m4 0h1m-6 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>Aktywuj grupę</span>
            </button>
            
            <button 
              v-else-if="group.is_active"
              @click="deactivateGroup(group)"
              class="w-full px-4 py-2 bg-red-600 text-white rounded-lg font-medium hover:bg-red-700 transition-colors duration-200 flex items-center justify-center space-x-2"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 9l6 6m0-6l-6 6" />
              </svg>
              <span>Dezaktywuj</span>
            </button>
            
            <div v-else-if="group.liczba_zawodnikow === 0"
                 class="w-full px-4 py-2 bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400 rounded-lg text-center text-sm">
              Brak zawodników
            </div>
            
            <div v-else-if="activeGroup && activeGroup.id !== group.id"
                 class="w-full px-4 py-2 bg-yellow-100 dark:bg-yellow-900/20 text-yellow-700 dark:text-yellow-400 rounded-lg text-center text-sm">
              Inna grupa aktywna
            </div>
          </div>

          <!-- Athletes list preview -->
          <div v-if="group.liczba_zawodnikow > 0" class="mt-3 pt-3 border-t border-gray-200 dark:border-gray-600">
            <div class="text-xs text-gray-500 dark:text-gray-400 mb-2">Zameldowani zawodnicy:</div>
            <div class="text-xs text-gray-700 dark:text-gray-300 max-h-16 overflow-y-auto">
              <div v-for="athlete in group.zawodnicy?.slice(0, 3)" :key="athlete.id" class="truncate">
                • {{ athlete.imie_nazwisko }}
              </div>
              <div v-if="group.zawodnicy?.length > 3" class="text-gray-500 dark:text-gray-400">
                ... i {{ group.zawodnicy.length - 3 }} więcej
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>

    <!-- Empty state -->
    <div v-else class="text-center py-12">
      <svg class="w-16 h-16 text-gray-400 dark:text-gray-600 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
      </svg>
      <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">Brak grup startowych</h3>
      <p class="text-gray-600 dark:text-gray-400 mb-4">
        Grupy startowe tworzone są automatycznie po zameldowaniu zawodników
      </p>
      <div class="text-sm text-gray-500 dark:text-gray-400">
        💡 Przejdź do QR Scanner aby zameldować pierwszych zawodników
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// ===== PROPS & EMITS =====
const props = defineProps({
  groups: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['group-activated', 'group-deactivated', 'refresh-requested'])

// ===== COMPUTED PROPERTIES =====
const activeGroup = computed(() => 
  props.groups.find(g => g.is_active)
)

// ===== STYLING METHODS =====
const getGroupCardClass = (group) => {
  if (group.is_active) {
    return 'bg-gradient-to-br from-purple-50 to-blue-50 dark:from-purple-900/20 dark:to-blue-900/20 border-purple-200 dark:border-purple-700'
  }
  if (group.liczba_zawodnikow > 0) {
    return 'bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 hover:border-blue-300 dark:hover:border-blue-600'
  }
  return 'bg-gray-50 dark:bg-gray-800/50 border-gray-200 dark:border-gray-700'
}

const getGroupIconClass = (group) => {
  if (group.is_active) {
    return 'bg-purple-600 text-white'
  }
  if (group.liczba_zawodnikow > 0) {
    return 'bg-blue-100 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400'
  }
  return 'bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400'
}

const getStatusBadgeClass = (group) => {
  if (group.is_active) {
    return 'bg-purple-100 dark:bg-purple-900/20 text-purple-600 dark:text-purple-400'
  }
  if (group.liczba_zawodnikow > 0) {
    return 'bg-green-100 dark:bg-green-900/20 text-green-600 dark:text-green-400'
  }
  return 'bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400'
}

const getStatusText = (group) => {
  if (group.is_active) return 'AKTYWNA'
  if (group.liczba_zawodnikow > 0) return 'GOTOWA'
  return 'PUSTA'
}

// ===== ACTION METHODS =====
const activateGroup = async (group) => {
  console.log('🏁 Activating group:', group)
  
  try {
    const response = await fetch('/api/unified/activate-group', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        kategoria: group.kategoria,
        plec: group.plec 
      })
    })
    
    const data = await response.json()
    
    if (data.success) {
      emit('group-activated', {
        group: group,
        session: data.session,
        message: data.message
      })
    } else {
      console.error('❌ Group activation failed:', data.error)
      alert(`Błąd aktywacji grupy: ${data.error}`)
    }
    
  } catch (error) {
    console.error('❌ Group activation error:', error)
    alert('Błąd połączenia podczas aktywacji grupy')
  }
}

const deactivateGroup = async (group) => {
  console.log('⏹️ Deactivating group:', group)
  
  try {
    const response = await fetch('/api/unified/activate-group', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        kategoria: null,  // Deactivation
        plec: null 
      })
    })
    
    const data = await response.json()
    
    if (data.success) {
      emit('group-deactivated', {
        group: group,
        message: data.message
      })
    } else {
      console.error('❌ Group deactivation failed:', data.error)
      alert(`Błąd dezaktywacji grupy: ${data.error}`)
    }
    
  } catch (error) {
    console.error('❌ Group deactivation error:', error)
    alert('Błąd połączenia podczas dezaktywacji grupy')
  }
}

const refreshGroups = () => {
  emit('refresh-requested')
}
</script>

<style scoped>
/* Smooth transitions */
.start-groups-card {
  transition: all 0.3s ease;
}

/* Grid responsive adjustments */
@media (max-width: 768px) {
  .grid-cols-1 {
    grid-template-columns: 1fr;
  }
}

/* Card hover effects */
.hover\:shadow-md:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

/* Active group pulse animation */
@keyframes pulse-subtle {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.8; }
}

.animate-pulse-subtle {
  animation: pulse-subtle 2s infinite;
}
</style> 