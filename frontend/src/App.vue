<template>
  <div class="app" :class="{ 'fullscreen': isFullscreen }">
    <!-- Mobile Header -->
    <header class="mobile-header">
      <div class="header-content">
        <div class="event-logo">
          <div class="logo-icon">🏆</div>
          <div class="event-info">
            <h1 class="event-title">Skatecross 2025</h1>
            <p class="event-subtitle">Mistrzostwa Polski</p>
          </div>
        </div>
        <button 
          class="menu-button"
          @click="showSettings = !showSettings"
          :class="{ active: showSettings }"
        >
          <span class="menu-icon">⚙️</span>
        </button>
      </div>
    </header>

    <!-- Settings Panel -->
    <div v-if="showSettings" class="settings-panel" @click="showSettings = false">
      <div class="settings-content" @click.stop>
        <div class="settings-header">
          <h3>Ustawienia</h3>
          <button @click="showSettings = false" class="close-btn">✕</button>
        </div>
        <div class="settings-options">
          <button @click="toggleFullscreen" class="setting-option">
            <span class="setting-icon">📱</span>
            <span>{{ isFullscreen ? 'Wyjdź z pełnego ekranu' : 'Pełny ekran' }}</span>
          </button>
          <button @click="refreshData" class="setting-option">
            <span class="setting-icon">🔄</span>
            <span>Odśwież dane</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Quick Stats Bar -->
    <div v-if="podsumowanie && !isFullscreen" class="quick-stats">
      <div class="stat-item">
        <span class="stat-number">{{ podsumowanie.łączna_liczba_zawodników }}</span>
        <span class="stat-label">zawodników</span>
      </div>
      <div class="stat-item">
        <span class="stat-number">{{ podsumowanie.wszystkie_kategorie?.length || 0 }}</span>
        <span class="stat-label">kategorii</span>
      </div>
      <div class="stat-item">
        <span class="stat-number">{{ filtrowaneCount }}</span>
        <span class="stat-label">wyników</span>
      </div>
    </div>

    <!-- Main Content -->
    <main class="main-content">
      <!-- Pull to Refresh -->
      <div v-if="isPulling" class="pull-refresh-indicator">
        <div class="refresh-icon">🔄</div>
        <span>Potągnij aby odświeżyć</span>
      </div>

      <!-- Filters -->
      <div v-if="showFilters" class="filters-overlay" @click="showFilters = false">
        <div class="filters-panel" @click.stop>
          <div class="filters-header">
            <h3>Filtry</h3>
            <button @click="showFilters = false" class="close-btn">✕</button>
          </div>
          <Kategorie @filtry-changed="handleFiltryChanged" />
        </div>
      </div>

      <!-- Content -->
      <div class="content-wrapper">
        <Wyniki 
          v-if="activeTab === 'wyniki'" 
          :filtry="filtry"
          @results-count="handleResultsCount"
        />
        <Drabinka 
          v-if="activeTab === 'drabinka'" 
          :filtry="filtry" 
          @podsumowanie-loaded="handlePodsumowanieLoaded"
        />
      </div>
    </main>

    <!-- Floating Action Button -->
    <button 
      class="fab-filter"
      @click="showFilters = true"
      v-if="activeTab === 'wyniki' || activeTab === 'drabinka'"
    >
      <span class="fab-icon">🔍</span>
    </button>

    <!-- Bottom Navigation -->
    <nav class="bottom-nav">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        @click="activeTab = tab.id"
        :class="['nav-tab', { active: activeTab === tab.id }]"
      >
        <span class="tab-icon">{{ tab.icon }}</span>
        <span class="tab-label">{{ tab.label }}</span>
        <div v-if="activeTab === tab.id" class="active-indicator"></div>
      </button>
    </nav>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="loading-spinner">
        <div class="spinner"></div>
        <p>Ładowanie danych...</p>
      </div>
    </div>

    <!-- Toast Notifications -->
    <div class="toast-container">
      <div 
        v-for="toast in toasts" 
        :key="toast.id"
        :class="['toast', toast.type]"
        @click="removeToast(toast.id)"
      >
        <span class="toast-icon">{{ getToastIcon(toast.type) }}</span>
        <span class="toast-message">{{ toast.message }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import Wyniki from './components/Wyniki.vue'
import Drabinka from './components/Drabinka.vue'
import Kategorie from './components/Kategorie.vue'

// State
const activeTab = ref('wyniki')
const podsumowanie = ref(null)
const filtry = reactive({ kategorie: [], plec: null })
const filtrowaneCount = ref(0)
const isFullscreen = ref(false)
const showSettings = ref(false)
const showFilters = ref(false)
const isLoading = ref(false)
const isPulling = ref(false)
const toasts = ref([])

// Tabs configuration
const tabs = [
  { id: 'wyniki', label: 'Wyniki', icon: '🏆' },
  { id: 'drabinka', label: 'Drabinka', icon: '🌟' }
]

// Touch/Gesture handling
let startY = 0
let pullDistance = 0

// Functions
function handleFiltryChanged(newFiltry) {
  Object.assign(filtry, newFiltry)
  showToast('Filtry zaktualizowane', 'success')
}

function handlePodsumowanieLoaded(data) {
  podsumowanie.value = data
}

function handleResultsCount(count) {
  filtrowaneCount.value = count
}

function toggleFullscreen() {
  isFullscreen.value = !isFullscreen.value
  showSettings.value = false
  showToast(isFullscreen.value ? 'Tryb pełnoekranowy' : 'Tryb normalny', 'info')
}

async function refreshData() {
  isLoading.value = true
  showSettings.value = false
  
  try {
    // Simulate refresh
    await new Promise(resolve => setTimeout(resolve, 1000))
    showToast('Dane odświeżone', 'success')
  } catch (error) {
    showToast('Błąd odświeżania', 'error')
  } finally {
    isLoading.value = false
  }
}

function showToast(message, type = 'info') {
  const id = Date.now()
  toasts.value.push({ id, message, type })
  
  setTimeout(() => {
    removeToast(id)
  }, 3000)
}

function removeToast(id) {
  const index = toasts.value.findIndex(t => t.id === id)
  if (index > -1) {
    toasts.value.splice(index, 1)
  }
}

function getToastIcon(type) {
  switch(type) {
    case 'success': return '✅'
    case 'error': return '❌'
    case 'warning': return '⚠️'
    default: return 'ℹ️'
  }
}

// Pull to refresh handling
function handleTouchStart(event) {
  if (window.scrollY === 0) {
    startY = event.touches[0].clientY
  }
}

function handleTouchMove(event) {
  if (window.scrollY === 0 && startY > 0) {
    pullDistance = event.touches[0].clientY - startY
    if (pullDistance > 50) {
      isPulling.value = true
    }
  }
}

function handleTouchEnd() {
  if (isPulling.value && pullDistance > 80) {
    refreshData()
  }
  isPulling.value = false
  startY = 0
  pullDistance = 0
}

// Lifecycle
onMounted(() => {
  document.addEventListener('touchstart', handleTouchStart, { passive: true })
  document.addEventListener('touchmove', handleTouchMove, { passive: true })
  document.addEventListener('touchend', handleTouchEnd, { passive: true })
})

onUnmounted(() => {
  document.removeEventListener('touchstart', handleTouchStart)
  document.removeEventListener('touchmove', handleTouchMove)
  document.removeEventListener('touchend', handleTouchEnd)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* CSS Variables */
:root {
  --primary: #3b82f6;
  --primary-dark: #2563eb;
  --secondary: #f59e0b;
  --success: #10b981;
  --error: #ef4444;
  --warning: #f59e0b;
  --surface: #ffffff;
  --background: #f8fafc;
  --text-primary: #1f2937;
  --text-secondary: #6b7280;
  --text-muted: #9ca3af;
  --border: #e5e7eb;
  --shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
  --radius: 0.75rem;
  --nav-height: 70px;
  --header-height: 60px;
}

* {
  box-sizing: border-box;
}

.app {
  font-family: 'Inter', sans-serif;
  min-height: 100vh;
  background: var(--background);
  color: var(--text-primary);
  display: flex;
  flex-direction: column;
  overflow-x: hidden;
}

/* Mobile Header */
.mobile-header {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  color: white;
  height: var(--header-height);
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: var(--shadow-lg);
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1rem;
  height: 100%;
  max-width: 100%;
}

.event-logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
  min-width: 0;
}

.logo-icon {
  font-size: 1.5rem;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
}

.event-info {
  min-width: 0;
  flex: 1;
}

.event-title {
  font-size: 1.1rem;
  font-weight: 700;
  margin: 0;
  line-height: 1.2;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.event-subtitle {
  font-size: 0.8rem;
  font-weight: 400;
  margin: 0;
  opacity: 0.9;
  line-height: 1;
}

.menu-button {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  backdrop-filter: blur(10px);
}

.menu-button:hover,
.menu-button.active {
  background: rgba(255, 255, 255, 0.3);
  transform: scale(1.05);
}

.menu-icon {
  font-size: 1.2rem;
}

/* Settings Panel */
.settings-panel {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 200;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: var(--header-height);
}

.settings-content {
  background: var(--surface);
  width: 90%;
  max-width: 400px;
  border-radius: var(--radius);
  margin-top: 1rem;
  box-shadow: var(--shadow-lg);
  animation: slideDown 0.3s ease;
}

.settings-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--border);
}

.settings-header h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
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

.settings-options {
  padding: 1rem;
}

.setting-option {
  display: flex;
  align-items: center;
  gap: 1rem;
  width: 100%;
  padding: 1rem;
  border: none;
  background: none;
  text-align: left;
  font-size: 1rem;
  color: var(--text-primary);
  border-radius: var(--radius);
  cursor: pointer;
  transition: all 0.2s ease;
}

.setting-option:hover {
  background: var(--background);
}

.setting-icon {
  font-size: 1.2rem;
}

/* Quick Stats */
.quick-stats {
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  display: flex;
  padding: 1rem;
  gap: 1rem;
  overflow-x: auto;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 0;
  flex: 1;
  text-align: center;
}

.stat-number {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--primary);
  line-height: 1;
}

