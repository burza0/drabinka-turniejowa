# 🔍 Uniwersalny System Filtrowania SKATECROSS v30.5

## 📋 Przegląd

Uniwersalny moduł filtrowania dla aplikacji SKATECROSS, który ujednolica filtry we wszystkich zakładkach przy zachowaniu specyficznych funkcjonalności każdej z nich.

## 🏗️ Architektura

### Komponenty:
- **`FilterSection.vue`** - Główny komponent uniwersalny
- **`useFilterConfigs.ts`** - Composable z konfiguracjami filtrów
- **Konfiguracje dla zakładek**: Zawodnicy, Rankingi, Drabinka, QrPrint

## 📱 Struktura komponentu FilterSection.vue

### Props:
- `config: FilterConfig` - Konfiguracja filtrów
- `filters: Record<string, any>` - Aktualne wartości filtrów  
- `data?: any` - Opcjonalne dane do obliczeń

### Events:
- `filtersChange` - Zmiana filtrów
- `clearFilters` - Wyczyszczenie wszystkich filtrów
- `quickAction` - Wykonanie szybkiej akcji

### Sekcje interfejsu:
1. **Nagłówek** - Tytuł + przycisk czyszczenia
2. **Główne filtry** - Select-y i inputy liczbowe w grid
3. **Chip filters** - Multi-select w stylu chipów z kolorami
4. **Szybkie akcje** - Przyciski operacji grupowych

## 🔧 Typy filtrów

### MainFilter (Select/Number):
```typescript
{
  key: string           // Klucz w obiekcie filters
  label: string         // Etykieta wyświetlana
  icon: string          // Emoji ikona  
  type: 'select' | 'number'
  options?: string[]    // Opcje dla select
  placeholder?: string  // Placeholder
  min?: number         // Min dla number
  max?: number         // Max dla number
  showCount?: boolean  // Pokazuj liczniki
}
```

### ChipFilter (Multi-select):
```typescript
{
  key: string
  label: string
  options: string[] | FilterOption[]
  color: 'blue' | 'green' | 'indigo' | 'pink' | 'yellow' | 'red' | 'purple' | 'orange'
  showCount?: boolean   // Pokazuj "X wybranych"
  showIcons?: boolean   // Pokazuj ikony w chipach
}
```

### QuickAction:
```typescript
{
  key: string
  label: string
  icon: string
  className: string            // Klasy CSS (kolor przycisku)
  action: (filters, data) => void
  disabled?: (filters, data) => boolean
  count?: number | function    // Licznik w przycisk
  showCount?: boolean
}
```

## 🎯 Konfiguracje dla zakładek

### 1. Zawodnicy (App.vue)
**Styl**: Chip/button filters
**Filtry**: 
- Kluby (chips, blue)
- Kategorie (chips, green) 
- Płeć (chips z ikonami, indigo)
- Statusy (chips z ikonami, yellow)

**Szybkie akcje**:
- Wszystkie kluby
- Wszystkie kategorie  
- Tylko ukończone

### 2. Rankingi (Rankingi.vue)
**Styl**: 4-kolumnowy grid z select-ami
**Filtry**:
- Kategoria (select)
- Klub (select)
- Płeć (select)
- Sortowanie (select z opcjami per typ rankingu)

### 3. Drabinka (DrabinkaPucharowa.vue)
**Styl**: Proste chipy
**Filtry**:
- Kategorie (chips, green)
- Płeć (chips z ikonami, indigo)

**Szybkie akcje**:
- Wszystkie kategorie
- Obie płcie

### 4. QrPrint (QrPrint.vue)
**Styl**: Mieszanka - selecty + operacje grupowe
**Filtry**:
- Kategoria (select z licznikami)
- Klub (select z licznikami)
- Status QR (select)
- Sortowanie (select)

**Operacje grupowe**:
- Zaznacz wszystkie (z licznikiem)
- Zaznacz kategorię (warunkowo)
- Zaznacz klub (warunkowo)  
- Zaznacz bez QR (z licznikiem)

## 🎨 Kolory chipów

- **blue**: Kluby
- **green**: Kategorie
- **indigo**: Płeć
- **pink**: Płeć (alternatywnie)
- **yellow**: Statusy
- **red**: Błędy/usuwanie
- **purple**: Operacje klubowe
- **orange**: QR/specjalne

