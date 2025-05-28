<template>
  <div class="drabinka-container">
    <!-- Tournament Header -->
    <div class="tournament-header">
      <div class="header-info">
        <h2 class="tournament-title">
          <span class="title-icon">🏆</span>
          Drabinka pucharowa
        </h2>
        <div class="tournament-status">
          <span class="status-dot"></span>
          <span class="status-text">Turniej w toku</span>
        </div>
      </div>
    </div>
    
    <!-- Loading State -->
    <div v-if="isLoading" class="loading-state">
      <div class="loading-spinner">
        <div class="spinner"></div>
        <p>Ładowanie drabinki...</p>
      </div>
    </div>
    
    <!-- Tournament Categories -->
    <div v-else-if="Object.keys(filtrowaneKategorie).length > 0" class="categories-container">
      <div v-for="(kategoriaData, kategoriaNazwa) in filtrowaneKategorie" :key="kategoriaNazwa" 
           class="category-section">
        
        <!-- Category Header -->
        <div class="category-header">
          <div class="category-title">
            <span class="category-icon">🏅</span>
            <h3 class="category-name">{{ kategoriaNazwa }}</h3>
          </div>
        </div>
        
        <!-- Gender Sections -->
        <div v-for="(plecData, plecNazwa) in kategoriaData" :key="plecNazwa"
             class="gender-section">
          
          <!-- Gender Header -->
          <div class="gender-header">
            <div class="gender-title">
              <span class="gender-icon">{{ plecNazwa === 'Mężczyźni' ? '👨' : '👩' }}</span>
              <h4 class="gender-name">{{ plecNazwa }}</h4>
            </div>
            
            <!-- Statistics -->
            <div v-if="plecData.statystyki" class="stats-container">
              <div class="stat-card total">
                <span class="stat-number">{{ plecData.statystyki.łącznie_zawodników }}</span>
                <span class="stat-label">Łącznie</span>
              </div>
              <div class="stat-card active">
                <span class="stat-number">{{ plecData.statystyki.w_ćwierćfinałach }}</span>
                <span class="stat-label">W grze</span>
              </div>
              <div v-if="plecData.statystyki.odpadło > 0" class="stat-card eliminated">
                <span class="stat-number">{{ plecData.statystyki.odpadło }}</span>
                <span class="stat-label">Odpadło</span>
              </div>
            </div>
          </div>

          <!-- Tournament Bracket -->
          <div class="tournament-bracket">
            
            <!-- Eliminated Players -->
            <div v-if="plecData.odpadli && plecData.odpadli.length > 0" class="eliminated-section">
              <div class="section-title">
                <span class="section-icon">❌</span>
                <span>Zawodnicy odpadli z turnieju</span>
              </div>
              <div class="eliminated-grid">
                <div v-for="zawodnik in plecData.odpadli" :key="zawodnik.nr_startowy"
                     class="eliminated-card">
                  <div class="player-number-small">{{ zawodnik.nr_startowy }}</div>
                  <div class="player-info-small">
                    <div class="player-name-small">{{ zawodnik.imie }} {{ zawodnik.nazwisko }}</div>
                    <div v-if="zawodnik.czas_przejazdu_s" class="player-time-small">
                      {{ zawodnik.czas_przejazdu_s }}s
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Main Bracket -->
            <div class="bracket-main">
              
              <!-- Quarterfinals -->
              <div v-if="plecData.ćwierćfinały && plecData.ćwierćfinały.length > 0" class="bracket-round quarterfinals">
                <div class="round-header">
                  <div class="round-title">
                    <span class="round-icon">🥉</span>
                    <span class="round-name">ĆWIERĆFINAŁY</span>
                  </div>
                  <div class="round-subtitle">{{ plecData.ćwierćfinały.length }} grup</div>
                </div>
                
                <div class="matches-grid">
                  <div v-for="grupa in plecData.ćwierćfinały" :key="grupa.grupa" class="match-card">
                    <div class="match-header">
                      <span class="match-title">Grupa {{ grupa.grupa }}</span>
                      <span class="advance-info">{{ grupa.awansują }} awansuje</span>
                    </div>
                    
                    <div class="players-container">
                      <div v-for="(zawodnik, index) in grupa.zawodnicy" :key="zawodnik.nr_startowy"
                           :class="['player-card', getPlayerClass(index, grupa.awansują)]"
                           @click="showPlayerDetails(zawodnik)">
                        
                        <!-- Player Position -->
                        <div class="player-position">
                          <div class="position-badge" :class="getPositionClass(index)">
                            {{ index + 1 }}
                          </div>
                        </div>
                        
                        <!-- Player Info -->
                        <div class="player-info">
                          <div class="player-name">{{ zawodnik.imie }} {{ zawodnik.nazwisko }}</div>
                          <div class="player-meta">
                            <span class="player-number">#{{ zawodnik.nr_startowy }}</span>
                            <span class="player-time" :class="getTimeClass(zawodnik.czas_przejazdu_s)">
                              {{ zawodnik.czas_przejazdu_s || 'brak' }}{{ zawodnik.czas_przejazdu_s ? 's' : '' }}
                            </span>
                          </div>
                        </div>
                        
                        <!-- Advance Indicator -->
                        <div v-if="index < grupa.awansują" class="advance-indicator">
                          <span class="advance-icon">→</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Round Connector -->
              <div v-if="plecData.ćwierćfinały?.length > 0 && plecData.półfinały?.length > 0" 
                   class="round-connector">
                <div class="connector-line"></div>
                <div class="connector-text">AWANS</div>
              </div>

              <!-- Semifinals -->
              <div v-if="plecData.półfinały && plecData.półfinały.length > 0" class="bracket-round semifinals">
                <div class="round-header">
                  <div class="round-title">
                    <span class="round-icon">🥈</span>
                    <span class="round-name">PÓŁFINAŁY</span>
                  </div>
                  <div class="round-subtitle">{{ plecData.półfinały.length }} grup</div>
                </div>
                
                <div class="matches-grid">
                  <div v-for="grupa in plecData.półfinały" :key="grupa.grupa" class="match-card">
                    <div class="match-header">
                      <span class="match-title">Grupa {{ grupa.grupa }}</span>
                      <span class="advance-info">{{ grupa.awansują }} awansuje</span>
                    </div>
                    
                    <div v-if="grupa.zawodnicy && grupa.zawodnicy.length > 0" class="players-container">
                      <div v-for="(zawodnik, index) in grupa.zawodnicy" :key="zawodnik.nr_startowy"
                           :class="['player-card', getPlayerClass(index, grupa.awansują)]"
                           @click="showPlayerDetails(zawodnik)">
                        
                        <div class="player-position">
                          <div class="position-badge" :class="getPositionClass(index)">
                            {{ index + 1 }}
                          </div>
                        </div>
                        
                        <div class="player-info">
                          <div class="player-name">{{ zawodnik.imie }} {{ zawodnik.nazwisko }}</div>
                          <div class="player-meta">
                            <span class="player-number">#{{ zawodnik.nr_startowy }}</span>
                            <span class="player-time" :class="getTimeClass(zawodnik.czas_przejazdu_s)">
                              {{ zawodnik.czas_przejazdu_s || 'brak' }}{{ zawodnik.czas_przejazdu_s ? 's' : '' }}
                            </span>
                          </div>
                        </div>
                        
                        <div v-if="index < grupa.awansują" class="advance-indicator">
                          <span class="advance-icon">→</span>
                        </div>
                      </div>
                    </div>
                    
                    <div v-else class="waiting-state">
                      <div class="waiting-icon">⏳</div>
                      <div class="waiting-text">{{ grupa.info || 'Oczekuje na wyniki ćwierćfinałów' }}</div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Final Connector -->
              <div v-if="plecData.półfinały?.length > 0 && plecData.finał?.length > 0" 
                   class="round-connector">
                <div class="connector-line"></div>
                <div class="connector-text">FINAŁ</div>
              </div>

              <!-- Final -->
              <div v-if="plecData.finał && plecData.finał.length > 0" class="bracket-round final">
                <div class="round-header final-header">
                  <div class="round-title">
                    <span class="round-icon">🥇</span>
                    <span class="round-name">WIELKI FINAŁ</span>
                  </div>
                  <div class="round-subtitle">Walka o mistrzostwo</div>
                </div>
                
                <div class="matches-grid">
                  <div v-for="grupa in plecData.finał" :key="grupa.grupa" class="match-card final-card">
                    <div class="match-header">
                      <span class="match-title">Grupa {{ grupa.grupa }}</span>
                      <span class="final-badge">FINAŁ</span>
                    </div>
                    
                    <div v-if="grupa.zawodnicy && grupa.zawodnicy.length > 0" class="players-container">
                      <div v-for="(zawodnik, index) in grupa.zawodnicy" :key="zawodnik.nr_startowy"
                           :class="['player-card final-player', getFinalPlayerClass(index)]"
                           @click="showPlayerDetails(zawodnik)">
                        
                        <div class="player-position">
                          <div class="position-badge" :class="getPositionClass(index)">
                            {{ index + 1 }}
                          </div>
                        </div>
                        
                        <div class="player-info">
                          <div class="player-name">{{ zawodnik.imie }} {{ zawodnik.nazwisko }}</div>
                          <div class="player-meta">
                            <span class="player-number">#{{ zawodnik.nr_startowy }}</span>
                            <span class="player-time" :class="getTimeClass(zawodnik.czas_przejazdu_s)">
                              {{ zawodnik.czas_przejazdu_s || 'brak' }}{{ zawodnik.czas_przejazdu_s ? 's' : '' }}
                            </span>
                          </div>
                        </div>
                        
                        <div class="medal-indicator">
                          <span v-if="index === 0" class="medal">🥇</span>
                          <span v-else-if="index === 1" class="medal">🥈</span>
                          <span v-else-if="index === 2" class="medal">🥉</span>
                        </div>
                      </div>
                    </div>
                    
                    <div v-else class="waiting-state">
                      <div class="waiting-icon">⏳</div>
                      <div class="waiting-text">{{ grupa.info || 'Oczekuje na wyniki półfinałów' }}</div>
                    </div>
                  </div>
                </div>
              </div>

            </div>
          </div>

          <!-- Info Notice -->
          <div v-if="plecData.info" class="info-notice">
            <span class="info-icon">ℹ️</span>
            <span class="info-text">{{ plecData.info }}</span>
          </div>

        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state">
      <div class="empty-icon">🏆</div>
      <h3 class="empty-title">Brak danych drabinki</h3>
      <p class="empty-text">Nie znaleziono danych drabinki turniejowej dla wybranych filtrów.</p>
    </div>

    <!-- Player Details Modal -->
    <div v-if="selectedPlayer" class="player-modal" @click="closePlayerDetails">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Szczegóły zawodnika</h3>
          <button @click="closePlayerDetails" class="close-btn">✕</button>
        </div>
        <div class="modal-body">
          <div class="detail-row">
            <span class="detail-label">Imię i nazwisko:</span>
            <span class="detail-value">{{ selectedPlayer.imie }} {{ selectedPlayer.nazwisko }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Numer startowy:</span>
            <span class="detail-value">#{{ selectedPlayer.nr_startowy }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Czas przejazdu:</span>
            <span class="detail-value">
              {{ selectedPlayer.czas_przejazdu_s ? selectedPlayer.czas_przejazdu_s + 's' : 'Brak czasu' }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { apiClient } from '../utils/api.js'

const props = defineProps({ 
  filtry: {
    type: Object,
    default: () => ({ kategorie: [], plec: null })
  }
})

const emit = defineEmits(['podsumowanie-loaded'])

// State
const drabinka = ref({})
const isLoading = ref(true)
const selectedPlayer = ref(null)

// Computed
const filtrowaneKategorie = computed(() => {
  const { podsumowanie, ...kategorie } = drabinka.value
  
  if (!props.filtry?.kategorie?.length && !props.filtry?.plec) {
    return kategorie
  }
  
  const wynik = {}
  
  const kategorieDoWyswietlenia = (props.filtry.kategorie && props.filtry.kategorie.length > 0)
    ? Object.fromEntries(
        Object.entries(kategorie).filter(([key]) => props.filtry.kategorie.includes(key))
      )
    : kategorie
  
  for (const [kategoriaKey, kategoriaData] of Object.entries(kategorieDoWyswietlenia)) {
    if (!kategoriaData) continue
    
    if (!props.filtry.plec) {
      wynik[kategoriaKey] = kategoriaData
    } else {
      const plecNazwa = props.filtry.plec === 'M' ? 'Mężczyźni' : 'Kobiety'
      if (kategoriaData[plecNazwa]) {
        wynik[kategoriaKey] = { [plecNazwa]: kategoriaData[plecNazwa] }
      }
    }
  }
  
  return wynik
})

// Functions
function getPlayerClass(index, awansuja) {
  const classes = []
  if (index < awansuja) classes.push('advancing')
  if (index === 0) classes.push('winner')
  return classes
}

function getFinalPlayerClass(index) {
  const classes = []
  if (index === 0) classes.push('champion')
  else if (index === 1) classes.push('runner-up')
  else if (index === 2) classes.push('third-place')
  return classes
}

function getPositionClass(index) {
  if (index === 0) return 'gold'
  if (index === 1) return 'silver'
  if (index === 2) return 'bronze'
  return 'regular'
}

function getTimeClass(czas) {
  if (!czas) return 'no-time'
  const czasNum = parseFloat(czas)
  if (czasNum < 45) return 'excellent'
  if (czasNum < 50) return 'good'
  if (czasNum < 60) return 'average'
  return 'poor'
}

function showPlayerDetails(player) {
  selectedPlayer.value = player
}

function closePlayerDetails() {
  selectedPlayer.value = null
}

async function loadDrabinka() {
  try {
    isLoading.value = true
    const res = await apiClient.getDrabinka()
    drabinka.value = res.data
    console.log('Załadowano drabinkę:', Object.keys(res.data).length, 'kategorii')
    
    if (res.data.podsumowanie) {
      emit('podsumowanie-loaded', res.data.podsumowanie)
    }
  } catch (error) {
    console.error('Błąd ładowania drabinki:', error)
    drabinka.value = {}
  } finally {
    isLoading.value = false
  }
}

// Watchers
watch(() => props.filtry, (newFilters) => {
  console.log('Zmiana filtrów drabinki na:', newFilters)
}, { deep: true })

// Lifecycle
onMounted(loadDrabinka)
</script>

<style scoped>
.drabinka-container {
  padding: 1rem;
  font-family: 'Inter', sans-serif;
  background: var(--background);
  min-height: 100%;
}

/* Tournament Header */
.tournament-header {
  margin-bottom: 1.5rem;
}

.header-info {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  color: white;
  padding: 1.5rem;
  border-radius: 1rem;
  box-shadow: var(--shadow-lg);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.tournament-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
}

.title-icon {
  font-size: 1.75rem;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
}

.tournament-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.2);
  padding: 0.5rem 1rem;
  border-radius: 1rem;
  backdrop-filter: blur(10px);
}

