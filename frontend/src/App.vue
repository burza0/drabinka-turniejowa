<template>
  <div style="font-family:sans-serif;max-width:920px;margin:auto">
    <h1>Drabinka Turniejowa – SECTRO Timing</h1>
    <Kategorie @select="selectedKat = $event" :selected="selectedKat"/>
    <Wyniki :kategoria="selectedKat" />
    <Drabinka :kategoria="selectedKat" />
  </div>
</template>
<script setup>
import { ref } from 'vue'
import Kategorie from './components/Kategorie.vue'
import Wyniki from './components/Wyniki.vue'
import Drabinka from './components/Drabinka.vue'
const selectedKat = ref(null)
</script>

