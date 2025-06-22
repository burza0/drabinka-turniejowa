#!/usr/bin/env python3

def fix_ranking_functions():
    """Dodaje brakujące funkcje pobierania danych rankingów"""
    
    with open('frontend/src/components/Rankingi.vue', 'r') as f:
        content = f.read()
    
    print('🔧 DODAJĘ BRAKUJĄCE FUNKCJE POBIERANIA DANYCH RANKINGÓW...')
    
    # Znajdź koniec funkcji refreshRankings i dodaj brakujące funkcje przed </script>
    script_end = content.rfind('</script>')
    
    # Funkcje do dodania
    functions_to_add = '''

// MISSING FUNCTIONS - RANKING DATA FETCHERS WITH CACHE-BUSTING
const fetchIndividualRanking = async () => {
  console.log('🔍 Pobieranie rankingu indywidualnego...')
  try {
    const response = await fetch(`/api/rankings/individual?season=${selectedSeason.value}&_t=${Date.now()}`)
    console.log('📡 Individual response status:', response.status)
    if (response.ok) {
      const data = await response.json()
      console.log('✅ Individual data received:', data.length, 'items')
      individualRanking.value = data
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
      const data = await response.json()
      console.log('✅ General data received:', data.length, 'items')
      generalRanking.value = data
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
      const data = await totalResponse.json()
      console.log('✅ Club total data received:', data.length, 'items')
      clubRankingTotal.value = data
      console.log("✅ clubRankingTotal updated, length:", clubRankingTotal.value.length)
    } else {
      console.error('❌ Club total ranking response not ok:', totalResponse.status, totalResponse.statusText)
    }
    
    if (top3Response.ok) {
      const data = await top3Response.json()
      console.log('✅ Club top3 data received:', data.length, 'items')
      clubRankingTop3.value = data
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
      const data = await response.json()
      console.log('✅ Medal data received:', data.length, 'items')
      medalRanking.value = data
      console.log("✅ medalRanking updated, length:", medalRanking.value.length)
    } else {
      console.error('❌ Medal ranking response not ok:', response.status, response.statusText)
    }
  } catch (error) {
    console.error('❌ Error fetching medal ranking:', error)
  }
}

// HELPER FUNCTIONS FOR FILTERS
const clearAllFilters = () => {
  selectedCategory.value = ''
  selectedClub.value = ''
  selectedGender.value = ''
  sortBy.value = 'pozycja_asc'
}

const clearGeneralFilters = () => {
  selectedCategoryGeneral.value = ''
  selectedClubGeneral.value = ''
  selectedGenderGeneral.value = ''
  sortByGeneral.value = 'punkty_desc'
}

const clearClubsTotalFilters = () => {
  minZawodnikow.value = null
  sortByClubsTotal.value = 'punkty_desc'
}

const clearClubsTop3Filters = () => {
  minKategorie.value = null
  sortByClubsTop3.value = 'punkty_desc'
}

// Setup uniwersalnego systemu filtrów - PLACEHOLDER funkcje
const individualFilterConfig = ref({})
const uniqueCategories = computed(() => categories.value)
const uniqueClubs = computed(() => clubs.value)

const handleIndividualFiltersChange = (newFilters) => {
  console.log('📋 Individual filters changed:', newFilters)
  // Aktualizuj filtry
  Object.assign(individualFilters.value, newFilters)
}

const handleQuickAction = (action) => {
  console.log('⚡ Quick action:', action)
}
'''

    # Wstaw funkcje przed </script>
    new_content = content[:script_end] + functions_to_add + '\n' + content[script_end:]
    
    # Zapisz plik
    with open('frontend/src/components/Rankingi.vue', 'w') as f:
        f.write(new_content)
    
    print('✅ Dodano brakujące funkcje pobierania danych rankingów:')
    print('   📊 fetchIndividualRanking() - z cache-busting')
    print('   📊 fetchGeneralRanking() - z cache-busting')
    print('   📊 fetchClubRankings() - z cache-busting')  
    print('   📊 fetchMedalRanking() - z cache-busting')
    print('   🔧 clearAllFilters(), clearGeneralFilters(), etc.')
    print('   🔧 Helper functions dla uniwersalnych filtrów')
    print('')
    print('🎯 RANKING POWINIEN TERAZ DZIAŁAĆ!')
    print('   ✅ Backend endpointy: gotowe')
    print('   ✅ Frontend funkcje: dodane') 
    print('   ✅ Cache-busting: aktywny')

if __name__ == '__main__':
    fix_ranking_functions() 