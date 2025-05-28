<template>
  <div class="app-container">
    <!-- Header -->
    <header class="main-header">
      <div class="header-content">
        <div class="event-logo">
          <div class="logo-icon">🏆</div>
          <div class="event-info">
            <h1 class="event-title">MISTRZOSTWA POLSKI</h1>
            <p class="event-subtitle">SKATECROSS 2025</p>
          </div>
        </div>
      </div>
    </header>

    <!-- Navigation -->
    <nav class="main-nav">
      <div class="nav-content">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="['nav-button', { active: activeTab === tab.id }]"
        >
          <span class="nav-icon">{{ tab.icon }}</span>
          <span class="nav-label">{{ tab.label }}</span>
        </button>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="main-content">
      
      <!-- Podsumowanie -->
      <div v-if="podsumowanie" class="summary-section">
        <div class="summary-grid">
          <div class="summary-card">
            <div class="summary-icon">👥</div>
            <div class="summary-info">
              <div class="summary-number">{{ podsumowanie.łączna_liczba_zawodników }}</div>
              <div class="summary-label">Zawodników</div>
            </div>
          </div>
          <div class="summary-card">
            <div class="summary-icon">🏅</div>
            <div class="summary-info">
              <div class="summary-number">{{ podsumowanie.wszystkie_kategorie?.length || 0 }}</div>
              <div class="summary-label">Kategorii</div>
            </div>
          </div>
          <div class="summary-card">
            <div class="summary-icon">👨</div>
            <div class="summary-info">
              <div class="summary-number">{{ podsumowanie.podział_płeć?.mężczyźni || 0 }}</div>
              <div class="summary-label">Mężczyzn</div>
            </div>
          </div>
          <div class="summary-card">
            <div class="summary-icon">👩</div>
            <div class="summary-info">
              <div class="summary-number">{{ podsumowanie.podział_płeć?.kobiety || 0 }}</div>
              <div class="summary-label">Kobiet</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Filtry -->
      <div v-if="activeTab === 'wyniki' || activeTab === 'drabinka'" class="filters-section">
        <div class="filters-container">
          <Kategorie @filtry-changed="handleFiltryChanged" />
        </div>
      </div>

      <!-- Content Sections -->
      <div class="content-section">
        <Wyniki 
          v-if="activeTab === 'wyniki'" 
          :filtry="filtry" 
        />
        <Drabinka 
          v-if="activeTab === 'drabinka'" 
          :filtry="filtry" 
          @podsumowanie-loaded="handlePodsumowanieLoaded"
        />
      </div>
    </main>

    <!-- Footer -->
    <footer class="main-footer">
      <div class="footer-content">
        <p>&copy; 2025 Mistrzostwa Polski Skatecross</p>
        <p>System zarządzania wynikami turniejowymi</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import Wyniki from './components/Wyniki.vue'
import Drabinka from './components/Drabinka.vue'
import Kategorie from './components/Kategorie.vue'

const activeTab = ref('wyniki')
const podsumowanie = ref(null)
const filtry = reactive({ kategorie: [], plec: null })

const tabs = [
  { id: 'wyniki', label: 'Wyniki', icon: '📊' },
  { id: 'drabinka', label: 'Drabinka', icon: '🏆' }
]

function handleFiltryChanged(newFiltry) {
  Object.assign(filtry, newFiltry)
}

function handlePodsumowanieLoaded(data) {
  podsumowanie.value = data
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

/* Global Variables */
:root {
  --primary-color: #1e40af;
  --secondary-color: #dc2626;
  --accent-color: #f59e0b;
  --success-color: #059669;
  --background-dark: #0f172a;
  --background-light: #f8fafc;
  --surface-dark: #1e293b;
  --surface-light: rgba(255, 255, 255, 0.95);
  --text-primary: #0f172a;
  --text-secondary: #64748b;
  --text-light: #ffffff;
  --border-color: #e2e8f0;
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
  --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1);
}

