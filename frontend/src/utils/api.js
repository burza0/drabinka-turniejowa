import axios from 'axios'

// Określ bazowy URL dla API
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

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