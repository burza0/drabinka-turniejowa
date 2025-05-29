<template>
  <span :class="badgeClass" class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium">
    {{ status }}
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  status: string
}

const props = defineProps<Props>()

const badgeClass = computed(() => {
  switch (props.status) {
    case 'FINISHED':
      return 'bg-green-100 text-green-800'
    case 'DNF':
      return 'bg-yellow-100 text-yellow-800'
    case 'DSQ':
      return 'bg-red-100 text-red-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
})
</script> 