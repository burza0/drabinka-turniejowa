import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

export interface Athlete {
  nr_startowy: number
  imie: string
  nazwisko: string
  kategoria: string
  plec: string
  klub: string
  qr_code?: string
  checked_in?: boolean
  czas_przejazdu_s?: number
  status?: string
  check_in_time?: string
}

interface AthleteState {
  athletes: Athlete[]
  loading: boolean
  error: string | null
  lastFetch: number | null
  searchQuery: string
  filters: {
    kategoria: string
    klub: string
    plec: string
    status: string
  }
}

export const useAthletesStore = defineStore('athletes', () => {
  // State
  const state = ref<AthleteState>({
    athletes: [],
    loading: false,
    error: null,
    lastFetch: null,
    searchQuery: '',
    filters: {
      kategoria: '',
      klub: '',
      plec: '',
      status: ''
    }
  })

  // Getters
  const allAthletes = computed(() => state.value.athletes)
  
  const filteredAthletes = computed(() => {
    let result = state.value.athletes

    // Text search
    if (state.value.searchQuery) {
      const query = state.value.searchQuery.toLowerCase()
      result = result.filter(athlete =>
        athlete.imie.toLowerCase().includes(query) ||
        athlete.nazwisko.toLowerCase().includes(query) ||
        athlete.klub.toLowerCase().includes(query) ||
        athlete.nr_startowy.toString().includes(query)
      )
    }

    // Filters
    if (state.value.filters.kategoria) {
      result = result.filter(a => a.kategoria === state.value.filters.kategoria)
    }
    if (state.value.filters.klub) {
      result = result.filter(a => a.klub === state.value.filters.klub)
    }
    if (state.value.filters.plec) {
      result = result.filter(a => a.plec === state.value.filters.plec)
    }
    if (state.value.filters.status) {
      if (state.value.filters.status === 'checked_in') {
        result = result.filter(a => a.checked_in === true)
      } else if (state.value.filters.status === 'not_checked_in') {
        result = result.filter(a => a.checked_in !== true)
      }
    }

    return result
  })

  const athletesByCategory = computed(() => {
    const grouped: Record<string, Athlete[]> = {}
    state.value.athletes.forEach(athlete => {
      if (!grouped[athlete.kategoria]) {
        grouped[athlete.kategoria] = []
      }
      grouped[athlete.kategoria].push(athlete)
    })
    return grouped
  })

  const athletesByClub = computed(() => {
    const grouped: Record<string, Athlete[]> = {}
    state.value.athletes.forEach(athlete => {
      if (!grouped[athlete.klub]) {
        grouped[athlete.klub] = []
      }
      grouped[athlete.klub].push(athlete)
    })
    return grouped
  })

  const uniqueCategories = computed(() => 
    [...new Set(state.value.athletes.map(a => a.kategoria))].sort()
  )

  const uniqueClubs = computed(() => 
    [...new Set(state.value.athletes.map(a => a.klub))].sort()
  )

  const stats = computed(() => ({
    total: state.value.athletes.length,
    checkedIn: state.value.athletes.filter(a => a.checked_in).length,
    withResults: state.value.athletes.filter(a => a.czas_przejazdu_s).length,
    withQR: state.value.athletes.filter(a => a.qr_code).length
  }))

  // Actions
  const fetchAthletes = async (force = false) => {
    // Check if we need to fetch (don't fetch if recent and not forced)
    const now = Date.now()
    const fiveMinutes = 5 * 60 * 1000
    if (!force && state.value.lastFetch && (now - state.value.lastFetch) < fiveMinutes) {
      console.log('📦 Using cached athletes data')
      return state.value.athletes
    }

    state.value.loading = true
    state.value.error = null

    try {
      const response = await axios.get('/api/zawodnicy?limit=1000')
      
      let athletes: Athlete[]
      if (response.data.success) {
        athletes = response.data.data || []
      } else {
        athletes = response.data.data || response.data || []
      }

      state.value.athletes = athletes
      state.value.lastFetch = now
      
      // Cache in localStorage
      localStorage.setItem('skatecross-athletes-cache', JSON.stringify({
        athletes,
        timestamp: now
      }))

      console.log(`✅ Fetched ${athletes.length} athletes`)
      return athletes

    } catch (error) {
      console.error('Error fetching athletes:', error)
      state.value.error = 'Błąd pobierania danych zawodników'
      
      // Try to load from cache if network failed
      await loadFromCache()
      
      throw error
    } finally {
      state.value.loading = false
    }
  }

  const findAthleteByQR = (qrCode: string): Athlete | null => {
    return state.value.athletes.find(athlete => athlete.qr_code === qrCode) || null
  }

  const findAthleteByNumber = (number: number): Athlete | null => {
    return state.value.athletes.find(athlete => athlete.nr_startowy === number) || null
  }

  const updateAthlete = (updatedAthlete: Athlete) => {
    const index = state.value.athletes.findIndex(a => a.nr_startowy === updatedAthlete.nr_startowy)
    if (index !== -1) {
      state.value.athletes[index] = { ...state.value.athletes[index], ...updatedAthlete }
      
      // Update cache
      localStorage.setItem('skatecross-athletes-cache', JSON.stringify({
        athletes: state.value.athletes,
        timestamp: state.value.lastFetch
      }))
    }
  }

  const setSearchQuery = (query: string) => {
    state.value.searchQuery = query
  }

  const setFilter = (filterType: keyof AthleteState['filters'], value: string) => {
    state.value.filters[filterType] = value
  }

  const clearFilters = () => {
    state.value.searchQuery = ''
    state.value.filters = {
      kategoria: '',
      klub: '',
      plec: '',
      status: ''
    }
  }

  const loadFromCache = async () => {
    const cached = localStorage.getItem('skatecross-athletes-cache')
    if (cached) {
      try {
        const { athletes, timestamp } = JSON.parse(cached)
        state.value.athletes = athletes
        state.value.lastFetch = timestamp
        console.log(`📦 Loaded ${athletes.length} athletes from cache`)
      } catch (error) {
        console.error('Error loading athletes from cache:', error)
        localStorage.removeItem('skatecross-athletes-cache')
      }
    }
  }

  const clearCache = () => {
    state.value.athletes = []
    state.value.lastFetch = null
    localStorage.removeItem('skatecross-athletes-cache')
  }

  // Initialize - load from cache first
  loadFromCache()

  return {
    // State
    state: computed(() => state.value),
    
    // Getters
    allAthletes,
    filteredAthletes,
    athletesByCategory,
    athletesByClub,
    uniqueCategories,
    uniqueClubs,
    stats,
    
    // Actions
    fetchAthletes,
    findAthleteByQR,
    findAthleteByNumber,
    updateAthlete,
    setSearchQuery,
    setFilter,
    clearFilters,
    loadFromCache,
    clearCache
  }
}) 