<template>
  <div>
    <h2>Drabinka</h2>
    
    <!-- Kategorie -->
    <div v-for="(kategoriaData, kategoriaNazwa) in filtrowaneKategorie" :key="kategoriaNazwa" 
         style="margin:2em 0;border:2px solid #ddd;border-radius:10px;padding:15px">
      
      <h3 style="color:#2c5aa0;margin-top:0">🏅 {{ kategoriaNazwa }}</h3>
      
      <!-- Płcie w kategorii -->
      <div v-for="(plecData, plecNazwa) in kategoriaData" :key="plecNazwa"
           style="margin:1.5em 0;border:1px solid #ccc;border-radius:8px;padding:12px;background:#fafafa">
        
        <h4 style="color:#444;margin-top:0">👥 {{ plecNazwa }}</h4>
        
        <!-- Statystyki -->
        <div v-if="plecData.statystyki" style="margin:0.5em 0;font-size:0.9em;color:#666">
          <span>Łącznie zawodników: {{ plecData.statystyki.łącznie_zawodników }}</span> |
          <span>W ćwierćfinałach: {{ plecData.statystyki.w_ćwierćfinałach }}</span> |
          <span v-if="plecData.statystyki.odpadło > 0" style="color:#dc3545">Odpadło: {{ plecData.statystyki.odpadło }}</span> |
          <span>Grup ćwierćfinały: {{ plecData.statystyki.grup_ćwierćfinały }}</span> |
          <span>Grup półfinały: {{ plecData.statystyki.grup_półfinały }}</span> |
          <span>Grup finał: {{ plecData.statystyki.grup_finał }}</span>
        </div>

        <!-- Info o małej liczbie zawodników -->
        <div v-if="plecData.info" style="margin:1em 0;padding:8px;background:#fff3cd;border-radius:5px;color:#856404">
          ℹ️ {{ plecData.info }}
        </div>

        <!-- Odpadli zawodnicy -->
        <div v-if="plecData.odpadli && plecData.odpadli.length > 0" style="margin:1em 0">
          <h5 style="color:#dc3545;margin:0.5em 0">❌ Odpadli z turnieju ({{ plecData.odpadli.length }})</h5>
          <div style="padding:8px;background:#f8d7da;border:1px solid #f5c6cb;border-radius:5px;max-height:150px;overflow-y:auto">
            <div v-for="zawodnik in plecData.odpadli" :key="zawodnik.nr_startowy"
                 style="margin:0.2em 0;padding:2px;font-size:0.9em;color:#721c24">
              {{ zawodnik.nr_startowy }}. {{ zawodnik.imie }} {{ zawodnik.nazwisko }}
              <span v-if="zawodnik.czas_przejazdu_s" style="color:#6c757d"> - {{ zawodnik.czas_przejazdu_s }}s</span>
              <span v-else style="color:#6c757d"> - brak czasu</span>
            </div>
          </div>
        </div>

        <!-- Ćwierćfinały -->
        <div v-if="plecData.ćwierćfinały && plecData.ćwierćfinały.length > 0" style="margin:1em 0">
          <h5 style="color:#cd7f32;margin:0.5em 0">🥉 Ćwierćfinały</h5>
          <div v-for="grupa in plecData.ćwierćfinały" :key="grupa.grupa"
               style="margin:0.5em 0;padding:8px;background:#fff;border:1px solid #ddd;border-radius:5px">
            <strong>Grupa {{ grupa.grupa }}</strong> (awansują: {{ grupa.awansują }})
            <div v-for="zawodnik in grupa.zawodnicy" :key="zawodnik.nr_startowy"
                 style="margin:0.2em 0;padding:4px;background:#f8f9fa">
              {{ zawodnik.nr_startowy }}. {{ zawodnik.imie }} {{ zawodnik.nazwisko }}
              <span v-if="zawodnik.czas_przejazdu_s" style="color:#28a745"> - {{ zawodnik.czas_przejazdu_s }}s</span>
              <span v-else style="color:#6c757d"> - brak czasu</span>
            </div>
          </div>
        </div>

        <!-- Półfinały -->
        <div v-if="plecData.półfinały && plecData.półfinały.length > 0" style="margin:1em 0">
          <h5 style="color:#c0c0c0;margin:0.5em 0">🥈 Półfinały</h5>
          <div v-for="grupa in plecData.półfinały" :key="grupa.grupa"
               style="margin:0.5em 0;padding:8px;background:#fff;border:1px solid #ddd;border-radius:5px">
            <strong>Grupa {{ grupa.grupa }}</strong> (awansują: {{ grupa.awansują }})
            <div v-if="grupa.zawodnicy && grupa.zawodnicy.length > 0">
              <div v-for="zawodnik in grupa.zawodnicy" :key="zawodnik.nr_startowy"
                   style="margin:0.2em 0;padding:4px;background:#f8f9fa">
                {{ zawodnik.nr_startowy }}. {{ zawodnik.imie }} {{ zawodnik.nazwisko }}
                <span v-if="zawodnik.czas_przejazdu_s" style="color:#28a745"> - {{ zawodnik.czas_przejazdu_s }}s</span>
                <span v-else style="color:#6c757d"> - brak czasu</span>
              </div>
            </div>
            <div v-else style="color:#6c757d;font-style:italic">
              {{ grupa.info || 'Oczekuje na wyniki ćwierćfinałów' }}
            </div>
          </div>
        </div>

        <!-- Finał -->
        <div v-if="plecData.finał && plecData.finał.length > 0" style="margin:1em 0">
          <h5 style="color:#ffd700;margin:0.5em 0">🥇 Finał</h5>
          <div v-for="grupa in plecData.finał" :key="grupa.grupa"
               style="margin:0.5em 0;padding:8px;background:#fff;border:2px solid #ffd700;border-radius:5px">
            <strong>Grupa {{ grupa.grupa }}</strong> (awansują: {{ grupa.awansują }})
            <div v-if="grupa.zawodnicy && grupa.zawodnicy.length > 0">
              <div v-for="zawodnik in grupa.zawodnicy" :key="zawodnik.nr_startowy"
                   style="margin:0.2em 0;padding:4px;background:#fffbf0">
                {{ zawodnik.nr_startowy }}. {{ zawodnik.imie }} {{ zawodnik.nazwisko }}
                <span v-if="zawodnik.czas_przejazdu_s" style="color:#28a745"> - {{ zawodnik.czas_przejazdu_s }}s</span>
                <span v-else style="color:#6c757d"> - brak czasu</span>
              </div>
            </div>
            <div v-else style="color:#6c757d;font-style:italic">
              {{ grupa.info || 'Oczekuje na wyniki półfinałów' }}
            </div>
          </div>
        </div>

      </div>
    </div>

    <!-- Komunikat gdy brak danych -->
    <div v-if="Object.keys(filtrowaneKategorie).length === 0" 
         style="margin:2em 0;padding:20px;background:#f8d7da;color:#721c24;border-radius:8px">
      Brak danych drabinki turniejowej.
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import axios from 'axios'