.status-dot {
  width: 8px;
  height: 8px;
  background: var(--success);
  border-radius: 50%;
  animation: blink 1.5s infinite;
}

.status-text {
  font-weight: 500;
  font-size: 0.9rem;
}

/* Loading State */
.loading-state {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 3rem 1rem;
}

.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--border);
  border-top: 3px solid var(--primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.loading-spinner p {
  margin: 0;
  color: var(--text-secondary);
  font-weight: 500;
}

/* Categories Container */
.categories-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Category Section */
.category-section {
  background: var(--surface);
  border-radius: 1rem;
  box-shadow: var(--shadow);
  overflow: hidden;
  border: 1px solid var(--border);
}

.category-header {
  background: var(--secondary);
  color: white;
  padding: 1rem 1.5rem;
}

.category-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.category-icon {
  font-size: 1.5rem;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
}

.category-name {
  font-size: 1.3rem;
  font-weight: 600;
  margin: 0;
}

/* Gender Section */
.gender-section {
  padding: 1.5rem;
  border-bottom: 1px solid var(--border);
}

.gender-section:last-child {
  border-bottom: none;
}

.gender-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
  gap: 1rem;
  flex-wrap: wrap;
}

.gender-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.gender-icon {
  font-size: 1.5rem;
}

.gender-name {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

/* Statistics */
.stats-container {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.stat-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.75rem 1rem;
  border-radius: 0.75rem;
  box-shadow: var(--shadow);
  min-width: 60px;
  text-align: center;
}

.stat-card.total {
  background: var(--primary);
  color: white;
}

.stat-card.active {
  background: var(--success);
  color: white;
}

.stat-card.eliminated {
  background: var(--error);
  color: white;
}

.stat-number {
  font-size: 1.2rem;
  font-weight: 700;
  line-height: 1;
}

.stat-label {
  font-size: 0.7rem;
  font-weight: 500;
  opacity: 0.9;
  margin-top: 0.25rem;
}

/* Tournament Bracket */
.tournament-bracket {
  margin-top: 1.5rem;
}

/* Eliminated Section */
.eliminated-section {
  margin-bottom: 2rem;
  background: #fef3c7;
  border: 2px solid var(--secondary);
  border-radius: 1rem;
  padding: 1rem;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.1rem;
  font-weight: 600;
  color: #92400e;
  margin-bottom: 1rem;
}

.section-icon {
  font-size: 1.2rem;
}

.eliminated-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.75rem;
}

