<template>
  <div>
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6 space-y-4 sm:space-y-0">
      <div class="flex items-center space-x-3">
        <ChartBarIcon class="h-8 w-8 text-purple-600 dark:text-purple-400" />
        <h2 class="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">Rankingi SKATECROSS</h2>
      </div>
      <div class="flex items-center space-x-4">
        <select 
          v-model="selectedSeason" 
          class="rounded-lg border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
        >
          <option value="2025">Sezon 2025</option>
          <option value="2024">Sezon 2024</option>
        </select>
        <button 
          @click="refreshRankings"
          :disabled="loading"
          class="inline-flex items-center px-3 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-purple-600 hover:bg-purple-700 disabled:opacity-50"
        >
          <ArrowPathIcon :class="['h-4 w-4 mr-2', loading ? 'animate-spin' : '']" />
          Odśwież
        </button>
      </div>
    </div>

    <!-- Tabs Navigation -->
    <div class="border-b border-gray-200 dark:border-gray-700 mb-6">
      <nav class="-mb-px flex space-x-8 overflow-x-auto">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="[
            'whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm flex items-center space-x-2',
            activeTab === tab.id
              ? 'border-purple-500 text-purple-600 dark:text-purple-400'
              : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300'
          ]"
        >
          <component :is="tab.icon" class="h-5 w-5" />
          <span>{{ tab.name }}</span>
          <span v-if="tab.count" class="ml-2 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 py-0.5 px-2 rounded-full text-xs">
            {{ tab.count }}
          </span>
        </button>
      </nav>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center py-12">
      <div class="text-center">
        <ArrowPathIcon class="h-8 w-8 text-purple-500 animate-spin mx-auto mb-4" />
        <p class="text-gray-600 dark:text-gray-400">Ładowanie rankingów...</p>
      </div>
    </div>

    <!-- Tab Content -->
    <div v-else>
      <!-- Wyniki Czasowe -->
      <div v-if="activeTab === 'times'" class="space-y-6">
        <!-- Filtry i sortowanie dla Wyników Czasowych -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-6 transition-colors duration-200">
          <!-- Nagłówek sekcji -->
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
            <div class="flex items-center gap-4">
              <h3 class="text-lg sm:text-xl font-semibold text-gray-900 dark:text-white">Filtry i sortowanie</h3>
              
              <!-- Pole wyszukiwania -->
              <div class="relative w-64">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"/>
                  </svg>
                </div>
                <input
                  v-model="searchQueryTime"
                  type="text"
                  placeholder="Szukaj zawodników..."
                  class="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white focus:border-purple-500 focus:ring-2 focus:ring-purple-500 text-sm pl-10 pr-3 py-2 transition-all duration-200"
                />
                <div v-if="searchQueryTime" class="absolute -bottom-5 left-0 text-xs text-gray-500 dark:text-gray-400">
                  {{ paginationDataTime.total_results }} wyników
                </div>
              </div>
            </div>
            
            <button 
              @click="clearTimeFilters" 
              class="text-sm text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300 flex items-center space-x-1 transition-colors duration-200"
            >
              <span>🗑️</span>
              <span>Wyczyść</span>
            </button>
          </div>

          <!-- Filtry w grid layout -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <!-- Filtr kategorii -->
            <div>
              <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
                <span class="flex items-center space-x-2">
                  <span>🏆</span>
                  <span>Kategoria</span>
                </span>
              </label>
              <select 
                v-model="selectedKategoriaTime" 
                class="w-full rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-md focus:border-purple-500 focus:ring-2 focus:ring-purple-500 text-sm font-medium py-2.5 px-3 transition-all duration-200 hover:shadow-lg"
              >
                <option value="">Wszystkie</option>
                <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
              </select>
            </div>
            
            <!-- Filtr płci -->
            <div>
              <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
                <span class="flex items-center space-x-2">
                  <span>👥</span>
                  <span>Płeć</span>
                </span>
              </label>
              <select 
                v-model="selectedPlecTime" 
                class="w-full rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-md focus:border-purple-500 focus:ring-2 focus:ring-purple-500 text-sm font-medium py-2.5 px-3 transition-all duration-200 hover:shadow-lg"
              >
                <option value="">Wszystkie</option>
                <option value="M">Mężczyźni</option>
                <option value="K">Kobiety</option>
              </select>
            </div>

            <!-- Filtr klubu -->
            <div>
              <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
                <span class="flex items-center space-x-2">
                  <span>🏢</span>
                  <span>Klub</span>
                </span>
              </label>
              <select 
                v-model="selectedKlubTime" 
                class="w-full rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-md focus:border-purple-500 focus:ring-2 focus:ring-purple-500 text-sm font-medium py-2.5 px-3 transition-all duration-200 hover:shadow-lg"
              >
                <option value="">Wszystkie</option>
                <option v-for="club in clubs" :key="club" :value="club">{{ club }}</option>
              </select>
            </div>



            <!-- Sortowanie -->
            <div>
              <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
                <span class="flex items-center space-x-2">
                  <span>🔄</span>
                  <span>Sortowanie</span>
                </span>
              </label>
              <select 
                v-model="sortByTime" 
                class="w-full rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-md focus:border-purple-500 focus:ring-2 focus:ring-purple-500 text-sm font-medium py-2.5 px-3 transition-all duration-200 hover:shadow-lg"
              >
                <option value="time_asc">Czas (najlepszy)</option>
                <option value="time_desc">Czas (najgorszy)</option>
                <option value="name_asc">Nazwisko (A-Z)</option>
                <option value="name_desc">Nazwisko (Z-A)</option>
                <option value="kategoria_asc">Kategoria (A-Z)</option>
                <option value="klub_asc">Klub (A-Z)</option>
              </select>
            </div>


          </div>
        </div>

        <!-- Nagłówek Wyników Czasowych z paginacją -->
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div class="flex items-center gap-4">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white">Wyniki Czasowe</h3>
            <div class="text-sm text-gray-600 dark:text-gray-400">
              <span v-if="paginationDataTime.total_results > 0">
                Wyniki {{ paginationDataTime.start_index }}-{{ paginationDataTime.end_index }} 
                z {{ paginationDataTime.total_results }}
              </span>
              <span v-else>Brak wyników</span>
            </div>

            <!-- Wybór ilości wyników na stronę -->
            <div class="flex items-center gap-2">
              <span class="text-sm text-gray-600 dark:text-gray-400">Na stronę:</span>
              <select 
                v-model="perPageTime" 
                @change="changePerPageTime"
                class="text-sm rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white px-2 py-1 focus:border-purple-500 focus:ring-1 focus:ring-purple-500"
              >
                <option :value="10">10</option>
                <option :value="25">25</option>
                <option :value="50">50</option>
                <option :value="100">100</option>
              </select>
            </div>
          </div>
          
          <!-- Kontrolki Paginacji w nagłówku -->
          <div v-if="paginationDataTime.total_pages > 1" class="flex items-center space-x-2">
            <!-- Pierwsza strona -->
            <button 
              @click="goToPageTime(1)"
              :disabled="paginationDataTime.current_page === 1"
              class="px-2 py-1 text-xs rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              ⏮️
            </button>

            <!-- Poprzednia strona -->
            <button 
              @click="previousPageTime"
              :disabled="!paginationDataTime.has_prev"
              class="px-2 py-1 text-xs rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              ←
            </button>

            <!-- Info o stronie -->
            <span class="text-xs text-gray-600 dark:text-gray-400 px-2">
              {{ paginationDataTime.current_page }}/{{ paginationDataTime.total_pages }}
            </span>

            <!-- Następna strona -->
            <button 
              @click="nextPageTime"
              :disabled="!paginationDataTime.has_next"
              class="px-2 py-1 text-xs rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              →
            </button>

            <!-- Ostatnia strona -->
            <button 
              @click="goToPageTime(paginationDataTime.total_pages)"
              :disabled="paginationDataTime.current_page === paginationDataTime.total_pages"
              class="px-2 py-1 text-xs rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              ⏭️
            </button>
          </div>
        </div>
        
        <!-- Tabela Wyników Czasowych -->
        <div class="bg-white dark:bg-gray-800 shadow rounded-lg overflow-hidden">
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead class="bg-gray-50 dark:bg-gray-700">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Pozycja</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Zawodnik</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Klub</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Kategoria</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Czas</th>
                </tr>
              </thead>
              <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                <tr v-if="timeRanking.length === 0">
                  <td colspan="5" class="px-6 py-12 text-center text-gray-500 dark:text-gray-400">
                    <div v-if="searchQueryTime">
                      Brak wyników dla wyszukiwania: "{{ searchQueryTime }}"
                    </div>
                    <div v-else>
                      Brak zawodników spełniających wybrane kryteria
                    </div>
                  </td>
                </tr>
                <tr v-for="(rider, index) in timeRanking" :key="rider.nr_startowy" class="hover:bg-gray-50 dark:hover:bg-gray-700">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                    <span v-if="rider.pozycja === 1">🥇</span>
                    <span v-else-if="rider.pozycja === 2">🥈</span>
                    <span v-else-if="rider.pozycja === 3">🥉</span>
                    <span v-else>{{ rider.pozycja }}</span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm font-medium text-gray-900 dark:text-white">{{ rider.imie }} {{ rider.nazwisko }}</div>
                    <div class="text-xs text-gray-500 dark:text-gray-400">Nr {{ rider.nr_startowy }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{{ rider.klub }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{{ rider.kategoria }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-purple-600 dark:text-purple-400">{{ formatTime(rider.total_time) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>


      </div>

      <!-- Klasyfikacja Indywidualna -->
      <div v-if="activeTab === 'individual'" class="space-y-6">
        <!-- Filtry i sortowanie dla Indywidualnej -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-6 transition-colors duration-200">
          <!-- Nagłówek sekcji -->
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
            <div class="flex items-center gap-4">
              <h3 class="text-lg sm:text-xl font-semibold text-gray-900 dark:text-white">Filtry i sortowanie</h3>
              
              <!-- Pole wyszukiwania -->
              <div class="relative w-64">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"/>
                  </svg>
                </div>
                <input
                  v-model="searchQuery"
                  type="text"
                  placeholder="Szukaj zawodników..."
                  class="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white focus:border-purple-500 focus:ring-2 focus:ring-purple-500 text-sm pl-10 pr-3 py-2 transition-all duration-200"
                />
                <div v-if="searchQuery" class="absolute -bottom-5 left-0 text-xs text-gray-500 dark:text-gray-400">
                  {{ filteredIndividualRanking.length }} wyników
                </div>
              </div>
            </div>
            
            <button 
              @click="clearAllFilters" 
              class="text-sm text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300 flex items-center space-x-1 transition-colors duration-200"
            >
              <span>🗑️</span>
              <span>Wyczyść</span>
            </button>
          </div>

          <!-- Filtry w grid layout -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <!-- Filtr kategorii -->
            <div>
              <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
                <span class="flex items-center space-x-2">
                  <span>🏆</span>
                  <span>Kategoria</span>
                </span>
              </label>
              <select 
                v-model="selectedCategory" 
                class="w-full rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-md focus:border-purple-500 focus:ring-2 focus:ring-purple-500 text-sm font-medium py-2.5 px-3 transition-all duration-200 hover:shadow-lg"
              >
                <option value="">Wszystkie</option>
                <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
              </select>
            </div>
            
            <!-- Filtr klubu -->
            <div>
              <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
                <span class="flex items-center space-x-2">
                  <span>🏢</span>
                  <span>Klub</span>
                </span>
              </label>
              <select 
                v-model="selectedClub" 
                class="w-full rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-md focus:border-purple-500 focus:ring-2 focus:ring-purple-500 text-sm font-medium py-2.5 px-3 transition-all duration-200 hover:shadow-lg"
              >
                <option value="">Wszystkie</option>
                <option v-for="club in clubs" :key="club" :value="club">{{ club }}</option>
              </select>
            </div>

            <!-- Filtr płci -->
            <div>
              <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
                <span class="flex items-center space-x-2">
                  <span>👥</span>
                  <span>Płeć</span>
                </span>
              </label>
              <select 
                v-model="selectedGender" 
                class="w-full rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-md focus:border-purple-500 focus:ring-2 focus:ring-purple-500 text-sm font-medium py-2.5 px-3 transition-all duration-200 hover:shadow-lg"
              >
                <option value="">Wszystkie</option>
                <option value="M">Mężczyźni</option>
                <option value="K">Kobiety</option>
              </select>
            </div>
            
            <!-- Sortowanie -->
            <div>
              <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
                <span class="flex items-center space-x-2">
                  <span>🔄</span>
                  <span>Sortowanie</span>
                </span>
              </label>
              <select 
                v-model="sortBy" 
                class="w-full rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-md focus:border-purple-500 focus:ring-2 focus:ring-purple-500 text-sm font-medium py-2.5 px-3 transition-all duration-200 hover:shadow-lg"
              >
                <option value="pozycja_asc">Pozycja (najlepsi)</option>
                <option value="pozycja_desc">Pozycja (najgorsi)</option>
                <option value="punkty_desc">Punkty (malejąco)</option>
                <option value="punkty_asc">Punkty (rosnąco)</option>
                <option value="nazwisko_asc">Nazwisko (A-Z)</option>
                <option value="nazwisko_desc">Nazwisko (Z-A)</option>
                <option value="kategoria_asc">Kategoria (A-Z)</option>
                <option value="starty_desc">Starty (malejąco)</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Nagłówek Klasyfikacji Indywidualnej z paginacją -->
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div class="flex items-center gap-4">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white">Klasyfikacja Indywidualna</h3>
            <div class="text-sm text-gray-600 dark:text-gray-400">
              <span v-if="paginationDataIndividual.total_results > 0">
                Wyniki {{ paginationDataIndividual.start_index }}-{{ paginationDataIndividual.end_index }} 
                z {{ paginationDataIndividual.total_results }}
              </span>
              <span v-else>Brak wyników</span>
            </div>
            <!-- Kontrolka Na stronę -->
            <div class="flex items-center gap-2">
              <span class="text-sm text-gray-600 dark:text-gray-400">Na stronę:</span>
              <select 
                v-model="perPageIndividual" 
                @change="changePerPageIndividual"
                class="text-sm border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded px-2 py-1 focus:ring-2 focus:ring-purple-500"
              >
                <option :value="10">10</option>
                <option :value="25">25</option>
                <option :value="50">50</option>
                <option :value="100">100</option>
              </select>
            </div>
          </div>
          
          <!-- Kontrolki Paginacji w nagłówku -->
          <div v-if="paginationDataIndividual.total_pages > 1" class="flex items-center space-x-2">
            <!-- Pierwsza strona -->
            <button 
              @click="goToPageIndividual(1)"
              :disabled="paginationDataIndividual.current_page === 1"
              class="px-2 py-1 text-xs rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              ⏮️
            </button>

            <!-- Poprzednia strona -->
            <button 
              @click="previousPageIndividual"
              :disabled="!paginationDataIndividual.has_prev"
              class="px-2 py-1 text-xs rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              ←
            </button>

            <!-- Info o stronie -->
            <span class="text-xs text-gray-600 dark:text-gray-400 px-2">
              {{ paginationDataIndividual.current_page }}/{{ paginationDataIndividual.total_pages }}
            </span>

            <!-- Następna strona -->
            <button 
              @click="nextPageIndividual"
              :disabled="!paginationDataIndividual.has_next"
              class="px-2 py-1 text-xs rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              →
            </button>

            <!-- Ostatnia strona -->
            <button 
              @click="goToPageIndividual(paginationDataIndividual.total_pages)"
              :disabled="paginationDataIndividual.current_page === paginationDataIndividual.total_pages"
              class="px-2 py-1 text-xs rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              ⏭️
            </button>
          </div>
        </div>
        
        <!-- Tabela rankingu indywidualnego -->
        <div class="bg-white dark:bg-gray-800 shadow rounded-lg overflow-hidden">
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead class="bg-gray-50 dark:bg-gray-700">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Pozycja</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Zawodnik</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Klub</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Kategoria</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Punkty</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Starty</th>
                </tr>
              </thead>
              <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                <tr v-if="paginatedIndividualRanking.length === 0">
                  <td colspan="6" class="px-6 py-12 text-center text-gray-500 dark:text-gray-400">
                    <div v-if="searchQuery">
                      Brak wyników dla wyszukiwania: "{{ searchQuery }}"
                    </div>
                    <div v-else>
                      Brak zawodników spełniających wybrane kryteria
                    </div>
                  </td>
                </tr>
                <tr v-for="(rider, index) in paginatedIndividualRanking" :key="rider.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                    <span v-if="index === 0">🥇</span>
                    <span v-else-if="index === 1">🥈</span>
                    <span v-else-if="index === 2">🥉</span>
                    <span v-else>{{ index + 1 }}</span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm font-medium text-gray-900 dark:text-white">{{ rider.imie }} {{ rider.nazwisko }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{{ rider.klub }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{{ rider.kategoria }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-purple-600 dark:text-purple-400">{{ rider.punkty }} pkt</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{{ rider.liczba_zawodow }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Klasyfikacja Generalna -->
      <div v-if="activeTab === 'general'" class="space-y-6">
        <!-- Filtry i sortowanie dla Generalnej -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-6 transition-colors duration-200">
          <!-- Nagłówek sekcji -->
          <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
            <div class="flex items-center gap-4">
              <h3 class="text-lg sm:text-xl font-semibold text-gray-900 dark:text-white">Filtry i sortowanie</h3>
              
              <!-- Pole wyszukiwania -->
              <div class="relative w-64">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg class="h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"/>
                  </svg>
                </div>
                <input
                  v-model="searchQueryGeneral"
                  type="text"
                  placeholder="Szukaj zawodników..."
                  class="w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-white focus:border-purple-500 focus:ring-2 focus:ring-purple-500 text-sm pl-10 pr-3 py-2 transition-all duration-200"
                />
                <div v-if="searchQueryGeneral" class="absolute -bottom-5 left-0 text-xs text-gray-500 dark:text-gray-400">
                  {{ filteredGeneralRanking.length }} wyników
                </div>
              </div>
            </div>
            
            <button 
              @click="clearGeneralFilters" 
              class="text-sm text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300 flex items-center space-x-1 transition-colors duration-200"
            >
              <span>🗑️</span>
              <span>Wyczyść</span>
            </button>
          </div>

          <!-- Filtry w grid layout -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <!-- Filtr kategorii -->
            <div>
              <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
                <span class="flex items-center space-x-2">
                  <span>🏆</span>
                  <span>Kategoria</span>
                </span>
              </label>
              <select 
                v-model="selectedCategoryGeneral" 
                class="w-full rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-md focus:border-purple-500 focus:ring-2 focus:ring-purple-500 text-sm font-medium py-2.5 px-3 transition-all duration-200 hover:shadow-lg"
              >
                <option value="">Wszystkie</option>
                <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
              </select>
            </div>
            
            <!-- Filtr klubu -->
            <div>
              <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
                <span class="flex items-center space-x-2">
                  <span>🏢</span>
                  <span>Klub</span>
                </span>
              </label>
              <select 
                v-model="selectedClubGeneral" 
                class="w-full rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-md focus:border-purple-500 focus:ring-2 focus:ring-purple-500 text-sm font-medium py-2.5 px-3 transition-all duration-200 hover:shadow-lg"
              >
                <option value="">Wszystkie</option>
                <option v-for="club in clubs" :key="club" :value="club">{{ club }}</option>
              </select>
              </div>

            <!-- Filtr płci -->
            <div>
              <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
                <span class="flex items-center space-x-2">
                  <span>👥</span>
                  <span>Płeć</span>
                </span>
              </label>
              <select 
                v-model="selectedGenderGeneral" 
                class="w-full rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-md focus:border-purple-500 focus:ring-2 focus:ring-purple-500 text-sm font-medium py-2.5 px-3 transition-all duration-200 hover:shadow-lg"
              >
                <option value="">Wszystkie</option>
                <option value="M">Mężczyźni</option>
                <option value="K">Kobiety</option>
              </select>
            </div>
            
            <!-- Sortowanie -->
            <div>
              <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
                <span class="flex items-center space-x-2">
                  <span>🔄</span>
                  <span>Sortowanie</span>
                </span>
              </label>
              <select 
                v-model="sortByGeneral" 
                class="w-full rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-md focus:border-purple-500 focus:ring-2 focus:ring-purple-500 text-sm font-medium py-2.5 px-3 transition-all duration-200 hover:shadow-lg"
              >
                <option value="punkty_desc">Punkty (malejąco)</option>
                <option value="punkty_asc">Punkty (rosnąco)</option>
                <option value="nazwisko_asc">Nazwisko (A-Z)</option>
                <option value="nazwisko_desc">Nazwisko (Z-A)</option>
                <option value="kategoria_asc">Kategoria (A-Z)</option>
                <option value="starty_desc">Starty (malejąco)</option>
                <option value="odrzucone_desc">Odrzucone (malejąco)</option>
              </select>
            </div>
          </div>
        </div>
        
        <!-- Nagłówek Klasyfikacji Generalnej z paginacją -->
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div class="flex items-center gap-4">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white">Klasyfikacja Generalna (n-2)</h3>
            <div class="text-sm text-gray-600 dark:text-gray-400">
              <span v-if="paginationDataGeneral.total_results > 0">
                Wyniki {{ paginationDataGeneral.start_index }}-{{ paginationDataGeneral.end_index }} 
                z {{ paginationDataGeneral.total_results }}
              </span>
              <span v-else>Brak wyników</span>
            </div>
            <!-- Kontrolka Na stronę -->
            <div class="flex items-center gap-2">
              <span class="text-sm text-gray-600 dark:text-gray-400">Na stronę:</span>
              <select 
                v-model="perPageGeneral" 
                @change="changePerPageGeneral"
                class="text-sm border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded px-2 py-1 focus:ring-2 focus:ring-purple-500"
              >
                <option :value="10">10</option>
                <option :value="25">25</option>
                <option :value="50">50</option>
                <option :value="100">100</option>
              </select>
            </div>
          </div>
          
          <!-- Kontrolki Paginacji w nagłówku -->
          <div v-if="paginationDataGeneral.total_pages > 1" class="flex items-center space-x-2">
            <!-- Pierwsza strona -->
            <button 
              @click="goToPageGeneral(1)"
              :disabled="paginationDataGeneral.current_page === 1"
              class="px-2 py-1 text-xs rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              ⏮️
            </button>

            <!-- Poprzednia strona -->
            <button 
              @click="previousPageGeneral"
              :disabled="!paginationDataGeneral.has_prev"
              class="px-2 py-1 text-xs rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              ←
            </button>

            <!-- Info o stronie -->
            <span class="text-xs text-gray-600 dark:text-gray-400 px-2">
              {{ paginationDataGeneral.current_page }}/{{ paginationDataGeneral.total_pages }}
            </span>

            <!-- Następna strona -->
            <button 
              @click="nextPageGeneral"
              :disabled="!paginationDataGeneral.has_next"
              class="px-2 py-1 text-xs rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              →
            </button>

            <!-- Ostatnia strona -->
            <button 
              @click="goToPageGeneral(paginationDataGeneral.total_pages)"
              :disabled="paginationDataGeneral.current_page === paginationDataGeneral.total_pages"
              class="px-2 py-1 text-xs rounded border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              ⏭️
            </button>
          </div>
        </div>
        
        <div class="bg-white dark:bg-gray-800 shadow rounded-lg overflow-hidden">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead class="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Pozycja</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Zawodnik</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Kategoria</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Punkty końcowe</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Starty</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Odrzucone</th>
              </tr>
            </thead>
            <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              <tr v-if="paginatedGeneralRanking.length === 0">
                <td colspan="6" class="px-6 py-12 text-center text-gray-500 dark:text-gray-400">
                  <div v-if="searchQueryGeneral">
                    Brak wyników dla wyszukiwania: "{{ searchQueryGeneral }}"
                  </div>
                  <div v-else>
                    Brak zawodników spełniających wybrane kryteria
                  </div>
                </td>
              </tr>
              <tr v-for="(rider, index) in paginatedGeneralRanking" :key="rider.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                  <span v-if="index === 0">🏆</span>
                  <span v-else>{{ index + 1 }}</span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm font-medium text-gray-900 dark:text-white">{{ rider.imie }} {{ rider.nazwisko }}</div>
                  <div class="text-sm text-gray-500 dark:text-gray-400">{{ rider.klub }}</div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{{ rider.kategoria }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-green-600 dark:text-green-400">{{ rider.punkty_koncowe }} pkt</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{{ rider.uczestnictwa }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-red-500 dark:text-red-400">{{ rider.odrzucone || 0 }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Klasyfikacja Klubowa - Suma -->
      <div v-if="activeTab === 'clubs-total'" class="space-y-6">
        <!-- Filtry i sortowanie dla Klubowej - Suma -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-6 transition-colors duration-200">
          <!-- Nagłówek sekcji -->
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg sm:text-xl font-semibold text-gray-900 dark:text-white">Filtry i sortowanie</h3>
            <button 
              @click="clearClubsTotalFilters" 
              class="text-sm text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300 flex items-center space-x-1 transition-colors duration-200"
            >
              <span>🗑️</span>
              <span>Wyczyść filtry</span>
            </button>
              </div>

          <!-- Filtry w grid layout -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Filtr min. zawodników -->
            <div>
              <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
                <span class="flex items-center space-x-2">
                  <span>👥</span>
                  <span>Min. zawodników</span>
                </span>
              </label>
              <input 
                v-model="minZawodnikow" 
                type="number"
                min="1"
                placeholder="Minimalna liczba"
                class="w-full rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-md focus:border-purple-500 focus:ring-2 focus:ring-purple-500 text-sm font-medium py-2.5 px-3 transition-all duration-200 hover:shadow-lg"
              />
            </div>
            
            <!-- Sortowanie -->
            <div>
              <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
                <span class="flex items-center space-x-2">
                  <span>🔄</span>
                  <span>Sortowanie</span>
                </span>
              </label>
              <select 
                v-model="sortByClubsTotal" 
                class="w-full rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-md focus:border-purple-500 focus:ring-2 focus:ring-purple-500 text-sm font-medium py-2.5 px-3 transition-all duration-200 hover:shadow-lg"
              >
                <option value="punkty_desc">Punkty (malejąco)</option>
                <option value="punkty_asc">Punkty (rosnąco)</option>
                <option value="srednia_desc">Średnia (malejąco)</option>
                <option value="srednia_asc">Średnia (rosnąco)</option>
                <option value="zawodnicy_desc">Zawodnicy (malejąco)</option>
                <option value="zawodnicy_asc">Zawodnicy (rosnąco)</option>
                <option value="nazwa_asc">Nazwa (A-Z)</option>
                <option value="nazwa_desc">Nazwa (Z-A)</option>
              </select>
            </div>
          </div>
        </div>
        
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">Klasyfikacja Klubowa - Suma Punktów</h3>
          <div class="text-sm text-gray-600 dark:text-gray-400">
            Wszystkie punkty zawodników klubu
          </div>
        </div>
        
        <div class="bg-white dark:bg-gray-800 shadow rounded-lg overflow-hidden">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead class="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Pozycja</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Klub</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Łączne punkty</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Zawodnicy</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Średnia</th>
              </tr>
            </thead>
            <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              <tr v-if="filteredClubsTotal.length === 0">
                <td colspan="5" class="px-6 py-12 text-center text-gray-500 dark:text-gray-400">
                  Brak klubów spełniających wybrane kryteria
                </td>
              </tr>
              <tr v-for="(club, index) in filteredClubsTotal" :key="club.klub" class="hover:bg-gray-50 dark:hover:bg-gray-700">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                  <span v-if="index === 0">🏆</span>
                  <span v-else-if="index === 1">🥈</span>
                  <span v-else-if="index === 2">🥉</span>
                  <span v-else>{{ index + 1 }}</span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">{{ club.klub }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-blue-600 dark:text-blue-400">{{ club.laczne_punkty }} pkt</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{{ club.liczba_zawodnikow }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{{ parseFloat(club.srednia).toFixed(1) }} pkt</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Klasyfikacja Klubowa - Top 3 -->
      <div v-if="activeTab === 'clubs-top3'" class="space-y-6">
        <!-- Filtry i sortowanie dla Klubowej - Top 3 -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-6 transition-colors duration-200">
          <!-- Nagłówek sekcji -->
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg sm:text-xl font-semibold text-gray-900 dark:text-white">Filtry i sortowanie</h3>
            <button 
              @click="clearClubsTop3Filters" 
              class="text-sm text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300 flex items-center space-x-1 transition-colors duration-200"
            >
              <span>🗑️</span>
              <span>Wyczyść filtry</span>
            </button>
          </div>

          <!-- Filtry w grid layout -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Filtr min. kategorii -->
            <div>
              <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
                <span class="flex items-center space-x-2">
                  <span>🏆</span>
                  <span>Min. aktywnych kategorii</span>
                </span>
              </label>
              <input 
                v-model="minKategorie" 
                type="number"
                min="1"
                placeholder="Minimalna liczba"
                class="w-full rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-md focus:border-purple-500 focus:ring-2 focus:ring-purple-500 text-sm font-medium py-2.5 px-3 transition-all duration-200 hover:shadow-lg"
              />
            </div>

            <!-- Sortowanie -->
            <div>
              <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
                <span class="flex items-center space-x-2">
                  <span>🔄</span>
                  <span>Sortowanie</span>
                </span>
              </label>
              <select 
                v-model="sortByClubsTop3" 
                class="w-full rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-md focus:border-purple-500 focus:ring-2 focus:ring-purple-500 text-sm font-medium py-2.5 px-3 transition-all duration-200 hover:shadow-lg"
              >
                <option value="punkty_desc">Punkty Top 3 (malejąco)</option>
                <option value="punkty_asc">Punkty Top 3 (rosnąco)</option>
                <option value="kategorie_desc">Kategorie (malejąco)</option>
                <option value="kategorie_asc">Kategorie (rosnąco)</option>
                <option value="balance_desc">Równowaga (malejąco)</option>
                <option value="balance_asc">Równowaga (rosnąco)</option>
                <option value="nazwa_asc">Nazwa (A-Z)</option>
                <option value="nazwa_desc">Nazwa (Z-A)</option>
              </select>
        </div>
      </div>
    </div>

        <div class="flex items-center justify-between">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">Klasyfikacja Klubowa - Top 3</h3>
          <div class="text-sm text-gray-600 dark:text-gray-400">
            3 najlepszych zawodników z każdej kategorii
          </div>
        </div>

        <div class="bg-white dark:bg-gray-800 shadow rounded-lg overflow-hidden">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead class="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Pozycja</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Klub</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Punkty Top 3</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Kategorie</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Równowaga</th>
              </tr>
            </thead>
            <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              <tr v-if="filteredClubsTop3.length === 0">
                <td colspan="5" class="px-6 py-12 text-center text-gray-500 dark:text-gray-400">
                  Brak klubów spełniających wybrane kryteria
                </td>
              </tr>
              <tr v-for="(club, index) in filteredClubsTop3" :key="club.klub" class="hover:bg-gray-50 dark:hover:bg-gray-700">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">{{ index + 1 }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">{{ club.klub }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-green-600 dark:text-green-400">{{ club.punkty_top3 }} pkt</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{{ club.aktywne_kategorie }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{{ club.balance }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- Klasyfikacja Medalowa -->
      <div v-if="activeTab === 'medals'" class="space-y-6">
        <!-- Filtry i sortowanie dla Medalowej -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-6 transition-colors duration-200">
          <!-- Nagłówek sekcji -->
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg sm:text-xl font-semibold text-gray-900 dark:text-white">Filtry i sortowanie</h3>
            <button 
              @click="clearMedalsFilters" 
              class="text-sm text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300 flex items-center space-x-1 transition-colors duration-200"
            >
              <span>🗑️</span>
              <span>Wyczyść filtry</span>
            </button>
          </div>

          <!-- Filtry w grid layout -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Filtr min. złotych medali -->
            <div>
              <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
                <span class="flex items-center space-x-2">
                  <span>🥇</span>
                  <span>Min. złotych medali</span>
                </span>
              </label>
              <input 
                v-model="minZlote" 
                type="number"
                min="0"
                placeholder="Minimalna liczba"
                class="w-full rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-md focus:border-purple-500 focus:ring-2 focus:ring-purple-500 text-sm font-medium py-2.5 px-3 transition-all duration-200 hover:shadow-lg"
              />
            </div>

            <!-- Sortowanie -->
            <div>
              <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
                <span class="flex items-center space-x-2">
                  <span>🔄</span>
                  <span>Sortowanie</span>
                </span>
              </label>
              <select 
                v-model="sortByMedals" 
                class="w-full rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-md focus:border-purple-500 focus:ring-2 focus:ring-purple-500 text-sm font-medium py-2.5 px-3 transition-all duration-200 hover:shadow-lg"
              >
                <option value="zlote_desc">Złote (malejąco)</option>
                <option value="zlote_asc">Złote (rosnąco)</option>
                <option value="srebrne_desc">Srebrne (malejąco)</option>
                <option value="srebrne_asc">Srebrne (rosnąco)</option>
                <option value="brazowe_desc">Brązowe (malejąco)</option>
                <option value="brazowe_asc">Brązowe (rosnąco)</option>
                <option value="lacznie_desc">Łącznie (malejąco)</option>
                <option value="lacznie_asc">Łącznie (rosnąco)</option>
                <option value="nazwa_asc">Nazwa (A-Z)</option>
                <option value="nazwa_desc">Nazwa (Z-A)</option>
              </select>
            </div>
          </div>
        </div>
        
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">Klasyfikacja Medalowa</h3>
          <div class="text-sm text-gray-600 dark:text-gray-400">
            Złote, srebrne i brązowe medale
          </div>
        </div>
        
        <div class="bg-white dark:bg-gray-800 shadow rounded-lg overflow-hidden">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead class="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Pozycja</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Klub</th>
                <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">🥇 Złote</th>
                <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">🥈 Srebrne</th>
                <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">🥉 Brązowe</th>
                <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">Łącznie</th>
            </tr>
          </thead>
            <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              <tr v-if="filteredMedalRanking.length === 0">
                <td colspan="6" class="px-6 py-12 text-center text-gray-500 dark:text-gray-400">
                  Brak klubów spełniających wybrane kryteria
                </td>
            </tr>
              <tr v-for="(club, index) in filteredMedalRanking" :key="club.klub" class="hover:bg-gray-50 dark:hover:bg-gray-700">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">{{ index + 1 }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">{{ club.klub }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-center text-sm font-bold text-yellow-600">{{ club.zlote }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-center text-sm font-bold text-gray-400">{{ club.srebrne }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-center text-sm font-bold text-yellow-700">{{ club.brazowe }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-center text-sm font-bold text-purple-600">{{ club.lacznie }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="!loading && isEmpty" class="text-center py-12">
      <ChartBarIcon class="h-16 w-16 text-gray-300 mx-auto mb-4" />
      <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">Brak danych rankingowych</h3>
      <p class="text-gray-600 dark:text-gray-400 mb-6">
        Rankingi będą dostępne po zakończeniu pierwszych zawodów w sezonie.
      </p>
      <button 
        @click="refreshRankings"
        class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-lg text-white bg-purple-600 hover:bg-purple-700"
      >
        <ArrowPathIcon class="h-4 w-4 mr-2" />
        Sprawdź ponownie
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { 
  ChartBarIcon, 
  TrophyIcon, 
  UsersIcon, 
  BuildingOfficeIcon,
  CalendarIcon,
  ArrowPathIcon,
  StarIcon,
  ClockIcon
} from '@heroicons/vue/24/outline'

// State
const loading = ref(false)
const selectedSeason = ref('2025')
const activeTab = ref('times')  // Default to times tab
const lastFetchTime = ref(0)
const CACHE_DURATION = 30000 // 30 sekund cache

// Rankings data
const timeRanking = ref([])
const individualRanking = ref([])
const generalRanking = ref([])
const clubRankingTotal = ref([])
const clubRankingTop3 = ref([])
const medalRanking = ref([])

// ===== TIME RANKING FILTERS =====
const selectedKategoriaTime = ref('')
const selectedPlecTime = ref('')
const selectedKlubTime = ref('')
const selectedStatusTime = ref('completed')
const sortByTime = ref('time_asc')

// ===== PAGINATION AND SEARCH =====
const currentPageTime = ref(1)
const perPageTime = ref(25)
const searchQueryTime = ref('')
const paginationDataTime = ref({
  current_page: 1,
  total_pages: 1,
  total_results: 0,
  per_page: 25,
  has_next: false,
  has_prev: false,
  start_index: 1,
  end_index: 0
})

// Filters - Individual
const selectedCategory = ref('')
const selectedClub = ref('')
const selectedGender = ref('')
const sortBy = ref('pozycja_asc')
const searchQuery = ref('')

// Pagination - Individual  
const currentPageIndividual = ref(1)
const perPageIndividual = ref(25)
const paginationDataIndividual = ref({
  current_page: 1,
  total_pages: 1,
  total_results: 0,
  per_page: 25,
  has_next: false,
  has_prev: false,
  start_index: 1,
  end_index: 0
})

// Filters - General
const selectedCategoryGeneral = ref('')
const selectedClubGeneral = ref('')
const selectedGenderGeneral = ref('')
const sortByGeneral = ref('punkty_desc')
const searchQueryGeneral = ref('')

// Pagination - General
const currentPageGeneral = ref(1)
const perPageGeneral = ref(25)
const paginationDataGeneral = ref({
  current_page: 1,
  total_pages: 1,
  total_results: 0,
  per_page: 25,
  has_next: false,
  has_prev: false,
  start_index: 1,
  end_index: 0
})

// Filters - Clubs Total
const minZawodnikow = ref(null)
const sortByClubsTotal = ref('punkty_desc')

// Filters - Clubs Top3
const minKategorie = ref(null)
const sortByClubsTop3 = ref('punkty_desc')

// Filters - Medals
const minZlote = ref(null)
const sortByMedals = ref('zlote_desc')

// Tabs configuration - TIMES FIRST!
const tabs = [
  { id: 'times', name: 'Wyniki Czasowe ⏱️', icon: ClockIcon },  // NEW FIRST TAB!
  { id: 'general', name: 'Generalna', icon: TrophyIcon },
  { id: 'individual', name: 'Indywidualna', icon: UsersIcon },
  { id: 'clubs-total', name: 'Klubowa - Suma', icon: BuildingOfficeIcon },
  { id: 'clubs-top3', name: 'Klubowa - TOP3', icon: BuildingOfficeIcon },
  { id: 'medals', name: 'Medale', icon: TrophyIcon }
]

// Data
const categories = ref(['Junior D', 'Junior C', 'Junior B', 'Junior A', 'Senior', 'Master'])

// Computed
const clubs = computed(() => {
  const uniqueClubs = [...new Set(individualRanking.value.map(rider => rider.klub).filter(Boolean))]
  return uniqueClubs.sort()
})

const genders = computed(() => {
  const uniqueGenders = [...new Set(individualRanking.value.map(rider => rider.plec).filter(Boolean))]
  return uniqueGenders.sort()
})

// REMOVED: filteredTimeRanking - unnecessary double filtering, backend handles all filtering

const paginatedIndividualRanking = computed(() => {
  let filtered = individualRanking.value
  
  // Filter by search query
  if (searchQuery.value.trim()) {
    const searchTerm = searchQuery.value.trim().toLowerCase()
    filtered = filtered.filter((rider: any) => 
      `${rider.imie} ${rider.nazwisko}`.toLowerCase().includes(searchTerm) ||
      rider.nazwisko.toLowerCase().includes(searchTerm) ||
      rider.imie.toLowerCase().includes(searchTerm)
    )
  }
  
  // Filter by category
  if (selectedCategory.value) {
    filtered = filtered.filter((rider: any) => rider.kategoria === selectedCategory.value)
  }
  
  // Filter by club
  if (selectedClub.value) {
    filtered = filtered.filter((rider: any) => rider.klub === selectedClub.value)
  }
  
  // Filter by gender
  if (selectedGender.value) {
    filtered = filtered.filter((rider: any) => rider.plec === selectedGender.value)
  }
  
  // Sorting
  if (sortBy.value === 'pozycja_asc') {
    // Default ranking order (by points descending, then by best time)
    filtered.sort((a: any, b: any) => parseFloat(b.punkty) - parseFloat(a.punkty))
  } else if (sortBy.value === 'pozycja_desc') {
    filtered.sort((a: any, b: any) => parseFloat(a.punkty) - parseFloat(b.punkty))
  } else if (sortBy.value === 'punkty_desc') {
    filtered.sort((a: any, b: any) => parseFloat(b.punkty) - parseFloat(a.punkty))
  } else if (sortBy.value === 'punkty_asc') {
    filtered.sort((a: any, b: any) => parseFloat(a.punkty) - parseFloat(b.punkty))
  } else if (sortBy.value === 'nazwisko_asc') {
    filtered.sort((a: any, b: any) => a.nazwisko.localeCompare(b.nazwisko))
  } else if (sortBy.value === 'nazwisko_desc') {
    filtered.sort((a: any, b: any) => b.nazwisko.localeCompare(a.nazwisko))
  } else if (sortBy.value === 'klub_asc') {
    filtered.sort((a: any, b: any) => (a.klub || '').localeCompare(b.klub || ''))
  } else if (sortBy.value === 'kategoria_asc') {
    filtered.sort((a: any, b: any) => a.kategoria.localeCompare(b.kategoria))
  } else if (sortBy.value === 'starty_desc') {
    filtered.sort((a: any, b: any) => parseInt(b.liczba_zawodow) - parseInt(a.liczba_zawodow))
  }
  
  // Update pagination data
  const totalResults = filtered.length
  const totalPages = Math.ceil(totalResults / perPageIndividual.value)
  const startIndex = (currentPageIndividual.value - 1) * perPageIndividual.value + 1
  const endIndex = Math.min(currentPageIndividual.value * perPageIndividual.value, totalResults)
  
  paginationDataIndividual.value = {
    current_page: currentPageIndividual.value,
    total_pages: totalPages,
    total_results: totalResults,
    per_page: perPageIndividual.value,
    has_next: currentPageIndividual.value < totalPages,
    has_prev: currentPageIndividual.value > 1,
    start_index: totalResults > 0 ? startIndex : 0,
    end_index: totalResults > 0 ? endIndex : 0
  }
  
  // Return paginated results
  const start = (currentPageIndividual.value - 1) * perPageIndividual.value
  const end = start + perPageIndividual.value
  return filtered.slice(start, end)
})

const paginatedGeneralRanking = computed(() => {
  let filtered = generalRanking.value
  
  // Filter by search query
  if (searchQueryGeneral.value.trim()) {
    const searchTerm = searchQueryGeneral.value.trim().toLowerCase()
    filtered = filtered.filter((rider: any) => 
      `${rider.imie} ${rider.nazwisko}`.toLowerCase().includes(searchTerm) ||
      rider.nazwisko.toLowerCase().includes(searchTerm) ||
      rider.imie.toLowerCase().includes(searchTerm)
    )
  }
  
  // Filter by category
  if (selectedCategoryGeneral.value) {
    filtered = filtered.filter((rider: any) => rider.kategoria === selectedCategoryGeneral.value)
  }
  
  // Filter by club
  if (selectedClubGeneral.value) {
    filtered = filtered.filter((rider: any) => rider.klub === selectedClubGeneral.value)
  }
  
  // Filter by gender
  if (selectedGenderGeneral.value) {
    filtered = filtered.filter((rider: any) => rider.plec === selectedGenderGeneral.value)
  }
  
  // Sorting
  if (sortByGeneral.value === 'punkty_desc') {
    filtered.sort((a: any, b: any) => parseFloat(b.punkty_koncowe) - parseFloat(a.punkty_koncowe))
  } else if (sortByGeneral.value === 'punkty_asc') {
    filtered.sort((a: any, b: any) => parseFloat(a.punkty_koncowe) - parseFloat(b.punkty_koncowe))
  } else if (sortByGeneral.value === 'nazwisko_asc') {
    filtered.sort((a: any, b: any) => a.nazwisko.localeCompare(b.nazwisko))
  } else if (sortByGeneral.value === 'nazwisko_desc') {
    filtered.sort((a: any, b: any) => b.nazwisko.localeCompare(a.nazwisko))
  } else if (sortByGeneral.value === 'kategoria_asc') {
    filtered.sort((a: any, b: any) => a.kategoria.localeCompare(b.kategoria))
  } else if (sortByGeneral.value === 'starty_desc') {
    filtered.sort((a: any, b: any) => parseInt(b.uczestnictwa) - parseInt(a.uczestnictwa))
  } else if (sortByGeneral.value === 'odrzucone_desc') {
    filtered.sort((a: any, b: any) => parseInt(b.odrzucone || 0) - parseInt(a.odrzucone || 0))
  }
  
  // Update pagination data
  const totalResults = filtered.length
  const totalPages = Math.ceil(totalResults / perPageGeneral.value)
  const startIndex = (currentPageGeneral.value - 1) * perPageGeneral.value + 1
  const endIndex = Math.min(currentPageGeneral.value * perPageGeneral.value, totalResults)
  
  paginationDataGeneral.value = {
    current_page: currentPageGeneral.value,
    total_pages: totalPages,
    total_results: totalResults,
    per_page: perPageGeneral.value,
    has_next: currentPageGeneral.value < totalPages,
    has_prev: currentPageGeneral.value > 1,
    start_index: totalResults > 0 ? startIndex : 0,
    end_index: totalResults > 0 ? endIndex : 0
  }
  
  // Return paginated results
  const start = (currentPageGeneral.value - 1) * perPageGeneral.value
  const end = start + perPageGeneral.value
  return filtered.slice(start, end)
})

const filteredClubsTotal = computed(() => {
  let filtered = clubRankingTotal.value
  
  // Filter by minimum zawodnikow
  if (minZawodnikow.value) {
    filtered = filtered.filter(club => parseInt(club.liczba_zawodnikow) >= parseInt(minZawodnikow.value))
  }
  
  // Sorting
  if (sortByClubsTotal.value === 'punkty_desc') {
    filtered.sort((a, b) => parseFloat(b.laczne_punkty) - parseFloat(a.laczne_punkty))
  } else if (sortByClubsTotal.value === 'punkty_asc') {
    filtered.sort((a, b) => parseFloat(a.laczne_punkty) - parseFloat(b.laczne_punkty))
  } else if (sortByClubsTotal.value === 'srednia_desc') {
    filtered.sort((a, b) => parseFloat(b.srednia) - parseFloat(a.srednia))
  } else if (sortByClubsTotal.value === 'srednia_asc') {
    filtered.sort((a, b) => parseFloat(a.srednia) - parseFloat(b.srednia))
  } else if (sortByClubsTotal.value === 'zawodnicy_desc') {
    filtered.sort((a, b) => parseInt(b.liczba_zawodnikow) - parseInt(a.liczba_zawodnikow))
  } else if (sortByClubsTotal.value === 'zawodnicy_asc') {
    filtered.sort((a, b) => parseInt(a.liczba_zawodnikow) - parseInt(b.liczba_zawodnikow))
  } else if (sortByClubsTotal.value === 'nazwa_asc') {
    filtered.sort((a, b) => a.klub.localeCompare(b.klub))
  } else if (sortByClubsTotal.value === 'nazwa_desc') {
    filtered.sort((a, b) => b.klub.localeCompare(a.klub))
  }
  
  return filtered
})

const filteredClubsTop3 = computed(() => {
  let filtered = clubRankingTop3.value
  
  // Filter by minimum aktywnych kategorii
  if (minKategorie.value) {
    filtered = filtered.filter(club => parseInt(club.aktywne_kategorie) >= parseInt(minKategorie.value))
  }
  
  // Sorting
  if (sortByClubsTop3.value === 'punkty_desc') {
    filtered.sort((a, b) => parseFloat(b.punkty_top3) - parseFloat(a.punkty_top3))
  } else if (sortByClubsTop3.value === 'punkty_asc') {
    filtered.sort((a, b) => parseFloat(a.punkty_top3) - parseFloat(b.punkty_top3))
  } else if (sortByClubsTop3.value === 'kategorie_desc') {
    filtered.sort((a, b) => parseInt(b.aktywne_kategorie) - parseInt(a.aktywne_kategorie))
  } else if (sortByClubsTop3.value === 'kategorie_asc') {
    filtered.sort((a, b) => parseInt(a.aktywne_kategorie) - parseInt(b.aktywne_kategorie))
  } else if (sortByClubsTop3.value === 'balance_desc') {
    filtered.sort((a, b) => parseFloat(b.balance) - parseFloat(a.balance))
  } else if (sortByClubsTop3.value === 'balance_asc') {
    filtered.sort((a, b) => parseFloat(a.balance) - parseFloat(b.balance))
  } else if (sortByClubsTop3.value === 'nazwa_asc') {
    filtered.sort((a, b) => a.klub.localeCompare(b.klub))
  } else if (sortByClubsTop3.value === 'nazwa_desc') {
    filtered.sort((a, b) => b.klub.localeCompare(a.klub))
  }
  
  return filtered
})

const filteredMedalRanking = computed(() => {
  let filtered = medalRanking.value
  
  // Filter by minimum złotych medali
  if (minZlote.value) {
    filtered = filtered.filter(club => parseInt(club.zlote) >= parseInt(minZlote.value))
  }
  
  // Sorting
  if (sortByMedals.value === 'zlote_desc') {
    filtered.sort((a, b) => parseInt(b.zlote) - parseInt(a.zlote) || parseInt(b.srebrne) - parseInt(a.srebrne) || parseInt(b.brazowe) - parseInt(a.brazowe))
  } else if (sortByMedals.value === 'zlote_asc') {
    filtered.sort((a, b) => parseInt(a.zlote) - parseInt(b.zlote))
  } else if (sortByMedals.value === 'srebrne_desc') {
    filtered.sort((a, b) => parseInt(b.srebrne) - parseInt(a.srebrne))
  } else if (sortByMedals.value === 'srebrne_asc') {
    filtered.sort((a, b) => parseInt(a.srebrne) - parseInt(b.srebrne))
  } else if (sortByMedals.value === 'brazowe_desc') {
    filtered.sort((a, b) => parseInt(b.brazowe) - parseInt(a.brazowe))
  } else if (sortByMedals.value === 'brazowe_asc') {
    filtered.sort((a, b) => parseInt(a.brazowe) - parseInt(b.brazowe))
  } else if (sortByMedals.value === 'lacznie_desc') {
    filtered.sort((a, b) => parseInt(b.lacznie) - parseInt(a.lacznie))
  } else if (sortByMedals.value === 'lacznie_asc') {
    filtered.sort((a, b) => parseInt(a.lacznie) - parseInt(b.lacznie))
  } else if (sortByMedals.value === 'nazwa_asc') {
    filtered.sort((a, b) => a.klub.localeCompare(b.klub))
  } else if (sortByMedals.value === 'nazwa_desc') {
    filtered.sort((a, b) => b.klub.localeCompare(a.klub))
  }
  
  return filtered
})

const isEmpty = computed(() => {
  return individualRanking.value.length === 0 && 
         generalRanking.value.length === 0 && 
         clubRankingTotal.value.length === 0 && 
         medalRanking.value.length === 0
})

// Methods
const refreshRankings = async () => {
  if (loading.value) {
    console.log('🚫 Refresh już w toku, przerywam')
    return
  }
  
  loading.value = true
  console.log('🔄 ROZPOCZYNAM refresh rankings...')
  
  try {
    // Fetch all ranking data from API
    await Promise.all([
      fetchTimeRanking(),
      fetchIndividualRanking(), 
      fetchGeneralRanking(),
      fetchClubRankings(),
      fetchMedalRanking()
    ])
    // Aktualizuj timestamp cache po udanym pobraniu
    lastFetchTime.value = Date.now()
    console.log('✅ ZAKOŃCZONO refresh rankings - wszystkie dane pobrane')
  } catch (error) {
    console.error('❌ Error fetching rankings:', error)
    // Nie czyścimy danych przy błędzie - zachowujemy cache
  } finally {
    loading.value = false
  }
}

const clearMedalsFilters = () => {
  minZlote.value = null
  sortByMedals.value = 'zlote_desc'
}

// Watch activeTab - nie pobieraj danych za każdym razem
watch(activeTab, (newTab, oldTab) => {
  console.log('🔀 Tab changed:', oldTab, '->', newTab)
  
  if (newTab === 'times') {
    // Fetch fresh data when switching to times tab
    fetchTimeRanking()
  } else {
    const now = Date.now()
    if (now - lastFetchTime.value > CACHE_DURATION) {
      console.log('📅 Cache wygasł, pobieram świeże dane...')
      refreshRankings()
    }
  }
})

// Watch selectedSeason - tylko wtedy pobieraj nowe dane
watch(selectedSeason, () => {
  console.log('📅 Zmiana sezonu na:', selectedSeason.value)
  refreshRankings()
})

// Lifecycle
onMounted(() => {
  refreshRankings()
})

// ===== TIME RANKING API FUNCTIONS =====
const fetchTimeRanking = async () => {
  console.log('🕐 Pobieranie rankingu czasowego...')
  try {
    const params = new URLSearchParams({
      typ: 'best',  // Always use best times
      status: selectedStatusTime.value,
      limit: perPageTime.value.toString(),
      page: currentPageTime.value.toString(),
      sort: sortByTime.value
    })
    
    if (selectedKategoriaTime.value) params.append('kategoria', selectedKategoriaTime.value)
    if (selectedPlecTime.value) params.append('plec', selectedPlecTime.value)
    if (selectedKlubTime.value) params.append('klub', selectedKlubTime.value)
    if (searchQueryTime.value.trim()) params.append('search', searchQueryTime.value.trim())
    
    const response = await fetch(`/api/rankings/times?${params}&_t=${Date.now()}`)
    console.log('📡 Time ranking response status:', response.status)
    
    if (response.ok) {
      const result = await response.json()
      console.log('✅ Time ranking data received:', result.data?.ranking?.length || 0, 'items')
      timeRanking.value = result.data?.ranking || []
      paginationDataTime.value = result.data?.pagination || paginationDataTime.value
      console.log("✅ timeRanking updated, length:", timeRanking.value.length)
      console.log("📊 Pagination:", paginationDataTime.value)
    } else {
      console.error('❌ Time ranking response not ok:', response.status, response.statusText)
    }
  } catch (error) {
    console.error('❌ Error fetching time ranking:', error)
  }
}

// Pagination controls
const nextPageTime = () => {
  if (paginationDataTime.value.has_next) {
    currentPageTime.value++
    fetchTimeRanking()
  }
}

const previousPageTime = () => {
  if (paginationDataTime.value.has_prev) {
    currentPageTime.value--
    fetchTimeRanking()
  }
}

const goToPageTime = (page) => {
  if (page >= 1 && page <= paginationDataTime.value.total_pages) {
    currentPageTime.value = page
    fetchTimeRanking()
  }
}

// Per page controls  
const changePerPageTime = () => {
  currentPageTime.value = 1  // Reset to first page
  fetchTimeRanking()
}

// Watch time ranking filters
watch([selectedStatusTime], () => {
  console.log('🔄 Time ranking filters changed, fetching new data...')
  currentPageTime.value = 1  // Reset to first page
  fetchTimeRanking()
})

// FIXED: Add missing watchers for all time ranking filters
watch([selectedKategoriaTime, selectedPlecTime, selectedKlubTime, sortByTime], () => {
  console.log('🔄 Time ranking filters/sort changed, fetching new data...')
  currentPageTime.value = 1  // Reset to first page
  fetchTimeRanking()
})

// Watch search query
watch(searchQueryTime, (newQuery) => {
  console.log('🔍 Search query changed:', newQuery)
  debouncedSearchTime(newQuery)
})

// Clear time ranking filters
const clearTimeFilters = () => {
  selectedKategoriaTime.value = ''
  selectedPlecTime.value = ''
  selectedKlubTime.value = ''
  selectedStatusTime.value = 'completed'
  sortByTime.value = 'time_asc'
  searchQueryTime.value = ''
  currentPageTime.value = 1
  perPageTime.value = 25
}

// PAGINATION FUNCTIONS FOR INDIVIDUAL
const nextPageIndividual = () => {
  if (paginationDataIndividual.value.has_next) {
    currentPageIndividual.value++
  }
}

const previousPageIndividual = () => {
  if (paginationDataIndividual.value.has_prev) {
    currentPageIndividual.value--
  }
}

const goToPageIndividual = (page: number) => {
  if (page >= 1 && page <= paginationDataIndividual.value.total_pages) {
    currentPageIndividual.value = page
  }
}

const changePerPageIndividual = () => {
  currentPageIndividual.value = 1  // Reset to first page
}

// PAGINATION FUNCTIONS FOR GENERAL
const nextPageGeneral = () => {
  if (paginationDataGeneral.value.has_next) {
    currentPageGeneral.value++
  }
}

const previousPageGeneral = () => {
  if (paginationDataGeneral.value.has_prev) {
    currentPageGeneral.value--
  }
}

const goToPageGeneral = (page: number) => {
  if (page >= 1 && page <= paginationDataGeneral.value.total_pages) {
    currentPageGeneral.value = page
  }
}

const changePerPageGeneral = () => {
  currentPageGeneral.value = 1  // Reset to first page
}

// HELPER FUNCTIONS FOR FILTERS
const clearAllFilters = () => {
  selectedCategory.value = ''
  selectedClub.value = ''
  selectedGender.value = ''
  sortBy.value = 'pozycja_asc'
  searchQuery.value = ''
  currentPageIndividual.value = 1
  perPageIndividual.value = 25
}

const clearGeneralFilters = () => {
  selectedCategoryGeneral.value = ''
  selectedClubGeneral.value = ''
  selectedGenderGeneral.value = ''
  sortByGeneral.value = 'punkty_desc'
  searchQueryGeneral.value = ''
  currentPageGeneral.value = 1
  perPageGeneral.value = 25
}

const clearClubsTotalFilters = () => {
  minZawodnikow.value = null
  sortByClubsTotal.value = 'punkty_desc'
}

const clearClubsTop3Filters = () => {
  minKategorie.value = null
  sortByClubsTop3.value = 'punkty_desc'
}

// Helper function for time formatting  
const formatTime = (seconds) => {
  if (!seconds) return '--:--'
  const totalSeconds = parseFloat(seconds)
  const minutes = Math.floor(totalSeconds / 60)
  const secs = (totalSeconds % 60).toFixed(3)
  return `${minutes}:${secs.padStart(6, '0')}`
}

// MISSING FUNCTIONS - RANKING DATA FETCHERS WITH CACHE-BUSTING
const fetchIndividualRanking = async () => {
  console.log('🔍 Pobieranie rankingu indywidualnego...')
  try {
    const response = await fetch(`/api/rankings/individual?season=${selectedSeason.value}&_t=${Date.now()}`)
    console.log('📡 Individual response status:', response.status)
    if (response.ok) {
      const result = await response.json()
      console.log('✅ Individual data received:', result.data?.length || 0, 'items')
      individualRanking.value = result.data || []
      console.log("✅ individualRanking updated, length:", individualRanking.value.length)
    } else {
      console.error('❌ Individual ranking response not ok:', response.status, response.statusText)
    }
  } catch (error) {
    console.error('❌ Error fetching individual ranking:', error)
  }
}

const fetchGeneralRanking = async () => {
  console.log('🔍 Pobieranie rankingu generalnego...')
  try {
    const response = await fetch(`/api/rankings/general?season=${selectedSeason.value}&_t=${Date.now()}`)
    console.log('📡 General response status:', response.status)
    if (response.ok) {
      const result = await response.json()
      console.log('✅ General data received:', result.data?.length || 0, 'items')
      generalRanking.value = result.data || []
      console.log("✅ generalRanking updated, length:", generalRanking.value.length)
    } else {
      console.error('❌ General ranking response not ok:', response.status, response.statusText)
    }
  } catch (error) {
    console.error('❌ Error fetching general ranking:', error)
  }
}

const fetchClubRankings = async () => {
  console.log('🔍 Pobieranie rankingów klubowych...')
  try {
    const [totalResponse, top3Response] = await Promise.all([
      fetch(`/api/rankings/clubs/total?season=${selectedSeason.value}&_t=${Date.now()}`),
      fetch(`/api/rankings/clubs/top3?season=${selectedSeason.value}&_t=${Date.now()}`)
    ])
    
    console.log('📡 Club total response status:', totalResponse.status)
    console.log('📡 Club top3 response status:', top3Response.status)
    
    if (totalResponse.ok) {
      const result = await totalResponse.json()
      console.log('✅ Club total data received:', result.data?.length || 0, 'items')
      clubRankingTotal.value = result.data || []
      console.log("✅ clubRankingTotal updated, length:", clubRankingTotal.value.length)
    } else {
      console.error('❌ Club total ranking response not ok:', totalResponse.status, totalResponse.statusText)
    }
    
    if (top3Response.ok) {
      const result = await top3Response.json()
      console.log('✅ Club top3 data received:', result.data?.length || 0, 'items')
      clubRankingTop3.value = result.data || []
      console.log("✅ clubRankingTop3 updated, length:", clubRankingTop3.value.length)
    } else {
      console.error('❌ Club top3 ranking response not ok:', top3Response.status, top3Response.statusText)
    }
  } catch (error) {
    console.error('❌ Error fetching club rankings:', error)
  }
}

const fetchMedalRanking = async () => {
  console.log('🔍 Pobieranie rankingu medalowego...')
  try {
    const response = await fetch(`/api/rankings/medals?season=${selectedSeason.value}&_t=${Date.now()}`)
    console.log('📡 Medal response status:', response.status)
    if (response.ok) {
      const result = await response.json()
      console.log('✅ Medal data received:', result.data?.length || 0, 'items')
      medalRanking.value = result.data || []
      console.log("✅ medalRanking updated, length:", medalRanking.value.length)
    } else {
      console.error('❌ Medal ranking response not ok:', response.status, response.statusText)
    }
  } catch (error) {
    console.error('❌ Error fetching medal ranking:', error)
  }
}

// Debounced search function
let searchTimeoutTime = null
const debouncedSearchTime = (query) => {
  if (searchTimeoutTime) clearTimeout(searchTimeoutTime)
  searchTimeoutTime = setTimeout(() => {
    currentPageTime.value = 1  // Reset to first page on search
    fetchTimeRanking()
  }, 500)  // 500ms delay
}

</script>

<style scoped>
/* Custom styles for placeholder */
</style> 