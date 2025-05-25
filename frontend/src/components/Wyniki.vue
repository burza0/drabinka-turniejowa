<template>
  <div>
    <h2>Wyniki</h2>
    <table border="1" cellpadding="6">
      <tr>
        <th>Nr startowy</th><th>Imię</th><th>Nazwisko</th><th>Kategoria</th><th>Czas</th><th>Status</th>
      </tr>
      <tr v-for="w in filtrowane" :key="w.nr_startowy">
        <td>{{ w.nr_startowy }}</td>
        <td>{{ w.imie }}</td>
        <td>{{ w.nazwisko }}</td>
        <td>{{ w.kategoria }}</td>
        <td>{{ w.czas_przejazdu_s }}</td>
        <td>{{ w.status }}</td>
      </tr>
    </table>
  </div>
</template>
<script setup>
import { ref, onMounted, watch } from 'vue'
import { getWyniki } from '../api'
const props = defineProps({ kategoria: String })
const wyniki = ref([])
const filtrowane = ref([])
onMounted(async () => {
  wyniki.value = await getWyniki()
  filtrowane.value = wyniki.value
})
watch(() => props.kategoria, (kat) => {
  if (!kat) filtrowane.value = wyniki.value
  else filtrowane.value = wyniki.value.filter(w => w.kategoria === kat)
})
</script>

