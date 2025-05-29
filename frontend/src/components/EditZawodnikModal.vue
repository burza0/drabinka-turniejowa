<template>
  <div v-if="show" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
    <div class="relative top-20 mx-auto p-5 border w-full max-w-lg shadow-lg rounded-lg bg-white dark:bg-gray-800">
      <!-- Header -->
      <div class="flex justify-between items-center pb-4 border-b dark:border-gray-600">
        <h3 class="text-xl font-semibold text-gray-900 dark:text-white">
          {{ originalData ? `Edycja zawodnika #${originalData.nr_startowy}` : 'Dodaj nowego zawodnika' }}
        </h3>
        <button @click="closeModal" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
          <XMarkIcon class="h-6 w-6" />
        </button>
      </div>

      <!-- Formularz -->
      <form @submit.prevent="saveChanges" class="mt-4 text-xl space-y-6">
        <!-- Rząd 1: Imię | Nazwisko -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-lg font-medium text-gray-700 dark:text-gray-300">Imię</label>
            <input v-model="formData.imie" type="text" required class="mt-1 block w-full rounded-full px-4 py-2 text-xl border-gray-300 shadow-sm bg-gray-100 dark:bg-gray-700 focus:border-indigo-500 focus:ring-indigo-500 dark:border-gray-600 dark:text-white" />
          </div>
          <div>
            <label class="block text-lg font-medium text-gray-700 dark:text-gray-300">Nazwisko</label>
            <input v-model="formData.nazwisko" type="text" required class="mt-1 block w-full rounded-full px-4 py-2 text-xl border-gray-300 shadow-sm bg-gray-100 dark:bg-gray-700 focus:border-indigo-500 focus:ring-indigo-500 dark:border-gray-600 dark:text-white" />
          </div>
        </div>
        <!-- Rząd 2: Nr startowy | Klub -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-lg font-medium text-gray-700 dark:text-gray-300">Nr startowy</label>
            <input v-model.number="formData.nr_startowy" type="number" required min="1" class="mt-1 block w-full rounded-full px-4 py-2 text-xl border-gray-300 shadow-sm bg-gray-100 dark:bg-gray-700 focus:border-indigo-500 focus:ring-indigo-500 dark:border-gray-600 dark:text-white" />
          </div>
          <div>
            <label class="block text-lg font-medium text-gray-700 dark:text-gray-300">Klub</label>
            <template v-if="kluby.length > 0">
              <select v-model="formData.klub" required class="mt-1 block w-full rounded-full px-4 py-2 text-xl border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white">
                <option value="" disabled>Wybierz klub...</option>
                <option v-for="klub in kluby" :key="klub" :value="klub">{{ klub }}</option>
              </select>
            </template>
            <template v-else>
              <input v-model="formData.klub" type="text" required placeholder="Wpisz klub" class="mt-1 block w-full rounded-full px-4 py-2 text-xl border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white" />
              <p class="text-xs text-red-500 mt-1">Brak klubów w bazie! Wpisz ręcznie.</p>
            </template>
          </div>
        </div>
        <!-- Rząd 3: Płeć | Kategoria -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-lg font-medium text-gray-700 dark:text-gray-300">Płeć</label>
            <select v-model="formData.plec" required class="mt-1 block w-full rounded-full px-4 py-2 text-xl border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white">
              <option value="M">👨 Mężczyzna</option>
              <option value="K">👩 Kobieta</option>
            </select>
          </div>
          <div>
            <label class="block text-lg font-medium text-gray-700 dark:text-gray-300">Kategoria</label>
            <select v-model="formData.kategoria" required class="mt-1 block w-full rounded-full px-4 py-2 text-xl border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white">
              <option value="Junior A">🏷️ Junior A</option>
              <option value="Junior B">🏷️ Junior B</option>
              <option value="Junior C">🏷️ Junior C</option>
              <option value="Junior D">🏷️ Junior D</option>
              <option value="Masters">🏷️ Masters</option>
              <option value="Senior">🏷️ Senior</option>
            </select>
          </div>
        </div>
        <!-- Rząd 4: Czas przejazdu | Status -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label class="block text-lg font-medium text-gray-700 dark:text-gray-300">Czas przejazdu</label>
            <input v-model="formData.czas_przejazdu" type="text" placeholder="MM:SS.ms lub SS.ms" class="mt-1 block w-full rounded-full px-4 py-2 text-xl border-gray-300 shadow-sm bg-gray-100 dark:bg-gray-700 focus:border-indigo-500 focus:ring-indigo-500 dark:border-gray-600 dark:text-white" />
            <p class="text-xs text-gray-500 mt-1">Format: MM:SS.ms lub SS.ms (np. 1:23.456 lub 45.123)</p>
          </div>
          <div>
            <label class="block text-lg font-medium text-gray-700 dark:text-gray-300">Status</label>
            <select v-model="formData.status" required class="mt-1 block w-full rounded-full px-4 py-2 text-xl border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white">
              <option value="NOT_STARTED">⏳ Nie wystartował</option>
              <option value="FINISHED">✅ Ukończył</option>
              <option value="DNF">❌ Nie ukończył</option>
              <option value="DSQ">🚫 Dyskwalifikacja</option>
            </select>
          </div>
        </div>

        <!-- Error/Success Messages -->
        <div v-if="error" class="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
          <p class="text-sm text-red-700">{{ error }}</p>
        </div>
        <div v-if="success" class="mt-4 p-3 bg-green-50 border border-green-200 rounded-md">
          <p class="text-sm text-green-700">{{ success }}</p>
        </div>

        <!-- Przyciski -->
        <div class="flex justify-end space-x-3 mt-6 pt-4 border-t dark:border-gray-600">
          <button type="button" @click="closeModal" class="px-6 py-2 text-base font-semibold text-indigo-700 bg-indigo-100 rounded-full hover:bg-indigo-200 transition-colors">✖ Anuluj</button>
          <button type="submit" :disabled="loading" class="px-6 py-2 text-base font-semibold text-white bg-green-400 rounded-full hover:bg-green-500 disabled:opacity-50 transition-colors">{{ loading ? '⏳ Zapisywanie...' : '💾 Zapisz' }}</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { XMarkIcon } from '@heroicons/vue/24/outline'
