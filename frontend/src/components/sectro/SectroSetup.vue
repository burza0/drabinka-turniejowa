<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
    <h2 class="text-xl font-bold mb-4 text-gray-900 dark:text-white">Nowa Sesja SECTRO</h2>
    
    <form @submit.prevent="createSession" class="space-y-4">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">Nazwa sesji</label>
          <input 
            v-model="sessionData.nazwa" 
            class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white" 
            placeholder="np. Trening Junior A"
            required
          >
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">Kategoria</label>
          <select v-model="sessionData.kategoria" class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white">
            <option value="">Wszystkie</option>
            <option>Junior A</option>
            <option>Junior B</option>
            <option>Senior</option>
            <option>Masters</option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">Płeć</label>
          <select v-model="sessionData.plec" class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white">
            <option value="">Wszystkie</option>
            <option value="M">Mężczyźni</option>
            <option value="K">Kobiety</option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">Status</label>
          <select v-model="sessionData.status" class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white">
            <option value="active">Aktywna</option>
            <option value="paused">Wstrzymana</option>
            <option value="completed">Zakończona</option>
          </select>
        </div>
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">Wejście START</label>
          <select v-model="sessionData.wejscie_start" class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white">
            <option :value="1">Wejście 1 (domyślne)</option>
            <option :value="2">Wejście 2</option>
            <option :value="3">Wejście 3</option>
            <option :value="4">Wejście 4</option>
          </select>
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-2 text-gray-700 dark:text-gray-300">Wejście FINISH</label>
          <select v-model="sessionData.wejscie_finish" class="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white">
            <option :value="1">Wejście 1</option>
            <option :value="2">Wejście 2</option>
            <option :value="3">Wejście 3</option>
            <option :value="4">Wejście 4 (domyślne)</option>
          </select>
        </div>
      </div>
      
      <div class="flex justify-end space-x-3 pt-4">
        <button 
          type="button"
          @click="$emit('cancel')"
          class="px-4 py-2 text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200"
        >
          Anuluj
        </button>
        
        <button 
          type="submit" 
          :disabled="loading || !sessionData.nazwa"
          class="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-6 py-2 rounded-md flex items-center space-x-2"
        >
          <span v-if="loading">⏳</span>
          <span v-else>🚀</span>
          <span>{{ loading ? 'Tworzenie...' : 'Utwórz Sesję' }}</span>
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

// Props & Emits
const emit = defineEmits(['session-created', 'cancel'])

// Reactive data
const loading = ref(false)
const sessionData = ref({
  nazwa: '',
  kategoria: '',
  plec: '',
  status: 'active',
  wejscie_start: 1,
  wejscie_finish: 4
})

// Methods
const createSession = async () => {
  if (!sessionData.value.nazwa) return
  
  loading.value = true
  
  try {
    const response = await axios.post('/api/sectro/sessions', sessionData.value)
    
    if (response.data.success) {
      console.log('✅ Sesja SECTRO utworzona:', response.data.session)
      emit('session-created', response.data.session)
      
      // Reset form
      sessionData.value = {
        nazwa: '',
        kategoria: '',
        plec: '',
        status: 'active',
        wejscie_start: 1,
        wejscie_finish: 4
      }
    } else {
      console.error('❌ Błąd tworzenia sesji:', response.data.error)
      alert('Błąd podczas tworzenia sesji: ' + response.data.error)
    }
  } catch (error) {
    console.error('❌ Błąd komunikacji z API:', error)
    alert('Błąd podczas komunikacji z serwerem')
  } finally {
    loading.value = false
  }
}
</script> 