.eliminated-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: white;
  padding: 0.75rem;
  border-radius: 0.75rem;
  border: 1px solid var(--secondary);
  box-shadow: var(--shadow);
}

.player-number-small {
  background: var(--secondary);
  color: white;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  font-weight: 600;
  flex-shrink: 0;
}

.player-info-small {
  flex: 1;
  min-width: 0;
}

.player-name-small {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.2;
}

.player-time-small {
  font-size: 0.8rem;
  color: var(--text-secondary);
  font-weight: 500;
}

/* Bracket Main */
.bracket-main {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Bracket Round */
.bracket-round {
  background: var(--surface);
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: var(--shadow);
  border: 1px solid var(--border);
}

.bracket-round.final {
  background: linear-gradient(135deg, #fef3c7 0%, #fbbf24 100%);
  border: 2px solid var(--secondary);
}

/* Round Header */
.round-header {
  text-align: center;
  margin-bottom: 1.5rem;
}

.final-header {
  background: var(--secondary);
  color: white;
  margin: -1.5rem -1.5rem 1.5rem -1.5rem;
  padding: 1.5rem;
  border-radius: 1rem 1rem 0 0;
}

.round-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.final-header .round-title {
  color: white;
}

.round-icon {
  font-size: 1.5rem;
}

.round-name {
  letter-spacing: 0.05em;
}

.round-subtitle {
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--text-secondary);
}

.final-header .round-subtitle {
  color: white;
  opacity: 0.9;
}

/* Matches Grid */
.matches-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
}

