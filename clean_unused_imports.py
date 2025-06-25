#!/usr/bin/env python3

def clean_unused_imports():
    """Usuwa niepotrzebne importy i zmienne w Rankingi.vue"""
    
    with open('frontend/src/components/Rankingi.vue', 'r') as f:
        content = f.read()
    
    print('🔧 CZYSZCZENIE NIEPOTRZEBNYCH IMPORTÓW...')
    
    # 1. Usuń niepotrzebne importy
    content = content.replace("import axios from 'axios'\n", "")
    content = content.replace("// Uniwersalny system filtrów v30.6\n", "")
    content = content.replace("import FilterSection from './FilterSection.vue'\n", "")
    content = content.replace("import { useFilterConfigs } from '../composables/useFilterConfigs'\n", "")
    print('✅ Usunięto niepotrzebne importy')
    
    # 2. Usuń niepotrzebne zmienne i funkcje związane z FilterSection
    unused_code_blocks = [
        "// Setup uniwersalnego systemu filtrów v30.6\nconst { rankingConfig } = useFilterConfigs()",
        
        """// Unified filters dla każdej zakładki
const individualFilters = ref({
  kategoria: '',
  klub: '',
  plec: '',
  sortowanie: 'pozycja_asc'
})

const generalFilters = ref({
  kategoria: '',
  klub: '',
  plec: '',
  sortowanie: 'punkty_desc'
})

const clubsTotalFilters = ref({
  minZawodnikow: '',
  sortowanie: 'punkty_desc'
})

const clubsTop3Filters = ref({
  minKategorie: '',
  sortowanie: 'punkty_desc'
})

const medalsFilters = ref({
  minZlote: '',
  sortowanie: 'zlote_desc'
})""",

        """// Setup uniwersalnego systemu filtrów - PLACEHOLDER funkcje
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
}"""
    ]
    
    for block in unused_code_blocks:
        content = content.replace(block, "")
    
    print('✅ Usunięto niepotrzebne zmienne i funkcje FilterSection')
    
    # 3. Wyczyść puste linie
    import re
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    # Zapisz plik
    with open('frontend/src/components/Rankingi.vue', 'w') as f:
        f.write(content)
    
    print('')
    print('✅ CZYSZCZENIE ZAKOŃCZONE!')
    print('   🗑️ Usunięto importy: axios, FilterSection, useFilterConfigs')
    print('   🗑️ Usunięto zmienne: individualFilters, generalFilters, etc.')
    print('   🗑️ Usunięto funkcje: handleIndividualFiltersChange, handleQuickAction')
    print('')
    print('🎯 PLIK RANKINGI.VUE JEST TERAZ CZYSTY!')

if __name__ == '__main__':
    clean_unused_imports() 