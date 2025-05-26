<template>
  <div>
    <h2>Wyniki</h2>
    <table border="1" cellpadding="4" style="margin:1em 0">
      <tr>
        <th>Nr</th>
        <th>Imię</th>
        <th>Nazwisko</th>
        <th>Kategoria</th>
        <th>Czas przejazdu [s]</th>
        <th>Status</th>
      </tr>
      <tr v-for="zawodnik in filtrowani" :key="zawodnik.nr_startowy">
        <td>{{ zawodnik.nr_startowy }}</td>
        <td>{{ zawodnik.imie }}</td>
        <td>{{ zawodnik.nazwisko }}</td>
        <td>{{ zawodnik.kategoria }}</td>
        <td>{{ zawodnik.czas_przejazdu_s ?? '-' }}</td>
        <td>{{ zawodnik.status }}</td>
      </tr>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'

const props = defineProps({ kategoria: String })
const wyniki = ref([])
const filtrowani = ref([])

async function loadWyniki() {
  const res = await axios.get('/api/wyniki')
  wyniki.value = res.data
  updateFilter()
}

function updateFilter() {
  if (!props.kategoria) {
    filtrowani.value = wyniki.value
  } else {
    filtrowani.value = wyniki.value.filter(z => z.kategoria === props.kategoria)
  }
}

onMounted(loadWyniki)
watch(() => props.kategoria, updateFilter)
</script>