/* Match Card */
.match-card {
  background: var(--background);
  border: 1px solid var(--border);
  border-radius: 1rem;
  padding: 1rem;
  transition: all 0.2s ease;
}

.match-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.final-card {
  background: linear-gradient(135deg, #fffbeb, #fef3c7);
  border: 2px solid var(--secondary);
}

/* Match Header */
.match-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--border);
}

.match-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.advance-info {
  background: var(--success);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.8rem;
  font-weight: 500;
}

.final-badge {
  background: var(--secondary);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.8rem;
  font-weight: 600;
}

/* Players Container */
.players-container {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

/* Player Card */
.player-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: var(--surface);
  padding: 1rem;
  border-radius: 0.75rem;
  border: 1px solid var(--border);
  transition: all 0.2s ease;
  cursor: pointer;
}

.player-card:hover {
  transform: translateX(4px);
  box-shadow: var(--shadow);
}

.player-card.advancing {
  background: linear-gradient(135deg, #dcfce7, #bbf7d0);
  border-color: var(--success);
}

.player-card.winner {
  background: linear-gradient(135deg, #fef3c7, #fbbf24);
  border-color: var(--secondary);
}

.final-player.champion {
  background: linear-gradient(135deg, #fef3c7, #fbbf24);
  border: 2px solid var(--secondary);
  box-shadow: var(--shadow-lg);
  animation: glow 2s infinite;
}

.final-player.runner-up {
  background: linear-gradient(135deg, #f3f4f6, #d1d5db);
  border: 2px solid #9ca3af;
}

.final-player.third-place {
  background: linear-gradient(135deg, #fef2f2, #fca5a5);
  border: 2px solid var(--error);
}

/* Player Position */
.player-position {
  flex-shrink: 0;
}

.position-badge {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--text-muted);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  font-weight: 600;
  box-shadow: var(--shadow);
}

.position-badge.gold {
  background: #fbbf24;
}

.position-badge.silver {
  background: #9ca3af;
}

.position-badge.bronze {
  background: #f97316;
}

/* Player Info */
.player-info {
  flex: 1;
  min-width: 0;
}

.player-name {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
  line-height: 1.2;
}

.player-meta {
  display: flex;
  gap: 0.75rem;
  align-items: center;
  flex-wrap: wrap;
}

.player-number {
  background: var(--primary);
  color: white;
  padding: 0.125rem 0.5rem;
  border-radius: 0.5rem;
  font-size: 0.8rem;
  font-weight: 500;
}

.player-time {
  font-size: 0.9rem;
  font-weight: 600;
  padding: 0.125rem 0.5rem;
  border-radius: 0.5rem;
}

.player-time.excellent {
  background: #dcfce7;
  color: #166534;
}

.player-time.good {
  background: #dbeafe;
  color: #1e40af;
}

.player-time.average {
  background: #fef3c7;
  color: #92400e;
}

.player-time.poor {
  background: #fecaca;
  color: #991b1b;
}

.player-time.no-time {
  background: var(--background);
  color: var(--text-muted);
  font-style: italic;
}

/* Advance Indicator */
.advance-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  flex-shrink: 0;
}

.advance-icon {
  color: var(--success);
  font-size: 1.2rem;
  font-weight: 900;
  animation: bounce 1.5s infinite;
}

/* Medal Indicator */
.medal-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  flex-shrink: 0;
}

.medal {
  font-size: 1.8rem;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
  animation: bounce 2s infinite;
}

/* Round Connector */
.round-connector {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  margin: 1.5rem 0;
}

.connector-line {
  width: 3px;
  height: 40px;
  background: var(--primary);
  border-radius: 2px;
}

.connector-text {
  background: var(--primary);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 1rem;
  font-weight: 600;
  font-size: 0.8rem;
  letter-spacing: 0.05em;
}

/* Waiting State */
.waiting-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 2rem;
  background: var(--background);
  border: 2px dashed var(--border);
  border-radius: 1rem;
  text-align: center;
}

.waiting-icon {
  font-size: 2rem;
  opacity: 0.6;
}

.waiting-text {
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--text-secondary);
  font-style: italic;
}

