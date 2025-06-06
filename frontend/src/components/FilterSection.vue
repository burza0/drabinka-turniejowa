<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-6 transition-colors duration-200">
    <!-- Nagłówek sekcji -->
    <div class="flex items-center justify-between mb-6">
      <h3 class="text-lg sm:text-xl font-semibold text-gray-900 dark:text-white">{{ config.title }}</h3>
      <button 
        @click="$emit('clearFilters')" 
        class="text-sm text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300 flex items-center space-x-1 transition-colors duration-200"
      >
        <span>🗑️</span>
        <span>{{ config.clearButtonText }}</span>
      </button>
    </div>

    <!-- Filtry główne (select, number) -->
    <div v-if="config.mainFilters?.length" class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
      <div v-for="filter in config.mainFilters" :key="filter.key">
        <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
          <span class="flex items-center space-x-2">
            <span>{{ filter.icon }}</span>
            <span>{{ filter.label }}</span>
          </span>
        </label>
        
        <!-- Select -->
        <select 
          v-if="filter.type === 'select'"
          v-model="localFilters[filter.key]"
          @change="emitFiltersChange"
          class="w-full rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-md focus:border-purple-500 focus:ring-2 focus:ring-purple-500 text-sm font-medium py-2.5 px-3 transition-all duration-200 hover:shadow-lg"
        >
          <option value="">{{ filter.placeholder }}</option>
          <option 
            v-for="option in filter.options" 
            :key="typeof option === 'string' ? option : option.value"
            :value="typeof option === 'string' ? option : option.value"
          >
            {{ typeof option === 'string' ? option : option.label }}
          </option>
        </select>

        <!-- Number input -->
        <input 
          v-else-if="filter.type === 'number'"
          v-model.number="localFilters[filter.key]"
          @input="emitFiltersChange"
          type="number"
          :min="filter.min"
          :max="filter.max"
          :placeholder="filter.placeholder"
          class="w-full rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-md focus:border-purple-500 focus:ring-2 focus:ring-purple-500 text-sm font-medium py-2.5 px-3 transition-all duration-200 hover:shadow-lg"
        />
      </div>
    </div>

    <!-- Filtry chip (przyciski) -->
    <div v-if="config.chipFilters?.length" class="space-y-4 mb-6">
      <div v-for="filter in config.chipFilters" :key="filter.key" class="space-y-2">
        <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200">
          {{ filter.label }}
        </label>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="option in filter.options"
            :key="typeof option === 'string' ? option : option.value"
            @click="toggleChipFilter(filter.key, typeof option === 'string' ? option : option.value)"
            :class="[
              'px-3 py-1.5 rounded-full text-sm font-medium transition-colors duration-200',
              isChipSelected(filter.key, typeof option === 'string' ? option : option.value)
                ? getChipColor(filter.color, true)
                : getChipColor(filter.color, false)
            ]"
          >
            <span v-if="filter.showIcons && typeof option !== 'string' && option.icon" class="mr-1">
              {{ option.icon }}
            </span>
            {{ typeof option === 'string' ? option : option.label }}
            <span v-if="filter.showCount" class="ml-1 text-xs opacity-75">
              ({{ getOptionCount(filter.key, typeof option === 'string' ? option : option.value) }})
            </span>
          </button>
        </div>
      </div>
    </div>

    <!-- Szybkie akcje -->
    <div v-if="config.quickActions?.buttons?.length" class="space-y-2">
      <h4 class="text-sm font-semibold text-gray-800 dark:text-gray-200">
        {{ config.quickActions.title }}
      </h4>
      <div class="flex flex-wrap gap-2">
        <button
          v-for="action in config.quickActions.buttons"
          :key="action.key"
          @click="handleQuickAction(action)"
          :disabled="action.disabled?.(localFilters, data)"
          :class="[
            'px-3 py-1.5 rounded-lg text-sm font-medium transition-colors duration-200 flex items-center space-x-1',
            action.className,
            action.disabled?.(localFilters, data) ? 'opacity-50 cursor-not-allowed' : ''
          ]"
        >
          <span>{{ action.icon }}</span>
          <span>{{ action.label }}</span>
          <span v-if="action.showCount" class="ml-1 text-xs opacity-75">
            ({{ typeof action.count === 'function' ? action.count(localFilters, data) : action.count }})
          </span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'

