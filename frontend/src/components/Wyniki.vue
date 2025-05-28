<template>
  <div class="wyniki-container">
    <!-- Results Header -->
    <div class="results-header">
      <div class="header-info">
        <h2 class="results-title">
          <span class="title-icon">🏆</span>
          Wyniki
        </h2>
        <div class="results-count">
          <span class="count-badge">{{ filtrowaneWyniki.length }}</span>
          <span class="count-text">zawodników</span>
        </div>
      </div>
      
      <!-- Sort Options -->
      <div class="sort-options">
        <button 
          @click="sortBy = 'czas'"
          :class="['sort-btn', { active: sortBy === 'czas' }]"
        >
          <span class="sort-icon">⏱️</span>
          <span>Czas</span>
        </button>
        <button 
          @click="sortBy = 'alfabetycznie'"
          :class="['sort-btn', { active: sortBy === 'alfabetycznie' }]"
        >
          <span class="sort-icon">🔤</span>
          <span>A-Z</span>
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-state">
      <div class="loading-spinner">
        <div class="spinner"></div>
        <p>Ładowanie wyników...</p>
      </div>
    </div>

    <!-- Results List -->
    <div v-else-if="filtrowaneWyniki.length > 0" class="results-list">
      <!-- Podium (Top 3) -->
      <div v-if="showPodium && podiumWyniki.length > 0" class="podium-section">
        <h3 class="podium-title">
          <span class="podium-icon">🥇</span>
          Podium
        </h3>
        <div class="podium-cards">
          <div 
            v-for="(zawodnik, index) in podiumWyniki" 
            :key="`podium-${zawodnik.nr_startowy}`"
            :class="['podium-card', getPodiumClass(index)]"
          >
            <div class="podium-position">
              <span class="position-icon">{{ getPodiumIcon(index) }}</span>
              <span class="position-number">{{ index + 1 }}</span>
            </div>
            <div class="podium-athlete">
              <div class="athlete-name">{{ zawodnik.imie }} {{ zawodnik.nazwisko }}</div>
              <div class="athlete-details">
                <span class="athlete-number">#{{ zawodnik.nr_startowy }}</span>
                <span class="athlete-category">{{ zawodnik.kategoria }}</span>
              </div>
            </div>
            <div class="podium-time">
              <span class="time-value">{{ zawodnik.czas_przejazdu_s }}s</span>
            </div>
          </div>
        </div>
      </div>

      <!-- All Results -->
      <div class="all-results">
        <h3 v-if="showPodium" class="section-title">
          <span class="section-icon">📊</span>
          Wszystkie wyniki
        </h3>
        
        <div class="results-grid">
          <div 
            v-for="(zawodnik, index) in sortedResults" 
            :key="zawodnik.nr_startowy"
            :class="['result-card', getResultClass(zawodnik, index)]"
            @click="selectResult(zawodnik)"
          >
            <!-- Card Header -->
            <div class="card-header">
              <div class="position-info">
                <div class="position-badge" :class="getPositionClass(index)">
                  {{ getGlobalPosition(zawodnik, index) }}
                </div>
                <div class="number-badge">
                  #{{ zawodnik.nr_startowy }}
                </div>
              </div>
              <div class="status-badge" :class="getStatusClass(zawodnik.status)">
                {{ getStatusIcon(zawodnik.status) }}
              </div>
            </div>

            <!-- Athlete Info -->
            <div class="athlete-section">
              <div class="athlete-name-main">
                {{ zawodnik.imie }} {{ zawodnik.nazwisko }}
              </div>
              <div class="athlete-meta">
                <span class="category-chip">{{ zawodnik.kategoria }}</span>
                <span class="gender-indicator" :class="zawodnik.plec === 'M' ? 'male' : 'female'">
                  {{ zawodnik.plec === 'M' ? '👨' : '👩' }}
                </span>
              </div>
            </div>

            <!-- Performance Info -->
            <div class="performance-section">
              <div v-if="zawodnik.czas_przejazdu_s" class="time-info">
                <div class="time-value" :class="getTimeClass(zawodnik.czas_przejazdu_s)">
                  {{ zawodnik.czas_przejazdu_s }}s
                </div>
                <div class="time-label">Czas przejazdu</div>
              </div>
              <div v-else class="no-time">
                <div class="no-time-icon">⏱️</div>
                <div class="no-time-text">Brak czasu</div>
              </div>
            </div>

            <!-- Card Footer -->
            <div class="card-footer">
              <div class="status-info">
                <span class="status-text" :class="getStatusClass(zawodnik.status)">
                  {{ getStatusText(zawodnik.status) }}
                </span>
              </div>
              <div class="card-actions">
                <button class="action-btn details" @click.stop="showDetails(zawodnik)">
                  <span>Detale</span>
                  <span class="action-icon">👁️</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state">
      <div class="empty-icon">🔍</div>
      <h3 class="empty-title">Brak wyników</h3>
      <p class="empty-text">
        Nie znaleziono zawodników spełniających kryteria wyszukiwania.
      </p>
      <button @click="clearFilters" class="empty-action">
        <span class="action-icon">🔄</span>
        Wyczyść filtry
      </button>
    </div>

    <!-- Result Details Modal -->
    <div v-if="selectedResult" class="details-modal" @click="closeDetails">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Szczegóły zawodnika</h3>
          <button @click="closeDetails" class="close-btn">✕</button>
        </div>
        <div class="modal-body">
          <div class="detail-row">
            <span class="detail-label">Imię i nazwisko:</span>
            <span class="detail-value">{{ selectedResult.imie }} {{ selectedResult.nazwisko }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Numer startowy:</span>
            <span class="detail-value">#{{ selectedResult.nr_startowy }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Kategoria:</span>
            <span class="detail-value">{{ selectedResult.kategoria }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Płeć:</span>
            <span class="detail-value">{{ selectedResult.plec === 'M' ? 'Mężczyzna' : 'Kobieta' }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Czas przejazdu:</span>
            <span class="detail-value">
              {{ selectedResult.czas_przejazdu_s ? selectedResult.czas_przejazdu_s + 's' : 'Brak czasu' }}
            </span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Status:</span>
            <span class="detail-value">{{ getStatusText(selectedResult.status) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { apiClient } from '../utils/api.js'

const emit = defineEmits(['results-count'])

const props = defineProps({
  filtry: {
    type: Object,
    default: () => ({ kategorie: [], plec: null })
  }
})

// State
const wyniki = ref([])
const isLoading = ref(true)
const sortBy = ref('czas')
const selectedResult = ref(null)

// Computed
const filtrowaneWyniki = computed(() => {
  let filtered = wyniki.value
  
  if (props.filtry?.kategorie && props.filtry.kategorie.length > 0) {
    filtered = filtered.filter(w => props.filtry.kategorie.includes(w.kategoria))
  }
  
  if (props.filtry?.plec) {
    filtered = filtered.filter(w => w.plec === props.filtry.plec)
  }
  
  return filtered
})

const sortedResults = computed(() => {
  const results = [...filtrowaneWyniki.value]
  
  if (sortBy.value === 'czas') {
    return results.sort((a, b) => {
      if (!a.czas_przejazdu_s && !b.czas_przejazdu_s) return 0
      if (!a.czas_przejazdu_s) return 1
      if (!b.czas_przejazdu_s) return -1
      return parseFloat(a.czas_przejazdu_s) - parseFloat(b.czas_przejazdu_s)
    })
  } else {
    return results.sort((a, b) => {
      const nameA = `${a.imie} ${a.nazwisko}`.toLowerCase()
      const nameB = `${b.imie} ${b.nazwisko}`.toLowerCase()
      return nameA.localeCompare(nameB)
    })
  }
})

const podiumWyniki = computed(() => {
  return sortedResults.value
    .filter(w => w.czas_przejazdu_s && w.status === 'FINISHED')
    .slice(0, 3)
})

const showPodium = computed(() => {
  return sortBy.value === 'czas' && podiumWyniki.value.length > 0
})

// Functions
function getGlobalPosition(zawodnik, index) {
  if (sortBy.value === 'alfabetycznie') return index + 1
  
  const allWithTimes = filtrowaneWyniki.value
    .filter(w => w.czas_przejazdu_s && w.status === 'FINISHED')
    .sort((a, b) => parseFloat(a.czas_przejazdu_s) - parseFloat(b.czas_przejazdu_s))
  
  const position = allWithTimes.findIndex(w => w.nr_startowy === zawodnik.nr_startowy)
  return position >= 0 ? position + 1 : '-'
}

function getPodiumClass(index) {
  const classes = ['gold', 'silver', 'bronze']
  return classes[index] || 'regular'
}

function getPodiumIcon(index) {
  const icons = ['🥇', '🥈', '🥉']
  return icons[index] || '🏅'
}

function getPositionClass(index) {
  if (sortBy.value === 'alfabetycznie') return 'regular'
  
  if (index === 0) return 'gold'
  if (index === 1) return 'silver'
  if (index === 2) return 'bronze'
  return 'regular'
}

function getResultClass(zawodnik, index) {
  const classes = []
  
  if (sortBy.value === 'czas' && zawodnik.czas_przejazdu_s && zawodnik.status === 'FINISHED') {
    if (index === 0) classes.push('winner')
    else if (index === 1) classes.push('second')
    else if (index === 2) classes.push('third')
  }
  
  if (!zawodnik.czas_przejazdu_s || zawodnik.status !== 'FINISHED') {
    classes.push('no-time')
  }
  
  return classes
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
    case 'FINISHED': return 'Ukończył'
    case 'DNF': return 'Nie ukończył'
    case 'DSQ': return 'Dyskwalifikacja'
    default: return 'Nieznany'
  }
}

function getStatusIcon(status) {
  switch(status) {
    case 'FINISHED': return '✅'
    case 'DNF': return '❌'
    case 'DSQ': return '🚫'
    default: return '❓'
  }
}

function selectResult(zawodnik) {
  selectedResult.value = zawodnik
}

function showDetails(zawodnik) {
  selectedResult.value = zawodnik
}

function closeDetails() {
  selectedResult.value = null
}

function clearFilters() {
  // This would need to be handled by parent component
  console.log('Clear filters requested')
}

async function loadWyniki() {
  try {
    isLoading.value = true
    const res = await apiClient.getWyniki()
    wyniki.value = res.data
    console.log('Załadowano wyniki:', res.data.length, 'zawodników')
  } catch (error) {
    console.error('Błąd ładowania wyników:', error)
    wyniki.value = []
  } finally {
    isLoading.value = false
  }
}

// Watchers
watch(filtrowaneWyniki, (newResults) => {
  emit('results-count', newResults.length)
}, { immediate: true })

watch(() => props.filtry, (newFilters) => {
  console.log('Zmiana filtrów wyników na:', newFilters)
}, { deep: true })

// Lifecycle
onMounted(loadWyniki)
</script>

<style scoped>
.wyniki-container {
  padding: 1rem;
  font-family: 'Inter', sans-serif;
  background: var(--background);
  min-height: 100%;
}

/* Results Header */
.results-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
  gap: 1rem;
}

.header-info {
  flex: 1;
  min-width: 0;
}

.results-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 0.5rem 0;
}

.title-icon {
  font-size: 1.5rem;
}

.results-count {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.count-badge {
  background: var(--primary);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.9rem;
  font-weight: 600;
}

.count-text {
  font-size: 0.9rem;
  color: var(--text-secondary);
  font-weight: 500;
}

/* Sort Options */
.sort-options {
  display: flex;
  gap: 0.5rem;
  flex-shrink: 0;
}

.sort-btn {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.5rem 0.75rem;
  border: 2px solid var(--border);
  background: var(--surface);
  color: var(--text-secondary);
  border-radius: 0.75rem;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.sort-btn:hover {
  border-color: var(--primary);
  color: var(--primary);
}

.sort-btn.active {
  background: var(--primary);
  border-color: var(--primary);
  color: white;
}

.sort-icon {
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

/* Podium Section */
.podium-section {
  margin-bottom: 2rem;
}

.podium-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 1rem 0;
}

.podium-icon {
  font-size: 1.3rem;
}

.podium-cards {
  display: grid;
  gap: 1rem;
  margin-bottom: 1rem;
}

.podium-card {
  background: var(--surface);
  border-radius: 1rem;
  padding: 1rem;
  border: 2px solid var(--border);
  box-shadow: var(--shadow);
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.2s ease;
}

.podium-card.gold {
  border-color: #fbbf24;
  background: linear-gradient(135deg, #fef3c7, #fbbf24);
}

.podium-card.silver {
  border-color: #9ca3af;
  background: linear-gradient(135deg, #f3f4f6, #d1d5db);
}

.podium-card.bronze {
  border-color: #f97316;
  background: linear-gradient(135deg, #fed7aa, #f97316);
}

.podium-position {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  flex-shrink: 0;
}

.position-icon {
  font-size: 1.5rem;
}

.position-number {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-secondary);
}

.podium-athlete {
  flex: 1;
  min-width: 0;
}

.athlete-name {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.athlete-details {
  display: flex;
  gap: 0.75rem;
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.athlete-number,
.athlete-category {
  font-weight: 500;
}

.podium-time {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
}

.time-value {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--primary);
}

/* All Results Section */
.all-results {
  margin-bottom: 2rem;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 1rem 0;
}

.section-icon {
  font-size: 1.2rem;
}

/* Results Grid */
.results-grid {
  display: grid;
  gap: 1rem;
}

.result-card {
  background: var(--surface);
  border-radius: 1rem;
  padding: 1rem;
  border: 2px solid var(--border);
  box-shadow: var(--shadow);
  transition: all 0.2s ease;
  cursor: pointer;
}

.result-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary);
}

.result-card.winner {
  border-color: #fbbf24;
  background: linear-gradient(135deg, #fef3c7 0%, var(--surface) 100%);
}

.result-card.second {
  border-color: #9ca3af;
  background: linear-gradient(135deg, #f3f4f6 0%, var(--surface) 100%);
}

.result-card.third {
  border-color: #f97316;
  background: linear-gradient(135deg, #fed7aa 0%, var(--surface) 100%);
}

.result-card.no-time {
  opacity: 0.8;
  border-color: var(--text-muted);
}

/* Card Header */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.position-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
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

.number-badge {
  background: var(--primary);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 0.5rem;
  font-size: 0.8rem;
  font-weight: 600;
}

.status-badge {
  font-size: 1.2rem;
}

/* Athlete Section */
.athlete-section {
  margin-bottom: 0.75rem;
}

.athlete-name-main {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.athlete-meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.category-chip {
  background: var(--secondary);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 0.5rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.gender-indicator {
  font-size: 1rem;
}

/* Performance Section */
.performance-section {
  margin-bottom: 0.75rem;
  padding: 0.75rem;
  background: var(--background);
  border-radius: 0.75rem;
}

.time-info {
  text-align: center;
}

.time-value {
  display: block;
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.time-value.excellent {
  color: var(--success);
}

.time-value.good {
  color: var(--primary);
}

.time-value.average {
  color: var(--secondary);
}

.time-value.poor {
  color: var(--error);
}

.time-label {
  font-size: 0.8rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.no-time {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.no-time-icon {
  font-size: 1.5rem;
  opacity: 0.5;
}

.no-time-text {
  font-size: 0.9rem;
  color: var(--text-muted);
  font-weight: 500;
}

/* Card Footer */
.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 0.75rem;
  border-top: 1px solid var(--border);
}

.status-info {
  display: flex;
  align-items: center;
}

.status-text {
  font-size: 0.8rem;
  font-weight: 500;
  padding: 0.25rem 0.5rem;
  border-radius: 0.5rem;
}

.status-text.finished {
  background: #dcfce7;
  color: #166534;
}

.status-text.dnf {
  background: #fecaca;
  color: #991b1b;
}

.status-text.dsq {
  background: #fed7d7;
  color: #991b1b;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.5rem;
  border: none;
  background: var(--primary);
  color: white;
  border-radius: 0.5rem;
  font-size: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.action-btn:hover {
  background: var(--primary-dark);
}

.action-icon {
  font-size: 0.8rem;
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
  margin: 0 0 2rem 0;
  max-width: 300px;
}

.empty-action {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: var(--primary);
  color: white;
  border: none;
  border-radius: 0.75rem;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.empty-action:hover {
  background: var(--primary-dark);
  transform: translateY(-1px);
}

/* Details Modal */
.details-modal {
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
  max-height: 80vh;
  overflow-y: auto;
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
  .wyniki-container {
    padding: 0.75rem;
  }
  
  .results-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .sort-options {
    align-self: stretch;
  }
  
  .sort-btn {
    flex: 1;
    justify-content: center;
    padding: 0.5rem;
    font-size: 0.75rem;
  }
  
  .podium-cards {
    gap: 0.75rem;
  }
  
  .podium-card {
    padding: 0.75rem;
    gap: 0.75rem;
  }
  
  .results-grid {
    gap: 0.75rem;
  }
  
  .result-card {
    padding: 0.75rem;
  }
  
  .athlete-name-main {
    font-size: 1rem;
  }
  
  .time-value {
    font-size: 1.2rem;
  }
}

/* Landscape mode for small screens */
@media (max-height: 500px) and (orientation: landscape) {
  .empty-state {
    padding: 2rem 1rem;
  }
  
  .empty-icon {
    font-size: 3rem;
  }
  
  .podium-section {
    margin-bottom: 1rem;
  }
}
</style>