.app-container {
  font-family: 'Inter', sans-serif;
  min-height: 100vh;
  /* Nowe, bardziej dynamiczne sportowe tło: energetyczne kolory, dynamiczne linie, piłki, kształty */
  background:
    linear-gradient(120deg, #00c3ff 0%, #ffff1c 100%),
    url('data:image/svg+xml;utf8,<svg width="800" height="800" viewBox="0 0 800 800" fill="none" xmlns="http://www.w3.org/2000/svg"><rect width="800" height="800" fill="none"/><circle cx="650" cy="120" r="80" fill="%23ff6a00" fill-opacity="0.13"/><circle cx="200" cy="700" r="120" fill="%2300c3ff" fill-opacity="0.10"/><ellipse cx="600" cy="600" rx="60" ry="30" fill="%2300ff94" fill-opacity="0.12"/><ellipse cx="120" cy="200" rx="50" ry="20" fill="%23ffef00" fill-opacity="0.10"/><rect x="300" y="100" width="200" height="20" rx="10" fill="%2300c3ff" fill-opacity="0.10"/><rect x="500" y="400" width="180" height="15" rx="7" fill="%23ff6a00" fill-opacity="0.10"/><path d="M0 400 Q400 300 800 400" stroke="%2300c3ff" stroke-width="8" fill="none" opacity="0.10"/><path d="M0 600 Q400 700 800 600" stroke="%23ff6a00" stroke-width="8" fill="none" opacity="0.10"/><circle cx="400" cy="400" r="60" fill="%23ffef00" fill-opacity="0.08"/><circle cx="700" cy="700" r="40" fill="%2300ff94" fill-opacity="0.10"/></svg>');
  background-repeat: no-repeat, repeat;
  background-size: cover, 800px 800px;
  background-position: center, top left;
  color: var(--text-primary);
}

/* Header */
.main-header {
  background: linear-gradient(135deg, var(--primary-color) 0%, #3730a3 100%);
  color: var(--text-light);
  padding: 2rem 0;
  box-shadow: var(--shadow-xl);
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.event-logo {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.logo-icon {
  font-size: 4rem;
  filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
  animation: pulse 2s infinite;
}

.event-info {
  text-align: left;
}

.event-title {
  font-size: 2.5rem;
  font-weight: 900;
  margin: 0;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
  letter-spacing: -0.025em;
}

.event-subtitle {
  font-size: 1.25rem;
  font-weight: 500;
  margin: 0.5rem 0 0 0;
  opacity: 0.9;
  letter-spacing: 0.05em;
}

/* Navigation */
.main-nav {
  background: #ffffff;
  border-bottom: 1px solid var(--border-color);
  box-shadow: var(--shadow-md);
  position: sticky;
  top: 0;
  z-index: 200;
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

.nav-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  gap: 0.5rem;
}

.nav-button {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 2rem;
  background: transparent;
  border: none;
  color: var(--text-secondary);
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
  border-bottom: 3px solid transparent;
  font-family: inherit;
}

.nav-button:hover {
  color: var(--primary-color);
  background: #f1f5f9;
}

.nav-button.active {
  color: var(--primary-color);
  border-bottom-color: var(--primary-color);
  background: #f1f5f9;
}

.nav-icon {
  font-size: 1.25rem;
}

.nav-label {
  font-weight: 700;
}

/* Main Content */
.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
  min-height: calc(100vh - 200px);
}

/* Summary Section */
.summary-section {
  margin-bottom: 2rem;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.summary-card {
  background: var(--surface-light);
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: var(--shadow-lg);
  display: flex;
  align-items: center;
  gap: 1.5rem;
  transition: transform 0.2s ease;
  border: 1px solid var(--border-color);
}

.summary-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-xl);
}

.summary-icon {
  font-size: 3rem;
  background: linear-gradient(135deg, var(--primary-color), #3730a3);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
}

.summary-info {
  flex: 1;
}

.summary-number {
  font-size: 2.5rem;
  font-weight: 900;
  color: var(--text-primary);
  line-height: 1;
}

.summary-label {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-secondary);
  margin-top: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Filters Section */
.filters-section {
  margin-bottom: 2rem;
}

.filters-container {
  background: #ffffff;
  padding: 1.5rem;
  border-radius: 1rem;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-color);
}

/* Content Section */
.content-section {
  background: #ffffff;
  border-radius: 1rem;
  box-shadow: var(--shadow-lg);
  overflow: hidden;
  border: 1px solid var(--border-color);
}

/* Footer */
.main-footer {
  background: var(--surface-dark);
  color: var(--text-light);
  padding: 2rem 0;
  margin-top: 4rem;
}

.footer-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
  text-align: center;
}

.footer-content p {
  margin: 0.5rem 0;
  opacity: 0.8;
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
  .header-content {
    flex-direction: column;
    gap: 1.5rem;
    text-align: center;
  }
  
  .event-title {
    font-size: 2rem;
  }
  
  .event-subtitle {
    font-size: 1rem;
  }
  
  .nav-content {
    padding: 0 1rem;
  }
  
  .nav-button {
    padding: 1rem 1.5rem;
    font-size: 0.9rem;
  }
  
  .main-content {
    padding: 1rem;
  }
  
  /* Układ 2x2 dla tabletów i większych mobilnych */
  .summary-grid {
    grid-template-columns: 1fr 1fr !important;
    gap: 1rem !important;
  }
  
  .summary-card {
    padding: 1.5rem !important;
    flex-direction: column !important;
    text-align: center !important;
    gap: 0.75rem !important;
  }
  
  .summary-number {
    font-size: 2rem !important;
  }
  
  .summary-icon {
    font-size: 2.5rem !important;
  }
}

@media (max-width: 480px) {
  .event-logo {
    flex-direction: column;
    gap: 1rem;
  }
  
  .logo-icon {
    font-size: 3rem;
  }
  
  .event-title {
    font-size: 1.75rem;
  }
  
  .nav-button {
    flex-direction: column;
    gap: 0.25rem;
    padding: 0.75rem 1rem;
  }
  
  .nav-label {
    font-size: 0.8rem;
  }
  
  /* Mniejsze karty na bardzo małych ekranach */
  .summary-grid {
    grid-template-columns: 1fr 1fr !important;
    gap: 0.8rem !important;
  }
  
  .summary-card {
    padding: 1rem !important;
    flex-direction: column !important;
    text-align: center !important;
    gap: 0.5rem !important;
  }
  
  .summary-number {
    font-size: 1.8rem !important;
  }
  
  .summary-icon {
    font-size: 2.2rem !important;
  }
}

/* Dodatkowy media query dla średnich ekranów (tablety pionowo) */
@media (max-width: 900px) and (min-width: 769px) {
  .summary-grid {
    grid-template-columns: 1fr 1fr !important;
    gap: 1.2rem !important;
  }
  
  .summary-card {
    flex-direction: column !important;
    text-align: center !important;
    gap: 0.75rem !important;
  }
}

@media (max-width: 600px) {
  .app-container {
    overflow-x: hidden;
  }
  .main-content {
    padding: 1rem;
  }
  .summary-grid {
    grid-template-columns: 1fr 1fr !important;
    gap: 0.8rem !important;
  }
  .summary-card {
    padding: 1rem !important;
    border-radius: 0.6rem !important;
    flex-direction: column !important;
    text-align: center !important;
    gap: 0.5rem !important;
  }
  .summary-number {
    font-size: 1.8rem !important;
  }
  .summary-label {
    font-size: 0.8rem !important;
  }
  .summary-icon {
    font-size: 2.2rem !important;
  }
  .filters-container {
    padding: 1rem;
  }
  .content-section {
    padding: 1rem;
  }
  .main-header {
    padding: 1.2rem 0.2rem;
    text-align: center;
  }
  .header-content {
    flex-direction: column;
    align-items: center;
    gap: 0.7rem;
    padding: 0 0.2rem;
  }
  .event-logo {
    flex-direction: column;
    align-items: center;
    gap: 0.3rem;
  }
  .logo-icon {
    font-size: 2.5rem;
  }
  .event-title {
    font-size: 1.3rem;
    margin: 0.2rem 0 0 0;
  }
  .event-subtitle {
    font-size: 1rem;
    margin: 0.2rem 0 0 0;
  }
  .main-nav {
    position: sticky;
    top: 0;
    z-index: 200;
    box-shadow: 0 2px 8px rgba(30,64,175,0.08);
    border-radius: 0 0 1rem 1rem;
    padding: 0.2rem 0;
  }
  .nav-content {
    flex-wrap: wrap;
    gap: 0.3rem !important;
    padding: 0 0.2rem;
    justify-content: center;
  }
  .nav-button {
    flex: 1 1 45%;
    min-width: 100px !important;
    max-width: 100%;
    padding: 0.7rem 0.3rem !important;
    font-size: 0.85rem !important;
    border-radius: 0.5rem;
    margin: 0.1rem 0;
    text-align: center;
  }
  .nav-label {
    font-size: 0.85rem !important;
  }
  .nav-icon {
    font-size: 1rem !important;
  }
  .main-footer {
    padding: 1rem 0;
  }
  .footer-content {
    padding: 0 1rem;
  }
  .footer-content p {
    margin: 0.3rem 0;
    font-size: 0.9rem;
  }
}

@media (max-width: 400px) {
  .main-content {
    padding: 0.3rem !important;
  }
  .summary-grid {
    gap: 0.3rem !important;
  }
  .summary-card {
    padding: 0.4rem !important;
    border-radius: 0.4rem !important;
    min-width: 0 !important;
  }
  .summary-number {
    font-size: 1rem !important;
  }
  .summary-label {
    font-size: 0.6rem !important;
  }
  .summary-icon {
    font-size: 1.5rem !important;
  }
  .filters-container {
    padding: 0.3rem !important;
    border-radius: 0.4rem !important;
  }
  .content-section {
    padding: 0.3rem !important;
    border-radius: 0.4rem !important;
  }
  .main-footer {
    padding: 0.3rem 0 !important;
  }
  .footer-content {
    padding: 0 0.3rem !important;
  }
  .footer-content p {
    font-size: 0.6rem !important;
  }
  .nav-button {
    padding: 0.5rem 0.75rem !important;
    font-size: 0.75rem !important;
  }
}
</style>