// Props
const props = defineProps<{
  config: {
    title?: string
    clearButtonText?: string
    mainFilters?: Array<{
      key: string
      label: string
      icon: string
      type: 'select' | 'number'
      options?: Array<{ label: string; value: any }> | string[]
      placeholder?: string
      min?: number
      max?: number
      showCount?: boolean
    }>
    chipFilters?: Array<{
      key: string
      label: string
      options: Array<{ label: string; value: any; icon?: string }> | string[]
      color: 'blue' | 'green' | 'indigo' | 'pink' | 'yellow' | 'red' | 'purple' | 'orange'
      showCount?: boolean
      showIcons?: boolean
    }>
    quickActions?: {
      title?: string
      buttons: Array<{
        key: string
        label: string
        icon: string
        className: string
        action: (filters: any, data: any) => void
        disabled?: (filters: any, data: any) => boolean
        count?: number | ((filters: any, data: any) => number)
        showCount?: boolean
      }>
    }
  }
  filters: Record<string, any>
  data?: Record<string, any>
}>()

// Emits
const emit = defineEmits<{
  (e: 'filtersChange', filters: Record<string, any>): void
  (e: 'clearFilters'): void
  (e: 'quickAction', key: string, data?: any): void
}>()

// Local state
const localFilters = ref<Record<string, any>>({ ...props.filters })

// Watch for external changes
watch(() => props.filters, (newFilters) => {
  localFilters.value = { ...newFilters }
}, { deep: true })

// Methods
const emitFiltersChange = () => {
  emit('filtersChange', { ...localFilters.value })
}

const toggleChipFilter = (key: string, value: any) => {
  if (!localFilters.value[key]) {
    localFilters.value[key] = []
  }
  
  const index = localFilters.value[key].indexOf(value)
  if (index > -1) {
    localFilters.value[key].splice(index, 1)
  } else {
    localFilters.value[key].push(value)
  }
  
  emitFiltersChange()
}

const isChipSelected = (key: string, value: any): boolean => {
  return localFilters.value[key]?.includes(value) || false
}

const getOptionCount = (key: string, value: any): number => {
  // TODO: Implement count logic based on data
  return 0
}

const handleQuickAction = (action: any) => {
  if (action.disabled?.(localFilters.value, props.data)) return
  
  action.action(localFilters.value, props.data)
  emitFiltersChange()
  emit('quickAction', action.key, props.data)
}

const getChipColor = (color: string, selected: boolean): string => {
  const colors = {
    blue: selected ? 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200' : 'bg-blue-50 text-blue-600 dark:bg-blue-800/50 dark:text-blue-300',
    green: selected ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200' : 'bg-green-50 text-green-600 dark:bg-green-800/50 dark:text-green-300',
    indigo: selected ? 'bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-200' : 'bg-indigo-50 text-indigo-600 dark:bg-indigo-800/50 dark:text-indigo-300',
    pink: selected ? 'bg-pink-100 text-pink-800 dark:bg-pink-900 dark:text-pink-200' : 'bg-pink-50 text-pink-600 dark:bg-pink-800/50 dark:text-pink-300',
    yellow: selected ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200' : 'bg-yellow-50 text-yellow-600 dark:bg-yellow-800/50 dark:text-yellow-300',
    red: selected ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200' : 'bg-red-50 text-red-600 dark:bg-red-800/50 dark:text-red-300',
    purple: selected ? 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200' : 'bg-purple-50 text-purple-600 dark:bg-purple-800/50 dark:text-purple-300',
    orange: selected ? 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200' : 'bg-orange-50 text-orange-600 dark:bg-orange-800/50 dark:text-orange-300'
  }
  return colors[color as keyof typeof colors] || colors.blue
}
</script> 