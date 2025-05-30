<template>
  <div>
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6 space-y-4 sm:space-y-0">
      <div class="flex items-center space-x-3">
        <ChartBarIcon class="h-8 w-8 text-purple-600" />
        <h2 class="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">Rankingi SKATECROSS</h2>
      </div>
      <p class="text-sm text-gray-600 dark:text-gray-400">
        System rankingowy zawodników - funkcjonalność w przygotowaniu
      </p>
    </div>

    <!-- Placeholder Content -->
    <div class="bg-white shadow rounded-lg">
      <div class="text-center py-16">
        <ChartBarIcon class="h-24 w-24 mx-auto text-gray-300 mb-6" />
        <h3 class="text-xl font-semibold text-gray-700 mb-2">Rankingi będą wkrótce dostępne</h3>
        <p class="text-gray-500 mb-8 max-w-md mx-auto">
          Pracujemy nad systemem rankingowym, który będzie uwzględniał wyniki z różnych zawodów 
          oraz punktację według kategorii wiekowych i płci.
        </p>
        
        <!-- Planned Features -->
        <div class="max-w-2xl mx-auto">
          <h4 class="text-lg font-medium text-gray-900 mb-4">Planowane funkcjonalności:</h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-left">
            <div class="bg-gray-50 rounded-lg p-4">
              <div class="flex items-center mb-2">
                <TrophyIcon class="h-5 w-5 text-yellow-500 mr-2" />
                <span class="font-medium">Ranking ogólny</span>
              </div>
              <p class="text-sm text-gray-600">Najlepsi zawodnicy we wszystkich kategoriach</p>
            </div>
            
            <div class="bg-gray-50 rounded-lg p-4">
              <div class="flex items-center mb-2">
                <UsersIcon class="h-5 w-5 text-blue-500 mr-2" />
                <span class="font-medium">Ranking według kategorii</span>
              </div>
              <p class="text-sm text-gray-600">Osobne rankingi dla każdej grupy wiekowej</p>
            </div>
            
            <div class="bg-gray-50 rounded-lg p-4">
              <div class="flex items-center mb-2">
                <BuildingOfficeIcon class="h-5 w-5 text-green-500 mr-2" />
                <span class="font-medium">Ranking klubów</span>
              </div>
              <p class="text-sm text-gray-600">Najlepsze kluby sportowe w SKATECROSS</p>
            </div>
            
            <div class="bg-gray-50 rounded-lg p-4">
              <div class="flex items-center mb-2">
                <CalendarIcon class="h-5 w-5 text-purple-500 mr-2" />
                <span class="font-medium">Ranking sezonowy</span>
              </div>
              <p class="text-sm text-gray-600">Punkty z całego sezonu zawodów</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Sample Ranking Preview -->
    <div class="mt-8 bg-white shadow rounded-lg p-6">
      <h3 class="text-lg font-medium text-gray-900 mb-4">📊 Podgląd przyszłego rankingu</h3>
      <div class="text-sm text-gray-500 mb-4">
        * Przykładowy wygląd tabeli rankingowej
      </div>
      
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Pozycja</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Zawodnik</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Klub</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Kategoria</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Punkty</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Najlepszy czas</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr class="opacity-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">🥇 1</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">--- ---</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">---</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">---</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">--- pkt</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">--:--</td>
            </tr>
            <tr class="opacity-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">🥈 2</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">--- ---</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">---</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">---</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">--- pkt</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">--:--</td>
            </tr>
            <tr class="opacity-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">🥉 3</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">--- ---</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">---</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">---</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">--- pkt</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">--:--</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { 
  ChartBarIcon, 
  TrophyIcon, 
  UsersIcon, 
  BuildingOfficeIcon,
  CalendarIcon
} from '@heroicons/vue/24/outline'
</script>

<style scoped>
/* Custom styles for placeholder */
</style> 