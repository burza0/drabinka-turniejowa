<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
    <!-- Header -->
    <header class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700 transition-colors duration-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <!-- Main Header Row -->
        <div class="flex justify-between items-center h-16">
          <!-- Logo/Brand -->
          <div class="flex items-center flex-shrink-0">
            <h1 class="text-lg sm:text-xl font-semibold text-gray-900 dark:text-white transition-colors duration-200">
              <span class="hidden sm:inline">SKATECROSS Dashboard</span>
              <span class="sm:hidden">SKATECROSS</span>
              <span v-if="isAdmin" class="ml-1 sm:ml-2 inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200">
                🔧
                <span class="hidden sm:inline ml-1">ADMIN</span>
              </span>
            </h1>
          </div>
          
          <!-- Search Bar - Desktop tylko w headerze -->
          <div class="hidden sm:block flex-1 max-w-lg mx-8">
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <MagnifyingGlassIcon class="h-5 w-5 text-gray-400" />
              </div>
              <input 
                type="text" 
                class="block w-full pl-10 pr-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg leading-5 bg-white dark:bg-gray-700 placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white focus:outline-none focus:placeholder-gray-400 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-sm transition-colors duration-200 shadow-sm"
                placeholder="Szukaj zawodników..."
                v-model="searchTerm"
              />
            </div>
          </div>
          
          <!-- Header Icons - Compact on mobile -->
          <div class="flex items-center space-x-2 sm:space-x-4">
            <!-- Admin Toggle - More compact on mobile -->
            <div class="flex items-center space-x-1 sm:space-x-2">
              <label class="text-xs sm:text-sm text-gray-600 dark:text-gray-300 hidden sm:inline">Admin:</label>
              <button
                @click="toggleAdminMode"
                :class="[
                  'relative inline-flex h-5 w-9 sm:h-6 sm:w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2',
                  isAdmin ? 'bg-indigo-600' : 'bg-gray-200 dark:bg-gray-600'
                ]"
              >
                <span
                  :class="[
                    'pointer-events-none inline-block h-4 w-4 sm:h-5 sm:w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                    isAdmin ? 'translate-x-4 sm:translate-x-5' : 'translate-x-0'
                  ]"
                />
              </button>
            </div>
            
            <button class="p-1 sm:p-2 text-gray-400 dark:text-gray-300 hover:text-gray-500 dark:hover:text-gray-200">
              <GlobeAltIcon class="h-5 w-5 sm:h-6 sm:w-6" />
            </button>
            <button 
              @click="toggleDarkMode"
              class="p-1 sm:p-2 text-gray-400 dark:text-gray-300 hover:text-gray-500 dark:hover:text-gray-200 transition-colors duration-200"
              :title="isDarkMode ? 'Przełącz na tryb jasny' : 'Przełącz na tryb ciemny'"
            >
              <SunIcon v-if="isDarkMode" class="h-5 w-5 sm:h-6 sm:w-6" />
              <MoonIcon v-else class="h-5 w-5 sm:h-6 sm:w-6" />
            </button>
            
            <!-- User Avatar -->
            <div class="w-7 h-7 sm:w-8 sm:h-8 bg-indigo-500 rounded-full flex items-center justify-center">
              <span class="text-white text-xs sm:text-sm font-medium">{{ isAdmin ? 'A' : 'U' }}</span>
            </div>
          </div>
        </div>
        
        <!-- Search Bar - Below header on mobile -->
        <div class="pb-4 sm:hidden">
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <MagnifyingGlassIcon class="h-4 w-4 text-gray-400" />
            </div>
            <input 
              type="text" 
              class="block w-full pl-9 pr-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md leading-5 bg-white dark:bg-gray-700 placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 text-sm transition-colors duration-200"
              placeholder="Szukaj zawodników..."
              v-model="searchTerm"
            />
          </div>
        </div>
      </div>
    </header>

    <!-- Navigation Tabs -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="border-b border-gray-200 dark:border-gray-700">
        <nav class="-mb-px flex flex-wrap gap-x-4 gap-y-2 sm:space-x-8 sm:gap-y-0" aria-label="Tabs">
          <button
            v-for="tab in filteredTabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="[
              activeTab === tab.id
                ? 'border-indigo-500 text-indigo-600 dark:text-indigo-400'
                : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:border-gray-300 dark:hover:border-gray-600',
              'whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm transition-colors duration-200 flex items-center'
            ]"
          >
            <component :is="tab.icon" class="h-4 w-4 sm:h-5 sm:w-5 mr-1 sm:mr-2" />
            <span class="text-xs sm:text-sm">{{ tab.name }}</span>
          </button>
        </nav>
      </div>
    </div>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- Dashboard -->
      <div v-if="activeTab === 'dashboard'">
        <Dashboard @navigate="handleDashboardNavigation" />
      </div>

      <!-- Zawodnicy -->
      <div v-if="activeTab === 'zawodnicy'" class="space-y-6">
        <!-- Stats -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <StatsCard 
            title="Łącznie zawodników" 
            :value="stats.total.toString()"
            icon="👥"
            color="blue"
            subtitle="Wszyscy zawodnicy"
          />
          <StatsCard 
            title="Ukończyli trasę" 
            :value="stats.finished.toString()"
            icon="✅"
            color="green"
            subtitle="Status FINISHED"
          />
          <StatsCard 
            title="DNF/DSQ" 
            :value="stats.dnfDsq.toString()"
            icon="⚠️"
            color="yellow"
            subtitle="Nie ukończyli"
          />
          <StatsCard 
            title="Najlepszy czas" 
            :value="stats.recordTime"
            icon="🏆"
            color="purple"
            :subtitle="stats.recordHolder !== '-' ? `Rekord: ${stats.recordHolder}` : ''"
          />
        </div>

        <!-- Table -->
        <div class="bg-white dark:bg-gray-800 shadow rounded-lg transition-colors duration-200">
          <!-- Filtry i sortowanie -->
          <div class="px-4 sm:px-6 py-4 border-b border-gray-200 dark:border-gray-700">
            <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-4">
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Filtry i sortowanie</h3>
              <button 
                @click="clearAllFilters"
                class="mt-2 sm:mt-0 px-3 py-1 text-sm bg-red-100 dark:bg-red-900 text-red-700 dark:text-red-300 rounded-md hover:bg-red-200 dark:hover:bg-red-800 transition-colors duration-200 flex items-center"
              >
                🗑️ Wyczyść filtry
              </button>
            </div>

            <!-- Filtry w grid layout -->
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
              <!-- Kategoria -->
              <div>
                <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
                  <span class="flex items-center space-x-2">
                    <span>🏆</span>
                    <span>Kategoria</span>
                  </span>
                </label>
                <select 
                  v-model="zawodnicyFilters.kategoria"
                  class="w-full rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-md focus:border-purple-500 focus:ring-2 focus:ring-purple-500 text-sm font-medium py-2.5 px-3 transition-all duration-200 hover:shadow-lg"
                >
                  <option value="">Wszystkie</option>
                  <option v-for="kategoria in uniqueKategorie" :key="kategoria" :value="kategoria">
                    {{ kategoria }}
                  </option>
                </select>
              </div>

              <!-- Klub -->
              <div>
                <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
                  <span class="flex items-center space-x-2">
                    <span>🏢</span>
                    <span>Klub</span>
                  </span>
                </label>
                <select 
                  v-model="zawodnicyFilters.klub"
                  class="w-full rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-md focus:border-purple-500 focus:ring-2 focus:ring-purple-500 text-sm font-medium py-2.5 px-3 transition-all duration-200 hover:shadow-lg"
                >
                  <option value="">Wszystkie</option>
                  <option v-for="klub in uniqueKluby" :key="klub" :value="klub">
                    {{ klub }}
                  </option>
                </select>
              </div>

              <!-- Status QR -->
              <div>
                <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-2">
                  <span class="flex items-center space-x-2">
                    <span>📱</span>
                    <span>Status QR</span>
                  </span>
                </label>
                <select 
                  v-model="zawodnicyFilters.statusQr"
                  class="w-full rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-md focus:border-purple-500 focus:ring-2 focus:ring-purple-500 text-sm font-medium py-2.5 px-3 transition-all duration-200 hover:shadow-lg"
                >
                  <option value="">Wszystkie</option>
                  <option value="z_qr">Z kodem QR</option>
                  <option value="bez_qr">Bez kodu QR</option>
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
                  v-model="zawodnicyFilters.sortowanie"
                  class="w-full rounded-lg border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-md focus:border-purple-500 focus:ring-2 focus:ring-purple-500 text-sm font-medium py-2.5 px-3 transition-all duration-200 hover:shadow-lg"
                >
                  <option value="nr_startowy_asc">Nr startowy (rosnąco)</option>
                  <option value="nr_startowy_desc">Nr startowy (malejąco)</option>
                  <option value="nazwisko_asc">Nazwisko (A-Z)</option>
                  <option value="nazwisko_desc">Nazwisko (Z-A)</option>
                  <option value="kategoria_asc">Kategoria (A-Z)</option>
                  <option value="klub_asc">Klub (A-Z)</option>
                  <option value="czas_asc">Czas (najlepszy)</option>
                  <option value="czas_desc">Czas (najgorszy)</option>
                </select>
              </div>
            </div>

            <!-- Operacje grupowe -->
            <div class="border-t border-gray-200 dark:border-gray-700 pt-4">
              <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200 mb-3">
                <span class="flex items-center space-x-2">
                  <span>⚡</span>
                  <span>Operacje grupowe</span>
                </span>
              </label>
              <div class="flex flex-wrap gap-3">
                <button 
                  @click="toggleAllZawodnicy"
                  :class="[
                    'px-4 py-2 text-sm font-medium rounded-lg transition-all duration-200 flex items-center space-x-2 border-2',
                    allSelected 
                      ? 'bg-indigo-700 text-white shadow-inner border-indigo-800' 
                      : 'bg-indigo-600 text-white hover:bg-indigo-700 border-transparent'
                  ]"
                >
                  <span>{{ allSelected ? '✅' : '☐' }}</span>
                  <span>{{ allSelected ? 'Odznacz wszystkie' : 'Zaznacz wszystkie' }} ({{ filteredZawodnicyNew.length }})</span>
                </button>
                
                <button 
                  @click="toggleByCategory"
                  :disabled="!zawodnicyFilters.kategoria"
                  :class="[
                    'px-4 py-2 text-sm font-medium rounded-lg transition-all duration-200 flex items-center space-x-2 border-2',
                    !zawodnicyFilters.kategoria 
                      ? 'bg-gray-300 dark:bg-gray-600 text-gray-500 dark:text-gray-400 cursor-not-allowed border-transparent'
                      : categorySelected
                        ? 'bg-green-700 text-white shadow-inner border-green-800'
                        : 'bg-green-600 text-white hover:bg-green-700 border-transparent'
                  ]"
                >
                  <span>{{ !zawodnicyFilters.kategoria ? '🏆' : categorySelected ? '✅' : '☐' }}</span>
                  <span>
                    {{ !zawodnicyFilters.kategoria 
                      ? 'Wybierz kategorię' 
                      : categorySelected 
                        ? `Odznacz: ${zawodnicyFilters.kategoria}` 
                        : `Zaznacz: ${zawodnicyFilters.kategoria}` 
                    }}
                  </span>
                </button>
                
                <button 
                  @click="toggleByClub"
                  :disabled="!zawodnicyFilters.klub"
                  :class="[
                    'px-4 py-2 text-sm font-medium rounded-lg transition-all duration-200 flex items-center space-x-2 border-2',
                    !zawodnicyFilters.klub 
                      ? 'bg-gray-300 dark:bg-gray-600 text-gray-500 dark:text-gray-400 cursor-not-allowed border-transparent'
                      : clubSelected
                        ? 'bg-purple-700 text-white shadow-inner border-purple-800'
                        : 'bg-purple-600 text-white hover:bg-purple-700 border-transparent'
                  ]"
                >
                  <span>{{ !zawodnicyFilters.klub ? '🏢' : clubSelected ? '✅' : '☐' }}</span>
                  <span>
                    {{ !zawodnicyFilters.klub 
                      ? 'Wybierz klub' 
                      : clubSelected 
                        ? `Odznacz: ${zawodnicyFilters.klub}` 
                        : `Zaznacz: ${zawodnicyFilters.klub}` 
                    }}
                  </span>
                </button>
                
                <button 
                  @click="toggleWithoutQr"
                  :class="[
                    'px-4 py-2 text-sm font-medium rounded-lg transition-all duration-200 flex items-center space-x-2 border-2',
                    countWithoutQr === 0
                      ? 'bg-gray-300 dark:bg-gray-600 text-gray-500 dark:text-gray-400 cursor-not-allowed border-transparent'
                      : withoutQrSelected
                        ? 'bg-orange-700 text-white shadow-inner border-orange-800'
                        : 'bg-orange-600 text-white hover:bg-orange-700 border-transparent'
                  ]"
                  :disabled="countWithoutQr === 0"
                >
                  <span>{{ withoutQrSelected ? '✅' : '☐' }}</span>
                  <span>{{ withoutQrSelected ? 'Odznacz bez QR' : 'Zaznacz bez QR' }} ({{ countWithoutQr }})</span>
                </button>
                
                <button 
                  @click="clearSelection"
                  :disabled="selectedZawodnicy.length === 0"
                  :class="[
                    'px-4 py-2 text-sm font-medium rounded-lg transition-all duration-200 flex items-center space-x-2 border-2 border-transparent',
                    selectedZawodnicy.length > 0
                      ? 'bg-gray-600 text-white hover:bg-gray-700'
                      : 'bg-gray-300 dark:bg-gray-600 text-gray-500 dark:text-gray-400 cursor-not-allowed'
                  ]"
                >
                  <span>🗑️</span>
                  <span>Wyczyść zaznaczenia ({{ selectedZawodnicy.length }})</span>
                </button>
              </div>
            </div>
          </div>
          
          <!-- Card Layout for Mobile -->
          <div class="md:hidden p-4 space-y-4">
            <ZawodnikCard 
              v-for="zawodnik in paginatedZawodnicy" 
              :key="zawodnik.nr_startowy"
              :zawodnik="zawodnik"
              :isAdmin="isAdmin"
              @edit="openEditModal"
            />
          </div>
          
          <!-- Table Layout for Desktop -->
          <div class="hidden md:block overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead class="bg-gray-50 dark:bg-gray-700">
                <tr>
                  <th class="px-6 py-3 text-left text-sm font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    <input 
                      type="checkbox" 
                      :checked="allSelected"
                      @change="toggleAllZawodnicy"
                      class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 dark:border-gray-600 rounded"
                    />
                  </th>
                  <th class="px-6 py-3 text-left text-sm font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Nr startowy
                  </th>
                  <th class="px-6 py-3 text-left text-sm font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Klub
                  </th>
                  <th class="px-6 py-3 text-left text-sm font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Zawodnik
                  </th>
                  <th class="px-6 py-3 text-left text-sm font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Kategoria
                  </th>
                  <th class="px-6 py-3 text-left text-sm font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Status
                  </th>
                  <th class="px-6 py-3 text-left text-sm font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Czas
                  </th>
                  <th v-if="isAdmin" class="px-6 py-3 text-left text-sm font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                    Akcje
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                <tr v-for="zawodnik in paginatedZawodnicy" :key="zawodnik.nr_startowy">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <input 
                      type="checkbox" 
                      :checked="selectedZawodnicy.includes(zawodnik.nr_startowy)"
                      @change="toggleZawodnik(zawodnik.nr_startowy)"
                      class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 dark:border-gray-600 rounded"
                    />
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-base font-medium text-gray-900 dark:text-white">
                    {{ zawodnik.nr_startowy }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-base text-gray-600 dark:text-gray-300">
                    {{ zawodnik.klub }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-base font-medium text-gray-900 dark:text-white">
                      {{ zawodnik.imie }} {{ zawodnik.nazwisko }}
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-base text-gray-600 dark:text-gray-300">
                    {{ zawodnik.kategoria }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <StatusBadge :status="zawodnik.status" :checked_in="zawodnik.checked_in" />
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-base font-medium text-gray-900 dark:text-white">
                    {{ zawodnik.czas_przejazdu_s ? formatTime(zawodnik.czas_przejazdu_s) : '-' }}
                  </td>
                  <td v-if="isAdmin" class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                    <div class="flex flex-col space-y-2">
                      <button 
                        @click="openEditModal(zawodnik)"
                        class="inline-flex items-center justify-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 dark:bg-indigo-900 text-indigo-800 dark:text-indigo-200 hover:bg-indigo-200 dark:hover:bg-indigo-800 transition-colors duration-200"
                      >
                        <PencilIcon class="h-3 w-3 mr-1" />
                        Edytuj
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <!-- Kontrolki paginacji -->
          <div v-if="totalPages > 1" class="bg-white dark:bg-gray-800 px-4 py-3 flex items-center justify-between border-t border-gray-200 dark:border-gray-700 sm:px-6">
            <div class="flex-1 flex justify-between sm:hidden">
              <!-- Mobile pagination -->
              <button 
                @click="prevPage"
                :disabled="currentPage <= 1"
                class="relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Poprzednie 50
              </button>
              <button 
                @click="nextPage"
                :disabled="currentPage >= totalPages"
                class="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Następne 50
              </button>
            </div>
            
            <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
              <!-- Desktop pagination info -->
              <div>
                <p class="text-sm text-gray-700 dark:text-gray-300">
                  Pokazano
                  <span class="font-medium">{{ ((currentPage - 1) * itemsPerPage) + 1 }}</span>
                  do
                  <span class="font-medium">{{ Math.min(currentPage * itemsPerPage, totalItems) }}</span>
                  z
                  <span class="font-medium">{{ totalItems }}</span>
                  wyników
                </p>
              </div>
              
              <!-- Desktop pagination controls -->
              <div>
                <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                  <!-- First page -->
                  <button 
                    @click="firstPage"
                    :disabled="currentPage <= 1"
                    class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm font-medium text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <span class="sr-only">Pierwsza strona</span>
                    «
                  </button>
                  
                  <!-- Previous page -->
                  <button 
                    @click="prevPage"
                    :disabled="currentPage <= 1"
                    class="relative inline-flex items-center px-2 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm font-medium text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <span class="sr-only">Poprzednia strona</span>
                    ‹
                  </button>
                  
                  <!-- Page numbers -->
                  <template v-for="page in Math.min(5, totalPages)" :key="page">
                    <button 
                      v-if="page <= totalPages"
                      @click="goToPage(page)"
                      :class="[
                        'relative inline-flex items-center px-4 py-2 border text-sm font-medium',
                        page === currentPage 
                          ? 'z-10 bg-indigo-50 dark:bg-indigo-900 border-indigo-500 text-indigo-600 dark:text-indigo-200' 
                          : 'bg-white dark:bg-gray-800 border-gray-300 dark:border-gray-600 text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700'
                      ]"
                    >
                      {{ page }}
                    </button>
                  </template>
                  
                  <!-- Show dots if there are more pages -->
                  <span v-if="totalPages > 5" class="relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm font-medium text-gray-700 dark:text-gray-300">
                    ...
                  </span>
                  
                  <!-- Next page -->
                  <button 
                    @click="nextPage"
                    :disabled="currentPage >= totalPages"
                    class="relative inline-flex items-center px-2 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm font-medium text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <span class="sr-only">Następna strona</span>
                    ›
                  </button>
                  
                  <!-- Last page -->
                  <button 
                    @click="lastPage"
                    :disabled="currentPage >= totalPages"
                    class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-sm font-medium text-gray-500 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <span class="sr-only">Ostatnia strona</span>
                    »
                  </button>
                </nav>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Drabinka Pucharowa -->
      <div v-if="activeTab === 'drabinka'">
        <DrabinkaPucharowa />
      </div>

      <!-- Rankingi -->
      <div v-if="activeTab === 'rankingi'">
        <Rankingi />
      </div>

      <!-- Unified Start Control -->
      <div v-if="activeTab === 'unified-start'">
        <UnifiedStartControl />
      </div>

      <!-- QR Admin Dashboard -->
      <div v-if="activeTab === 'qr-dashboard'">
        <QrAdminDashboard />
      </div>

      <!-- QR Print -->
      <div v-if="activeTab === 'qr-print'">
        <QrPrint />
      </div>

    </main>

    <!-- Edit Modal -->
    <EditZawodnikModal 
      :show="showEditModal"
      :zawodnik="selectedZawodnik"
      @close="closeEditModal"
      @updated="handleZawodnikUpdated"
      @deleted="handleZawodnikDeleted"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'
import { 
  MagnifyingGlassIcon, 
  GlobeAltIcon, 
  SunIcon, 
  MoonIcon,
  UsersIcon,
  CheckCircleIcon,
  XCircleIcon,
  ClockIcon,
  TrophyIcon,
  ChartBarIcon,
  ListBulletIcon,
  PencilIcon,
  TrashIcon,
  PlusIcon,
  QrCodeIcon,
  ArrowPathIcon,
  ArrowDownTrayIcon,
  DevicePhoneMobileIcon,
  ExclamationTriangleIcon,
  WrenchScrewdriverIcon,
  DocumentTextIcon,
  UserGroupIcon,
  PrinterIcon
} from '@heroicons/vue/24/outline'
import StatsCard from './components/StatsCard.vue'
import StatusBadge from './components/StatusBadge.vue'
import ZawodnikCard from './components/ZawodnikCard.vue'
import DrabinkaPucharowa from './components/DrabinkaPucharowa.vue'
import EditZawodnikModal from './components/EditZawodnikModal.vue'
import Rankingi from './components/Rankingi.vue'

import QrAdminDashboard from './components/QrAdminDashboard.vue'
import QrPrint from './components/QrPrint.vue'
import QrPrintAdvanced from './components/QrPrintAdvanced.vue'
import Dashboard from './components/Dashboard.vue'
import UnifiedStartControl from './components/unified/UnifiedStartControl.vue'


// Types
interface Zawodnik {
  nr_startowy: number
  imie: string
  nazwisko: string
  kategoria: string
  plec: string
  klub: string
  qr_code?: string
  czas_przejazdu_s?: number | null
  status?: string
  checked_in?: boolean
  id?: number
}

interface Stats {
  total: number
  finished: number
  dnfDsq: number
  recordTime: string
  recordHolder: string
}

// Reactive variables
const zawodnicy = ref<Zawodnik[]>([])
const searchTerm = ref('')
const isAdmin = ref(true)
const isDarkMode = ref(localStorage.getItem('darkMode') === 'true')
const loading = ref(true)
const error = ref<string | null>(null)
const showEditModal = ref(false)
const selectedZawodnik = ref<Zawodnik | null>(null)
const activeTab = ref('unified-start')
const filters = ref({
  kluby: [],
  kategorie: [],
  plcie: [],
  statusy: []
})
const zawodnicyFilters = ref({
  kategoria: '',
  klub: '',
  statusQr: '',
  sortowanie: 'nr_startowy_asc'
})
const selectedZawodnicy = ref<number[]>([])

// Client-side paginacja
const currentPage = ref(1)
const itemsPerPage = 50
const totalItems = computed(() => filteredZawodnicyNew.value.length)
const totalPages = computed(() => Math.ceil(totalItems.value / itemsPerPage))

// Tabs configuration
const tabs = [
  { id: 'dashboard', name: 'Dashboard', icon: ChartBarIcon, adminOnly: false },
  { id: 'zawodnicy', name: 'Zawodnicy', icon: UsersIcon, adminOnly: false },
  { id: 'drabinka', name: 'Drabinka', icon: TrophyIcon, adminOnly: false },
  { id: 'rankingi', name: 'Rankingi', icon: ListBulletIcon, adminOnly: false },
  { id: 'unified-start', name: 'Start Control', icon: ClockIcon, adminOnly: true },
  { id: 'qr-print', name: 'Drukowanie QR', icon: PrinterIcon, adminOnly: true },
  { id: 'qr-dashboard', name: 'QR Dashboard', icon: QrCodeIcon, adminOnly: true },
]

// Computed
const filteredZawodnicyNew = computed(() => {
  let result = zawodnicy.value
  
  // Filtrowanie tekstowe
  if (searchTerm.value) {
    const term = searchTerm.value.toLowerCase()
    result = result.filter(z => 
      z.imie.toLowerCase().includes(term) ||
      z.nazwisko.toLowerCase().includes(term) ||
      z.kategoria.toLowerCase().includes(term) ||
      z.nr_startowy.toString().includes(term) ||
      z.klub.toLowerCase().includes(term)
    )
  }
  
  // Filtrowanie po kategorii
  if (zawodnicyFilters.value.kategoria) {
    result = result.filter(z => z.kategoria === zawodnicyFilters.value.kategoria)
  }
  
  // Filtrowanie po klubie
  if (zawodnicyFilters.value.klub) {
    result = result.filter(z => z.klub === zawodnicyFilters.value.klub)
  }
  
  // Filtrowanie po statusie QR
  if (zawodnicyFilters.value.statusQr === 'z_qr') {
    result = result.filter(z => z.qr_code)
  } else if (zawodnicyFilters.value.statusQr === 'bez_qr') {
    result = result.filter(z => !z.qr_code)
  }
  
  // Sortowanie
  if (zawodnicyFilters.value.sortowanie === 'nr_startowy_asc') {
    result.sort((a, b) => a.nr_startowy - b.nr_startowy)
  } else if (zawodnicyFilters.value.sortowanie === 'nr_startowy_desc') {
    result.sort((a, b) => b.nr_startowy - a.nr_startowy)
  } else if (zawodnicyFilters.value.sortowanie === 'nazwisko_asc') {
    result.sort((a, b) => `${a.nazwisko} ${a.imie}`.localeCompare(`${b.nazwisko} ${b.imie}`))
  } else if (zawodnicyFilters.value.sortowanie === 'nazwisko_desc') {
    result.sort((a, b) => `${b.nazwisko} ${b.imie}`.localeCompare(`${a.nazwisko} ${a.imie}`))
  } else if (zawodnicyFilters.value.sortowanie === 'kategoria_asc') {
    result.sort((a, b) => a.kategoria.localeCompare(b.kategoria))
  } else if (zawodnicyFilters.value.sortowanie === 'klub_asc') {
    result.sort((a, b) => a.klub.localeCompare(b.klub))
  } else if (zawodnicyFilters.value.sortowanie === 'czas_asc') {
    result.sort((a, b) => {
      if (!a.czas_przejazdu_s && !b.czas_przejazdu_s) return 0
      if (!a.czas_przejazdu_s) return 1
      if (!b.czas_przejazdu_s) return -1
      return a.czas_przejazdu_s - b.czas_przejazdu_s
    })
  } else if (zawodnicyFilters.value.sortowanie === 'czas_desc') {
    result.sort((a, b) => {
      if (!a.czas_przejazdu_s && !b.czas_przejazdu_s) return 0
      if (!a.czas_przejazdu_s) return 1
      if (!b.czas_przejazdu_s) return -1
      return b.czas_przejazdu_s - a.czas_przejazdu_s
    })
  }
  
  return result
})

// Client-side pagination - zwraca tylko aktualną stronę przefiltrowanych wyników
const paginatedZawodnicy = computed(() => {
  const startIndex = (currentPage.value - 1) * itemsPerPage
  const endIndex = startIndex + itemsPerPage
  return filteredZawodnicyNew.value.slice(startIndex, endIndex)
})

const stats = computed((): Stats => {
  const total = zawodnicy.value.length
  const finished = zawodnicy.value.filter(z => z.status === 'FINISHED' || z.checked_in === true).length
  const dnfDsq = zawodnicy.value.filter(z => z.status === 'DNF' || z.status === 'DSQ' || z.checked_in === false).length
  
  const finishedContestants = zawodnicy.value.filter(z => (z.status === 'FINISHED' || z.checked_in === true) && z.czas_przejazdu_s)
  
  let recordTime = '-'
  let recordHolder = '-'
  
  if (finishedContestants.length > 0) {
    const bestContestant = finishedContestants.reduce((best, current) => 
      current.czas_przejazdu_s! < best.czas_przejazdu_s! ? current : best
    )
    recordTime = formatTime(bestContestant.czas_przejazdu_s!)
    recordHolder = `${bestContestant.imie} ${bestContestant.nazwisko}`
  }

  return { total, finished, dnfDsq, recordTime, recordHolder }
})

const uniqueKluby = computed(() => {
  return [...new Set(zawodnicy.value.map(z => z.klub))]
})

const uniqueKategorie = computed(() => {
  return [...new Set(zawodnicy.value.map(z => z.kategoria))]
})

const filteredTabs = computed(() => {
  return tabs.filter(tab => !tab.adminOnly || isAdmin.value)
})

// Computed properties dla operacji grupowych
const allSelected = computed(() => 
  filteredZawodnicyNew.value.length > 0 && 
  filteredZawodnicyNew.value.every(z => selectedZawodnicy.value.includes(z.nr_startowy))
)

const categorySelected = computed(() => {
  if (!zawodnicyFilters.value.kategoria) return false
  const categoryMembers = filteredZawodnicyNew.value.filter(z => z.kategoria === zawodnicyFilters.value.kategoria)
  return categoryMembers.length > 0 && categoryMembers.every(z => selectedZawodnicy.value.includes(z.nr_startowy))
})

const clubSelected = computed(() => {
  if (!zawodnicyFilters.value.klub) return false
  const clubMembers = filteredZawodnicyNew.value.filter(z => z.klub === zawodnicyFilters.value.klub)
  return clubMembers.length > 0 && clubMembers.every(z => selectedZawodnicy.value.includes(z.nr_startowy))
})

const withoutQrSelected = computed(() => {
  const withoutQrMembers = filteredZawodnicyNew.value.filter(z => !z.qr_code)
  return withoutQrMembers.length > 0 && withoutQrMembers.every(z => selectedZawodnicy.value.includes(z.nr_startowy))
})

const countWithoutQr = computed(() => filteredZawodnicyNew.value.filter(z => !z.qr_code).length)

const filteredZawodnicy = computed(() => {
  let result = zawodnicy.value
  
  // Filtrowanie tekstowe
  if (searchTerm.value) {
    const term = searchTerm.value.toLowerCase()
    result = result.filter(z => 
      z.imie.toLowerCase().includes(term) ||
      z.nazwisko.toLowerCase().includes(term) ||
      z.kategoria.toLowerCase().includes(term) ||
      z.nr_startowy.toString().includes(term) ||
      z.klub.toLowerCase().includes(term)
    )
  }
  
  // Filtrowanie po klubie
  if (filters.value.kluby.length > 0) {
    result = result.filter(z => filters.value.kluby.includes(z.klub))
  }
  
  // Filtrowanie po kategorii
  if (filters.value.kategorie.length > 0) {
    result = result.filter(z => filters.value.kategorie.includes(z.kategoria))
  }
  
  // Filtrowanie po płci
  if (filters.value.plcie.length > 0) {
    result = result.filter(z => filters.value.plcie.includes(z.plec))
  }
  
  // Filtrowanie po statusie
  if (filters.value.statusy.length > 0) {
    result = result.filter(z => filters.value.statusy.includes(z.status))
  }
  
  return result
})

// Methods
const formatTime = (seconds: number): string => {
  const mins = Math.floor(seconds / 60)
  const secs = (seconds % 60).toFixed(2)
  return `${mins}:${secs.padStart(5, '0')}`
}

const fetchZawodnicy = async () => {
  try {
    loading.value = true
    // Pobierz WSZYSTKICH zawodników jednym zapytaniem
    const response = await axios.get(`/api/zawodnicy?limit=1000`)
    
    // Backend zwraca obiekt z paginacją
    if (response.data.success) {
      zawodnicy.value = response.data.data || []
    } else {
      // Fallback dla starszego formatu
      zawodnicy.value = response.data.data || response.data || []
    }
    
    console.log(`✅ Pobrano ${zawodnicy.value.length} zawodników dla client-side pagination`)
  } catch (error) {
    console.error('Błąd podczas pobierania zawodników:', error)
    error.value = 'Nie udało się pobrać danych zawodników'
  } finally {
    loading.value = false
  }
}

const clearFilters = () => {
  filters.value = {
    kluby: [],
    kategorie: [],
    plcie: [],
    statusy: []
  }
}

const selectAllClubs = () => {
  filters.value.kluby = [...uniqueKluby.value]
}

const selectAllCategories = () => {
  filters.value.kategorie = [...uniqueKategorie.value]
}

const selectFinishedOnly = () => {
  filters.value.statusy = ['FINISHED']
}

const toggleFilter = (filterType: keyof typeof filters.value, value: string) => {
  const currentFilter = filters.value[filterType]
  if (currentFilter.includes(value)) {
    filters.value[filterType] = currentFilter.filter(v => v !== value)
  } else {
    filters.value[filterType] = [...currentFilter, value]
  }
}

const toggleAdminMode = () => {
  isAdmin.value = !isAdmin.value
}

const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value
  // Zapisz preferencje w localStorage
  localStorage.setItem("darkMode", isDarkMode.value.toString())
  // Aplikuj dark mode do dokumentu
  if (isDarkMode.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}

// Modal functions
const openEditModal = (zawodnik: Zawodnik) => {
  selectedZawodnik.value = zawodnik
  showEditModal.value = true
}

const closeEditModal = () => {
  showEditModal.value = false
  selectedZawodnik.value = null
}

const handleZawodnikUpdated = () => {
  // Refresh data after update
  fetchZawodnicy()
  // Inicjalizacja dark mode na podstawie localStorage
  if (isDarkMode.value) {
    document.documentElement.classList.add("dark")
  } else {
    document.documentElement.classList.remove("dark")
  }
}

const handleZawodnikDeleted = () => {
  // Refresh data after delete
  fetchZawodnicy()
  // Inicjalizacja dark mode na podstawie localStorage
  if (isDarkMode.value) {
    document.documentElement.classList.add("dark")
  } else {
    document.documentElement.classList.remove("dark")
  }
}

const openAddModal = () => {
  selectedZawodnik.value = null
  showEditModal.value = true
}

const clearAllFilters = () => {
  zawodnicyFilters.value = {
    kategoria: '',
    klub: '',
    statusQr: '',
    sortowanie: 'nr_startowy_asc'
  }
  selectedZawodnicy.value = []
}

const toggleZawodnik = (nrStartowy: number) => {
  const index = selectedZawodnicy.value.indexOf(nrStartowy)
  if (index > -1) {
    selectedZawodnicy.value.splice(index, 1)
  } else {
    selectedZawodnicy.value.push(nrStartowy)
  }
}

const toggleAllZawodnicy = () => {
  if (allSelected.value) {
    // Odznacz wszystkich z filtrowanych
    const filteredNumbers = filteredZawodnicyNew.value.map(z => z.nr_startowy)
    selectedZawodnicy.value = selectedZawodnicy.value.filter(nr => !filteredNumbers.includes(nr))
  } else {
    // Zaznacz wszystkich z filtrowanych
    const filteredNumbers = filteredZawodnicyNew.value.map(z => z.nr_startowy)
    const uniqueNumbers = [...new Set([...selectedZawodnicy.value, ...filteredNumbers])]
    selectedZawodnicy.value = uniqueNumbers
  }
}

const toggleByCategory = () => {
  if (!zawodnicyFilters.value.kategoria) return
  
  const categoryMembers = filteredZawodnicyNew.value
    .filter(z => z.kategoria === zawodnicyFilters.value.kategoria)
    .map(z => z.nr_startowy)
  
  if (categorySelected.value) {
    selectedZawodnicy.value = selectedZawodnicy.value.filter(nr => !categoryMembers.includes(nr))
  } else {
    const uniqueNumbers = [...new Set([...selectedZawodnicy.value, ...categoryMembers])]
    selectedZawodnicy.value = uniqueNumbers
  }
}

const toggleByClub = () => {
  if (!zawodnicyFilters.value.klub) return
  
  const clubMembers = filteredZawodnicyNew.value
    .filter(z => z.klub === zawodnicyFilters.value.klub)
    .map(z => z.nr_startowy)
  
  if (clubSelected.value) {
    selectedZawodnicy.value = selectedZawodnicy.value.filter(nr => !clubMembers.includes(nr))
  } else {
    const uniqueNumbers = [...new Set([...selectedZawodnicy.value, ...clubMembers])]
    selectedZawodnicy.value = uniqueNumbers
  }
}

const toggleWithoutQr = () => {
  const withoutQrMembers = filteredZawodnicyNew.value
    .filter(z => !z.qr_code)
    .map(z => z.nr_startowy)
  
  if (withoutQrSelected.value) {
    selectedZawodnicy.value = selectedZawodnicy.value.filter(nr => !withoutQrMembers.includes(nr))
  } else {
    const uniqueNumbers = [...new Set([...selectedZawodnicy.value, ...withoutQrMembers])]
    selectedZawodnicy.value = uniqueNumbers
  }
}

const clearSelection = () => {
  selectedZawodnicy.value = []
}

const handleDashboardNavigation = (section: string) => {
  activeTab.value = section
}

// Client-side funkcje paginacji
const goToPage = (page: number) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value += 1
  }
}

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value -= 1
  }
}

const firstPage = () => {
  currentPage.value = 1
}

const lastPage = () => {
  currentPage.value = totalPages.value
}

// Reset strony na 1 gdy zmieniają się filtry
watch([zawodnicyFilters, searchTerm], () => {
  currentPage.value = 1
}, { deep: true })

// Lifecycle
onMounted(() => {
  fetchZawodnicy()
  // Inicjalizacja dark mode na podstawie localStorage
  if (isDarkMode.value) {
    document.documentElement.classList.add("dark")
  } else {
    document.documentElement.classList.remove("dark")
  }
})
</script>

<style>
/* Custom styles if needed */
</style>

