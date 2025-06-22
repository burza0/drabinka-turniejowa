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
      
      <!-- Setup Phase -->
      <SectroSetup 
        v-if="!currentSession" 
        @session-created="onSessionCreated"
      />
      
      <!-- Active Session -->
      <div v-else class="space-y-6">
        
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