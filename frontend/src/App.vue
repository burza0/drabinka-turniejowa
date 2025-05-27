<template>
  <div style="font-family:sans-serif;max-width:920px;margin:auto">
    <h1>DRABINKA PUCHAROWA SKATECROSS</h1>
    
    <!-- Podsumowanie -->
    <div v-if="podsumowanie" style="margin:1em 0;padding:12px;background:#f0f8ff;border-radius:8px">
      <h3>📊 Podsumowanie</h3>
      <p><strong>Kategorie:</strong> {{ podsumowanie.wszystkie_kategorie?.join(', ') }}</p>
      <p><strong>Łącznie zawodników:</strong> {{ podsumowanie.łączna_liczba_zawodników }}</p>
      <p><strong>Mężczyźni:</strong> {{ podsumowanie.podział_płeć?.mężczyźni }} | 
         <strong>Kobiety:</strong> {{ podsumowanie.podział_płeć?.kobiety }}</p>
    </div>
    
    <Wyniki @kategoria-changed="selectedFilters = $event" />
    <Drabinka :filtry="selectedFilters" @podsumowanie-loaded="podsumowanie = $event" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Wyniki from './components/Wyniki.vue'
import Drabinka from './components/Drabinka.vue'

const selectedFilters = ref({ kategoria: null, plec: null })
const podsumowanie = ref(null)
</script>

