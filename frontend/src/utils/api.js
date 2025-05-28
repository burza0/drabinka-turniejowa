import axios from 'axios'

// Automatyczne wykrycie środowiska
function getApiBaseUrl() {
  // Jeśli jest ustawiona zmienna środowiskowa, użyj jej
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL
  }
  
  // Automatyczne wykrycie dla różnych platform
  const currentHost = window.location.hostname
  
  if (currentHost === 'localhost' || currentHost === '127.0.0.1') {
    // Lokalne środowisko
    return 'http://localhost:5000'
  } else if (currentHost.includes('vercel.app')) {
    // Frontend na Vercel - backend na Heroku
    return 'https://drabinka-turniejowa-670178daae8c.herokuapp.com'
  } else if (currentHost.includes('herokuapp.com')) {
    // Fullstack na Heroku (ten sam URL)
    return `https://${currentHost}`
  } else {
    // Fallback - spróbuj względnych URL-i (backend na tej samej domenie)
    return window.location.origin
  }
}

// Określ bazowy URL dla API
const API_BASE_URL = getApiBaseUrl()

console.log('🔗 API Base URL:', API_BASE_URL)

// Utwórz instancję axios z konfiguracją
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Funkcje API
export const apiClient = {
  // Wyniki
  getWyniki: () => api.get('/api/wyniki'),
  
  // Kategorie  
  getKategorie: () => api.get('/api/kategorie'),
  
  // Drabinka
  getDrabinka: () => api.get('/api/drabinka'),
  
  // Statystyki
  getStatystyki: () => api.get('/api/statystyki'),
  
  // Zawodnicy
  getZawodnicy: () => api.get('/api/zawodnicy')
}

export default api 