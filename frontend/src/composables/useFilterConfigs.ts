import { computed } from 'vue'

// Types
interface FilterOption {
  label: string
  value: any
  count?: number
  icon?: string
}

interface MainFilter {
  key: string
  label: string
  icon: string
  type: 'select' | 'number'
  options?: FilterOption[] | string[]
  placeholder?: string
  min?: number
  max?: number
  showCount?: boolean
}

interface ChipFilter {
  key: string
  label: string
  options: FilterOption[] | string[]
  color: 'blue' | 'green' | 'indigo' | 'pink' | 'yellow' | 'red' | 'purple' | 'orange'
  showCount?: boolean
  showIcons?: boolean
}

interface QuickAction {
  key: string
  label: string
  icon: string
  className: string
  action: (filters: any, data: any) => void
  disabled?: (filters: any, data: any) => boolean
  count?: number | ((filters: any, data: any) => number)
  showCount?: boolean
}

interface FilterConfig {
  title?: string
  clearButtonText?: string
  mainFilters?: MainFilter[]
  chipFilters?: ChipFilter[]
  quickActions?: {
    title?: string
    buttons: QuickAction[]
  }
}

export function useFilterConfigs() {
  
  // ===== KONFIGURACJA DLA ZAWODNIKÓW =====
  const zawodnicyConfig = (categories: string[], clubs: string[]) => ({
    title: 'Filtry i sortowanie',
    clearButtonText: 'Wyczyść wszystko',
    chipFilters: [
      {
        key: 'kluby',
        label: 'Kluby',
        options: clubs,
        color: 'blue' as const,
        showCount: true
      },
      {
        key: 'kategorie', 
        label: 'Kategorie',
        options: categories,
        color: 'green' as const,
        showCount: true
      },
      {
        key: 'plcie',
        label: 'Płeć',
        options: [
          { label: '👨 Mężczyźni', value: 'M', icon: '👨' },
          { label: '👩 Kobiety', value: 'K', icon: '👩' }
        ],
        color: 'indigo' as const,
        showIcons: true
      },
      {
        key: 'statusy',
        label: 'Status',
        options: [
          { label: '✅ Ukończone', value: 'FINISHED', icon: '✅' },
          { label: '⚠️ DNF', value: 'DNF', icon: '⚠️' },
          { label: '❌ DSQ', value: 'DSQ', icon: '❌' }
        ],
        color: 'yellow' as const,
        showIcons: true
      }
    ],
    quickActions: {
      title: 'Szybkie akcje',
      buttons: [
        {
          key: 'all_clubs',
          label: 'Wszystkie kluby',
          icon: '🏢',
          className: 'bg-blue-500 text-white',
          action: (filters: any) => {
            filters.kluby = clubs
          }
        },
        {
          key: 'all_categories',
          label: 'Wszystkie kategorie',
          icon: '🏆',
          className: 'bg-green-500 text-white', 
          action: (filters: any) => {
            filters.kategorie = categories
          }
        },
        {
          key: 'finished_only',
          label: 'Tylko ukończone',
          icon: '✅',
          className: 'bg-emerald-500 text-white',
          action: (filters: any) => {
            filters.statusy = ['FINISHED']
          }
        }
      ]
    }
  })

  // ===== KONFIGURACJA DLA RANKINGÓW =====
  const rankingConfig = (categories: string[], clubs: string[], type: string) => ({
    title: 'Filtry i sortowanie',
    clearButtonText: 'Wyczyść filtry',
    mainFilters: [
      {
        key: 'kategoria',
        label: 'Kategoria', 
        icon: '🏆',
        type: 'select' as const,
        options: categories,
        placeholder: 'Wszystkie'
      },
      {
        key: 'klub',
        label: 'Klub',
        icon: '🏢', 
        type: 'select' as const,
        options: clubs,
        placeholder: 'Wszystkie'
      },
      {
        key: 'plec',
        label: 'Płeć',
        icon: '👥',
        type: 'select' as const,
        options: [
          { label: 'Mężczyźni', value: 'M' },
          { label: 'Kobiety', value: 'K' }
        ],
        placeholder: 'Wszystkie'
      },
      {
        key: 'sortowanie',
        label: 'Sortowanie',
        icon: '🔄',
        type: 'select' as const,
        options: getSortingOptions(type),
        placeholder: 'Pozycja (najlepsi)'
      }
    ]
  })

  // ===== KONFIGURACJA DLA DRABINKI =====
  const drabinkaConfig = () => ({
    title: 'Filtry i sortowanie',
    clearButtonText: 'Wyczyść filtry',
    mainFilters: [
      {
        key: 'kategoria',
        label: 'Kategoria',
        icon: '🏆',
        type: 'select',
        options: [], // Będzie wypełnione dynamicznie
        placeholder: 'Wybierz kategorię',
        showCount: true
      },
      {
        key: 'sortBy',
        label: 'Sortuj według',
        icon: '↕️',
        type: 'select',
        options: [
          { label: 'Kategoria', value: 'kategoria' },
          { label: 'Liczba zawodników', value: 'liczbaZawodnikow' }
        ],
        placeholder: 'Wybierz sortowanie'
      }
    ],
    chipFilters: [
      {
        key: 'plcie',
        label: 'Płeć',
        options: [
          { label: 'Mężczyźni', value: 'M', icon: '👨' },
          { label: 'Kobiety', value: 'K', icon: '👩' }
        ],
        color: 'purple',
        showIcons: true
      }
    ],
    quickActions: {
      title: 'Szybkie akcje',
      buttons: [
        {
          key: 'clearKategoria',
          label: 'Wyczyść kategorię',
          icon: '🗑️',
          className: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
          action: (filters: any) => {
            filters.kategoria = ''
          },
          disabled: (filters: any) => !filters.kategoria
        },
        {
          key: 'clearPlcie',
          label: 'Wyczyść płeć',
          icon: '🗑️',
          className: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
          action: (filters: any) => {
            filters.plcie = []
          },
          disabled: (filters: any) => !filters.plcie?.length
        }
      ]
    }
  })

  // ===== KONFIGURACJA DLA DRUKOWANIA QR =====
  const qrPrintConfig = (categories: string[], clubs: string[]) => ({
    title: 'Filtry i sortowanie',
    clearButtonText: 'Wyczyść wszystko',
    mainFilters: [
      {
        key: 'kategoria',
        label: 'Kategoria',
        icon: '🏆',
        type: 'select' as const,
        options: categories,
        placeholder: 'Wszystkie',
        showCount: true
      },
      {
        key: 'klub',
        label: 'Klub',
        icon: '🏢',
        type: 'select' as const,
        options: clubs,
        placeholder: 'Wszystkie',
        showCount: true
      },
      {
        key: 'qrStatus',
        label: 'Status QR',
        icon: '📱',
        type: 'select' as const,
        options: [
          { label: '✅ Z QR kodami', value: 'with_qr' },
          { label: '❌ Bez QR kodów', value: 'without_qr' }
        ],
        placeholder: 'Wszystkie'
      },
      {
        key: 'sortowanie',
        label: 'Sortowanie',
        icon: '🔄',
        type: 'select' as const,
        options: [
          { label: 'Nr startowy (rosnąco)', value: 'nr_startowy_asc' },
          { label: 'Nr startowy (malejąco)', value: 'nr_startowy_desc' },
          { label: 'Nazwisko (A-Z)', value: 'nazwisko_asc' },
          { label: 'Nazwisko (Z-A)', value: 'nazwisko_desc' },
          { label: 'Kategoria (A-Z)', value: 'kategoria_asc' },
          { label: 'Klub (A-Z)', value: 'klub_asc' },
          { label: 'Status QR (najpierw bez QR)', value: 'qr_status' }
        ]
      }
    ],
    quickActions: {
      title: 'Operacje grupowe',
      buttons: [
        {
          key: 'select_all',
          label: 'Zaznacz wszystkie',
          icon: '☐',
          className: 'bg-indigo-600 text-white',
          action: (filters: any, data: any) => {
            // Logic handled by parent component
          },
          count: (filters: any, data: any) => data?.filteredCount || 0,
          showCount: true
        },
        {
          key: 'select_category',
          label: 'Zaznacz kategorię',
          icon: '🏆',
          className: 'bg-green-600 text-white',
          action: (filters: any, data: any) => {
            // Logic handled by parent component  
          },
          disabled: (filters: any) => !filters.kategoria
        },
        {
          key: 'select_club',
          label: 'Zaznacz klub',
          icon: '🏢',
          className: 'bg-purple-600 text-white',
          action: (filters: any, data: any) => {
            // Logic handled by parent component
          },
          disabled: (filters: any) => !filters.klub
        },
        {
          key: 'select_without_qr',
          label: 'Zaznacz bez QR',
          icon: '📱',
          className: 'bg-orange-600 text-white',
          action: (filters: any, data: any) => {
            // Logic handled by parent component
          },
          count: (filters: any, data: any) => data?.withoutQrCount || 0,
          showCount: true
        }
      ]
    }
  })

  // ===== HELPER FUNCTIONS =====
  function getSortingOptions(type: string) {
    const commonOptions = [
      { label: 'Punkty (malejąco)', value: 'punkty_desc' },
      { label: 'Punkty (rosnąco)', value: 'punkty_asc' },
      { label: 'Nazwisko (A-Z)', value: 'nazwisko_asc' },
      { label: 'Nazwisko (Z-A)', value: 'nazwisko_desc' },
      { label: 'Kategoria (A-Z)', value: 'kategoria_asc' }
    ]

    switch(type) {
      case 'individual':
        return [
          { label: 'Pozycja (najlepsi)', value: 'pozycja_asc' },
          { label: 'Pozycja (najgorsi)', value: 'pozycja_desc' },
          ...commonOptions,
          { label: 'Klub (A-Z)', value: 'klub_asc' },
          { label: 'Starty (malejąco)', value: 'starty_desc' }
        ]
      
      case 'general':
        return [
          ...commonOptions,
          { label: 'Starty (malejąco)', value: 'starty_desc' },
          { label: 'Odrzucone (malejąco)', value: 'odrzucone_desc' }
        ]
      
      case 'clubsTotal':
        return [
          ...commonOptions.slice(0, 2), // tylko punkty
          { label: 'Średnia (malejąco)', value: 'srednia_desc' },
          { label: 'Średnia (rosnąco)', value: 'srednia_asc' },
          { label: 'Zawodnicy (malejąco)', value: 'zawodnicy_desc' },
          { label: 'Zawodnicy (rosnąco)', value: 'zawodnicy_asc' },
          { label: 'Nazwa (A-Z)', value: 'nazwa_asc' },
          { label: 'Nazwa (Z-A)', value: 'nazwa_desc' }
        ]
      
      case 'clubsTop3':
        return [
          { label: 'Punkty Top 3 (malejąco)', value: 'punkty_desc' },
          { label: 'Punkty Top 3 (rosnąco)', value: 'punkty_asc' },
          { label: 'Kategorie (malejąco)', value: 'kategorie_desc' },
          { label: 'Kategorie (rosnąco)', value: 'kategorie_asc' },
          { label: 'Równowaga (malejąco)', value: 'balance_desc' },
          { label: 'Równowaga (rosnąco)', value: 'balance_asc' },
          { label: 'Nazwa (A-Z)', value: 'nazwa_asc' },
          { label: 'Nazwa (Z-A)', value: 'nazwa_desc' }
        ]
      
      case 'medals':
        return [
          { label: 'Złote (malejąco)', value: 'zlote_desc' },
          { label: 'Srebrne (malejąco)', value: 'srebrne_desc' },
          { label: 'Brązowe (malejąco)', value: 'brazowe_desc' },
          { label: 'Łącznie (malejąco)', value: 'lacznie_desc' },
          { label: 'Nazwa (A-Z)', value: 'nazwa_asc' },
          { label: 'Nazwa (Z-A)', value: 'nazwa_desc' }
        ]
      
      default:
        return commonOptions
    }
  }

  return {
    zawodnicyConfig,
    rankingConfig,
    drabinkaConfig,
    qrPrintConfig
  }
} 