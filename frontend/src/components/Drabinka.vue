<template>
  <div class="drabinka-container">
    <div class="section-header">
      <h2 class="section-title">
        <span class="title-icon">🏆</span>
        Drabinka pucharowa
      </h2>
      <div class="tournament-status">
        <span class="status-dot"></span>
        <span class="status-text">Turniej w toku</span>
      </div>
    </div>
    
    <!-- Kategorie -->
    <div v-for="(kategoriaData, kategoriaNazwa) in filtrowaneKategorie" :key="kategoriaNazwa" 
         class="category-section">
      
      <div class="category-header">
        <div class="category-title">
          <span class="category-icon">🏅</span>
          <h3 class="category-name">{{ kategoriaNazwa }}</h3>
        </div>
      </div>
      
      <!-- Płcie w kategorii -->
      <div v-for="(plecData, plecNazwa) in kategoriaData" :key="plecNazwa"
           class="gender-section">
        
        <div class="gender-header">
          <div class="gender-title">
            <span class="gender-icon">{{ plecNazwa === 'Mężczyźni' ? '👨' : '👩' }}</span>
            <h4 class="gender-name">{{ plecNazwa }}</h4>
          </div>
          
          <!-- Statystyki -->
          <div v-if="plecData.statystyki" class="stats-badges">
            <div class="stat-badge total">
              <span class="stat-number">{{ plecData.statystyki.łącznie_zawodników }}</span>
              <span class="stat-label">Łącznie</span>
            </div>
            <div class="stat-badge active">
              <span class="stat-number">{{ plecData.statystyki.w_ćwierćfinałach }}</span>
              <span class="stat-label">W grze</span>
            </div>
            <div v-if="plecData.statystyki.odpadło > 0" class="stat-badge eliminated">
              <span class="stat-number">{{ plecData.statystyki.odpadło }}</span>
              <span class="stat-label">Odpadło</span>
            </div>
          </div>
        </div>

        <!-- Tournament Bracket - Nowy Professional Design -->
        <div class="tournament-bracket">
          
          <!-- Odpadli zawodnicy -->
          <div v-if="plecData.odpadli && plecData.odpadli.length > 0" class="eliminated-section">
            <div class="section-title eliminated-title">
              <span class="section-icon">❌</span>
              Zawodnicy odpadli z turnieju
            </div>
            <div class="eliminated-players">
              <div v-for="zawodnik in plecData.odpadli" :key="zawodnik.nr_startowy"
                   class="eliminated-player">
                <div class="player-number">{{ zawodnik.nr_startowy }}</div>
                <div class="player-info">
                  <div class="player-name">{{ zawodnik.imie }} {{ zawodnik.nazwisko }}</div>
                  <div class="player-time" v-if="zawodnik.czas_przejazdu_s">
                    {{ zawodnik.czas_przejazdu_s }}s
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Główna drabinka -->
          <div class="bracket-main">
            
            <!-- Ćwierćfinały -->
            <div v-if="plecData.ćwierćfinały && plecData.ćwierćfinały.length > 0" class="bracket-round quarterfinals">
              <div class="round-header">
                <div class="round-title">
                  <span class="round-icon">🥉</span>
                  <span class="round-name">ĆWIERĆFINAŁY</span>
                </div>
                <div class="round-subtitle">{{ plecData.ćwierćfinały.length }} grup</div>
              </div>
              
              <div class="matches-container">
                <div v-for="grupa in plecData.ćwierćfinały" :key="grupa.grupa" class="match-card">
                  <div class="match-header">
                    <span class="match-title">Grupa {{ grupa.grupa }}</span>
                    <span class="advance-info">{{ grupa.awansują }} awansuje</span>
                  </div>
                  
                  <div class="players-list">
                    <div v-for="(zawodnik, index) in grupa.zawodnicy" :key="zawodnik.nr_startowy"
                         :class="['player-entry', { advancing: index < grupa.awansują, winner: index === 0 }]">
                      
                      <!-- Desktop view -->
                      <div class="desktop-player-layout desktop-only">
                        <div class="position-indicator">
                          <span class="position-number">{{ index + 1 }}</span>
                        </div>
                        
                        <div class="player-number-badge">{{ zawodnik.nr_startowy }}</div>
                        
                        <div class="player-details">
                          <div class="player-name">{{ zawodnik.imie }} {{ zawodnik.nazwisko }}</div>
                          <div class="player-time" :class="getTimeClass(zawodnik.czas_przejazdu_s)">
                            {{ zawodnik.czas_przejazdu_s || 'brak' }}{{ zawodnik.czas_przejazdu_s ? 's' : '' }}
                          </div>
                        </div>
                        
                        <div v-if="index < grupa.awansują" class="advance-indicator">
                          <span class="advance-arrow">→</span>
                        </div>
                      </div>

                      <!-- Mobile card view -->
                      <div class="mobile-player-card mobile-only">
                        <div class="mobile-card-header">
                          <div class="position-badge-card" :class="{ 
                            'gold': index === 0, 
                            'silver': index === 1, 
                            'bronze': index === 2,
                            'regular': index > 2 
                          }">
                            {{ index + 1 }}
                          </div>
                          <div class="player-name-card">{{ zawodnik.imie }} {{ zawodnik.nazwisko }}</div>
                          <div v-if="index < grupa.awansują" class="advance-badge">AWANS</div>
                        </div>
                        <div class="mobile-card-details">
                          <div class="detail-row">
                            <div class="detail-item">
                              <span class="detail-label">Nr startowy:</span>
                              <span class="detail-value">{{ zawodnik.nr_startowy }}</span>
                            </div>
                            <div class="detail-item">
                              <span class="detail-label">Czas:</span>
                              <span class="detail-value time-text" :class="getTimeClass(zawodnik.czas_przejazdu_s)">
                                {{ zawodnik.czas_przejazdu_s || 'brak' }}{{ zawodnik.czas_przejazdu_s ? 's' : '' }}
                              </span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Połączenie między rundami -->
            <div v-if="plecData.ćwierćfinały && plecData.ćwierćfinały.length > 0 && plecData.półfinały && plecData.półfinały.length > 0" 
                 class="round-connector">
              <div class="connector-line"></div>
              <div class="connector-text">AWANS</div>
            </div>

            <!-- Półfinały -->
            <div v-if="plecData.półfinały && plecData.półfinały.length > 0" class="bracket-round semifinals">
              <div class="round-header">
                <div class="round-title">
                  <span class="round-icon">🥈</span>
                  <span class="round-name">PÓŁFINAŁY</span>
                </div>
                <div class="round-subtitle">{{ plecData.półfinały.length }} grup</div>
              </div>
              
              <div class="matches-container">
                <div v-for="grupa in plecData.półfinały" :key="grupa.grupa" class="match-card">
                  <div class="match-header">
                    <span class="match-title">Grupa {{ grupa.grupa }}</span>
                    <span class="advance-info">{{ grupa.awansują }} awansuje</span>
                  </div>
                  
                  <div v-if="grupa.zawodnicy && grupa.zawodnicy.length > 0" class="players-list">
                    <div v-for="(zawodnik, index) in grupa.zawodnicy" :key="zawodnik.nr_startowy"
                         :class="['player-entry', { advancing: index < grupa.awansują, winner: index === 0 }]">
                      
                      <!-- Desktop view -->
                      <div class="desktop-player-layout desktop-only">
                        <div class="position-indicator">
                          <span class="position-number">{{ index + 1 }}</span>
                        </div>
                        
                        <div class="player-number-badge">{{ zawodnik.nr_startowy }}</div>
                        
                        <div class="player-details">
                          <div class="player-name">{{ zawodnik.imie }} {{ zawodnik.nazwisko }}</div>
                          <div class="player-time" :class="getTimeClass(zawodnik.czas_przejazdu_s)">
                            {{ zawodnik.czas_przejazdu_s || 'brak' }}{{ zawodnik.czas_przejazdu_s ? 's' : '' }}
                          </div>
                        </div>
                        
                        <div v-if="index < grupa.awansują" class="advance-indicator">
                          <span class="advance-arrow">→</span>
                        </div>
                      </div>

                      <!-- Mobile card view -->
                      <div class="mobile-player-card mobile-only">
                        <div class="mobile-card-header">
                          <div class="position-badge-card" :class="{ 
                            'gold': index === 0, 
                            'silver': index === 1, 
                            'bronze': index === 2,
                            'regular': index > 2 
                          }">
                            {{ index + 1 }}
                          </div>
                          <div class="player-name-card">{{ zawodnik.imie }} {{ zawodnik.nazwisko }}</div>
                          <div v-if="index < grupa.awansują" class="advance-badge">AWANS</div>
                        </div>
                        <div class="mobile-card-details">
                          <div class="detail-row">
                            <div class="detail-item">
                              <span class="detail-label">Nr startowy:</span>
                              <span class="detail-value">{{ zawodnik.nr_startowy }}</span>
                            </div>
                            <div class="detail-item">
                              <span class="detail-label">Czas:</span>
                              <span class="detail-value time-text" :class="getTimeClass(zawodnik.czas_przejazdu_s)">
                                {{ zawodnik.czas_przejazdu_s || 'brak' }}{{ zawodnik.czas_przejazdu_s ? 's' : '' }}
                              </span>
                            </div>
                          </div>
                        </div>
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

            <!-- Połączenie do finału -->
            <div v-if="plecData.półfinały && plecData.półfinały.length > 0 && plecData.finał && plecData.finał.length > 0" 
                 class="round-connector">
              <div class="connector-line"></div>
              <div class="connector-text">FINAŁ</div>
            </div>

            <!-- Finał -->
            <div v-if="plecData.finał && plecData.finał.length > 0" class="bracket-round final">
              <div class="round-header final-header">
                <div class="round-title">
                  <span class="round-icon">🥇</span>
                  <span class="round-name">WIELKI FINAŁ</span>
                </div>
                <div class="round-subtitle">Walka o mistrzostwo</div>
              </div>
              
              <div class="matches-container">
                <div v-for="grupa in plecData.finał" :key="grupa.grupa" class="match-card final-card">
                  <div class="match-header final-match-header">
                    <span class="match-title">Grupa {{ grupa.grupa }}</span>
                    <span class="final-badge">FINAŁ</span>
                  </div>
                  
                  <div v-if="grupa.zawodnicy && grupa.zawodnicy.length > 0" class="players-list final-players">
                    <div v-for="(zawodnik, index) in grupa.zawodnicy" :key="zawodnik.nr_startowy"
                         :class="['player-entry final-player', { 
                           champion: index === 0, 
                           runner_up: index === 1, 
                           third_place: index === 2 
                         }]">
                      
                      <!-- Desktop view -->
                      <div class="desktop-player-layout desktop-only">
                        <div class="position-indicator final-position">
                          <span class="position-number">{{ index + 1 }}</span>
                        </div>
                        
                        <div class="player-number-badge">{{ zawodnik.nr_startowy }}</div>
                        
                        <div class="player-details">
                          <div class="player-name">{{ zawodnik.imie }} {{ zawodnik.nazwisko }}</div>
                          <div class="player-time" :class="getTimeClass(zawodnik.czas_przejazdu_s)">
                            {{ zawodnik.czas_przejazdu_s || 'brak' }}{{ zawodnik.czas_przejazdu_s ? 's' : '' }}
                          </div>
                        </div>
                        
                        <div class="medal-indicator">
                          <span v-if="index === 0" class="medal gold">🥇</span>
                          <span v-else-if="index === 1" class="medal silver">🥈</span>
                          <span v-else-if="index === 2" class="medal bronze">🥉</span>
                        </div>
                      </div>

                      <!-- Mobile card view -->
                      <div class="mobile-player-card mobile-only">
                        <div class="mobile-card-header">
                          <div class="position-badge-card" :class="{ 
                            'gold': index === 0, 
                            'silver': index === 1, 
                            'bronze': index === 2,
                            'regular': index > 2 
                          }">
                            {{ index + 1 }}
                          </div>
                          <div class="player-name-card">{{ zawodnik.imie }} {{ zawodnik.nazwisko }}</div>
                          <div v-if="index === 0" class="medal-badge">🥇</div>
                          <div v-else-if="index === 1" class="medal-badge">🥈</div>
                          <div v-else-if="index === 2" class="medal-badge">🥉</div>
                        </div>
                        <div class="mobile-card-details">
                          <div class="detail-row">
                            <div class="detail-item">
                              <span class="detail-label">Nr startowy:</span>
                              <span class="detail-value">{{ zawodnik.nr_startowy }}</span>
                            </div>
                            <div class="detail-item">
                              <span class="detail-label">Czas:</span>
                              <span class="detail-value time-text" :class="getTimeClass(zawodnik.czas_przejazdu_s)">
                                {{ zawodnik.czas_przejazdu_s || 'brak' }}{{ zawodnik.czas_przejazdu_s ? 's' : '' }}
                              </span>
                            </div>
                          </div>
                        </div>
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

        <!-- Info o małej liczbie zawodników -->
        <div v-if="plecData.info" class="info-notice">
          <span class="info-icon">ℹ️</span>
          <span class="info-text">{{ plecData.info }}</span>
        </div>

      </div>
    </div>

    <!-- Komunikat gdy brak danych -->
    <div v-if="Object.keys(filtrowaneKategorie).length === 0" class="no-data">
      <div class="no-data-icon">🔍</div>
      <h3 class="no-data-title">Brak danych drabinki</h3>
      <p class="no-data-text">Nie znaleziono danych drabinki turniejowej dla wybranych filtrów.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'