.stat-label {
  font-size: 0.75rem;
  color: var(--text-secondary);
  font-weight: 500;
  margin-top: 0.25rem;
}

/* Main Content */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-bottom: var(--nav-height);
  min-height: 0;
}

.content-wrapper {
  flex: 1;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}

/* Pull to Refresh */
.pull-refresh-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem;
  background: var(--primary);
  color: white;
  font-size: 0.9rem;
  font-weight: 500;
}

.refresh-icon {
  animation: spin 1s linear infinite;
}

/* Filters Panel */
.filters-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 150;
  display: flex;
  align-items: flex-end;
}

.filters-panel {
  background: var(--surface);
  width: 100%;
  max-height: 80vh;
  border-radius: var(--radius) var(--radius) 0 0;
  animation: slideUp 0.3s ease;
  overflow-y: auto;
}

.filters-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  background: var(--surface);
  z-index: 10;
}

.filters-header h3 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
}

/* Floating Action Button */
.fab-filter {
  position: fixed;
  bottom: calc(var(--nav-height) + 1rem);
  right: 1rem;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: var(--primary);
  color: white;
  border: none;
  box-shadow: var(--shadow-lg);
  cursor: pointer;
  transition: all 0.2s ease;
  z-index: 50;
  display: flex;
  align-items: center;
  justify-content: center;
}

