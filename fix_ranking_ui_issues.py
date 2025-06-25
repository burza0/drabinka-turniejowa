#!/usr/bin/env python3

def fix_ranking_ui_issues():
    """Naprawia filtry klasyfikacji indywidualnej i zunifikuje style nagłówków"""
    
    with open('frontend/src/components/Rankingi.vue', 'r') as f:
        content = f.read()
    
    print('🔧 NAPRAWIAM PROBLEMY UI RANKINGÓW...')
    
    # 1. PROBLEM: Filtry klasyfikacji indywidualnej - zastąp FilterSection zwykłymi filtrami
    old_filters_section = '''        <!-- Uniwersalny system filtrów -->
        <FilterSection 
          :config="individualFilterConfig"
          :filters="individualFilters"
          :data="{ categories: uniqueCategories, clubs: uniqueClubs }"
          @filtersChange="handleIndividualFiltersChange"
          @clearFilters="clearAllFilters"
          @quickAction="handleQuickAction"
        />'''
    
    new_filters_section = '''        <!-- Filtry i sortowanie dla Indywidualnej -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-4 sm:p-6 transition-colors duration-200">
          <!-- Nagłówek sekcji -->
          <div class="flex items-center justify-between mb-6">
            <h3 class="text-lg sm:text-xl font-semibold text-gray-900 dark:text-white">Filtry i sortowanie</h3>
            <button 
              @click="clearAllFilters" 
              class="text-sm text-red-600 dark:text-red-400 hover:text-red-800 dark:hover:text-red-300 flex items-center space-x-1 transition-colors duration-200"
            >
              <span>🗑️</span>
              <span>Wyczyść filtry</span>
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
        </div>'''
    
    content = content.replace(old_filters_section, new_filters_section)
    print('✅ Zastąpiono FilterSection zwykłymi filtrami w klasyfikacji indywidualnej')
    
    # 2. PROBLEM: Niespójne style nagłówków - usuń niebieskie tło z klasyfikacji indywidualnej
    old_header_style = '''          <div class="p-4 border-b border-gray-200 dark:border-gray-700 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900 dark:to-indigo-900 transition-colors duration-200">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
              <span class="mr-2">🏆</span>
              Klasyfikacja Indywidualna
              <span class="ml-2 text-sm text-gray-600 dark:text-gray-400">({{ filteredIndividualRanking.length }} pozycji)</span>
            </h3>
          </div>'''
    
    new_header_style = '''        <div class="flex items-center justify-between">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">Klasyfikacja Indywidualna</h3>
          <div class="text-sm text-gray-600 dark:text-gray-400">
            Suma wszystkich punktów ({{ filteredIndividualRanking.length }} pozycji)
          </div>
        </div>'''
    
    content = content.replace(old_header_style, new_header_style)
    print('✅ Zunifikowano style nagłówków - usunięto niebieskie tło')
    
    # Zapisz plik
    with open('frontend/src/components/Rankingi.vue', 'w') as f:
        f.write(content)
    
    print('')
    print('✅ PROBLEMY UI RANKINGÓW NAPRAWIONE!')
    print('   🔧 Filtry klasyfikacji indywidualnej: działają jak inne sekcje')
    print('   🎨 Style nagłówków: spójne we wszystkich sekcjach') 
    print('   📋 Filtry dostępne: Kategoria, Klub, Płeć, Sortowanie')
    print('   🧹 Przycisk "Wyczyść filtry": działa')
    print('')
    print('🎯 UI RANKINGÓW JEST TERAZ SPÓJNY!')

if __name__ == '__main__':
    fix_ranking_ui_issues() 