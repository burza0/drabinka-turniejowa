<template>
  <div v-if="show" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
    <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white dark:bg-gray-800">
      <!-- Header -->
      <div class="flex justify-between items-center pb-4 border-b dark:border-gray-600">
        <h3 class="text-lg font-medium text-gray-900 dark:text-white">
          🔧 Edycja zawodnika #{{ originalData?.nr_startowy }}
        </h3>
        <button @click="closeModal" class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
          <XMarkIcon class="h-6 w-6" />
        </button>
      </div>

      <!-- Formularz -->
      <form @submit.prevent="saveChanges" class="mt-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Dane osobowe -->
          <div class="space-y-4">
            <h4 class="font-medium text-gray-700 dark:text-gray-300">👤 Dane osobowe</h4>
            
            <!-- Imię -->
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Imię</label>
              <input 
                v-model="formData.imie"
                type="text" 
                required
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              />
            </div>

            <!-- Nazwisko -->
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Nazwisko</label>
              <input 
                v-model="formData.nazwisko"
                type="text" 
                required
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              />
            </div>

            <!-- Nr startowy -->
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Nr startowy</label>
              <input 
                v-model.number="formData.nr_startowy"
                type="number" 
                required
                min="1"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              />
            </div>

            <!-- Płeć -->
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Płeć</label>
              <select 
                v-model="formData.plec"
                required
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              >
                <option value="M">👨 Mężczyzna</option>
                <option value="K">👩 Kobieta</option>
              </select>
            </div>

            <!-- Kategoria -->
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Kategoria</label>
              <select 
                v-model="formData.kategoria"
                required
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              >
                <option value="Junior A">🏷️ Junior A</option>
                <option value="Junior B">🏷️ Junior B</option>
                <option value="Junior C">🏷️ Junior C</option>
                <option value="Junior D">🏷️ Junior D</option>
                <option value="Masters">🏷️ Masters</option>
                <option value="Senior">🏷️ Senior</option>
              </select>
            </div>

            <!-- Klub -->
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Klub</label>
              <select 
                v-model="formData.klub"
                required
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              >
                <option v-for="klub in kluby" :key="klub" :value="klub">
                  🏢 {{ klub }}
                </option>
              </select>
            </div>
          </div>

          <!-- Dane wynikowe -->
          <div class="space-y-4">
            <h4 class="font-medium text-gray-700 dark:text-gray-300">⏱️ Dane wynikowe</h4>
            
            <!-- Czas -->
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                Czas przejazdu
                <span class="text-xs text-gray-500">(MM:SS.ms lub SS.ms)</span>
              </label>
              <input 
                v-model="formData.czas_przejazdu"
                type="text" 
                placeholder="1:23.45 lub 83.45"
                pattern="^(?:\d{1,2}:)?\d{1,2}\.\d{1,3}$"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              />
              <p class="mt-1 text-xs text-gray-500">Przykłady: 1:23.45, 83.450, 2:05.12</p>
            </div>

            <!-- Status -->
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Status</label>
              <select 
                v-model="formData.status"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
              >
                <option value="FINISHED">✅ FINISHED</option>
                <option value="DNF">⚠️ DNF (Did Not Finish)</option>
                <option value="DSQ">❌ DSQ (Disqualified)</option>
              </select>
            </div>
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
          <button 
            type="button"
            @click="closeModal"
            class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 border border-gray-300 rounded-md hover:bg-gray-200 dark:bg-gray-700 dark:text-gray-300 dark:border-gray-600 dark:hover:bg-gray-600"
          >
            ❌ Anuluj
          </button>
          <button 
            type="button"
            @click="deleteZawodnik"
            :disabled="loading"
            class="px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-md hover:bg-red-700 disabled:opacity-50"
          >
            🗑️ Usuń
          </button>
          <button 
            type="submit"
            :disabled="loading"
            class="px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md hover:bg-indigo-700 disabled:opacity-50"
          >
            {{ loading ? '⏳ Zapisywanie...' : '💾 Zapisz' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { XMarkIcon } from '@heroicons/vue/24/outline'
import axios from 'axios'

// Props
const props = defineProps<{
  show: boolean
  zawodnik: any | null
}>()

// Emits
const emit = defineEmits<{
  close: []
  updated: []
  deleted: []
}>()

// Reactive data
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

// Lista klubów (można później pobrać z API)
const kluby = ref([
  'KS Zorza Koszalin',
  'UKS Rodziewiczówka',
  'BKS SKF Białystok',
  'KSł Klub Sportowy łaziska',
  'UKS Speed Demons',
  'WKS Wawel Kraków',
  'MKS Korona Handball'
])

// Watchers
watch(() => props.zawodnik, (newZawodnik) => {
  if (newZawodnik && props.show) {
    originalData.value = { ...newZawodnik }
    formData.value = {
      nr_startowy: newZawodnik.nr_startowy,
      imie: newZawodnik.imie,
      nazwisko: newZawodnik.nazwisko,
      kategoria: newZawodnik.kategoria,
      plec: newZawodnik.plec,
      klub: newZawodnik.klub,
      czas_przejazdu: formatTimeForInput(newZawodnik.czas_przejazdu_s),
      status: newZawodnik.status || 'DNF'
    }
    error.value = ''
    success.value = ''
  }
})

// Methods
const formatTimeForInput = (seconds: number | null): string => {
  if (!seconds) return ''
  const mins = Math.floor(seconds / 60)
  const secs = (seconds % 60).toFixed(3)
  return mins > 0 ? `${mins}:${secs.padStart(6, '0')}` : secs
}

const closeModal = () => {
  emit('close')
}

const saveChanges = async () => {
  if (!originalData.value) return
  
  loading.value = true
  error.value = ''
  success.value = ''
  
  try {
    const response = await axios.put(`/api/zawodnicy/${originalData.value.nr_startowy}`, formData.value)
    
    success.value = 'Zawodnik został zaktualizowany!'
    
    setTimeout(() => {
      emit('updated')
      closeModal()
    }, 1000)
    
  } catch (err: any) {
    console.error('Błąd podczas zapisywania:', err)
    error.value = err.response?.data?.error || 'Wystąpił błąd podczas zapisywania'
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
    console.error('Błąd podczas usuwania:', err)
    error.value = err.response?.data?.error || 'Wystąpił błąd podczas usuwania'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
/* Modal specific styles */
</style> 