/* Info Notice */
.info-notice {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-top: 1.5rem;
  padding: 1rem;
  background: #fef3c7;
  border: 1px solid var(--secondary);
  border-radius: 1rem;
  color: #92400e;
}

.info-icon {
  font-size: 1.2rem;
  flex-shrink: 0;
}

.info-text {
  font-weight: 500;
  font-size: 0.9rem;
}

/* Empty State */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 1rem;
  text-align: center;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 0.5rem 0;
}

.empty-text {
  font-size: 1rem;
  color: var(--text-secondary);
  margin: 0;
  max-width: 300px;
}

/* Player Details Modal */
.player-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 200;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.modal-content {
  background: var(--surface);
  border-radius: 1rem;
  max-width: 400px;
  width: 100%;
  box-shadow: var(--shadow-lg);
  animation: slideDown 0.3s ease;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--border);
}

.modal-header h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.2rem;
  color: var(--text-secondary);
  cursor: pointer;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.2s ease;
}

.close-btn:hover {
  background: var(--background);
  color: var(--text-primary);
}

.modal-body {
  padding: 1rem 1.5rem;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--border);
}

.detail-row:last-child {
  border-bottom: none;
}

.detail-label {
  font-weight: 500;
  color: var(--text-secondary);
  font-size: 0.9rem;
}

