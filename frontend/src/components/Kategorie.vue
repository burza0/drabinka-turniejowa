<template>
  <div style="margin:1em 0">
    <label>Kategoria: </label>
    <select v-model="localSelected" @change="onChange">
      <option :value="null">Wszystkie</option>
      <option v-for="kat in kategorie" :key="kat" :value="kat">{{ kat }}</option>
    </select>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
const emit = defineEmits(['select'])
const kategorie = ref([])
const localSelected = ref(null)

onMounted(async () => {
  try {
    const res = await axios.get('/api/kategorie')
    console.log('Kategorie z backendu:', res.data)
    if (Array.isArray(res.data)) {
      kategorie.value = res.data
    } else {
      kategorie.value = []
      console.warn('API /api/kategorie zwróciło:', res.data)
    }
  } catch (err) {
    kategorie.value = []
    console.error('Błąd pobierania kategorii:', err)
  }
})

function onChange() {
  emit('select', localSelected.value ? localSelected.value : null)
}
</script>

