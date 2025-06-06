<template>
  <div 
    :class="[
      'bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 transition-colors duration-200',
      spacingClass
    ]"
  >
    <!-- Header Section -->
    <div class="flex items-center justify-between mb-6">
      <h3 class="text-lg sm:text-xl font-semibold text-gray-900 dark:text-white">
        📝 {{ config.title || 'Filtry i sortowanie' }}
      </h3>
      <button 
        v-if="config.showClearButton !== false"
        @click="clearAllFilters" 
        :disabled="!hasActiveFilters"
        :class="[
          'text-sm font-medium flex items-center space-x-1 transition-colors duration-200 px-3 py-1 rounded-md',
          hasActiveFilters 
            ? 'text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300 hover:bg-red-50 dark:hover:bg-red-900/20'
            : 'text-gray-400 dark:text-gray-600 cursor-not-allowed'
        ]"
      >
        <span>🗑️</span>
        <span>Wyczyść filtry</span>
      </button>
    </div>

    <!-- Level 1: Main Filters -->
    <div v-if="config.enabledFilters && hasMainFilters" class="mb-6">
      <div :class="mainFiltersGridClass">
        <!-- Search Filter -->
        <div v-if="config.enabledFilters.search">
          <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
            <span class="flex items-center space-x-2">
              <span>🔍</span>
              <span>{{ config.labels?.search || 'Szukaj' }}</span>
            </span>
          </label>
          <input
            v-model="internalFilters.search"
            type="text"
            :placeholder="config.placeholders?.search || 'Szukaj...'"
            :class="inputClass"
          />
        </div>

        <!-- Category Filter -->
        <div v-if="config.enabledFilters.category">
          <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
            <span class="flex items-center space-x-2">
              <span>🏆</span>
              <span>{{ config.labels?.category || 'Kategoria' }}</span>
            </span>
          </label>
          <select v-model="internalFilters.category" :class="selectClass">
            <option value="">Wszystkie</option>
            <option 
              v-for="category in processedCategories" 
              :key="category.value" 
              :value="category.value"
            >
              {{ category.label }}{{ category.count ? ` (${category.count})` : '' }}
            </option>
          </select>
        </div>

        <!-- Club Filter -->
        <div v-if="config.enabledFilters.club">
          <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
            <span class="flex items-center space-x-2">
              <span>🏢</span>
              <span>{{ config.labels?.club || 'Klub' }}</span>
            </span>
          </label>
          <select v-model="internalFilters.club" :class="selectClass">
            <option value="">Wszystkie</option>
            <option 
              v-for="club in processedClubs" 
              :key="club.value" 
              :value="club.value"
            >
              {{ club.label }}{{ club.count ? ` (${club.count})` : '' }}
            </option>
          </select>
        </div>

        <!-- Gender Filter -->
        <div v-if="config.enabledFilters.gender">
          <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
            <span class="flex items-center space-x-2">
              <span>👥</span>
              <span>{{ config.labels?.gender || 'Płeć' }}</span>
            </span>
          </label>
          <select v-model="internalFilters.gender" :class="selectClass">
            <option value="">Wszystkie</option>
            <option value="M">Mężczyźni</option>
            <option value="K">Kobiety</option>
          </select>
        </div>

        <!-- Custom Filters -->
        <div 
          v-for="customFilter in config.customFilters" 
          :key="customFilter.id"
        >
          <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
            <span class="flex items-center space-x-2">
              <span>{{ customFilter.icon }}</span>
              <span>{{ customFilter.label }}</span>
            </span>
          </label>
          <select v-model="internalFilters[customFilter.id]" :class="selectClass">
            <option 
              v-for="option in customFilter.options" 
              :key="option.value" 
              :value="option.value"
            >
              {{ option.label }}{{ getCustomFilterCount(customFilter, option) }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <!-- Level 2: Sorting -->
    <div v-if="config.enabledFilters?.sorting" class="mb-6">
      <div :class="sortingGridClass">
        <div>
          <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
            <span class="flex items-center space-x-2">
              <span>🔄</span>
              <span>{{ config.labels?.sorting || 'Sortowanie' }}</span>
            </span>
          </label>
          <select v-model="internalFilters.sorting" :class="selectClass">
            <option 
              v-for="sortOption in processedSortOptions" 
              :key="sortOption.value" 
              :value="sortOption.value"
            >
              {{ sortOption.label }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <!-- Level 3: Group Operations -->
    <div 
      v-if="config.groupOperations?.enabled && config.groupOperations?.operations?.length" 
      class="border-t border-gray-200 dark:border-gray-700 pt-6"
    >
      <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-4">
        <span class="flex items-center space-x-2">
          <span>⚡</span>
          <span>Operacje grupowe</span>
        </span>
      </label>
      <div class="flex flex-wrap gap-3">
        <button 
          v-for="operation in visibleOperations" 
          :key="operation.id"
          @click="handleGroupOperation(operation)"
          :disabled="!isOperationEnabled(operation)"
          :class="getOperationButtonClass(operation)"
        >
          <span>{{ getOperationIcon(operation) }}</span>
          <span>{{ getOperationLabel(operation) }}</span>
        </button>
      </div>
    </div>

    <!-- Debug Info (Development only) -->
    <div v-if="config.debug" class="mt-6 p-4 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg border border-yellow-200 dark:border-yellow-800">
      <details>
        <summary class="text-sm font-medium text-yellow-800 dark:text-yellow-200 cursor-pointer">
          🐛 Debug Info
        </summary>
        <pre class="mt-2 text-xs text-yellow-700 dark:text-yellow-300 whitespace-pre-wrap">{{ debugInfo }}</pre>
      </details>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, watch } from 'vue'

// Types
interface FilterOption {
  value: string
  label: string
  count?: number
  countKey?: string
}

interface CustomFilter {
  id: string
  type: 'select' | 'text'
  icon: string
  label: string
  options: FilterOption[]
  showCounts?: boolean
}

interface GroupOperation {
  id: string
  label: string
  icon: string
  color: 'indigo' | 'green' | 'purple' | 'orange' | 'red' | 'yellow'
  condition: 'always' | 'hasActiveFilters' | 'hasSelectedCategory' | 'hasSelectedClub' | 'hasItemsWithoutQr' | string
  dynamic?: boolean
}

interface FilterConfig {
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

interface FilterData {
  categories?: string[]
  clubs?: string[]
  sortOptions?: FilterOption[]
  stats?: Record<string, number>
  customStats?: Record<string, Record<string, number>>
}

interface FilterState {
  search: string
  category: string
  club: string
  gender: string
  sorting: string
  [key: string]: any
}

// Props
const props = defineProps<{
  config: FilterConfig
  data: FilterData
  modelValue?: FilterState
}>()

// Emits
const emit = defineEmits<{
  'update:modelValue': [value: FilterState]
  'filtersChange': [filters: FilterState]
  'groupOperation': [operation: string, data?: any]
  'clearFilters': []
}>()

// Internal state
const internalFilters = reactive<FilterState>({
  search: '',
  category: '',
  club: '',
  gender: '',
  sorting: props.data.sortOptions?.[0]?.value || '',
  ...(props.modelValue || {})
})

// Initialize custom filters
if (props.config.customFilters) {
  props.config.customFilters.forEach(filter => {
    if (!(filter.id in internalFilters)) {
      internalFilters[filter.id] = ''
    }
  })
}

// Computed properties
const spacingClass = computed(() => {
  const spacing = props.config.theme?.spacing || 'normal'
  return {
    'compact': 'p-3',
    'normal': 'p-4 sm:p-6', 
    'relaxed': 'p-6 sm:p-8'
  }[spacing]
})

const focusColorClass = computed(() => {
  const color = props.config.theme?.focusColor || 'purple'
  return {
    'purple': 'focus:border-purple-500 focus:ring-purple-500',
    'indigo': 'focus:border-indigo-500 focus:ring-indigo-500',
    'blue': 'focus:border-blue-500 focus:ring-blue-500',
    'green': 'focus:border-green-500 focus:ring-green-500'
  }[color]
})

const borderStyleClass = computed(() => {
  const style = props.config.theme?.borderStyle || 'thick'
  return {
    'normal': 'border',
    'thick': 'border-2',
    'minimal': 'border-0 shadow-md'
  }[style]
})

const baseInputClass = computed(() => {
  return `w-full rounded-lg ${borderStyleClass.value} border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-md ${focusColorClass.value} focus:ring-2 text-sm font-medium py-2.5 px-3 transition-all duration-200 hover:shadow-lg`
})

const inputClass = computed(() => baseInputClass.value)
const selectClass = computed(() => baseInputClass.value)

const mainFiltersGridClass = computed(() => {
  const columns = props.config.columns || 'auto'
  if (columns === 'auto') {
    // Auto-determine based on enabled filters count
    const enabledCount = Object.values(props.config.enabledFilters || {}).filter(Boolean).length + 
                         (props.config.customFilters?.length || 0)
    
    if (enabledCount <= 2) return 'grid grid-cols-1 md:grid-cols-2 gap-4'
    if (enabledCount <= 3) return 'grid grid-cols-1 md:grid-cols-3 gap-4'
    return 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4'
  }
  
  return `grid grid-cols-1 md:grid-cols-${Math.min(columns, 2)} lg:grid-cols-${Math.min(columns, 3)} xl:grid-cols-${columns} gap-4`
})

const sortingGridClass = computed(() => 'grid grid-cols-1 md:grid-cols-2 gap-4')

const hasMainFilters = computed(() => {
  return Object.values(props.config.enabledFilters || {}).some(Boolean) || 
         (props.config.customFilters?.length || 0) > 0
})

const hasActiveFilters = computed(() => {
  return Object.entries(internalFilters).some(([key, value]) => {
    if (key === 'sorting') return false // Sorting is not considered "active filter"
    return value !== '' && value !== null && value !== undefined
  })
})

const processedCategories = computed(() => {
  if (!props.data.categories) return []
  
  return props.data.categories.map(category => ({
    value: category,
    label: category,
    count: props.data.stats?.[`category_${category}`]
  }))
})

const processedClubs = computed(() => {
  if (!props.data.clubs) return []
  
  return props.data.clubs.map(club => ({
    value: club,
    label: club,
    count: props.data.stats?.[`club_${club}`]
  }))
})

const processedSortOptions = computed(() => {
  return props.data.sortOptions || [
    { value: 'name_asc', label: 'Nazwa (A-Z)' },
    { value: 'name_desc', label: 'Nazwa (Z-A)' },
    { value: 'number_asc', label: 'Numer (rosnąco)' },
    { value: 'number_desc', label: 'Numer (malejąco)' }
  ]
})

const visibleOperations = computed(() => {
  return props.config.groupOperations?.operations.filter(op => isOperationVisible(op)) || []
})

const debugInfo = computed(() => {
  return {
    filters: internalFilters,
    hasActiveFilters: hasActiveFilters.value,
    config: props.config,
    data: props.data
  }
})

// Methods
const getCustomFilterCount = (filter: CustomFilter, option: FilterOption): string => {
  if (!filter.showCounts || !option.countKey) return ''
  const count = props.data.customStats?.[filter.id]?.[option.countKey] || props.data.stats?.[option.countKey]
  return count !== undefined ? ` (${count})` : ''
}

const isOperationVisible = (operation: GroupOperation): boolean => {
  switch (operation.condition) {
    case 'always':
      return true
    case 'hasActiveFilters':
      return hasActiveFilters.value
    case 'hasSelectedCategory':
      return !!internalFilters.category
    case 'hasSelectedClub':
      return !!internalFilters.club
    case 'hasItemsWithoutQr':
      return (props.data.stats?.withoutQr || 0) > 0
    default:
      return true
  }
}

const isOperationEnabled = (operation: GroupOperation): boolean => {
  // Additional logic for disabled states
  if (operation.condition === 'hasSelectedCategory' && !internalFilters.category) return false
  if (operation.condition === 'hasSelectedClub' && !internalFilters.club) return false
  return true
}

const getOperationIcon = (operation: GroupOperation): string => {
  if (operation.dynamic) {
    // Dynamic icons based on state
    switch (operation.id) {
      case 'toggle_all':
        return hasActiveFilters.value ? '✅' : '☐'
      case 'toggle_by_category':
        return internalFilters.category ? '✅' : '☐'
      case 'toggle_by_club':
        return internalFilters.club ? '✅' : '☐'
      default:
        return operation.icon
    }
  }
  return operation.icon
}

const getOperationLabel = (operation: GroupOperation): string => {
  if (operation.dynamic) {
    switch (operation.id) {
      case 'toggle_by_category':
        return internalFilters.category 
          ? `Odznacz: ${internalFilters.category}`
          : 'Wybierz kategorię'
      case 'toggle_by_club':
        return internalFilters.club
          ? `Odznacz: ${internalFilters.club}`
          : 'Wybierz klub'
      default:
        return operation.label
    }
  }
  return operation.label
}

const getOperationButtonClass = (operation: GroupOperation): string => {
  const baseClass = 'px-4 py-2 text-sm font-medium rounded-lg transition-all duration-200 flex items-center space-x-2 border-2'
  
  const colorClasses = {
    indigo: 'bg-indigo-600 border-transparent text-white hover:bg-indigo-700',
    green: 'bg-green-600 border-transparent text-white hover:bg-green-700',
    purple: 'bg-purple-600 border-transparent text-white hover:bg-purple-700',
    orange: 'bg-orange-600 border-transparent text-white hover:bg-orange-700',
    red: 'bg-red-600 border-transparent text-white hover:bg-red-700',
    yellow: 'bg-yellow-600 border-transparent text-white hover:bg-yellow-700'
  }
  
  const disabledClass = 'bg-gray-300 dark:bg-gray-600 text-gray-500 dark:text-gray-400 cursor-not-allowed border-transparent'
  
  if (!isOperationEnabled(operation)) {
    return `${baseClass} ${disabledClass}`
  }
  
  return `${baseClass} ${colorClasses[operation.color]}`
}

const handleGroupOperation = (operation: GroupOperation) => {
  if (!isOperationEnabled(operation)) return
  
  emit('groupOperation', operation.id, {
    operation,
    currentFilters: { ...internalFilters }
  })
}

const clearAllFilters = () => {
  Object.keys(internalFilters).forEach(key => {
    if (key === 'sorting') {
      internalFilters[key] = props.data.sortOptions?.[0]?.value || ''
    } else {
      internalFilters[key] = ''
    }
  })
  
  emit('clearFilters')
}

// Watchers
watch(
  () => internalFilters,
  (newFilters) => {
    emit('update:modelValue', { ...newFilters })
    emit('filtersChange', { ...newFilters })
  },
  { deep: true }
)

watch(
  () => props.modelValue,
  (newValue) => {
    if (newValue) {
      Object.assign(internalFilters, newValue)
    }
  },
  { deep: true }
)
</script> 