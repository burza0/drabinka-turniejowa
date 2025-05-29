<template>
  <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-3 border border-gray-200 dark:border-gray-700 transition-colors duration-200">
    <!-- Numer + Imię/nazwisko + klub + kategoria w jednej linii -->
    <div class="flex items-center justify-between mb-3 text-lg">
      <div class="flex items-center space-x-3 flex-1">
        <span class="inline-flex items-center justify-center w-10 h-10 rounded-full bg-indigo-100 dark:bg-indigo-900 text-indigo-800 dark:text-indigo-200 text-base font-bold">
          {{ zawodnik.nr_startowy }}
        </span>
        <h3 class="font-bold text-gray-900 dark:text-white leading-tight">
          {{ zawodnik.imie }} {{ zawodnik.nazwisko }}
        </h3>
      </div>
      <div class="flex items-center space-x-3 text-base">
        <div class="flex items-center space-x-1">
          <BuildingOfficeIcon class="h-4 w-4 text-blue-500 dark:text-blue-400 flex-shrink-0" />
          <span class="font-medium text-gray-700 dark:text-gray-300 truncate">
            {{ zawodnik.klub }}
          </span>
        </div>
        <div class="flex items-center space-x-1">
          <TagIcon class="h-4 w-4 text-green-500 dark:text-green-400 flex-shrink-0" />
          <span class="font-medium text-gray-700 dark:text-gray-300">
            {{ zawodnik.kategoria }}
          </span>
        </div>
      </div>
    </div>

    <!-- Czas + status w jednej linii -->
    <div class="flex items-center justify-between bg-gray-50 dark:bg-gray-700 rounded-lg p-3 mb-3">
      <div class="flex items-center space-x-2">
        <ClockIcon class="h-5 w-5 text-purple-500 dark:text-purple-400" />
        <span class="text-2xl font-bold text-gray-900 dark:text-white">
          {{ zawodnik.czas_przejazdu_s ? formatTime(zawodnik.czas_przejazdu_s) : '-' }}
        </span>
      </div>
      <StatusBadge :status="zawodnik.status" />
    </div>

    <!-- Akcje admin (jeśli admin mode) -->
    <div v-if="isAdmin" class="flex space-x-2">
      <button class="flex-1 inline-flex items-center justify-center px-3 py-2 text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 transition-colors duration-200">
        <PencilIcon class="h-3 w-3 mr-1" />
        Edytuj
      </button>
      <button class="flex-1 inline-flex items-center justify-center px-3 py-2 text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 transition-colors duration-200">
        <TrashIcon class="h-3 w-3 mr-1" />
        Usuń
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { PencilIcon, TrashIcon, ClockIcon, BuildingOfficeIcon, TagIcon } from '@heroicons/vue/24/outline'
import StatusBadge from './StatusBadge.vue'

interface Zawodnik {
  nr_startowy: number
  imie: string
  nazwisko: string
  kategoria: string
  plec: string
  klub: string
  czas_przejazdu_s: number | null
  status: string
}

interface Props {
  zawodnik: Zawodnik
  isAdmin: boolean
}

defineProps<Props>()

const formatTime = (seconds: number): string => {
  const mins = Math.floor(seconds / 60)
  const secs = (seconds % 60).toFixed(2)
  return `${mins}:${secs.padStart(5, '0')}`
}
</script> 