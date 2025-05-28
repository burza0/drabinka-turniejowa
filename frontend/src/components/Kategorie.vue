<template>
  <div class="kategorie-container">
    <!-- Categories Section -->
    <div class="filter-section">
      <div class="section-header">
        <h3 class="section-title">
          <span class="section-icon">🏅</span>
          Kategorie wiekowe
        </h3>
        <div class="selection-count" v-if="wybraneKategorie.length > 0">
          {{ wybraneKategorie.length }} wybrano
        </div>
      </div>
      
      <div class="category-grid">
        <button 
          v-for="kategoria in dostepneKategorie" 
          :key="kategoria"
          @click="toggleKategoria(kategoria)"
          :class="['category-chip', { 
            selected: wybraneKategorie.includes(kategoria),
            'has-selection': wybraneKategorie.length > 0 && !wybraneKategorie.includes(kategoria)
          }]"
        >
          <span class="chip-text">{{ kategoria }}</span>
          <span v-if="wybraneKategorie.includes(kategoria)" class="selected-icon">✓</span>
        </button>
      </div>
    </div>

    <!-- Gender Section -->
    <div class="filter-section">
      <div class="section-header">
        <h3 class="section-title">
          <span class="section-icon">👥</span>
          Płeć
        </h3>
      </div>
      
      <div class="gender-options">
        <button 
          @click="togglePlec(null)"
          :class="['gender-chip', 'all', { selected: wybranaPlec === null }]"
        >
          <span class="gender-icon">👥</span>
          <span class="gender-text">Wszyscy</span>
          <span v-if="wybranaPlec === null" class="selected-icon">✓</span>
        </button>
        
        <button 
          @click="togglePlec('M')"
          :class="['gender-chip', 'male', { selected: wybranaPlec === 'M' }]"
        >
          <span class="gender-icon">👨</span>
          <span class="gender-text">Mężczyźni</span>
          <span v-if="wybranaPlec === 'M'" class="selected-icon">✓</span>
        </button>
        
        <button 
          @click="togglePlec('K')"
          :class="['gender-chip', 'female', { selected: wybranaPlec === 'K' }]"
        >
          <span class="gender-icon">👩</span>
          <span class="gender-text">Kobiety</span>
          <span v-if="wybranaPlec === 'K'" class="selected-icon">✓</span>
        </button>
      </div>
    </div>

    <!-- Active Filters -->
    <div v-if="hasActiveFilters" class="active-filters">
      <div class="active-header">
        <span class="active-icon">🎯</span>
        <span class="active-title">Aktywne filtry</span>
        <button @click="clearAllFilters" class="clear-all-btn">
          <span class="clear-icon">🗑️</span>
          Wyczyść wszystko
        </button>
      </div>
      
      <div class="active-list">
        <!-- Selected Categories -->
        <div 
          v-for="kategoria in wybraneKategorie" 
          :key="`kategoria-${kategoria}`"
          class="active-tag category-tag"
        >
          <span class="tag-icon">🏅</span>
          <span class="tag-text">{{ kategoria }}</span>
          <button @click="removeKategoria(kategoria)" class="remove-btn">
            <span class="remove-icon">✕</span>
          </button>
        </div>
        
        <!-- Selected Gender -->
        <div 
          v-if="wybranaPlec" 
          class="active-tag gender-tag"
        >
          <span class="tag-icon">{{ wybranaPlec === 'M' ? '👨' : '👩' }}</span>
          <span class="tag-text">{{ wybranaPlec === 'M' ? 'Mężczyźni' : 'Kobiety' }}</span>
          <button @click="togglePlec(null)" class="remove-btn">
            <span class="remove-icon">✕</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="quick-actions">
      <button 
        v-if="dostepneKategorie.length > 0 && wybraneKategorie.length < dostepneKategorie.length"
        @click="selectAllCategories"
        class="quick-btn select-all"
      >
        <span class="quick-icon">✅</span>
        <span>Wybierz wszystkie kategorie</span>
      </button>
      
      <button 
        v-if="wybraneKategorie.length > 0"
        @click="clearCategories"
        class="quick-btn clear-categories"
      >
        <span class="quick-icon">❌</span>
        <span>Wyczyść kategorie</span>
      </button>
    </div>

    <!-- Filter Summary -->
    <div v-if="hasActiveFilters" class="filter-summary">
      <div class="summary-content">
        <span class="summary-icon">📊</span>
        <span class="summary-text">
          Filtr aktywny: {{ getFilterSummary() }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { apiClient } from '../utils/api.js'

const emit = defineEmits(['filtry-changed'])

// State
const kategorie = ref([])
const wybraneKategorie = ref([])
const wybranaPlec = ref(null)

// Computed
const dostepneKategorie = computed(() => {
  return [...new Set(kategorie.value)].sort()
})

const hasActiveFilters = computed(() => {
  return wybraneKategorie.value.length > 0 || wybranaPlec.value
})

// Functions
function toggleKategoria(kategoria) {
  const index = wybraneKategorie.value.indexOf(kategoria)
  if (index > -1) {
    wybraneKategorie.value.splice(index, 1)
  } else {
    wybraneKategorie.value.push(kategoria)
  }
  emitFilters()
}

function removeKategoria(kategoria) {
  const index = wybraneKategorie.value.indexOf(kategoria)
  if (index > -1) {
    wybraneKategorie.value.splice(index, 1)
    emitFilters()
  }
}

function togglePlec(plec) {
  wybranaPlec.value = plec
  emitFilters()
}

function selectAllCategories() {
  wybraneKategorie.value = [...dostepneKategorie.value]
  emitFilters()
}

function clearCategories() {
  wybraneKategorie.value = []
  emitFilters()
}

function clearAllFilters() {
  wybraneKategorie.value = []
  wybranaPlec.value = null
  emitFilters()
}

function getFilterSummary() {
  const parts = []
  
  if (wybraneKategorie.value.length > 0) {
    if (wybraneKategorie.value.length === 1) {
      parts.push(`kategoria "${wybraneKategorie.value[0]}"`)
    } else {
      parts.push(`${wybraneKategorie.value.length} kategorii`)
    }
  }
  
  if (wybranaPlec.value) {
    parts.push(wybranaPlec.value === 'M' ? 'mężczyźni' : 'kobiety')
  }
  
  return parts.join(', ')
}

function emitFilters() {
  const filters = {
    kategorie: wybraneKategorie.value,
    plec: wybranaPlec.value
  }
  emit('filtry-changed', filters)
}

async function loadKategorie() {
  try {
    const res = await apiClient.getKategorie()
    if (res.data && res.data.kategorie) {
      kategorie.value = res.data.kategorie
      console.log('Załadowano kategorie:', kategorie.value.length)
    }
  } catch (error) {
    console.error('Błąd ładowania kategorii:', error)
    kategorie.value = []
  }
}

// Lifecycle
onMounted(loadKategorie)
</script>

<style scoped>
.kategorie-container {
  font-family: 'Inter', sans-serif;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Filter Section */
.filter-section {
  background: var(--surface);
  border-radius: 1rem;
  padding: 1rem;
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.section-icon {
  font-size: 1.1rem;
}

.selection-count {
  background: var(--primary);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.8rem;
  font-weight: 500;
}

/* Category Grid */
.category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 0.75rem;
}

.category-chip {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  padding: 0.75rem 1rem;
  border: 2px solid var(--border);
  background: var(--surface);
  color: var(--text-secondary);
  border-radius: 0.75rem;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  min-height: 44px;
  position: relative;
}

.category-chip:hover {
  border-color: var(--primary);
  color: var(--primary);
  transform: translateY(-1px);
  box-shadow: var(--shadow);
}

.category-chip.selected {
  background: var(--primary);
  border-color: var(--primary);
  color: white;
  box-shadow: var(--shadow);
}

.category-chip.has-selection {
  opacity: 0.6;
}

.chip-text {
  flex: 1;
  text-align: center;
}

.selected-icon {
  font-size: 0.9rem;
  font-weight: 700;
}

/* Gender Options */
.gender-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 0.75rem;
}

.gender-chip {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem;
  border: 2px solid var(--border);
  background: var(--surface);
  color: var(--text-secondary);
  border-radius: 0.75rem;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  min-height: 60px;
  position: relative;
}

.gender-chip:hover {
  border-color: var(--primary);
  color: var(--primary);
  transform: translateY(-1px);
  box-shadow: var(--shadow);
}

.gender-chip.selected {
  background: var(--primary);
  border-color: var(--primary);
  color: white;
  box-shadow: var(--shadow);
}

.gender-chip.male.selected {
  background: #3b82f6;
  border-color: #3b82f6;
}

.gender-chip.female.selected {
  background: #ec4899;
  border-color: #ec4899;
}

.gender-icon {
  font-size: 1.2rem;
}

.gender-text {
  font-weight: 600;
}

/* Active Filters */
.active-filters {
  background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
  border: 2px solid #bae6fd;
  border-radius: 1rem;
  padding: 1rem;
}

.active-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;
}

