<template>
  <div class="group relative overflow-hidden rounded-2xl bg-white dark:bg-gray-800 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105">
    <!-- Background Gradient -->
    <div :class="[
      'absolute inset-0 opacity-5 group-hover:opacity-10 transition-opacity duration-300',
      gradientClass
    ]"></div>
    
    <!-- Main Content -->
    <div class="relative p-6">
      <!-- Header -->
      <div class="flex items-center justify-between mb-4">
        <div :class="['p-3 rounded-xl shadow-lg', iconBgClass]">
          <component 
            v-if="typeof icon !== 'string'" 
            :is="icon" 
            :class="iconClass"
            class="h-6 w-6" 
          />
          <span 
            v-else 
            :class="iconClass"
            class="text-xl font-semibold"
          >
            {{ icon }}
          </span>
        </div>
        
        <!-- Trend Indicator -->
        <div v-if="trend" class="flex items-center space-x-1">
          <svg v-if="trend === 'up'" class="w-4 h-4 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 17l9.2-9.2M17 17V7h-10" />
          </svg>
          <svg v-else-if="trend === 'down'" class="w-4 h-4 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 7l-9.2 9.2M7 7v10h10" />
          </svg>
          <svg v-else class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h8" />
          </svg>
          <span v-if="trendValue" :class="trendTextClass" class="text-sm font-medium">
            {{ trendValue }}
          </span>
        </div>
      </div>

      <!-- Title -->
      <h3 class="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">{{ title }}</h3>
      
      <!-- Value -->
      <div class="flex items-baseline justify-between">
        <span class="text-3xl font-bold text-gray-900 dark:text-white">{{ displayValue }}</span>
        <span v-if="unit" class="text-sm text-gray-500 dark:text-gray-400 ml-2">{{ unit }}</span>
      </div>
      
      <!-- Subtitle/Description -->
      <p v-if="subtitle" class="text-xs text-gray-500 dark:text-gray-400 mt-2">{{ subtitle }}</p>
      
      <!-- Progress Bar -->
      <div v-if="progress !== undefined" class="mt-4">
        <div class="flex justify-between text-xs text-gray-600 dark:text-gray-400 mb-1">
          <span>Progress</span>
          <span>{{ Math.round(progress) }}%</span>
        </div>
        <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
          <div 
            :class="progressBarClass"
            class="h-2 rounded-full transition-all duration-500 ease-out"
            :style="`width: ${Math.min(progress, 100)}%`"
          ></div>
        </div>
      </div>
    </div>
    
    <!-- Action Button -->
    <div v-if="actionLabel" class="px-6 pb-6">
      <button 
        @click="$emit('action')"
        :class="[
          'w-full py-2 px-4 rounded-lg text-sm font-medium transition-all duration-200',
          actionButtonClass
        ]"
      >
        {{ actionLabel }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  title: string
  value: string | number
  icon: any
  color: 'blue' | 'green' | 'red' | 'purple' | 'yellow' | 'indigo' | 'pink' | 'cyan'
  subtitle?: string
  unit?: string
  trend?: 'up' | 'down' | 'neutral'
  trendValue?: string
  progress?: number
  actionLabel?: string
}

const props = defineProps<Props>()
const emit = defineEmits(['action'])

const displayValue = computed(() => {
  if (typeof props.value === 'number') {
    return props.value.toLocaleString()
  }
  return props.value
})

const gradientClass = computed(() => {
  const gradients = {
    blue: 'bg-gradient-to-br from-blue-500 to-blue-600',
    green: 'bg-gradient-to-br from-green-500 to-green-600',
    red: 'bg-gradient-to-br from-red-500 to-red-600',
    purple: 'bg-gradient-to-br from-purple-500 to-purple-600',
    yellow: 'bg-gradient-to-br from-yellow-500 to-yellow-600',
    indigo: 'bg-gradient-to-br from-indigo-500 to-indigo-600',
    pink: 'bg-gradient-to-br from-pink-500 to-pink-600',
    cyan: 'bg-gradient-to-br from-cyan-500 to-cyan-600'
  }
  return gradients[props.color]
})

const iconClass = computed(() => {
  const colors = {
    blue: 'text-blue-600',
    green: 'text-green-600',
    red: 'text-red-600',
    purple: 'text-purple-600',
    yellow: 'text-yellow-600',
    indigo: 'text-indigo-600',
    pink: 'text-pink-600',
    cyan: 'text-cyan-600'
  }
  return colors[props.color]
})

const iconBgClass = computed(() => {
  const backgrounds = {
    blue: 'bg-blue-100 dark:bg-blue-900',
    green: 'bg-green-100 dark:bg-green-900',
    red: 'bg-red-100 dark:bg-red-900',
    purple: 'bg-purple-100 dark:bg-purple-900',
    yellow: 'bg-yellow-100 dark:bg-yellow-900',
    indigo: 'bg-indigo-100 dark:bg-indigo-900',
    pink: 'bg-pink-100 dark:bg-pink-900',
    cyan: 'bg-cyan-100 dark:bg-cyan-900'
  }
  return backgrounds[props.color]
})

const progressBarClass = computed(() => {
  const progressColors = {
    blue: 'bg-blue-500',
    green: 'bg-green-500',
    red: 'bg-red-500',
    purple: 'bg-purple-500',
    yellow: 'bg-yellow-500',
    indigo: 'bg-indigo-500',
    pink: 'bg-pink-500',
    cyan: 'bg-cyan-500'
  }
  return progressColors[props.color]
})

const actionButtonClass = computed(() => {
  const buttonColors = {
    blue: 'bg-blue-50 dark:bg-blue-900 text-blue-700 dark:text-blue-300 hover:bg-blue-100 dark:hover:bg-blue-800',
    green: 'bg-green-50 dark:bg-green-900 text-green-700 dark:text-green-300 hover:bg-green-100 dark:hover:bg-green-800',
    red: 'bg-red-50 dark:bg-red-900 text-red-700 dark:text-red-300 hover:bg-red-100 dark:hover:bg-red-800',
    purple: 'bg-purple-50 dark:bg-purple-900 text-purple-700 dark:text-purple-300 hover:bg-purple-100 dark:hover:bg-purple-800',
    yellow: 'bg-yellow-50 dark:bg-yellow-900 text-yellow-700 dark:text-yellow-300 hover:bg-yellow-100 dark:hover:bg-yellow-800',
    indigo: 'bg-indigo-50 dark:bg-indigo-900 text-indigo-700 dark:text-indigo-300 hover:bg-indigo-100 dark:hover:bg-indigo-800',
    pink: 'bg-pink-50 dark:bg-pink-900 text-pink-700 dark:text-pink-300 hover:bg-pink-100 dark:hover:bg-pink-800',
    cyan: 'bg-cyan-50 dark:bg-cyan-900 text-cyan-700 dark:text-cyan-300 hover:bg-cyan-100 dark:hover:bg-cyan-800'
  }
  return buttonColors[props.color]
})

const trendTextClass = computed(() => {
  if (props.trend === 'up') return 'text-green-600 dark:text-green-400'
  if (props.trend === 'down') return 'text-red-600 dark:text-red-400'
  return 'text-gray-600 dark:text-gray-400'
})
</script> 