<template>
  <div>
    <label>Kategoria:</label>
    <select v-model="selected" @change="$emit('select', selected)">
      <option value="">Wszystkie</option>
      <option v-for="k in kategorie" :key="k" :value="k">{{ k }}</option>
    </select>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { getKategorie } from '../api'
const kategorie = ref([])
const selected = ref("")
onMounted(async () => {
  kategorie.value = await getKategorie()
})
defineProps({ selected: String })
</script>