const props = defineProps({ 
  filtry: {
    type: Object,
    default: () => ({ kategorie: [], plec: null })
  }
})
const emit = defineEmits(['podsumowanie-loaded'])
const drabinka = ref({})

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

function getTimeClass(czas) {
  if (!czas) return 'no-time'
  const czasNum = parseFloat(czas)
  if (czasNum < 45) return 'excellent'
  if (czasNum < 50) return 'good'
  if (czasNum < 60) return 'average'
  return 'poor'
}

async function loadDrabinka() {
  try {
    const res = await axios.get('/api/drabinka')
    drabinka.value = res.data
    console.log('Załadowano drabinkę:', res.data)
    
    if (res.data.podsumowanie) {
      emit('podsumowanie-loaded', res.data.podsumowanie)
    }
  } catch (error) {
    console.error('Błąd ładowania drabinki:', error)
    drabinka.value = {}
  }
}

onMounted(loadDrabinka)

watch(() => props.filtry, (newFilters) => {
  console.log('Zmiana filtrów drabinki na:', newFilters)
}, { deep: true })
</script>

<style scoped>
.drabinka-container {
  padding: 2rem;
  font-family: 'Inter', sans-serif;
  background: #f8fafc;
  min-height: 100vh;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 3rem;
  padding: 2rem;
  background: linear-gradient(135deg, #1e40af 0%, #3730a3 100%);
  color: white;
  border-radius: 1.5rem;
  box-shadow: 0 10px 30px rgba(30, 64, 175, 0.3);
}

.section-title {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 2.5rem;
  font-weight: 900;
  margin: 0;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.title-icon {
  font-size: 3rem;
  filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
  animation: pulse 2s infinite;
}

.tournament-status {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: rgba(255, 255, 255, 0.2);
  padding: 1rem 1.5rem;
  border-radius: 2rem;
  backdrop-filter: blur(10px);
}

.status-dot {
  width: 12px;
  height: 12px;
  background: #22c55e;
  border-radius: 50%;
  animation: blink 1.5s infinite;
}

.status-text {
  font-weight: 700;
  font-size: 1rem;
}

.category-section {
  margin-bottom: 4rem;
  background: white;
  border-radius: 2rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  border: 1px solid #e2e8f0;
}

.category-header {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  color: white;
  padding: 2rem;
}

.category-title {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.category-icon {
  font-size: 2rem;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
}

.category-name {
  font-size: 2rem;
  font-weight: 800;
  margin: 0;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
}

.gender-section {
  padding: 2rem;
  border-bottom: 1px solid #f1f5f9;
}

.gender-section:last-child {
  border-bottom: none;
}

.gender-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f1f5f9;
}

.gender-title {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.gender-icon {
  font-size: 2rem;
}

.gender-name {
  font-size: 1.75rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0;
}

.stats-badges {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.stat-badge {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem 1.5rem;
  border-radius: 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  min-width: 80px;
}

.stat-badge.total {
  background: linear-gradient(135deg, #3b82f6, #1e40af);
  color: white;
}

.stat-badge.active {
  background: linear-gradient(135deg, #22c55e, #16a34a);
  color: white;
}

.stat-badge.eliminated {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  color: white;
}

.stat-number {
  font-size: 1.5rem;
  font-weight: 900;
  line-height: 1;
}

.stat-label {
  font-size: 0.8rem;
  font-weight: 600;
  opacity: 0.9;
  margin-top: 0.25rem;
}

.tournament-bracket {
  margin-top: 2rem;
}

.eliminated-section {
  margin-bottom: 3rem;
  background: #fef3c7;
  border: 2px solid #f59e0b;
  border-radius: 1.5rem;
  padding: 2rem;
}

.eliminated-section .section-title {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: #92400e;
  margin-bottom: 1.5rem;
}

.eliminated-title {
  color: #92400e;
}

.section-icon {
  font-size: 1.75rem;
}

.eliminated-players {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

.eliminated-player {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: white;
  padding: 1rem;
  border-radius: 1rem;
  border: 2px solid #f59e0b;
  box-shadow: 0 2px 8px rgba(245, 158, 11, 0.2);
}

.bracket-main {
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.bracket-round {
  background: white;
  border-radius: 1.5rem;
  padding: 2rem;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
}

.bracket-round.final {
  background: linear-gradient(135deg, #fef3c7 0%, #fbbf24 100%);
  border: 3px solid #f59e0b;
  box-shadow: 0 12px 35px rgba(245, 158, 11, 0.3);
}

.round-header {
  text-align: center;
  margin-bottom: 2rem;
}

.final-header {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
  margin: -2rem -2rem 2rem -2rem;
  padding: 2rem;
  border-radius: 1.5rem 1.5rem 0 0;
}

.round-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  font-size: 1.75rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 0.5rem;
}

.final-header .round-title {
  color: white;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
}

.round-icon {
  font-size: 2rem;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
}

.round-name {
  letter-spacing: 0.05em;
}

.round-subtitle {
  font-size: 1rem;
  font-weight: 600;
  color: #64748b;
  opacity: 0.8;
}

.final-header .round-subtitle {
  color: white;
  opacity: 0.9;
}

.matches-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
}

.match-card {
  background: #f8fafc;
  border: 2px solid #e2e8f0;
  border-radius: 1.5rem;
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.match-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.final-card {
  background: linear-gradient(135deg, #fffbeb, #fef3c7);
  border: 3px solid #f59e0b;
  box-shadow: 0 8px 25px rgba(245, 158, 11, 0.2);
}

.match-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e2e8f0;
}

.final-match-header {
  border-bottom-color: #f59e0b;
}

.match-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #0f172a;
}

.advance-info {
  background: #22c55e;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 1rem;
  font-size: 0.8rem;
  font-weight: 700;
}

.final-badge {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 1rem;
  font-size: 0.8rem;
  font-weight: 700;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
}

.players-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.player-entry {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: white;
  padding: 1rem;
  border-radius: 1rem;
  border: 2px solid #e2e8f0;
  transition: all 0.2s ease;
}

.player-entry:hover {
  transform: translateX(4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.player-entry.advancing {
  background: linear-gradient(135deg, #dcfce7, #bbf7d0);
  border-color: #22c55e;
  box-shadow: 0 4px 12px rgba(34, 197, 94, 0.2);
}

.player-entry.winner {
  background: linear-gradient(135deg, #fef3c7, #fbbf24);
  border-color: #f59e0b;
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
}

.final-player.champion {
  background: linear-gradient(135deg, #fef3c7, #fbbf24);
  border: 3px solid #f59e0b;
  box-shadow: 0 8px 25px rgba(245, 158, 11, 0.4);
  animation: glow 2s infinite;
}

.final-player.runner_up {
  background: linear-gradient(135deg, #f3f4f6, #d1d5db);
  border: 3px solid #9ca3af;
  box-shadow: 0 6px 20px rgba(156, 163, 175, 0.3);
}

.final-player.third_place {
  background: linear-gradient(135deg, #fef2f2, #fca5a5);
  border: 3px solid #ef4444;
  box-shadow: 0 6px 20px rgba(239, 68, 68, 0.3);
}

.position-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: #64748b;
  color: white;
  border-radius: 50%;
  font-weight: 900;
  font-size: 1.1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.final-position {
  width: 50px;
  height: 50px;
  font-size: 1.3rem;
}

.player-number-badge {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 45px;
  height: 45px;
  background: #1e40af;
  color: white;
  border-radius: 50%;
  font-weight: 700;
  font-size: 1.1rem;
  box-shadow: 0 2px 8px rgba(30, 64, 175, 0.3);
}

.player-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.player-name {
  font-weight: 700;
  font-size: 1.1rem;
  color: #0f172a;
}

.player-time {
  font-weight: 600;
  font-size: 1rem;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  display: inline-block;
  max-width: fit-content;
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
  background: #f1f5f9;
  color: #64748b;
  font-style: italic;
}

.advance-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
}

.advance-arrow {
  color: #22c55e;
  font-size: 1.5rem;
  font-weight: 900;
  animation: bounce 1.5s infinite;
}

.medal-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
}

.medal {
  font-size: 2.5rem;
  filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
  animation: bounce 2s infinite;
}

.round-connector {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  margin: 2rem 0;
}

.connector-line {
  width: 4px;
  height: 60px;
  background: linear-gradient(to bottom, #1e40af, #3730a3);
  border-radius: 2px;
  box-shadow: 0 2px 8px rgba(30, 64, 175, 0.3);
}

.connector-text {
  background: #1e40af;
  color: white;
  padding: 0.75rem 2rem;
  border-radius: 2rem;
  font-weight: 700;
  font-size: 1rem;
  letter-spacing: 0.05em;
  box-shadow: 0 4px 12px rgba(30, 64, 175, 0.3);
}

.waiting-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 2rem;
  background: #f8fafc;
  border: 2px dashed #cbd5e1;
  border-radius: 1rem;
  text-align: center;
}

.waiting-icon {
  font-size: 3rem;
  opacity: 0.6;
}

.waiting-text {
  font-size: 1.1rem;
  font-weight: 600;
  color: #64748b;
  font-style: italic;
}

.info-notice {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
  padding: 1.5rem;
  background: #fef3c7;
  border: 2px solid #f59e0b;
  border-radius: 1rem;
  color: #92400e;
}

.info-icon {
  font-size: 1.5rem;
}

.info-text {
  font-weight: 600;
  font-size: 1rem;
}

.no-data {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 2rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
}

.no-data-icon {
  font-size: 4rem;
  margin-bottom: 1.5rem;
  opacity: 0.5;
}

.no-data-title {
  font-size: 2rem;
  font-weight: 700;
  color: #374151;
  margin: 0 0 1rem 0;
}

.no-data-text {
  font-size: 1.1rem;
  color: #6b7280;
  margin: 0;
}

/* Animations */
@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

@keyframes blink {
  0%, 50% {
    opacity: 1;
  }
  51%, 100% {
    opacity: 0.3;
  }
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-8px);
  }
  60% {
    transform: translateY(-4px);
  }
}

@keyframes glow {
  0%, 100% {
    box-shadow: 0 8px 25px rgba(245, 158, 11, 0.4);
  }
  50% {
    box-shadow: 0 12px 35px rgba(245, 158, 11, 0.6);
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .drabinka-container {
    padding: 1rem;
  }
  
  .section-header {
    flex-direction: column;
    gap: 1.5rem;
    text-align: center;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .gender-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .stats-badges {
    justify-content: center;
  }
  
  .matches-container {
    grid-template-columns: 1fr;
  }
  
  .eliminated-players {
    grid-template-columns: 1fr;
  }
  
  .player-entry {
    padding: 0.75rem;
    gap: 0.75rem;
  }
  
  .player-name {
    font-size: 1rem;
  }
  
  .round-title {
    font-size: 1.5rem;
  }
}

@media (max-width: 480px) {
  .section-title {
    font-size: 1.75rem;
  }
  
  .title-icon {
    font-size: 2.5rem;
  }
  
  .category-name {
    font-size: 1.5rem;
  }
  
  .gender-name {
    font-size: 1.5rem;
  }
  
  .player-entry {
    flex-direction: column;
    text-align: center;
    gap: 0.5rem;
  }
  
  .advance-indicator {
    transform: rotate(90deg);
  }
  
  .round-title {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .round-name {
    font-size: 1.25rem;
  }
}

/* Mobile cards styles */
@media (max-width: 600px) {
  .mobile-hidden {
    display: none !important;
  }
  
  .mobile-only {
    display: block !important;
  }
  
  .desktop-only {
    display: none !important;
  }
  
  /* Usunięcie kolorowych tłem player-entry na mobile */
  .player-entry {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    box-shadow: none !important;
  }
  
  .player-entry.advancing {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
  }
  
  .player-entry.winner {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
  }
  
  .final-player.champion {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    animation: none !important;
  }
  
  .final-player.runner_up {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
  }
  
  .final-player.third_place {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
  }
  
  .mobile-player-card {
    background: white !important;
    border: 1px solid #e2e8f0;
    border-radius: 0.75rem;
    padding: 1rem;
    margin: 0.5rem 0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    transition: all 0.2s ease;
    width: 100%;
  }
  
  .mobile-player-card:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    transform: translateY(-1px);
  }
  
  .mobile-card-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.75rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid #e2e8f0;
  }
  
  .position-badge-card {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 35px;
    height: 35px;
    border-radius: 50%;
    font-weight: 900;
    font-size: 1rem;
    color: white;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    flex-shrink: 0;
  }
  
  .position-badge-card.gold {
    background: linear-gradient(135deg, #f59e0b, #d97706);
  }
  
  .position-badge-card.silver {
    background: linear-gradient(135deg, #9ca3af, #6b7280);
  }
  
  .position-badge-card.bronze {
    background: linear-gradient(135deg, #ef4444, #dc2626);
  }
  
  .position-badge-card.regular {
    background: linear-gradient(135deg, #64748b, #475569);
  }
  
  .player-name-card {
    font-weight: 700;
    font-size: 1.1rem;
    color: #0f172a;
    flex: 1;
  }
  
  .advance-badge {
    background: #22c55e;
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 1rem;
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  
  .medal-badge {
    font-size: 1.5rem;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
  }
  
  .mobile-card-details {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .detail-row {
    display: flex;
    gap: 1rem;
  }
  
  .detail-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .detail-label {
    font-weight: 600;
    color: #64748b;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  
  .detail-value {
    font-weight: 600;
    font-size: 0.9rem;
    color: #0f172a;
  }
  
  .time-text.excellent {
    color: #166534;
    font-weight: 800;
  }
  
  .time-text.good {
    color: #1e40af;
    font-weight: 800;
  }
  
  .time-text.average {
    color: #92400e;
    font-weight: 800;
  }
  
  .time-text.poor {
    color: #991b1b;
    font-weight: 800;
  }
  
  .time-text.no-time {
    color: #64748b;
    font-style: italic;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
    padding: 1rem;
    border-radius: 0.75rem;
    text-align: left;
  }
  .section-title {
    justify-content: flex-start;
    font-size: 1.2rem;
    gap: 0.75rem;
  }
  .title-icon {
    width: 32px;
    height: 32px;
    font-size: 1.2rem;
    border-radius: 5px;
  }
  .tournament-status {
    align-self: flex-end;
    margin-top: 0.5rem;
    padding: 0.5rem 1rem;
    font-size: 0.95rem;
  }
  .category-section {
    border-radius: 1rem;
    margin-bottom: 2rem;
    padding: 0.5rem;
  }
  .category-header {
    padding: 1rem;
    font-size: 1rem;
  }
  .gender-section {
    padding: 1rem;
  }
  .gender-header {
    flex-direction: column;
    gap: 0.5rem;
    align-items: flex-start;
    padding-bottom: 0.5rem;
  }
  .stats-badges {
    gap: 0.5rem;
  }
  .stat-badge {
    padding: 0.5rem 1rem;
    min-width: 60px;
    font-size: 0.9rem;
  }
  .matches-container {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  .match-card {
    padding: 0.75rem;
    border-radius: 1rem;
  }
  .player-number-badge, .position-indicator {
    width: 32px;
    height: 32px;
    font-size: 1rem;
  }
  .player-details {
    gap: 0.1rem;
  }
  .advance-indicator {
    width: 32px;
    height: 32px;
    font-size: 1.1rem;
  }
  .medal-indicator {
    width: 32px;
    height: 32px;
    font-size: 1.1rem;
  }
  .round-title {
    font-size: 1.1rem;
  }
  .round-header, .final-header {
    padding: 1rem;
    font-size: 1rem;
  }
  .bracket-round {
    padding: 1rem;
    border-radius: 1rem;
  }
  .eliminated-section {
    padding: 1rem;
    border-radius: 1rem;
  }
  .no-data {
    padding: 2rem 0.5rem;
    border-radius: 1rem;
  }
}

.mobile-only {
  display: none;
}

.desktop-only {
  display: flex;
  align-items: center;
  gap: 1rem;
  width: 100%;
}
</style>