.fab-filter:hover {
  transform: scale(1.1);
  background: var(--primary-dark);
}

.fab-icon {
  font-size: 1.5rem;
}

/* Bottom Navigation */
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: var(--surface);
  border-top: 1px solid var(--border);
  display: flex;
  height: var(--nav-height);
  z-index: 100;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
}

.nav-tab {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  padding: 0.5rem;
}

.nav-tab.active {
  color: var(--primary);
}

.tab-icon {
  font-size: 1.5rem;
  transition: transform 0.2s ease;
}

.tab-label {
  font-size: 0.7rem;
  font-weight: 500;
  line-height: 1;
}

.nav-tab.active .tab-icon {
  transform: scale(1.1);
}

.active-indicator {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 30px;
  height: 3px;
  background: var(--primary);
  border-radius: 0 0 2px 2px;
}

/* Loading */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.9);
  z-index: 300;
  display: flex;
  align-items: center;
  justify-content: center;
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

/* Toast Notifications */
.toast-container {
  position: fixed;
  top: calc(var(--header-height) + 1rem);
  left: 1rem;
  right: 1rem;
  z-index: 250;
  pointer-events: none;
}

.toast {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background: var(--surface);
  padding: 1rem;
  border-radius: var(--radius);
  box-shadow: var(--shadow-lg);
  margin-bottom: 0.5rem;
  border-left: 4px solid var(--primary);
  pointer-events: auto;
  cursor: pointer;
  animation: slideInRight 0.3s ease;
}

.toast.success {
  border-left-color: var(--success);
}

.toast.error {
  border-left-color: var(--error);
}

.toast.warning {
  border-left-color: var(--warning);
}

.toast-icon {
  font-size: 1.2rem;
  flex-shrink: 0;
}

.toast-message {
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--text-primary);
}

/* Fullscreen Mode */
.app.fullscreen .mobile-header,
.app.fullscreen .bottom-nav,
.app.fullscreen .quick-stats,
.app.fullscreen .fab-filter {
  display: none;
}

.app.fullscreen .main-content {
  margin-bottom: 0;
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

@keyframes slideUp {
  from {
    transform: translateY(100%);
  }
  to {
    transform: translateY(0);
  }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(100%);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Very small screens (320px+) */
@media (max-width: 360px) {
  .event-title {
    font-size: 1rem;
  }
  
  .event-subtitle {
    font-size: 0.7rem;
  }
  
  .header-content {
    padding: 0 0.75rem;
  }
  
  .quick-stats {
    padding: 0.75rem;
    gap: 0.75rem;
  }
  
  .stat-number {
    font-size: 1.3rem;
  }
  
  .stat-label {
    font-size: 0.7rem;
  }
  
  .tab-label {
    font-size: 0.65rem;
  }
  
  .tab-icon {
    font-size: 1.3rem;
  }
}

/* Landscape orientation for mobile */
@media (max-height: 500px) and (orientation: landscape) {
  .bottom-nav {
    height: 50px;
  }
  
  :root {
    --nav-height: 50px;
  }
  
  .tab-icon {
    font-size: 1.2rem;
  }
  
  .tab-label {
    display: none;
  }
  
  .nav-tab {
    gap: 0;
  }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  :root {
    --surface: #1f2937;
    --background: #111827;
    --text-primary: #f9fafb;
    --text-secondary: #d1d5db;
    --text-muted: #9ca3af;
    --border: #374151;
  }
}
</style>

