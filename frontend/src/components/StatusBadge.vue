<template>
  <span :class="badgeClass" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
    {{ displayStatus }}
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  status?: string
  checked_in?: boolean
}

const props = defineProps<Props>()

const displayStatus = computed(() => {
  if (props.status) {
    return props.status
  }
  return props.checked_in ? 'ZAMELDOWANY' : 'NIEZAMELDOWANY'
})

const badgeClass = computed(() => {
  if (props.status) {
    switch (props.status) {
      case 'FINISHED':
        return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
      case 'DNF':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
      case 'DSQ':
        return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
    }
  }
  
  // Fallback na checked_in
  return props.checked_in
    ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
    : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
})
</script> 