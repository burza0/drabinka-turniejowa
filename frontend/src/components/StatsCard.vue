<template>
  <div class="bg-white overflow-hidden shadow rounded-lg">
    <div class="p-5">
      <div class="flex items-center">
        <div class="flex-shrink-0">
          <component 
            :is="icon" 
            :class="iconClass"
            class="h-6 w-6" 
          />
        </div>
        <div class="ml-5 w-0 flex-1">
          <dl>
            <dt class="text-sm font-medium text-gray-500 truncate">{{ title }}</dt>
            <dd class="text-lg font-medium text-gray-900">{{ value }}</dd>
            <dd v-if="subtitle" class="text-xs text-gray-400 mt-1">{{ subtitle }}</dd>
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