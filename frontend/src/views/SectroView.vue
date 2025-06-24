<template>
  <div class="sectro-main min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Header -->
    <div class="bg-white dark:bg-gray-800 shadow">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <h1 class="text-2xl font-bold text-gray-900 dark:text-white">
              SECTRO Live Timing
            </h1>
          </div>
          <div class="flex items-center space-x-4">
            <!-- Connection Status -->
            <div class="flex items-center space-x-2">
              <div class="w-3 h-3 rounded-full bg-green-500"></div>
              <span class="text-sm text-gray-600 dark:text-gray-400">
                Połączono
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      
      <!-- Unified System Notice -->
      <div v-if="!currentSession" class="bg-gradient-to-br from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 rounded-xl border border-blue-200 dark:border-blue-700 p-8 text-center">
        <div class="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center mx-auto mb-6">
          <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </div>
        
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          🚀 Unified Start Control
        </h2>
        
        <p class="text-lg text-gray-600 dark:text-gray-400 mb-6 max-w-2xl mx-auto">
          System SECTRO został zintegrowany z Centrum Startu! <br>
          Sesje są teraz tworzone <strong>automatycznie</strong> przy aktywacji grup startowych.
        </p>
        
        <div class="bg-white dark:bg-gray-800 rounded-lg p-6 mb-6 text-left max-w-2xl mx-auto border border-gray-200 dark:border-gray-700">
          <h3 class="font-bold text-gray-900 dark:text-white mb-3">💡 Nowy workflow:</h3>
          <ol class="space-y-2 text-sm text-gray-600 dark:text-gray-400">
            <li class="flex items-center space-x-2">
              <span class="w-6 h-6 bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-400 rounded-full flex items-center justify-center text-xs font-bold">1</span>
              <span>Skanuj QR → meldowanie zawodników</span>
            </li>
            <li class="flex items-center space-x-2">
              <span class="w-6 h-6 bg-green-100 dark:bg-green-900 text-green-600 dark:text-green-400 rounded-full flex items-center justify-center text-xs font-bold">2</span>
              <span>Aktywuj grupę → automatyczne tworzenie sesji SECTRO</span>
            </li>
            <li class="flex items-center space-x-2">
              <span class="w-6 h-6 bg-purple-100 dark:bg-purple-900 text-purple-600 dark:text-purple-400 rounded-full flex items-center justify-center text-xs font-bold">3</span>
              <span>Live timing → automatyczne pomiary</span>
            </li>
          </ol>
        </div>
        
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <a href="#" @click="$emit('switch-to-unified')" 
             class="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-8 py-3 rounded-lg font-medium transition-all duration-200 shadow-lg hover:shadow-xl">
            🚀 Przejdź do Unified System
          </a>
          
          <button @click="showManualForm = !showManualForm"
                  class="bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-300 px-6 py-3 rounded-lg font-medium transition-all duration-200">
            ⚙️ Utwórz sesję ręcznie (zaawansowane)
          </button>
        </div>
      </div>
      
      <!-- Manual Session Form (collapsed by default) -->
      <div v-if="!currentSession && showManualForm" class="mt-6">
        <SectroSetup 
          @session-created="onSessionCreated"
          @cancel="showManualForm = false"
        />
      </div>
      
      <!-- Active Session -->
      <div v-else-if="currentSession" class="space-y-6">
        
        <!-- Session Controls -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div class="flex justify-between items-center">
            <div>
              <h2 class="text-lg font-medium text-gray-900 dark:text-white">
                {{ currentSession.nazwa }}
              </h2>
              <p class="text-sm text-gray-500 dark:text-gray-400">
                {{ currentSession.kategoria }} {{ currentSession.plec }}
              </p>
            </div>
            
            <div class="flex space-x-3">
              <button 
                @click="startSession"
                class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-md"
              >
                Start
              </button>
              
              <button 
                @click="endSession"
                class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-md"
              >
                Nowa sesja
              </button>
            </div>
          </div>
        </div>
        
        <!-- Live Timing Dashboard -->
        <LiveTiming 
          :session="currentSession"
          @session-updated="onSessionUpdated"
          @athlete-started="onAthleteStarted"
          @athlete-finished="onAthleteFinished"
        />
        
        <!-- Live Results Table -->
        <LiveResults 
          :session-id="currentSession.id"
          :results="sessionResults"
        />
        
      </div>
    </div>
    
  </div>
</template>

<script>
import { ref } from 'vue'
import SectroSetup from '../components/sectro/SectroSetup.vue'
import LiveTiming from '../components/sectro/LiveTiming.vue'
import LiveResults from '../components/sectro/LiveResults.vue'