.detail-value {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.9rem;
}

/* Animations */
@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0.3; }
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-6px); }
  60% { transform: translateY(-3px); }
}

@keyframes glow {
  0%, 100% { box-shadow: var(--shadow-lg); }
  50% { box-shadow: 0 12px 35px rgba(245, 158, 11, 0.6); }
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Very small screens */
@media (max-width: 360px) {
  .drabinka-container {
    padding: 0.75rem;
  }
  
  .header-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .tournament-title {
    font-size: 1.3rem;
  }
  
  .title-icon {
    font-size: 1.5rem;
  }
  
  .gender-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .stats-container {
    gap: 0.5rem;
  }
  
  .stat-card {
    padding: 0.5rem 0.75rem;
    min-width: 50px;
  }
  
  .stat-number {
    font-size: 1rem;
  }
  
  .stat-label {
    font-size: 0.65rem;
  }
  
  .matches-grid {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }
  
  .match-card {
    padding: 0.75rem;
  }
  
  .player-card {
    padding: 0.75rem;
    gap: 0.75rem;
  }
  
  .player-name {
    font-size: 0.9rem;
  }
  
  .position-badge {
    width: 28px;
    height: 28px;
    font-size: 0.8rem;
  }
  
  .advance-indicator,
  .medal-indicator {
    width: 28px;
    height: 28px;
  }
  
  .medal {
    font-size: 1.5rem;
  }
  
  .eliminated-grid {
    grid-template-columns: 1fr;
  }
}

/* Landscape mode for small screens */
@media (max-height: 500px) and (orientation: landscape) {
  .header-info {
    padding: 1rem;
  }
  
  .tournament-title {
    font-size: 1.2rem;
  }
  
  .gender-section {
    padding: 1rem;
  }
  
  .bracket-round {
    padding: 1rem;
  }
  
  .round-header {
    margin-bottom: 1rem;
  }
  
  .waiting-state {
    padding: 1.5rem;
  }
}

/* Medium screens */
@media (min-width: 768px) and (max-width: 1024px) {
  .matches-grid {
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  }
  
  .eliminated-grid {
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  }
}

/* Large screens */
@media (min-width: 1025px) {
  .drabinka-container {
    padding: 2rem;
  }
  
  .categories-container {
    gap: 3rem;
  }
  
  .tournament-header {
    margin-bottom: 2rem;
  }
  
  .gender-section {
    padding: 2rem;
  }
  
  .bracket-round {
    padding: 2rem;
  }
  
  .matches-grid {
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 1.5rem;
  }
  
  .eliminated-grid {
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  }
}
</style>

