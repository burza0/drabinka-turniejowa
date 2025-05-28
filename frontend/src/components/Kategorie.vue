<template>
  <div class="kategorie-container">
    <div class="filters-header">
      <h3 class="filters-title">
        <span class="filters-icon">🔍</span>
        Filtry wyszukiwania
      </h3>
      <button 
        v-if="hasActiveFilters" 
        @click="clearFilters"
        class="clear-button"
      >
        <span class="clear-icon">✕</span>
        Wyczyść filtry
      </button>
    </div>

    <div class="filters-grid">
      <!-- Filtr kategorii -->
      <div class="filter-group">
        <label class="filter-label">
          <span class="label-icon">🏅</span>
          Kategoria wiekowa
        </label>
        <div class="filter-options">
          <button 
            v-for="kategoria in dostepneKategorie" 
            :key="kategoria"
            @click="selectKategoria(kategoria)"
            :class="['filter-option', { active: wybranaKategoria === kategoria }]"
          >
            {{ kategoria }}
          </button>
        </div>
      </div>

      <!-- Filtr płci -->
      <div class="filter-group">
        <label class="filter-label">
          <span class="label-icon">👥</span>
          Płeć
        </label>
        <div class="filter-options">
          <button 
            @click="selectPlec('M')"
            :class="['filter-option gender-male', { active: wybranaPlec === 'M' }]"
          >
            <span class="gender-icon">👨</span>
            Mężczyźni
          </button>
          <button 
            @click="selectPlec('K')"
            :class="['filter-option gender-female', { active: wybranaPlec === 'K' }]"
          >
            <span class="gender-icon">👩</span>
            Kobiety
          </button>
        </div>
      </div>
    </div>

    <!-- Aktywne filtry -->
    <div v-if="hasActiveFilters" class="active-filters">
      <div class="active-filters-header">
        <span class="active-icon">🎯</span>
        Aktywne filtry:
      </div>
      <div class="active-filters-list">
        <div v-if="wybranaKategoria" class="active-filter">
          <span class="filter-text">{{ wybranaKategoria }}</span>
          <button @click="selectKategoria(null)" class="remove-filter">✕</button>
        </div>
        <div v-if="wybranaPlec" class="active-filter">
          <span class="filter-text">{{ wybranaPlec === 'M' ? 'Mężczyźni' : 'Kobiety' }}</span>
          <button @click="selectPlec(null)" class="remove-filter">✕</button>
        </div>
      </div>
    </div>

    <!-- Statystyki filtrowania -->
    <div class="filter-stats">
      <div class="stats-item">
        <span class="stats-icon">📊</span>
        <span class="stats-text">
          Znaleziono <strong>{{ filteredCount }}</strong> z <strong>{{ totalCount }}</strong> zawodników
          <span v-if="hasActiveFilters" class="filter-info">
            ({{ wybranaKategoria ? `kategoria: ${wybranaKategoria}` : '' }}{{ wybranaKategoria && wybranaPlec ? ', ' : '' }}{{ wybranaPlec ? `płeć: ${wybranaPlec === 'M' ? 'Mężczyźni' : 'Kobiety'}` : '' }})
          </span>
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'

const emit = defineEmits(['filtry-changed'])

const kategorie = ref([])
const wybranaKategoria = ref(null)
const wybranaPlec = ref(null)
const totalCount = ref(0)
const filteredCount = ref(0)

const dostepneKategorie = computed(() => {
  return [...new Set(kategorie.value)].sort()
})

const hasActiveFilters = computed(() => {
  return wybranaKategoria.value || wybranaPlec.value
})

function selectKategoria(kategoria) {
  wybranaKategoria.value = wybranaKategoria.value === kategoria ? null : kategoria
  emitFilters()
}

function selectPlec(plec) {
  wybranaPlec.value = wybranaPlec.value === plec ? null : plec
  emitFilters()
}

function clearFilters() {
  wybranaKategoria.value = null
  wybranaPlec.value = null
  emitFilters()
}

function emitFilters() {
  const filters = {
    kategoria: wybranaKategoria.value,
    plec: wybranaPlec.value
  }
  emit('filtry-changed', filters)
  updateFilteredCount()
}

async function updateFilteredCount() {
  try {
    // Pobierz wszystkich zawodników i przefiltruj lokalnie
    const res = await axios.get('/api/wyniki')
    let filtered = res.data
    
    if (wybranaKategoria.value) {
      filtered = filtered.filter(w => w.kategoria === wybranaKategoria.value)
    }
    
    if (wybranaPlec.value) {
      filtered = filtered.filter(w => w.plec === wybranaPlec.value)
    }
    
    filteredCount.value = filtered.length
  } catch (error) {
    console.error('Błąd aktualizacji liczby filtrowanych:', error)
    filteredCount.value = totalCount.value
  }
}