import axios from 'axios'

const props = defineProps<{ show: boolean, zawodnik: any | null }>()
const emit = defineEmits<{ close: []; updated: []; deleted: [] }>()

const formData = ref({
  nr_startowy: 0,
  imie: '',
  nazwisko: '',
  kategoria: '',
  plec: '',
  klub: '',
  czas_przejazdu: '',
  status: ''
})
const originalData = ref<any>(null)
const loading = ref(false)
const error = ref('')
const success = ref('')

// Lista klubów pobierana z API lub fallback z zawodników
const kluby = ref<string[]>([])

onMounted(async () => {
  try {
    const res = await axios.get('/api/kluby')
    if (res.data && res.data.nazwy_klubow && res.data.nazwy_klubow.length > 0) {
      kluby.value = res.data.nazwy_klubow
    } else if (props.zawodnik) {
      kluby.value = [props.zawodnik.klub].filter(Boolean)
    }
  } catch (e) {
    if (props.zawodnik) {
      kluby.value = [props.zawodnik.klub].filter(Boolean)
    } else {
      kluby.value = []
    }
  }
})

watch(() => props.zawodnik, (newZawodnik) => {
  if (newZawodnik && props.show) {
    originalData.value = { ...newZawodnik }
    formData.value = {
      nr_startowy: newZawodnik.nr_startowy,
      imie: newZawodnik.imie,
      nazwisko: newZawodnik.nazwisko,
      kategoria: newZawodnik.kategoria,
      plec: newZawodnik.plec,
      klub: newZawodnik.klub || '',
      czas_przejazdu: formatTimeForInput(newZawodnik.czas_przejazdu_s),
      status: newZawodnik.status || 'DNF'
    }
    error.value = ''
    success.value = ''
  }
})

const formatTimeForInput = (seconds: number | null): string => {
  if (!seconds) return ''
  const mins = Math.floor(seconds / 60)
  const secs = (seconds % 60).toFixed(3)
  return mins > 0 ? `${mins}:${secs.padStart(6, '0')}` : secs
}

const closeModal = () => emit('close')

const saveChanges = async () => {
  loading.value = true
  error.value = ''
  success.value = ''
  try {
    if (originalData.value) {
      // Edycja istniejącego zawodnika
      const response = await axios.put(`/api/zawodnicy/${originalData.value.nr_startowy}`, {
        imie: formData.value.imie,
        nazwisko: formData.value.nazwisko,
        kategoria: formData.value.kategoria,
        plec: formData.value.plec,
        klub: formData.value.klub
      })
      
      // Aktualizuj wynik
      await axios.put('/api/wyniki', {
        nr_startowy: formData.value.nr_startowy,
        czas_przejazdu_s: formData.value.czas_przejazdu,
        status: formData.value.status
      })
      
      success.value = 'Zawodnik został zaktualizowany!'
    } else {
      // Dodawanie nowego zawodnika
      const response = await axios.post('/api/zawodnicy', {
        nr_startowy: formData.value.nr_startowy,
        imie: formData.value.imie,
        nazwisko: formData.value.nazwisko,
        kategoria: formData.value.kategoria,
        plec: formData.value.plec,
        klub: formData.value.klub
      })
      
      // Dodaj wynik
      await axios.put('/api/wyniki', {
        nr_startowy: formData.value.nr_startowy,
        czas_przejazdu_s: formData.value.czas_przejazdu,
        status: formData.value.status
      })
      
      success.value = 'Zawodnik został dodany!'
    }
    setTimeout(() => {
      emit('updated')
      closeModal()
    }, 1000)
  } catch (err: any) {
    error.value = err.response?.data?.error || (err.message || 'Wystąpił błąd podczas zapisywania')
  } finally {
    loading.value = false
  }
}

const deleteZawodnik = async () => {
  if (!originalData.value) return
  const confirmed = confirm(`Czy na pewno chcesz usunąć zawodnika ${originalData.value.imie} ${originalData.value.nazwisko} (nr ${originalData.value.nr_startowy})?`)
  if (!confirmed) return
  loading.value = true
  error.value = ''
  try {
    await axios.delete(`/api/zawodnicy/${originalData.value.nr_startowy}`)
    success.value = 'Zawodnik został usunięty!'
    setTimeout(() => {
      emit('deleted')
      closeModal()
    }, 1000)
  } catch (err: any) {
    error.value = err.response?.data?.error || (err.message || 'Wystąpił błąd podczas usuwania')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
</style> 