const props = defineProps({ 
  filtry: {
    type: Object,
    default: () => ({ kategoria: null, plec: null })
  }
})
const emit = defineEmits(['podsumowanie-loaded'])
const drabinka = ref({})

const filtrowaneKategorie = computed(() => {
  const { podsumowanie, ...kategorie } = drabinka.value
  
  if (!props.filtry?.kategoria && !props.filtry?.plec) {
    // Pokaż wszystkie kategorie i płcie
    return kategorie
  }
  
  const wynik = {}
  
  // Filtruj kategorie
  const kategorieDoWyswietlenia = props.filtry.kategoria 
    ? { [props.filtry.kategoria]: kategorie[props.filtry.kategoria] }
    : kategorie
  
  // Dla każdej kategorii filtruj płcie
  for (const [kategoriaKey, kategoriaData] of Object.entries(kategorieDoWyswietlenia)) {
    if (!kategoriaData) continue
    
    if (!props.filtry.plec) {
      // Pokaż wszystkie płcie w tej kategorii
      wynik[kategoriaKey] = kategoriaData
    } else {
      // Pokaż tylko wybraną płeć
      const plecNazwa = props.filtry.plec === 'M' ? 'Mężczyźni' : 'Kobiety'
      if (kategoriaData[plecNazwa]) {
        wynik[kategoriaKey] = { [plecNazwa]: kategoriaData[plecNazwa] }
      }
    }
  }
  
  return wynik
})

async function loadDrabinka() {
  try {
    const res = await axios.get('/api/drabinka')
    drabinka.value = res.data
    console.log('Załadowano drabinkę:', res.data)
    
    // Emituj podsumowanie do App.vue
    if (res.data.podsumowanie) {
      emit('podsumowanie-loaded', res.data.podsumowanie)
    }
  } catch (error) {
    console.error('Błąd ładowania drabinki:', error)
    drabinka.value = {}
  }
}

onMounted(loadDrabinka)

// Obserwuj zmiany filtrów
watch(() => props.filtry, (newFilters) => {
  console.log('Zmiana filtrów drabinki na:', newFilters)
}, { deep: true })
</script>