async function loadKategorie() {
  try {
    const res = await axios.get('/api/kategorie')
    kategorie.value = res.data.kategorie || []
    totalCount.value = res.data.total_zawodnikow || 0
    filteredCount.value = totalCount.value
    console.log('Załadowano kategorie:', kategorie.value)
  } catch (error) {
    console.error('Błąd ładowania kategorii:', error)
    kategorie.value = []
  }
}

onMounted(loadKategorie)

// Obserwuj zmiany i aktualizuj licznik
watch([wybranaKategoria, wybranaPlec], () => {
  updateFilteredCount()
})
</script>

<style scoped>
.kategorie-container {
  font-family: 'Inter', sans-serif;
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
}

.filters-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f1f5f9;
}

.filters-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0;
}

.filters-icon {
  font-size: 1.75rem;
  background: linear-gradient(135deg, #1e40af, #3730a3);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.clear-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #ef4444;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 2rem;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.3);
}

.clear-button:hover {
  background: #dc2626;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
}

.clear-icon {
  font-size: 1rem;
  font-weight: 700;
}

.filters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.filter-label {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.1rem;
  font-weight: 700;
  color: #374151;
  margin-bottom: 0.5rem;
}

.label-icon {
  font-size: 1.25rem;
}

.filter-options {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.filter-option {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #f8fafc;
  color: #64748b;
  border: 2px solid #e2e8f0;
  padding: 0.75rem 1.25rem;
  border-radius: 2rem;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: inherit;
  white-space: nowrap;
}

.filter-option:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.filter-option.active {
  background: #1e40af;
  color: white;
  border-color: #1e40af;
  box-shadow: 0 4px 12px rgba(30, 64, 175, 0.3);
}

.filter-option.gender-male.active {
  background: #3b82f6;
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

.filter-option.gender-female.active {
  background: #ec4899;
  border-color: #ec4899;
  box-shadow: 0 4px 12px rgba(236, 72, 153, 0.3);
}

.gender-icon {
  font-size: 1.1rem;
}

.active-filters {
  background: #f0f9ff;
  border: 2px solid #bfdbfe;
  border-radius: 1rem;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.active-filters-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 700;
  color: #1e40af;
  margin-bottom: 1rem;
  font-size: 1rem;
}

.active-icon {
  font-size: 1.25rem;
}

.active-filters-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.active-filter {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: white;
  border: 2px solid #3b82f6;
  border-radius: 2rem;
  padding: 0.5rem 1rem;
  font-weight: 600;
  color: #1e40af;
  box-shadow: 0 2px 6px rgba(59, 130, 246, 0.2);
}

.filter-text {
  font-size: 0.9rem;
}

.remove-filter {
  background: #ef4444;
  color: white;
  border: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 0.75rem;
  font-weight: 700;
  transition: all 0.2s ease;
}

.remove-filter:hover {
  background: #dc2626;
  transform: scale(1.1);
}

.filter-stats {
  background: #f8fafc;
  border: 2px solid #e2e8f0;
  border-radius: 1rem;
  padding: 1.25rem;
}

.stats-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1rem;
  color: #374151;
}

.stats-icon {
  font-size: 1.25rem;
  color: #1e40af;
}

.stats-text strong {
  color: #1e40af;
  font-weight: 800;
}

.filter-info {
  color: #64748b;
  font-style: italic;
  font-size: 0.9em;
}

/* Responsive Design */
@media (max-width: 768px) {
  .kategorie-container {
    padding: 1.5rem;
  }
  
  .filters-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .filters-title {
    font-size: 1.25rem;
  }
  
  .filters-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .filter-options {
    gap: 0.5rem;
  }
  
  .filter-option {
    padding: 0.5rem 1rem;
    font-size: 0.85rem;
  }
  
  .active-filters-list {
    gap: 0.5rem;
  }
}

@media (max-width: 480px) {
  .kategorie-container {
    padding: 1rem;
  }
  
  .filters-title {
    font-size: 1.1rem;
  }
  
  .filters-icon {
    font-size: 1.5rem;
  }
  
  .filter-option {
    padding: 0.5rem 0.75rem;
    font-size: 0.8rem;
  }
  
  .clear-button {
    padding: 0.5rem 1rem;
    font-size: 0.8rem;
  }
}
</style>

