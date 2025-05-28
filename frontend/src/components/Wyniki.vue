<template>
  <div class="wyniki-container">
    <div class="section-header">
      <h2 class="section-title">
        <span class="title-icon">📊</span>
        Wyniki zawodników
      </h2>
      <div class="results-count">
        <span class="count-number">{{ filtrowaneWyniki.length }}</span>
        <span class="count-label">zawodników</span>
      </div>
    </div>

    <!-- Tabela wyników -->
    <div class="results-table-container">
      <div class="table-wrapper">
        <table class="results-table">
          <thead>
            <tr>
              <th class="col-position">Poz.</th>
              <th class="col-number">Nr</th>
              <th class="col-name">Zawodnik</th>
              <th class="col-category">Kategoria</th>
              <th class="col-gender">Płeć</th>
              <th class="col-time">Czas</th>
              <th class="col-status">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(zawodnik, index) in filtrowaneWyniki" 
                :key="zawodnik.nr_startowy"
                :class="['result-row', getRowClass(index, zawodnik)]">
              <td class="col-position">
                <div class="position-badge" :class="getPositionClass(index)">
                  {{ index + 1 }}
                </div>
              </td>
              <td class="col-number">
                <div class="number-badge">{{ zawodnik.nr_startowy }}</div>
              </td>
              <td class="col-name">
                <div class="athlete-info">
                  <div class="athlete-name">{{ zawodnik.imie }} {{ zawodnik.nazwisko }}</div>
                </div>
              </td>
              <td class="col-category">
                <div class="category-badge">{{ zawodnik.kategoria }}</div>
              </td>
              <td class="col-gender">
                <div class="gender-badge" :class="zawodnik.plec === 'M' ? 'male' : 'female'">
                  {{ zawodnik.plec === 'M' ? '👨' : '👩' }}
                  {{ zawodnik.plec === 'M' ? 'M' : 'K' }}
                </div>
              </td>
              <td class="col-time">
                <div v-if="zawodnik.czas_przejazdu_s" 
                     class="time-display" 
                     :class="getTimeClass(zawodnik.czas_przejazdu_s)">
                  {{ zawodnik.czas_przejazdu_s }}s
                </div>
                <div v-else class="time-display no-time">
                  Brak czasu
                </div>
              </td>
              <td class="col-status">
                <div class="status-badge" :class="getStatusClass(zawodnik.status)">
                  {{ getStatusText(zawodnik.status) }}
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Brak wyników -->
    <div v-if="filtrowaneWyniki.length === 0" class="no-results">
      <div class="no-results-icon">🔍</div>
      <h3 class="no-results-title">Brak wyników</h3>
      <p class="no-results-text">Nie znaleziono zawodników spełniających kryteria wyszukiwania.</p>
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

const wyniki = ref([])

const filtrowaneWyniki = computed(() => {
  let filtered = wyniki.value
  
  if (props.filtry?.kategoria) {
    filtered = filtered.filter(w => w.kategoria === props.filtry.kategoria)
  }
  
  if (props.filtry?.plec) {
    filtered = filtered.filter(w => w.plec === props.filtry.plec)
  }
  
  // Sortowanie po czasie (najlepszy czas na górze)
  return filtered.sort((a, b) => {
    if (!a.czas_przejazdu_s && !b.czas_przejazdu_s) return 0
    if (!a.czas_przejazdu_s) return 1
    if (!b.czas_przejazdu_s) return -1
    return parseFloat(a.czas_przejazdu_s) - parseFloat(b.czas_przejazdu_s)
  })
})