## 📋 Użycie w komponentach

### Podstawowe użycie:
```vue
<template>
  <FilterSection 
    :config="filterConfig"
    :filters="currentFilters"
    :data="{ clubs, categories }"
    @filtersChange="handleFiltersChange"
    @clearFilters="clearAllFilters"
    @quickAction="handleQuickAction"
  />
</template>

<script setup>
import FilterSection from './FilterSection.vue'
import { useFilterConfigs } from '../composables/useFilterConfigs'

const { zawodnicyConfig } = useFilterConfigs()
const filterConfig = zawodnicyConfig(categories, clubs)

const currentFilters = ref({
  kluby: [],
  kategorie: [],
  plcie: [],
  statusy: []
})
</script>
```

### Obsługa zdarzeń:
```javascript
const handleFiltersChange = (newFilters) => {
  currentFilters.value = newFilters
  // Logika filtrowania danych
}

const clearAllFilters = () => {
  currentFilters.value = {
    kluby: [],
    kategorie: [],
    plcie: [],
    statusy: []
  }
}

const handleQuickAction = (actionKey, data) => {
  switch(actionKey) {
    case 'all_clubs':
      // Obsługa w action function
      break
    case 'select_all':
      // Specjalna logika w komponencie rodzica
      break
  }
}
```

## 🚀 Plan implementacji

### Faza 1: Podstawa
- [x] Stworzenie `FilterSection.vue`
- [x] Stworzenie `useFilterConfigs.ts`
- [x] Definicja typów TypeScript

### Faza 2: Implementacja w zakładkach
- [ ] Refaktor zakładki Zawodnicy (App.vue)
- [ ] Refaktor zakładki Rankingi (Rankingi.vue)
- [ ] Refaktor zakładki Drabinka (DrabinkaPucharowa.vue)  
- [ ] Refaktor zakładki QrPrint (QrPrint.vue)

### Faza 3: Testowanie i optymalizacja
- [ ] Testy funkcjonalności
- [ ] Optymalizacja wydajności
- [ ] Dokumentacja użytkownika

## 🔄 Migracja z obecnego systemu

### Zawodnicy (App.vue):
```diff
- <!-- Stary kod filtrów -->
- <div class="bg-white">
-   <div class="flex flex-wrap gap-2">
-     <button v-for="klub in uniqueKluby">
+ <!-- Nowy uniwersalny system -->
+ <FilterSection 
+   :config="zawodnicyConfig(categories, clubs)"
+   :filters="filters"
+   @filtersChange="handleFiltersChange"
+ />
```

### Rankingi (Rankingi.vue):
```diff
- <!-- 5x duplikowane sekcje filtrów -->
- <div class="grid grid-cols-4">
-   <select v-model="selectedCategory">
+ <!-- Jeden uniwersalny komponent -->
+ <FilterSection 
+   :config="rankingConfig(categories, clubs, activeTab)"
+   :filters="currentFilters"
+ />
```

## ✨ Korzyści

1. **Spójność UX** - Jednolity wygląd i zachowanie
2. **Mniej kodu** - Eliminacja duplikacji (~500 linii)
3. **Łatwość utrzymania** - Zmiany w jednym miejscu
4. **Type Safety** - Pełne typowanie TypeScript
5. **Skalowalność** - Łatwe dodawanie nowych filtrów
6. **Responsywność** - Automatyczne dostosowanie do mobile

## 🎯 Przykłady konkretnych zastosowań

### Zawodnicy - filtrowanie po klubach:
- Chipy z nazwami klubów w kolorze blue
- Licznik "X wybranych" 
- Szybka akcja "Wszystkie kluby"

### Rankingi - sortowanie:
- Select z opcjami specyficznymi dla typu rankingu
- Individual: pozycja, punkty, starty
- Medals: złote, srebrne, brązowe, łącznie

### QrPrint - operacje grupowe:
- Zaznacz wszystkie z licznikiem przefiltrowanych
- Zaznacz kategorię (aktywne tylko gdy wybrana)
- Zaznacz bez QR z licznikiem

Uniwersalny system zapewni spójność przy zachowaniu specyfiki każdej zakładki! 🚀 