<template>
  <div class="drabinka-container">
    <h2 class="drabinka-title">🏆 Drabinka pucharowa Mistrzostw Polski w SKATECROSS</h2>
    
    <!-- Kategorie -->
    <div v-for="(kategoriaData, kategoriaNazwa) in filtrowaneKategorie" :key="kategoriaNazwa" 
         class="kategoria-section">
      
      <h3 class="kategoria-header">
        <span class="kategoria-icon">🏅</span>
        {{ kategoriaNazwa }}
      </h3>
      
      <!-- Płcie w kategorii -->
      <div v-for="(plecData, plecNazwa) in kategoriaData" :key="plecNazwa"
           class="plec-section">
        
        <h4 class="plec-header">
          <span class="plec-icon">{{ plecNazwa === 'Mężczyźni' ? '👨' : '👩' }}</span>
          {{ plecNazwa }}
        </h4>
        
        <!-- Statystyki -->
        <div v-if="plecData.statystyki" class="stats-container">
          <div class="stat-item">
            <span class="stat-label">Łącznie:</span>
            <span class="stat-value">{{ plecData.statystyki.łącznie_zawodników }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">W ćwierćfinałach:</span>
            <span class="stat-value">{{ plecData.statystyki.w_ćwierćfinałach }}</span>
          </div>
          <div v-if="plecData.statystyki.odpadło > 0" class="stat-item eliminated">
            <span class="stat-label">Odpadło:</span>
            <span class="stat-value">{{ plecData.statystyki.odpadło }}</span>
          </div>
        </div>

        <!-- Tournament Bracket -->
        <div class="tournament-bracket">
          
          <!-- Odpadli zawodnicy -->
          <div v-if="plecData.odpadli && plecData.odpadli.length > 0" class="eliminated-section">
            <h5 class="round-title eliminated-title">❌ Odpadli z turnieju</h5>
            <div class="eliminated-players">
              <div v-for="zawodnik in plecData.odpadli" :key="zawodnik.nr_startowy"
                   class="player-card eliminated">
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

          <!-- Ćwierćfinały -->
          <div v-if="plecData.ćwierćfinały && plecData.ćwierćfinały.length > 0" class="round-section">
            <h5 class="round-title quarterfinals">🥉 Ćwierćfinały</h5>
            <div class="groups-container">
              <div v-for="grupa in plecData.ćwierćfinały" :key="grupa.grupa"
                   class="group-card quarterfinals">
                <div class="group-header">
                  <span class="group-title">Grupa {{ grupa.grupa }}</span>
                  <span class="advance-info">Awansują: {{ grupa.awansują }}</span>
                </div>
                <div class="players-list">
                  <div v-for="(zawodnik, index) in grupa.zawodnicy" :key="zawodnik.nr_startowy"
                       class="player-card" :class="{ advancing: index < grupa.awansują }">
                    <div class="player-position">{{ index + 1 }}</div>
                    <div class="player-number">{{ zawodnik.nr_startowy }}</div>
                    <div class="player-info">
                      <div class="player-name">{{ zawodnik.imie }} {{ zawodnik.nazwisko }}</div>
                      <div class="player-time" :class="getTimeClass(zawodnik.czas_przejazdu_s)">
                        {{ zawodnik.czas_przejazdu_s || 'brak' }}{{ zawodnik.czas_przejazdu_s ? 's' : '' }}
                      </div>
                    </div>
                    <div v-if="index < grupa.awansują" class="advance-indicator">
                      <span class="advance-arrow">→</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Półfinały -->
          <div v-if="plecData.półfinały && plecData.półfinały.length > 0" class="round-section">
            <h5 class="round-title semifinals">🥈 Półfinały</h5>
            <div class="groups-container">
              <div v-for="grupa in plecData.półfinały" :key="grupa.grupa"
                   class="group-card semifinals">
                <div class="group-header">
                  <span class="group-title">Grupa {{ grupa.grupa }}</span>
                  <span class="advance-info">Awansują: {{ grupa.awansują }}</span>
                </div>
                <div v-if="grupa.zawodnicy && grupa.zawodnicy.length > 0" class="players-list">
                  <div v-for="(zawodnik, index) in grupa.zawodnicy" :key="zawodnik.nr_startowy"
                       class="player-card" :class="{ advancing: index < grupa.awansują }">
                    <div class="player-position">{{ index + 1 }}</div>
                    <div class="player-number">{{ zawodnik.nr_startowy }}</div>
                    <div class="player-info">
                      <div class="player-name">{{ zawodnik.imie }} {{ zawodnik.nazwisko }}</div>
                      <div class="player-time" :class="getTimeClass(zawodnik.czas_przejazdu_s)">
                        {{ zawodnik.czas_przejazdu_s || 'brak' }}{{ zawodnik.czas_przejazdu_s ? 's' : '' }}
                      </div>
                    </div>
                    <div v-if="index < grupa.awansują" class="advance-indicator">
                      <span class="advance-arrow">→</span>
                    </div>
                  </div>
                </div>
                <div v-else class="waiting-info">
                  {{ grupa.info || 'Oczekuje na wyniki ćwierćfinałów' }}
                </div>
              </div>
            </div>
          </div>

          <!-- Finał -->
          <div v-if="plecData.finał && plecData.finał.length > 0" class="round-section">
            <h5 class="round-title final">🥇 Finał</h5>
            <div class="groups-container">
              <div v-for="grupa in plecData.finał" :key="grupa.grupa"
                   class="group-card final">
                <div class="group-header">
                  <span class="group-title">Grupa {{ grupa.grupa }}</span>
                  <span class="advance-info">Zwycięzca: 1</span>
                </div>
                <div v-if="grupa.zawodnicy && grupa.zawodnicy.length > 0" class="players-list">
                  <div v-for="(zawodnik, index) in grupa.zawodnicy" :key="zawodnik.nr_startowy"
                       class="player-card" :class="{ winner: index === 0 }">
                    <div class="player-position">{{ index + 1 }}</div>
                    <div class="player-number">{{ zawodnik.nr_startowy }}</div>
                    <div class="player-info">
                      <div class="player-name">{{ zawodnik.imie }} {{ zawodnik.nazwisko }}</div>
                      <div class="player-time" :class="getTimeClass(zawodnik.czas_przejazdu_s)">
                        {{ zawodnik.czas_przejazdu_s || 'brak' }}{{ zawodnik.czas_przejazdu_s ? 's' : '' }}
                      </div>
                    </div>
                    <div v-if="index === 0" class="winner-crown">👑</div>
                  </div>
                </div>
                <div v-else class="waiting-info">
                  {{ grupa.info || 'Oczekuje na wyniki półfinałów' }}
                </div>
              </div>
            </div>
          </div>

        </div>

        <!-- Info o małej liczbie zawodników -->
        <div v-if="plecData.info" class="info-message">
          ℹ️ {{ plecData.info }}
        </div>

      </div>
    </div>

    <!-- Komunikat gdy brak danych -->
    <div v-if="Object.keys(filtrowaneKategorie).length === 0" class="no-data">
      Brak danych drabinki turniejowej.
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'

const props = defineProps({ 
  filtry: {
    type: Object,
    default: () => ({ kategoria: null, plec: null })
  }
})
const emit = defineEmits(['podsumowanie-loaded'])
const drabinka = ref({})

const filtrowaneKategorie = computed(() => {
  const { podsumowanie, ...kategorie } = drabinka.value
  
  if (!props.filtry?.kategoria && !props.filtry?.plec) {
    return kategorie
  }
  
  const wynik = {}
  
  const kategorieDoWyswietlenia = props.filtry.kategoria 
    ? { [props.filtry.kategoria]: kategorie[props.filtry.kategoria] }
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
  if (!czas) return ''
  const czasNum = parseFloat(czas)
  if (czasNum < 45) return 'time-excellent'
  if (czasNum < 50) return 'time-good'
  if (czasNum < 60) return 'time-average'
  return 'time-poor'
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
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.drabinka-title {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 20px;
  border-radius: 15px;
  text-align: center;
  margin: 20px 0;
  box-shadow: 0 8px 32px rgba(0,0,0,0.1);
  font-size: 1.8em;
  font-weight: bold;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.kategoria-section {
  margin: 30px 0;
  background: linear-gradient(145deg, #f8f9fa, #e9ecef);
  border-radius: 20px;
  padding: 25px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  border: 1px solid rgba(255,255,255,0.2);
}

.kategoria-header {
  color: #2c5aa0;
  margin: 0 0 20px 0;
  font-size: 1.5em;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 10px;
}

.kategoria-icon {
  font-size: 1.2em;
  animation: bounce 2s infinite;
}

.plec-section {
  margin: 20px 0;
  background: rgba(255,255,255,0.8);
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.05);
  backdrop-filter: blur(10px);
}

.plec-header {
  color: #495057;
  margin: 0 0 15px 0;
  font-size: 1.2em;
  display: flex;
  align-items: center;
  gap: 8px;
}

.plec-icon {
  font-size: 1.1em;
}

.stats-container {
  display: flex;
  gap: 20px;
  margin: 15px 0;
  flex-wrap: wrap;
}

.stat-item {
  background: linear-gradient(135deg, #e3f2fd, #bbdefb);
  padding: 8px 15px;
  border-radius: 20px;
  font-size: 0.9em;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.stat-item.eliminated {
  background: linear-gradient(135deg, #ffebee, #ffcdd2);
}

.stat-label {
  font-weight: 600;
  color: #37474f;
}

.stat-value {
  font-weight: bold;
  color: #1565c0;
  margin-left: 5px;
}

.tournament-bracket {
  margin: 20px 0;
}

.round-section {
  margin: 25px 0;
}

.round-title {
  font-size: 1.3em;
  font-weight: bold;
  margin: 0 0 15px 0;
  padding: 10px 20px;
  border-radius: 25px;
  text-align: center;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
}

.round-title.quarterfinals {
  background: linear-gradient(135deg, #cd7f32, #b8860b);
  color: white;
}

.round-title.semifinals {
  background: linear-gradient(135deg, #c0c0c0, #a8a8a8);
  color: white;
}

.round-title.final {
  background: linear-gradient(135deg, #ffd700, #ffb300);
  color: #333;
  animation: pulse 2s infinite;
}

.round-title.eliminated-title {
  background: linear-gradient(135deg, #f44336, #d32f2f);
  color: white;
}

.groups-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin: 15px 0;
}

.group-card {
  background: white;
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 8px 25px rgba(0,0,0,0.1);
  border: 2px solid transparent;
  transition: all 0.3s ease;
}

.group-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(0,0,0,0.15);
}

.group-card.quarterfinals {
  border-color: #cd7f32;
}

.group-card.semifinals {
  border-color: #c0c0c0;
}

.group-card.final {
  border-color: #ffd700;
  background: linear-gradient(145deg, #fffbf0, #fff8e1);
  animation: glow 3s ease-in-out infinite alternate;
}

.group-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 2px solid #e9ecef;
}

.group-title {
  font-weight: bold;
  font-size: 1.1em;
  color: #2c5aa0;
}

.advance-info {
  font-size: 0.9em;
  color: #6c757d;
  background: #f8f9fa;
  padding: 4px 12px;
  border-radius: 15px;
}

.players-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.player-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 10px;
  transition: all 0.3s ease;
  position: relative;
  border: 2px solid transparent;
}

.player-card:hover {
  background: #e9ecef;
  transform: translateX(5px);
}

.player-card.advancing {
  background: linear-gradient(135deg, #d4edda, #c3e6cb);
  border-color: #28a745;
}

.player-card.winner {
  background: linear-gradient(135deg, #fff3cd, #ffeaa7);
  border-color: #ffd700;
  animation: glow 2s ease-in-out infinite alternate;
}

.player-card.eliminated {
  background: linear-gradient(135deg, #f8d7da, #f5c6cb);
  border-color: #dc3545;
  opacity: 0.8;
}

.player-position {
  font-weight: bold;
  font-size: 1.2em;
  color: #495057;
  min-width: 25px;
  text-align: center;
}

.player-number {
  background: #007bff;
  color: white;
  padding: 6px 10px;
  border-radius: 50%;
  font-weight: bold;
  min-width: 35px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0,123,255,0.3);
}

.player-info {
  flex: 1;
}

.player-name {
  font-weight: 600;
  color: #2c5aa0;
  font-size: 1em;
}

.player-time {
  font-family: 'Courier New', monospace;
  font-weight: bold;
  font-size: 0.9em;
  margin-top: 2px;
}

.player-time.time-excellent {
  color: #28a745;
}

.player-time.time-good {
  color: #007bff;
}

.player-time.time-average {
  color: #ffc107;
}

.player-time.time-poor {
  color: #dc3545;
}

.advance-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 30px;
  background: #28a745;
  border-radius: 50%;
  color: white;
  font-weight: bold;
  animation: pulse 1.5s infinite;
}

.advance-arrow {
  font-size: 1.2em;
}

.winner-crown {
  font-size: 1.5em;
  animation: bounce 1s infinite;
}

.eliminated-section {
  margin: 20px 0;
}

.eliminated-players {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 10px;
  max-height: 200px;
  overflow-y: auto;
  padding: 10px;
  background: rgba(248, 215, 218, 0.3);
  border-radius: 10px;
}

.waiting-info {
  text-align: center;
  color: #6c757d;
  font-style: italic;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 10px;
}

.info-message {
  margin: 15px 0;
  padding: 12px;
  background: linear-gradient(135deg, #fff3cd, #ffeaa7);
  color: #856404;
  border-radius: 10px;
  border-left: 4px solid #ffc107;
}

.no-data {
  text-align: center;
  padding: 40px;
  background: linear-gradient(135deg, #f8d7da, #f5c6cb);
  color: #721c24;
  border-radius: 15px;
  font-size: 1.1em;
  margin: 20px 0;
}

/* Animations */
@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
  }
}

@keyframes glow {
  from {
    box-shadow: 0 8px 25px rgba(255, 215, 0, 0.3);
  }
  to {
    box-shadow: 0 8px 25px rgba(255, 215, 0, 0.6);
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .drabinka-container {
    padding: 10px;
  }
  
  .drabinka-title {
    font-size: 1.4em;
    padding: 15px;
  }
  
  .groups-container {
    grid-template-columns: 1fr;
  }
  
  .stats-container {
    flex-direction: column;
    gap: 10px;
  }
  
  .eliminated-players {
    grid-template-columns: 1fr;
  }
}
</style>