function getRowClass(index, zawodnik) {
  const classes = []
  
  if (index === 0 && zawodnik.czas_przejazdu_s) classes.push('first-place')
  else if (index === 1 && zawodnik.czas_przejazdu_s) classes.push('second-place')
  else if (index === 2 && zawodnik.czas_przejazdu_s) classes.push('third-place')
  
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

function getStatusClass(status) {
  switch(status) {
    case 'FINISHED': return 'finished'
    case 'DNF': return 'dnf'
    case 'DSQ': return 'dsq'
    default: return 'unknown'
  }
}

function getStatusText(status) {
  switch(status) {
    case 'FINISHED': return '✅ Ukończył'
    case 'DNF': return '❌ DNF'
    case 'DSQ': return '🚫 DSQ'
    default: return '❓ Nieznany'
  }
}

async function loadWyniki() {
  try {
    const res = await axios.get('/api/wyniki')
    wyniki.value = res.data
    console.log('Załadowano wyniki:', res.data.length, 'zawodników')
  } catch (error) {
    console.error('Błąd ładowania wyników:', error)
    wyniki.value = []
  }
}

onMounted(loadWyniki)

watch(() => props.filtry, (newFilters) => {
  console.log('Zmiana filtrów wyników na:', newFilters)
}, { deep: true })
</script>

<style scoped>
.wyniki-container {
  padding: 2rem;
  font-family: 'Inter', sans-serif;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e2e8f0;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 2rem;
  font-weight: 800;
  color: #0f172a;
  margin: 0;
}

.title-icon {
  font-size: 2.5rem;
  background: linear-gradient(135deg, #1e40af, #3730a3);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.results-count {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
  background: #1e40af;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 2rem;
  font-weight: 700;
  box-shadow: 0 4px 12px rgba(30, 64, 175, 0.3);
}

.count-number {
  font-size: 1.5rem;
  font-weight: 900;
}

.count-label {
  font-size: 0.9rem;
  opacity: 0.9;
}

.results-table-container {
  background: white;
  border-radius: 1rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  border: 1px solid #e2e8f0;
}

.table-wrapper {
  overflow-x: auto;
}

.results-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 1rem;
}

.results-table thead {
  background: linear-gradient(135deg, #1e40af, #3730a3);
  color: white;
}

.results-table th {
  padding: 1.5rem 1rem;
  text-align: left;
  font-weight: 700;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 2px solid rgba(255, 255, 255, 0.2);
}

.results-table th:first-child {
  border-top-left-radius: 1rem;
}

.results-table th:last-child {
  border-top-right-radius: 1rem;
}

.result-row {
  transition: all 0.2s ease;
  border-bottom: 1px solid #f1f5f9;
}

.result-row:hover {
  background: #f8fafc;
  transform: scale(1.01);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.result-row.first-place {
  background: linear-gradient(135deg, #fef3c7, #fbbf24);
  border-left: 4px solid #f59e0b;
}

.result-row.second-place {
  background: linear-gradient(135deg, #f3f4f6, #d1d5db);
  border-left: 4px solid #9ca3af;
}

.result-row.third-place {
  background: linear-gradient(135deg, #fef2f2, #fca5a5);
  border-left: 4px solid #ef4444;
}

.results-table td {
  padding: 1.25rem 1rem;
  vertical-align: middle;
}

.col-position {
  width: 80px;
  text-align: center;
}

.col-number {
  width: 80px;
  text-align: center;
}

.col-name {
  min-width: 200px;
}

.col-category {
  width: 120px;
}

.col-gender {
  width: 100px;
  text-align: center;
}

.col-time {
  width: 120px;
  text-align: center;
}

.col-status {
  width: 140px;
  text-align: center;
}

.position-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  font-weight: 900;
  font-size: 1.1rem;
  color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.position-badge.gold {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  animation: pulse 2s infinite;
}

.position-badge.silver {
  background: linear-gradient(135deg, #9ca3af, #6b7280);
}

.position-badge.bronze {
  background: linear-gradient(135deg, #ef4444, #dc2626);
}

.position-badge.regular {
  background: linear-gradient(135deg, #64748b, #475569);
}

.number-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: #1e40af;
  color: white;
  border-radius: 50%;
  font-weight: 700;
  font-size: 1rem;
  box-shadow: 0 2px 8px rgba(30, 64, 175, 0.3);
}

.athlete-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.athlete-name {
  font-weight: 700;
  font-size: 1.1rem;
  color: #0f172a;
}

.category-badge {
  display: inline-block;
  background: #f59e0b;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 1rem;
  font-weight: 700;
  font-size: 0.9rem;
  text-align: center;
  box-shadow: 0 2px 6px rgba(245, 158, 11, 0.3);
}

.gender-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 1rem;
  font-weight: 700;
  font-size: 0.9rem;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.gender-badge.male {
  background: #dbeafe;
  color: #1e40af;
  border: 2px solid #3b82f6;
}

.gender-badge.female {
  background: #fce7f3;
  color: #be185d;
  border: 2px solid #ec4899;
}

.time-display {
  display: inline-block;
  padding: 0.75rem 1.25rem;
  border-radius: 1rem;
  font-weight: 800;
  font-size: 1.1rem;
  text-align: center;
  min-width: 80px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.time-display.excellent {
  background: #dcfce7;
  color: #166534;
  border: 2px solid #22c55e;
}

.time-display.good {
  background: #dbeafe;
  color: #1e40af;
  border: 2px solid #3b82f6;
}

.time-display.average {
  background: #fef3c7;
  color: #92400e;
  border: 2px solid #f59e0b;
}

.time-display.poor {
  background: #fecaca;
  color: #991b1b;
  border: 2px solid #ef4444;
}

.time-display.no-time {
  background: #f1f5f9;
  color: #64748b;
  border: 2px solid #cbd5e1;
  font-style: italic;
}

.status-badge {
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: 1rem;
  font-weight: 700;
  font-size: 0.9rem;
  text-align: center;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.status-badge.finished {
  background: #dcfce7;
  color: #166534;
  border: 2px solid #22c55e;
}

.status-badge.dnf {
  background: #fecaca;
  color: #991b1b;
  border: 2px solid #ef4444;
}

.status-badge.dsq {
  background: #fed7aa;
  color: #9a3412;
  border: 2px solid #ea580c;
}

.status-badge.unknown {
  background: #f1f5f9;
  color: #64748b;
  border: 2px solid #cbd5e1;
}

.no-results {
  text-align: center;
  padding: 4rem 2rem;
  background: white;
  border-radius: 1rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
}

.no-results-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.no-results-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #374151;
  margin: 0 0 1rem 0;
}

.no-results-text {
  font-size: 1rem;
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

/* Responsive Design */
@media (max-width: 768px) {
  .wyniki-container {
    padding: 1rem;
  }
  
  .section-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .section-title {
    font-size: 1.5rem;
  }
  
  .results-table {
    font-size: 0.9rem;
  }
  
  .results-table th,
  .results-table td {
    padding: 1rem 0.5rem;
  }
  
  .col-name {
    min-width: 150px;
  }
  
  .athlete-name {
    font-size: 1rem;
  }
  
  .position-badge,
  .number-badge {
    width: 35px;
    height: 35px;
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .results-table th,
  .results-table td {
    padding: 0.75rem 0.25rem;
  }
  
  .section-title {
    font-size: 1.25rem;
  }
  
  .title-icon {
    font-size: 2rem;
  }
  
  .results-table {
    font-size: 0.8rem;
  }
}
</style>

