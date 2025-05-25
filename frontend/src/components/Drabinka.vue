<template>
  <div>
    <h2>Drabinka (mockup)</h2>
    <div v-for="(match, i) in filtrowane" :key="i" style="margin:1em 0;padding:8px;background:#eee">
      <strong>Mecz {{ i+1 }}:</strong>
      <span v-if="match.team1">{{ match.team1.imie }} {{ match.team1.nazwisko }} (#{{ match.team1.nr_startowy }})</span>
      <span v-else>---</span>
      vs
      <span v-if="match.team2">{{ match.team2.imie }} {{ match.team2.nazwisko }} (#{{ match.team2.nr_startowy }})</span>
      <span v-else>---</span>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted, watch } from 'vue'
import { getDrabinka } from '../api'
const props = defineProps({ kategoria: String })
const drabinka = ref([])
const filtrowane = ref([])
onMounted(async () => {
  drabinka.value = await getDrabinka()
  filtrowane.value = drabinka.value
})
watch(() => props.kategoria, (kat) => {
  if (!kat) filtrowane.value = drabinka.value
  else filtrowane.value = drabinka.value.filter(m =>
    (!m.team1 || m.team1.kategoria === kat) && (!m.team2 || m.team2.kategoria === kat)
  )
})
</script>

