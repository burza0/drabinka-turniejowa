<template>
  <div>
    <h2>Wyniki</h2>
    
    <!-- Filtry -->
    <div style="margin:1em 0;padding:12px;background:#f8f9fa;border-radius:8px">
      <div style="display:flex;gap:20px;align-items:center;flex-wrap:wrap">
        <div>
          <label style="font-weight:bold;margin-right:8px">Kategoria:</label>
          <select v-model="wybranaKategoria" @change="updateFilter" style="padding:4px">
            <option value="">Wszystkie</option>
            <option v-for="kat in dostepneKategorie" :key="kat" :value="kat">{{ kat }}</option>
          </select>
        </div>
        <div>
          <label style="font-weight:bold;margin-right:8px">Płeć:</label>
          <select v-model="wybranaPlec" @change="updateFilter" style="padding:4px">
            <option value="">Wszystkie</option>
            <option value="M">Mężczyźni</option>
            <option value="K">Kobiety</option>
          </select>
        </div>
        <div style="color:#666;font-size:0.9em">
          Wyników: {{ filtrowani.length }} / {{ wyniki.length }}
        </div>
      </div>
    </div>

    <!-- Tabela wyników -->
    <div style="overflow-x:auto">
      <table border="1" cellpadding="8" cellspacing="0" style="width:100%;border-collapse:collapse;margin:1em 0">
        <thead style="background:#e9ecef">
          <tr>
            <th style="text-align:center">Nr</th>
            <th>Imię</th>
            <th>Nazwisko</th>
            <th>Kategoria</th>
            <th>Płeć</th>
            <th style="text-align:center">Czas [s]</th>
            <th style="text-align:center">Status</th>
            <th style="text-align:center">Pozycja</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(zawodnik, index) in filtrowani" :key="zawodnik.nr_startowy"
              :style="getRowStyle(zawodnik.status)">
            <td style="text-align:center;font-weight:bold">{{ zawodnik.nr_startowy }}</td>
            <td>{{ zawodnik.imie }}</td>
            <td>{{ zawodnik.nazwisko }}</td>
            <td style="text-align:center">
              <span :style="getKategoriaStyle(zawodnik.kategoria)">{{ zawodnik.kategoria }}</span>
            </td>
            <td style="text-align:center">
              <span :style="getPlecStyle(zawodnik.plec)">
                {{ zawodnik.plec === 'M' ? '👨 M' : '👩 K' }}
              </span>
            </td>
            <td style="text-align:center;font-family:monospace">
              <span v-if="zawodnik.czas_przejazdu_s" :style="getCzasStyle(zawodnik.czas_przejazdu_s)">
                {{ parseFloat(zawodnik.czas_przejazdu_s).toFixed(3) }}
              </span>
              <span v-else style="color:#6c757d">-</span>
            </td>
            <td style="text-align:center">
              <span :style="getStatusStyle(zawodnik.status)">{{ zawodnik.status }}</span>
            </td>
            <td style="text-align:center;font-weight:bold;color:#495057">
              {{ zawodnik.status === 'FINISHED' ? index + 1 : '-' }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Podsumowanie -->
    <div v-if="filtrowani.length > 0" style="margin:1em 0;padding:12px;background:#e7f3ff;border-radius:8px">
      <h4 style="margin:0 0 8px 0;color:#0056b3">📊 Podsumowanie wyników</h4>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px">
        <div>
          <strong>Ukończone:</strong> {{ statystyki.finished }}
        </div>
        <div>
          <strong>DNF:</strong> {{ statystyki.dnf }}
        </div>
        <div>
          <strong>DSQ:</strong> {{ statystyki.dsq }}
        </div>
        <div v-if="statystyki.najlepszyCzas">
          <strong>Najlepszy czas:</strong> {{ statystyki.najlepszyCzas }}s
        </div>
      </div>
    </div>

    <!-- Komunikat gdy brak wyników -->
    <div v-if="filtrowani.length === 0 && wyniki.length > 0" 
         style="margin:2em 0;padding:20px;background:#fff3cd;color:#856404;border-radius:8px;text-align:center">
      Brak wyników dla wybranych filtrów.
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'

const emit = defineEmits(['kategoria-changed'])
const wyniki = ref([])
const wybranaKategoria = ref('')
const wybranaPlec = ref('')

// Dostępne kategorie z danych
const dostepneKategorie = computed(() => {
  const kategorie = [...new Set(wyniki.value.map(z => z.kategoria))].sort()
  return kategorie
})

// Filtrowane wyniki
const filtrowani = computed(() => {
  let filtered = wyniki.value

  // Filtr kategorii
  if (wybranaKategoria.value) {
    filtered = filtered.filter(z => z.kategoria === wybranaKategoria.value)
  }

  // Filtr płci
  if (wybranaPlec.value) {
    filtered = filtered.filter(z => z.plec === wybranaPlec.value)
  }

  // Sortowanie: FINISHED na górze (po czasie), potem DNF, potem DSQ
  return filtered.sort((a, b) => {
    if (a.status === 'FINISHED' && b.status === 'FINISHED') {
      return parseFloat(a.czas_przejazdu_s) - parseFloat(b.czas_przejazdu_s)
    }
    if (a.status === 'FINISHED') return -1
    if (b.status === 'FINISHED') return 1
    if (a.status === 'DNF' && b.status === 'DSQ') return -1
    if (a.status === 'DSQ' && b.status === 'DNF') return 1
    return a.nr_startowy - b.nr_startowy
  })
})

// Statystyki
const statystyki = computed(() => {
  const finished = filtrowani.value.filter(z => z.status === 'FINISHED')
  const dnf = filtrowani.value.filter(z => z.status === 'DNF').length
  const dsq = filtrowani.value.filter(z => z.status === 'DSQ').length
  
  const najlepszyCzas = finished.length > 0 
    ? Math.min(...finished.map(z => parseFloat(z.czas_przejazdu_s))).toFixed(3)
    : null

  return {
    finished: finished.length,
    dnf,
    dsq,
    najlepszyCzas
  }
})

// Style functions
function getRowStyle(status) {
  if (status === 'FINISHED') return 'background:#f8fff8'
  if (status === 'DNF') return 'background:#fff8e1'
  if (status === 'DSQ') return 'background:#ffebee'
  return ''
}

function getKategoriaStyle(kategoria) {
  const colors = {
    'U18': 'color:#28a745;font-weight:bold',
    'OPEN': 'color:#007bff;font-weight:bold', 
    'MASTERS': 'color:#6f42c1;font-weight:bold'
  }
  return colors[kategoria] || ''
}

function getPlecStyle(plec) {
  return plec === 'M' ? 'color:#0066cc' : 'color:#cc0066'
}

function getStatusStyle(status) {
  const styles = {
    'FINISHED': 'color:#28a745;font-weight:bold',
    'DNF': 'color:#ffc107;font-weight:bold',
    'DSQ': 'color:#dc3545;font-weight:bold'
  }
  return styles[status] || ''
}

function getCzasStyle(czas) {
  const czasNum = parseFloat(czas)
  if (czasNum < 45) return 'color:#28a745;font-weight:bold' // Bardzo dobry
  if (czasNum < 50) return 'color:#007bff;font-weight:bold' // Dobry
  if (czasNum < 60) return 'color:#ffc107;font-weight:bold' // Średni
  return 'color:#dc3545;font-weight:bold' // Słaby
}

async function loadWyniki() {
  try {
    const res = await axios.get('/api/wyniki')
    wyniki.value = res.data
    console.log('Załadowano wyniki:', res.data.length, 'zawodników')
  } catch (error) {
    console.error('Błąd ładowania wyników:', error)
    wyniki.value = []
  }
}

function updateFilter() {
  // Funkcja do wymuszenia reaktywności - computed już obsługuje filtrowanie
  // Emituj zmianę kategorii i płci do App.vue
  emit('kategoria-changed', {
    kategoria: wybranaKategoria.value || null,
    plec: wybranaPlec.value || null
  })
}

// Obserwuj zmiany kategorii i płci i emituj je
watch([wybranaKategoria, wybranaPlec], () => {
  emit('kategoria-changed', {
    kategoria: wybranaKategoria.value || null,
    plec: wybranaPlec.value || null
  })
})

onMounted(loadWyniki)
</script>