export default {
  name: 'SectroView',
  components: {
    SectroSetup,
    LiveTiming,
    LiveResults
  },
  setup() {
    const currentSession = ref(null)
    const sessionResults = ref([])
    const showManualForm = ref(false)

    const onSessionCreated = (session) => {
      currentSession.value = session
      console.log('New session created:', session)
    }

    const startSession = async () => {
      console.log('Starting session...')
      try {
        const response = await fetch(`/api/sectro/sessions/${currentSession.value.id}/start`, {
          method: 'POST'
        });
        
        if (response.ok) {
          const data = await response.json();
          if (data.success) {
            // Aktualizuj dane sesji, aby LiveTiming reagował na zmianę
            currentSession.value = {
              ...currentSession.value,
              status: 'active' // Ustaw status na aktywny
            };
            console.log('Session started successfully:', currentSession.value);
          }
        }
      } catch (error) {
        console.error('Error starting session:', error);
      }
    }

    const endSession = () => {
      currentSession.value = null
      sessionResults.value = []
    }

    const onSessionUpdated = async () => {
      // Refresh session data
      console.log('Session updated, refreshing data...')
      
      try {
        // Pobierz aktualne dane sesji
        const response = await fetch(`/api/sectro/sessions/${currentSession.value.id}`);
        
        if (response.ok) {
          const data = await response.json();
          if (data.success && data.session) {
            currentSession.value = data.session;
            console.log('Session data refreshed:', currentSession.value);
          }
        }
      } catch (error) {
        console.error('Error refreshing session data:', error);
      }
    }

    const onAthleteStarted = (data) => {
      console.log('Athlete started:', data)
      
      // Dodaj zawodnika do wyników z oznaczeniem IN_PROGRESS
      if (data.athlete && data.frame) {
        // Sprawdź, czy zawodnik jest już w wynikach
        const existingIndex = sessionResults.value.findIndex(
          result => result.nr_startowy === data.athlete.nr_startowy
        )
        
        if (existingIndex >= 0) {
          // Aktualizuj istniejący wynik
          sessionResults.value[existingIndex] = {
            ...sessionResults.value[existingIndex],
            status: 'in_progress',
            start_time: data.frame.timestamp
          }
        } else {
          // Dodaj nowy wynik
          sessionResults.value.push({
            nr_startowy: data.athlete.nr_startowy,
            imie: data.athlete.imie,
            nazwisko: data.athlete.nazwisko,
            kategoria: data.athlete.kategoria,
            plec: data.athlete.plec,
            klub: data.athlete.klub,
            status: 'in_progress',
            start_time: data.frame.timestamp,
            finish_time: null,
            total_time: null
          })
        }
      }
    }

    const onAthleteFinished = (data) => {
      console.log('Athlete finished:', data)
      
      // Update results
      if (data.result) {
        // Znajdź i zaktualizuj istniejący wynik
        const existingIndex = sessionResults.value.findIndex(
          result => result.nr_startowy === data.athlete.nr_startowy
        )
        
        if (existingIndex >= 0) {
          // Aktualizuj istniejący wynik zachowując dane zawodnika
          sessionResults.value[existingIndex] = {
            ...sessionResults.value[existingIndex],
            status: data.result.status,
            finish_time: data.result.finish_time,
            total_time: data.result.total_time,
            // Zachowaj start_time jeśli jest w result (może się zmienić)
            ...(data.result.start_time && { start_time: data.result.start_time })
          }
        } else {
          // Dodaj nowy wynik z danymi zawodnika
          sessionResults.value.push({
            nr_startowy: data.athlete.nr_startowy,
            imie: data.athlete.imie,
            nazwisko: data.athlete.nazwisko,
            kategoria: data.athlete.kategoria,
            plec: data.athlete.plec,
            klub: data.athlete.klub,
            ...data.result
          })
        }
        
        // Sortuj wyniki po czasie (najszybsze na górze)
        sessionResults.value.sort((a, b) => {
          // Najpierw ukończone biegi
          if (a.status === 'completed' && b.status !== 'completed') return -1
          if (a.status !== 'completed' && b.status === 'completed') return 1
          
          // Sortuj ukończone biegi po czasie
          if (a.status === 'completed' && b.status === 'completed') {
            return a.total_time - b.total_time
          }
          
          // Sortuj nieukończone biegi po czasie startu (od najnowszego)
          return (b.start_time || 0) - (a.start_time || 0)
        })
      }
    }

    return {
      currentSession,
      sessionResults,
      showManualForm,
      onSessionCreated,
      startSession,
      endSession,
      onSessionUpdated,
      onAthleteStarted,
      onAthleteFinished
    }
  }
}
</script>

<style scoped>
.sectro-main {
  min-height: 100vh;
}
</style> 