.active-icon {
  font-size: 1.1rem;
}

.active-title {
  font-weight: 600;
  color: var(--primary);
  flex: 1;
  min-width: 0;
}

.clear-all-btn {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.5rem 0.75rem;
  background: var(--error);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 0.8rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.clear-all-btn:hover {
  background: #dc2626;
  transform: translateY(-1px);
}

.clear-icon {
  font-size: 0.9rem;
}

.active-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.active-tag {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  background: white;
  border: 2px solid var(--primary);
  border-radius: 1rem;
  font-size: 0.8rem;
  font-weight: 500;
  color: var(--primary);
  box-shadow: var(--shadow);
}

.category-tag {
  border-color: var(--secondary);
  color: var(--secondary);
}

.gender-tag {
  border-color: #ec4899;
  color: #ec4899;
}

.tag-icon {
  font-size: 0.9rem;
}

.tag-text {
  font-weight: 600;
}

.remove-btn {
  background: var(--error);
  color: white;
  border: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 0.7rem;
  font-weight: 700;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.remove-btn:hover {
  background: #dc2626;
  transform: scale(1.1);
}

.remove-icon {
  line-height: 1;
}

/* Quick Actions */
.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.quick-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border: 2px solid var(--border);
  background: var(--surface);
  color: var(--text-secondary);
  border-radius: 0.75rem;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.quick-btn:hover {
  border-color: var(--primary);
  color: var(--primary);
  transform: translateY(-1px);
  box-shadow: var(--shadow);
}

.quick-btn.select-all:hover {
  border-color: var(--success);
  color: var(--success);
}

.quick-btn.clear-categories:hover {
  border-color: var(--error);
  color: var(--error);
}

.quick-icon {
  font-size: 1rem;
}

/* Filter Summary */
.filter-summary {
  background: var(--primary);
  color: white;
  border-radius: 0.75rem;
  padding: 1rem;
  box-shadow: var(--shadow);
}

.summary-content {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.summary-icon {
  font-size: 1.2rem;
  flex-shrink: 0;
}

.summary-text {
  font-size: 0.9rem;
  font-weight: 500;
  line-height: 1.4;
}

/* Very small screens */
@media (max-width: 360px) {
  .kategorie-container {
    padding: 0.75rem;
    gap: 1rem;
  }
  
  .filter-section {
    padding: 0.75rem;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .category-grid {
    grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
    gap: 0.5rem;
  }
  
  .category-chip {
    padding: 0.5rem 0.75rem;
    font-size: 0.75rem;
    min-height: 40px;
  }
  
  .gender-options {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
  
  .gender-chip {
    padding: 0.75rem;
    min-height: 50px;
  }
  
  .active-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .clear-all-btn {
    align-self: stretch;
    justify-content: center;
  }
  
  .quick-actions {
    gap: 0.75rem;
  }
  
  .quick-btn {
    padding: 1rem;
    font-size: 0.8rem;
  }
}

/* Landscape mode adjustments */
@media (max-height: 500px) and (orientation: landscape) {
  .kategorie-container {
    gap: 1rem;
  }
  
  .filter-section {
    padding: 0.75rem;
  }
  
  .gender-chip {
    min-height: 50px;
  }
  
  .category-chip {
    min-height: 40px;
  }
}

/* Medium screens - tablets */
@media (min-width: 768px) and (max-width: 1024px) {
  .category-grid {
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  }
  
  .gender-options {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .quick-actions {
    flex-direction: row;
    gap: 1rem;
  }
  
  .quick-btn {
    flex: 1;
  }
}

/* Large screens */
@media (min-width: 1025px) {
  .kategorie-container {
    gap: 2rem;
  }
  
  .category-grid {
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  }
  
  .gender-options {
    grid-template-columns: repeat(3, 1fr);
    max-width: 600px;
  }
  
  .quick-actions {
    flex-direction: row;
    gap: 1rem;
    max-width: 600px;
  }
  
  .quick-btn {
    flex: 1;
  }
}
</style>

