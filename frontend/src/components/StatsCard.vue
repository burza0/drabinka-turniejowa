<template>
  <div class="bg-white dark:bg-gray-800 overflow-hidden shadow rounded-lg transition-colors duration-200">
    <div class="p-3 sm:p-5">
      <div class="flex items-center">
        <div class="flex-shrink-0">
          <component 
            :is="icon" 
            :class="iconClass"
            class="h-5 w-5 sm:h-6 sm:w-6" 
          />
        </div>
        <div class="ml-3 sm:ml-5 w-0 flex-1">
          <dl>
            <dt class="text-xs sm:text-sm font-medium text-gray-500 dark:text-gray-400 truncate">{{ title }}</dt>
            <dd class="text-base sm:text-lg font-medium text-gray-900 dark:text-white">{{ value }}</dd>
            <dd v-if="subtitle" class="text-xs text-gray-400 dark:text-gray-500 mt-1">{{ subtitle }}</dd>
          </dl>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  title: string
  value: string | number
  icon: any
  color: 'blue' | 'green' | 'red' | 'purple'
  subtitle?: string
}

const props = defineProps<Props>()

const iconClass = computed(() => {
  const colors = {
    blue: 'text-blue-400',
    green: 'text-green-400',
    red: 'text-red-400',
    purple: 'text-purple-400'
  }
  return colors[props.color]
})
</script> 