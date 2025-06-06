import { computed, ref, reactive } from 'vue'

// Types (re-export from component)
export interface FilterOption {
  value: string
  label: string
  count?: number
  countKey?: string
}

export interface CustomFilter {
  id: string
  type: 'select' | 'text'
  icon: string
  label: string
  options: FilterOption[]
  showCounts?: boolean
}

export interface GroupOperation {
  id: string
  label: string
  icon: string
  color: 'indigo' | 'green' | 'purple' | 'orange' | 'red' | 'yellow'
  condition: 'always' | 'hasActiveFilters' | 'hasSelectedCategory' | 'hasSelectedClub' | 'hasItemsWithoutQr' | string
  dynamic?: boolean
}

export interface FilterConfig {
  layout: 'compact' | 'single-row' | 'multi-row' | 'advanced'
  columns?: 1 | 2 | 3 | 4 | 'auto'
  title?: string
  labels?: Record<string, string>
  placeholders?: Record<string, string>
  enabledFilters?: {
    search?: boolean
    category?: boolean  
    club?: boolean
    gender?: boolean
    sorting?: boolean
  }
  customFilters?: CustomFilter[]
  groupOperations?: {
    enabled: boolean
    operations: GroupOperation[]
  }
  theme?: {
    focusColor?: 'purple' | 'indigo' | 'blue' | 'green'
    borderStyle?: 'normal' | 'thick' | 'minimal'
    spacing?: 'compact' | 'normal' | 'relaxed'
  }
  showClearButton?: boolean
  debug?: boolean
}

export interface FilterData {
  categories?: string[]
  clubs?: string[]
  sortOptions?: FilterOption[]
  stats?: Record<string, number>
  customStats?: Record<string, Record<string, number>>
}

export interface FilterState {
  search: string
  category: string
  club: string
  gender: string
  sorting: string
  [key: string]: any
}

// Predefined configurations for different components
export const useUniversalFilters = () => {
  
  // QrPrint.vue - Advanced configuration
  const qrPrintConfig = computed((): FilterConfig => ({
    layout: 'advanced',
    title: 'Filtry i sortowanie',
    theme: {
      focusColor: 'indigo',
      borderStyle: 'thick',
      spacing: 'normal'
    },
    enabledFilters: {
      category: true,
      club: true,
      sorting: true
    },
    customFilters: [
      {
        id: 'qr_status',
        type: 'select',
        icon: '📱',
        label: 'Status QR',
        showCounts: true,
        options: [
          { value: '', label: 'Wszystkie' },
          { value: 'with_qr', label: '✅ Z QR kodami', countKey: 'withQr' },
          { value: 'without_qr', label: '❌ Bez QR kodów', countKey: 'withoutQr' }
        ]
      }
    ],
    groupOperations: {
      enabled: true,
      operations: [
        {
          id: 'toggle_all',
          label: 'Zaznacz wszystkie',
          icon: '☐',
          color: 'indigo',
          condition: 'always',
          dynamic: true
        },
        {
          id: 'toggle_by_category',
          label: 'Toggle kategoria',
          icon: '🏆',
          color: 'green',
          condition: 'hasSelectedCategory',
          dynamic: true
        },
        {
          id: 'toggle_by_club', 
          label: 'Toggle klub',
          icon: '🏢',
          color: 'purple',
          condition: 'hasSelectedClub',
          dynamic: true
        },
        {
          id: 'toggle_without_qr',
          label: 'Zaznacz bez QR',
          icon: '📱',
          color: 'orange',
          condition: 'hasItemsWithoutQr'
        }
      ]
    }
  }))

  // Rankingi.vue - Multi-row configuration 
  const rankingConfig = computed((): FilterConfig => ({
    layout: 'multi-row',
    columns: 4,
    title: 'Filtry i sortowanie',
    theme: {
      focusColor: 'purple',
      borderStyle: 'thick',
      spacing: 'normal'
    },
    enabledFilters: {
      category: true,
      club: true,
      gender: true,
      sorting: true
    }
  }))

  // App.vue (Zawodnicy) - Single-row configuration
  const zawodnicyConfig = computed((): FilterConfig => ({
    layout: 'single-row',
    columns: 4,
    title: 'Filtry i sortowanie',
    theme: {
      focusColor: 'purple',
      borderStyle: 'thick',
      spacing: 'normal'
    },
    enabledFilters: {
      category: true,
      club: true,
      gender: true,
      sorting: true
    },
    customFilters: [
      {
        id: 'status_qr',
        type: 'select',
        icon: '📱',
        label: 'Status QR',
        options: [
          { value: '', label: 'Wszystkie' },
          { value: 'z_qr', label: 'Z kodem QR' },
          { value: 'bez_qr', label: 'Bez kodu QR' }
        ]
      },
      {
        id: 'status',
        type: 'select',
        icon: '📊',
        label: 'Status',
        options: [
          { value: '', label: 'Wszystkie' },
          { value: 'FINISHED', label: 'Ukończyli' },
          { value: 'DNF', label: 'DNF' },
          { value: 'DSQ', label: 'DSQ' }
        ]
      }
    ],
    groupOperations: {
      enabled: true,
      operations: [
        {
          id: 'toggle_all',
          label: 'Zaznacz wszystkie',
          icon: '☐',
          color: 'indigo',
          condition: 'always',
          dynamic: true
        },
        {
          id: 'toggle_by_category',
          label: 'Zaznacz kategorię',
          icon: '🏆',
          color: 'green',
          condition: 'hasSelectedCategory',
          dynamic: true
        },
        {
          id: 'toggle_by_club', 
          label: 'Zaznacz klub',
          icon: '🏢',
          color: 'purple',
          condition: 'hasSelectedClub',
          dynamic: true
        },
        {
          id: 'toggle_without_qr',
          label: 'Zaznacz bez QR',
          icon: '📱',
          color: 'orange',
          condition: 'hasItemsWithoutQr'
        }
      ]
    }
  }))

  // DrabinkaPucharowa.vue - Tournament-specific configuration
  const drabinkaConfig = computed((): FilterConfig => ({
    layout: 'advanced',
    columns: 4,
    title: 'Filtry i sortowanie',
    theme: {
      focusColor: 'purple',
      borderStyle: 'thick',
      spacing: 'normal'
    },
    enabledFilters: {
      category: true,
      gender: true,
      sorting: true
    },
    customFilters: [
      {
        id: 'tournament_phase',
        type: 'select',
        icon: '🎯',
        label: 'Faza turnieju',
        options: [
          { value: '', label: 'Wszystkie fazy' },
          { value: 'ćwierćfinały', label: 'Ćwierćfinały' },
          { value: 'półfinały', label: 'Półfinały' },
          { value: 'finał', label: 'Finał' }
        ]
      }
    ],
    groupOperations: {
      enabled: true,
      operations: [
        {
          id: 'toggle_all_categories',
          label: 'Zaznacz wszystkie kategorie',
          icon: '🏆',
          color: 'indigo',
          condition: 'always'
        },
        {
          id: 'toggle_genders',
          label: 'Obie płcie',
          icon: '👥',
          color: 'green',
          condition: 'always'
        },
        {
          id: 'show_finals_only',
          label: 'Tylko finały',
          icon: '🏆',
          color: 'yellow',
          condition: 'always'
        }
      ]
    }
  }))

  // StartLineScanner.vue - Compact configuration
  const startLineScannerConfig = computed((): FilterConfig => ({
    layout: 'compact',
    title: 'Filtry grup',
    theme: {
      focusColor: 'green',
      borderStyle: 'thick',
      spacing: 'compact'
    },
    enabledFilters: {
      search: true,
      category: true
    },
    labels: {
      search: 'Szukaj grup',
      category: 'Kategoria'
    },
    placeholders: {
      search: 'Szukaj grup startowych...'
    }
  }))

  // Default sort options for different contexts
  const getDefaultSortOptions = (context: 'qr' | 'ranking' | 'zawodnicy' | 'drabinka' | 'groups'): FilterOption[] => {
    switch (context) {
      case 'qr':
        return [
          { value: 'nr_startowy_asc', label: 'Nr startowy (rosnąco)' },
          { value: 'nr_startowy_desc', label: 'Nr startowy (malejąco)' },
          { value: 'nazwisko_asc', label: 'Nazwisko (A-Z)' },
          { value: 'nazwisko_desc', label: 'Nazwisko (Z-A)' },
          { value: 'kategoria_asc', label: 'Kategoria (A-Z)' },
          { value: 'klub_asc', label: 'Klub (A-Z)' },
          { value: 'qr_status', label: 'Status QR (najpierw bez QR)' }
        ]
      
      case 'ranking':
        return [
          { value: 'punkty_desc', label: 'Punkty (malejąco)' },
          { value: 'punkty_asc', label: 'Punkty (rosnąco)' },
          { value: 'nazwisko_asc', label: 'Nazwisko (A-Z)' },
          { value: 'kategoria_asc', label: 'Kategoria (A-Z)' },
          { value: 'klub_asc', label: 'Klub (A-Z)' }
        ]
      
      case 'zawodnicy':
        return [
          { value: 'nr_startowy_asc', label: 'Nr startowy (rosnąco)' },
          { value: 'nr_startowy_desc', label: 'Nr startowy (malejąco)' },
          { value: 'nazwisko_asc', label: 'Nazwisko (A-Z)' },
          { value: 'nazwisko_desc', label: 'Nazwisko (Z-A)' },
          { value: 'czas_asc', label: 'Czas (najlepszy)' },
          { value: 'kategoria_asc', label: 'Kategoria (A-Z)' },
          { value: 'klub_asc', label: 'Klub (A-Z)' }
        ]
      
      case 'drabinka':
        return [
          { value: 'kategoria_asc', label: 'Kategoria (A-Z)' },
          { value: 'kategoria_desc', label: 'Kategoria (Z-A)' },
          { value: 'zawodnikow_desc', label: 'Liczba zawodników (malejąco)' },
          { value: 'zawodnikow_asc', label: 'Liczba zawodników (rosnąco)' }
        ]
      
      case 'groups':
        return [
          { value: 'numer_asc', label: 'Numer grupy (rosnąco)' },
          { value: 'numer_desc', label: 'Numer grupy (malejąco)' },
          { value: 'nazwa_asc', label: 'Nazwa (A-Z)' },
          { value: 'liczba_asc', label: 'Liczba zawodników (rosnąco)' },
          { value: 'liczba_desc', label: 'Liczba zawodników (malejąco)' }
        ]
      
      default:
        return [
          { value: 'name_asc', label: 'Nazwa (A-Z)' },
          { value: 'name_desc', label: 'Nazwa (Z-A)' }
        ]
    }
  }

  // Helper to create filter data with counts
  const createFilterData = (
    categories: string[] = [],
    clubs: string[] = [],
    sortContext: 'qr' | 'ranking' | 'zawodnicy' | 'drabinka' | 'groups' = 'zawodnicy',
    stats: Record<string, number> = {},
    customStats: Record<string, Record<string, number>> = {}
  ): FilterData => ({
    categories,
    clubs,
    sortOptions: getDefaultSortOptions(sortContext),
    stats,
    customStats
  })

  // Helper to generate stats from data arrays
  const generateStats = (data: any[], options: {
    categoryKey?: string
    clubKey?: string
    customKeys?: Record<string, string>
  } = {}): Record<string, number> => {
    const { categoryKey = 'kategoria', clubKey = 'klub', customKeys = {} } = options
    const stats: Record<string, number> = {}
    
    // Count by category
    if (categoryKey) {
      data.forEach(item => {
        const category = item[categoryKey]
        if (category) {
          const key = `category_${category}`
          stats[key] = (stats[key] || 0) + 1
        }
      })
    }
    
    // Count by club
    if (clubKey) {
      data.forEach(item => {
        const club = item[clubKey]
        if (club) {
          const key = `club_${club}`
          stats[key] = (stats[key] || 0) + 1
        }
      })
    }
    
    // Count by custom keys
    Object.entries(customKeys).forEach(([statKey, dataKey]) => {
      data.forEach(item => {
        const value = item[dataKey]
        if (value !== undefined && value !== null) {
          stats[statKey] = (stats[statKey] || 0) + 1
        }
      })
    })
    
    return stats
  }

  return {
    // Configurations
    qrPrintConfig,
    rankingConfig,
    zawodnicyConfig,
    drabinkaConfig,
    startLineScannerConfig,
    
    // Helpers
    getDefaultSortOptions,
    createFilterData,
    generateStats
  }
} 