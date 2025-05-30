<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6 space-y-4 sm:space-y-0">
      <div class="flex items-center space-x-3">
        <QrCodeIcon class="h-8 w-8 text-indigo-600" />
        <h2 class="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">QR Admin Dashboard</h2>
      </div>
      
      <div class="flex space-x-2">
        <button
          @click="refreshData"
          :disabled="loading"
          class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 flex items-center"
        >
          <ArrowPathIcon class="h-4 w-4 mr-2" :class="{ 'animate-spin': loading }" />
          Odśwież
        </button>
        <button
          @click="exportData"
          class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 flex items-center"
        >
          <ArrowDownTrayIcon class="h-4 w-4 mr-2" />
          Eksport CSV
        </button>
      </div>
    </div>

    <!-- Quick Status -->
    <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
          <div class="text-2xl font-bold text-blue-600 dark:text-blue-400">
            {{ basicStats.total_zawodnikow || 0 }}
          </div>
          <div class="text-sm text-blue-700 dark:text-blue-300">Wszyscy zawodnicy</div>
        </div>
        <div class="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg">
          <div class="text-2xl font-bold text-green-600 dark:text-green-400">
            {{ basicStats.z_qr_kodami || 0 }}
          </div>
          <div class="text-sm text-green-700 dark:text-green-300">Z QR kodami</div>
        </div>
        <div class="bg-orange-50 dark:bg-orange-900/20 p-4 rounded-lg">
          <div class="text-2xl font-bold text-orange-600 dark:text-orange-400">
            {{ basicStats.zameldowanych || 0 }}
          </div>
          <div class="text-sm text-orange-700 dark:text-orange-300">Zameldowanych</div>
        </div>
        <div class="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg">
          <div class="text-2xl font-bold text-purple-600 dark:text-purple-400">
            {{ basicStats.procent_zameldowanych || 0 }}%
          </div>
          <div class="text-sm text-purple-700 dark:text-purple-300">% zameldowanych</div>
        </div>
      </div>
    </div>

    <!-- Warnings/Issues -->
    <div v-if="issues.length > 0" class="bg-yellow-50 dark:bg-yellow-900/20 border-l-4 border-yellow-400 p-4 rounded-lg">
      <div class="flex">
        <ExclamationTriangleIcon class="h-5 w-5 text-yellow-400" />
        <div class="ml-3">
          <h3 class="text-sm font-medium text-yellow-800 dark:text-yellow-200">
            Wykryto problemy ({{ issues.length }})
          </h3>
          <div class="mt-2 text-sm text-yellow-700 dark:text-yellow-300">
            <ul class="list-disc list-inside space-y-1">
              <li v-for="issue in issues" :key="issue.type">
                {{ issue.title }}: {{ issue.count }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Live Feed -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Recent Activity -->
      <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
        <h2 class="text-lg font-medium text-gray-900 dark:text-white mb-4 flex items-center">
          <ClockIcon class="h-5 w-5 mr-2 text-gray-500" />
          Ostatnia aktywność
          <span class="ml-2 text-xs bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded-full">
            {{ recentCheckpoints.length }}
          </span>
        </h2>
        <div class="space-y-3 max-h-80 overflow-y-auto">
          <div 
            v-for="checkpoint in recentCheckpoints.slice(0, 10)" 
            :key="`${checkpoint.nr_startowy}-${checkpoint.scan_time}`"
            class="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg"
          >
            <div class="flex items-center space-x-3">
              <div class="w-10 h-10 bg-indigo-100 dark:bg-indigo-900 rounded-full flex items-center justify-center">
                <span class="text-sm font-medium text-indigo-600 dark:text-indigo-400">
                  {{ checkpoint.nr_startowy }}
                </span>
              </div>
              <div>
                <div class="text-sm font-medium text-gray-900 dark:text-white">
                  {{ checkpoint.imie }} {{ checkpoint.nazwisko }}
                </div>
                <div class="text-xs text-gray-500 dark:text-gray-400">
                  {{ checkpoint.kategoria }} • {{ formatCheckpointName(checkpoint.checkpoint_name) }}
                </div>
              </div>
            </div>
            <div class="text-right">
              <div class="text-xs text-gray-500 dark:text-gray-400">
                {{ formatTime(checkpoint.scan_time) }}
              </div>
              <div class="text-xs text-gray-400 dark:text-gray-500">
                {{ checkpoint.device_id }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Active Devices -->
      <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
        <h2 class="text-lg font-medium text-gray-900 dark:text-white mb-4 flex items-center">
          <DevicePhoneMobileIcon class="h-5 w-5 mr-2 text-gray-500" />
          Aktywne urządzenia
          <span class="ml-2 text-xs bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded-full">
            {{ deviceActivity.length }}
          </span>
        </h2>
        <div class="space-y-3">
          <div 
            v-for="device in deviceActivity" 
            :key="device.device_id"
            class="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg"
          >
            <div class="flex items-center space-x-3">
              <div class="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
              <div>
                <div class="text-sm font-medium text-gray-900 dark:text-white">
                  {{ device.device_id }}
                </div>
                <div class="text-xs text-gray-500 dark:text-gray-400">
                  {{ device.total_scans }} skanów • {{ device.unique_zawodnicy }} zawodników
                </div>
              </div>
            </div>
            <div class="text-right">
              <div class="text-xs text-gray-500 dark:text-gray-400">
                {{ formatTime(device.last_activity) }}
              </div>
              <div class="flex space-x-1 text-xs">
                <span class="bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-2 py-1 rounded">
                  {{ device.check_ins }} check-in
                </span>
                <span class="bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 px-2 py-1 rounded">
                  {{ device.results }} wyniki
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Category Statistics -->
    <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
      <h2 class="text-lg font-medium text-gray-900 dark:text-white mb-4 flex items-center">
        <ChartBarIcon class="h-5 w-5 mr-2 text-gray-500" />
        Statystyki według kategorii
      </h2>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
          <thead class="bg-gray-50 dark:bg-gray-700">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Kategoria
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Łącznie
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Zameldowanych
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Z wynikami
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                Postęp
              </th>
            </tr>
          </thead>
          <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
            <tr v-for="category in categoryStats" :key="category.kategoria">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                {{ category.kategoria }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                {{ category.total }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                {{ category.zameldowanych }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300">
                {{ category.z_wynikami }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="w-16 bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div 
                      class="bg-indigo-600 h-2 rounded-full transition-all duration-300"
                      :style="{ width: `${Math.round((category.z_wynikami / category.total) * 100)}%` }"
                    ></div>
                  </div>
                  <span class="ml-2 text-sm text-gray-500 dark:text-gray-300">
                    {{ Math.round((category.z_wynikami / category.total) * 100) }}%
                  </span>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Hourly Progress Chart -->
    <div v-if="hourlyProgress.length > 0" class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
      <h2 class="text-lg font-medium text-gray-900 dark:text-white mb-4 flex items-center">
        <ChartBarIcon class="h-5 w-5 mr-2 text-gray-500" />
        Postęp w ciągu dnia
      </h2>
      <div class="space-y-2">
        <div 
          v-for="hour in hourlyProgress" 
          :key="hour.hour"
          class="flex items-center space-x-4"
        >
          <div class="text-sm font-medium text-gray-600 dark:text-gray-300 w-20">
            {{ formatHour(hour.hour) }}
          </div>
          <div class="flex-1 bg-gray-200 dark:bg-gray-700 rounded-full h-4 relative">
            <div 
              class="bg-blue-500 h-full rounded-full transition-all duration-300"
              :style="{ width: `${Math.min((hour.check_ins / maxHourlyActivity) * 100, 100)}%` }"
            ></div>
            <div 
              class="bg-green-500 h-full rounded-full absolute top-0 transition-all duration-300"
              :style="{ 
                width: `${Math.min((hour.results / maxHourlyActivity) * 100, 100)}%`,
                left: `${Math.min((hour.check_ins / maxHourlyActivity) * 100, 100)}%`
              }"
            ></div>
          </div>
          <div class="text-sm text-gray-500 dark:text-gray-400 w-24 text-right">
            {{ hour.check_ins }} / {{ hour.results }}
          </div>
        </div>
      </div>
      <div class="flex items-center space-x-4 mt-4 text-xs text-gray-500">
        <div class="flex items-center">
          <div class="w-3 h-3 bg-blue-500 rounded-full mr-2"></div>
          Check-ins
        </div>
        <div class="flex items-center">
          <div class="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
          Wyniki
        </div>
      </div>
    </div>

    <!-- Działania diagnostyczne -->
    <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
      <h2 class="text-lg font-medium text-gray-900 dark:text-white mb-4 flex items-center">
        <WrenchScrewdriverIcon class="h-5 w-5 mr-2 text-gray-500" />
        Narzędzia diagnostyczne
      </h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <button
          @click="generateMissingQR"
          class="p-4 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg hover:border-indigo-400 transition-colors"
        >
          <QrCodeIcon class="h-8 w-8 mx-auto text-gray-400 mb-2" />
          <div class="text-sm font-medium text-gray-600 dark:text-gray-300">
            Generuj brakujące QR
          </div>
          <div class="text-xs text-gray-500">
            {{ basicStats.bez_qr_kodow }} zawodników
          </div>
        </button>
        
        <button
          @click="resetAllCheckIns"
          class="p-4 border-2 border-dashed border-red-300 dark:border-red-600 rounded-lg hover:border-red-400 transition-colors"
        >
          <ArrowPathIcon class="h-8 w-8 mx-auto text-red-400 mb-2" />
          <div class="text-sm font-medium text-red-600 dark:text-red-300">
            Reset check-inów
          </div>
          <div class="text-xs text-red-500">
            Usuń wszystkie meldunki
          </div>
        </button>
        
        <button
          @click="viewSystemLogs"
          class="p-4 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg hover:border-indigo-400 transition-colors"
        >
          <DocumentTextIcon class="h-8 w-8 mx-auto text-gray-400 mb-2" />
          <div class="text-sm font-medium text-gray-600 dark:text-gray-300">
            Logi systemu
          </div>
          <div class="text-xs text-gray-500">
            Ostatnie wydarzenia
          </div>
        </button>
      </div>
    </div>

    <!-- Ręczne zameldowanie -->
    <div class="bg-white dark:bg-gray-800 shadow rounded-lg p-6">
      <h2 class="text-lg font-medium text-gray-900 dark:text-white mb-4 flex items-center">
        <HandRaisedIcon class="h-5 w-5 mr-2 text-orange-500" />
        Ręczne zameldowanie
        <span class="ml-2 text-xs bg-orange-100 dark:bg-orange-900 text-orange-800 dark:text-orange-200 px-2 py-1 rounded-full">
          BACKUP
        </span>
      </h2>
      
      <div class="bg-orange-50 dark:bg-orange-900/20 border-l-4 border-orange-400 p-4 mb-6">
        <div class="flex">
          <ExclamationTriangleIcon class="h-5 w-5 text-orange-400" />
          <div class="ml-3">
            <p class="text-sm text-orange-700 dark:text-orange-300">
              <strong>Uwaga:</strong> Używaj tylko gdy skaner QR nie działa lub w sytuacjach awaryjnych. 
              Każde ręczne zameldowanie jest rejestrowane z identyfikatorem urządzenia "manual-admin".
            </p>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Formularz zameldowania -->
        <div class="space-y-4">
          <h3 class="text-md font-medium text-gray-900 dark:text-white">Zamelduj zawodnika</h3>
          
          <div>
            <label for="nr_startowy" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Numer startowy
            </label>
            <input
              id="nr_startowy"
              v-model="manualCheckInForm.nr_startowy"
              type="number"
              min="1"
              :disabled="manualCheckInLoading"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
              placeholder="Wprowadź numer startowy..."
            />
          </div>

          <div>
            <label for="powod" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Powód ręcznego zameldowania
            </label>
            <select
              id="powod"
              v-model="manualCheckInForm.powod"
              :disabled="manualCheckInLoading"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
            >
              <option value="">Wybierz powód...</option>
              <option value="awaria_skanera">Awaria skanera QR</option>
              <option value="brak_kodu">Brak/uszkodzony kod QR</option>
              <option value="problem_techniczny">Problem techniczny</option>
              <option value="decyzja_organizatora">Decyzja organizatora</option>
              <option value="inne">Inne</option>
            </select>
          </div>

          <div v-if="manualCheckInForm.powod === 'inne'">
            <label for="opis" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Opis szczegółowy
            </label>
            <textarea
              id="opis"
              v-model="manualCheckInForm.opis"
              rows="2"
              :disabled="manualCheckInLoading"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
              placeholder="Opisz powód ręcznego zameldowania..."
            />
          </div>

          <button
            @click="performManualCheckIn"
            :disabled="!canPerformManualCheckIn || manualCheckInLoading"
            class="w-full px-4 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
          >
            <CheckCircleIcon v-if="!manualCheckInLoading" class="h-4 w-4 mr-2" />
            <ArrowPathIcon v-if="manualCheckInLoading" class="h-4 w-4 mr-2 animate-spin" />
            {{ manualCheckInLoading ? 'Meldowanie...' : 'Zamelduj zawodnika' }}
          </button>
        </div>

        <!-- Podgląd zawodnika -->
        <div class="space-y-4">
          <h3 class="text-md font-medium text-gray-900 dark:text-white">Podgląd zawodnika</h3>
          
          <div v-if="previewZawodnik" class="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
            <div class="flex items-center space-x-4 mb-3">
              <div class="w-12 h-12 bg-indigo-100 dark:bg-indigo-900 rounded-full flex items-center justify-center">
                <span class="text-lg font-bold text-indigo-600 dark:text-indigo-400">
                  {{ previewZawodnik.nr_startowy }}
                </span>
              </div>
              <div>
                <div class="text-lg font-medium text-gray-900 dark:text-white">
                  {{ previewZawodnik.imie }} {{ previewZawodnik.nazwisko }}
                </div>
                <div class="text-sm text-gray-500 dark:text-gray-400">
                  {{ previewZawodnik.kategoria }} • {{ previewZawodnik.plec === 'M' ? 'Mężczyzna' : 'Kobieta' }}
                </div>
              </div>
            </div>
            
            <div class="grid grid-cols-2 gap-3 text-sm">
              <div>
                <span class="text-gray-500 dark:text-gray-400">Klub:</span>
                <div class="font-medium text-gray-900 dark:text-white">{{ previewZawodnik.klub || 'Brak danych' }}</div>
              </div>
              <div>
                <span class="text-gray-500 dark:text-gray-400">Status:</span>
                <div class="flex items-center mt-1">
                  <span v-if="previewZawodnik.checked_in" class="inline-flex items-center px-2 py-1 text-xs bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 rounded-full">
                    <CheckCircleIcon class="h-3 w-3 mr-1" />
                    Zameldowany
                  </span>
                  <span v-else class="inline-flex items-center px-2 py-1 text-xs bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200 rounded-full">
                    <XCircleIcon class="h-3 w-3 mr-1" />
                    Nie zameldowany
                  </span>
                </div>
              </div>
              <div>
                <span class="text-gray-500 dark:text-gray-400">QR kod:</span>
                <div class="font-medium text-gray-900 dark:text-white">
                  {{ previewZawodnik.qr_code ? 'Dostępny' : 'Brak' }}
                </div>
              </div>
              <div>
                <span class="text-gray-500 dark:text-gray-400">Wynik:</span>
                <div class="font-medium text-gray-900 dark:text-white">
                  {{ previewZawodnik.ma_wynik ? 'Tak' : 'Nie' }}
                </div>
              </div>
            </div>

            <div v-if="previewZawodnik.checked_in && previewZawodnik.check_in_time" class="mt-3 pt-3 border-t border-gray-200 dark:border-gray-600">
              <span class="text-xs text-gray-500 dark:text-gray-400">
                Zameldowany: {{ formatTime(previewZawodnik.check_in_time) }}
              </span>
            </div>
          </div>

          <div v-else-if="manualCheckInForm.nr_startowy && !previewLoading" class="bg-red-50 dark:bg-red-900/20 p-4 rounded-lg">
            <div class="flex">
              <XCircleIcon class="h-5 w-5 text-red-400" />
              <div class="ml-3">
                <h3 class="text-sm font-medium text-red-800 dark:text-red-200">
                  Zawodnik nie znaleziony
                </h3>
                <p class="text-sm text-red-700 dark:text-red-300 mt-1">
                  Nie znaleziono zawodnika z numerem startowym {{ manualCheckInForm.nr_startowy }}.
                </p>
              </div>
            </div>
          </div>

          <div v-else-if="previewLoading" class="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
            <div class="animate-pulse">
              <div class="flex items-center space-x-4">
                <div class="w-12 h-12 bg-gray-300 dark:bg-gray-600 rounded-full"></div>
                <div class="space-y-2">
                  <div class="h-4 bg-gray-300 dark:bg-gray-600 rounded w-32"></div>
                  <div class="h-3 bg-gray-300 dark:bg-gray-600 rounded w-24"></div>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg text-center">
            <UserIcon class="h-12 w-12 mx-auto text-gray-400 mb-2" />
            <p class="text-sm text-gray-500 dark:text-gray-400">
              Wprowadź numer startowy, aby zobaczyć podgląd zawodnika
            </p>
          </div>
        </div>
      </div>

      <!-- Historia ręcznych zameldowań -->
      <div v-if="manualCheckIns.length > 0" class="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
        <h3 class="text-md font-medium text-gray-900 dark:text-white mb-4">
          Ostatnie ręczne zameldowania ({{ manualCheckIns.length }})
        </h3>
        <div class="space-y-2 max-h-40 overflow-y-auto">
          <div
            v-for="checkIn in manualCheckIns.slice(0, 5)"
            :key="`manual-${checkIn.nr_startowy}-${checkIn.timestamp}`"
            class="flex items-center justify-between p-3 bg-orange-50 dark:bg-orange-900/20 rounded-lg"
          >
            <div class="flex items-center space-x-3">
              <div class="w-8 h-8 bg-orange-100 dark:bg-orange-900 rounded-full flex items-center justify-center">
                <span class="text-sm font-medium text-orange-600 dark:text-orange-400">
                  {{ checkIn.nr_startowy }}
                </span>
              </div>
              <div>
                <div class="text-sm font-medium text-gray-900 dark:text-white">
                  {{ checkIn.imie }} {{ checkIn.nazwisko }}
                </div>
                <div class="text-xs text-gray-500 dark:text-gray-400">
                  {{ formatCheckInReason(checkIn.powod) }}
                </div>
              </div>
            </div>
            <div class="text-xs text-gray-500 dark:text-gray-400">
              {{ formatTime(checkIn.timestamp) }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import axios from 'axios'
import {
  QrCodeIcon,
  ArrowPathIcon,
  ArrowDownTrayIcon,
  ClockIcon,
  DevicePhoneMobileIcon,
  ChartBarIcon,
  ExclamationTriangleIcon,
  WrenchScrewdriverIcon,
  DocumentTextIcon,
  HandRaisedIcon,
  XCircleIcon,
  UserIcon,
  CheckCircleIcon
} from '@heroicons/vue/24/outline'

// Types
interface BasicStats {
  total_zawodnikow: number
  z_qr_kodami: number
  zameldowanych: number
  bez_qr_kodow: number
  procent_zameldowanych: number
}

interface RecentCheckpoint {
  nr_startowy: number
  imie: string
  nazwisko: string
  kategoria: string
  checkpoint_name: string
  scan_time: string
  device_id: string
}

interface DeviceActivity {
  device_id: string
  total_scans: number
  last_activity: string
  unique_zawodnicy: number
  check_ins: number
  results: number
}

interface CategoryStats {
  kategoria: string
  total: number
  zameldowanych: number
  z_wynikami: number
}

interface HourlyProgress {
  hour: string
  scans: number
  check_ins: number
  results: number
}

interface Issue {
  type: string
  title: string
  count: number
  details: any[]
}

interface ManualCheckInForm {
  nr_startowy: number
  powod: string
  opis: string
}

interface ManualCheckIn {
  nr_startowy: number
  imie: string
  nazwisko: string
  kategoria: string
  checked_in: boolean
  check_in_time: string
  qr_code: boolean
  ma_wynik: boolean
  klub: string
  plec: string
  powod?: string
  timestamp?: string
}

// Reactive state
const loading = ref(false)
const basicStats = ref<BasicStats>({
  total_zawodnikow: 0,
  z_qr_kodami: 0,
  zameldowanych: 0,
  bez_qr_kodow: 0,
  procent_zameldowanych: 0
})
const recentCheckpoints = ref<RecentCheckpoint[]>([])
const deviceActivity = ref<DeviceActivity[]>([])
const categoryStats = ref<CategoryStats[]>([])
const hourlyProgress = ref<HourlyProgress[]>([])
const issues = ref<Issue[]>([])
const manualCheckInForm = ref<ManualCheckInForm>({
  nr_startowy: 0,
  powod: '',
  opis: ''
})
const manualCheckInLoading = ref(false)
const previewZawodnik = ref<ManualCheckIn | null>(null)
const previewLoading = ref(false)
const manualCheckIns = ref<ManualCheckIn[]>([])

// Auto refresh interval
let refreshInterval: NodeJS.Timeout | null = null
let previewTimeout: NodeJS.Timeout | null = null

// Computed
const maxHourlyActivity = computed(() => {
  if (hourlyProgress.value.length === 0) return 1
  return Math.max(...hourlyProgress.value.map(h => Math.max(h.check_ins, h.results)))
})

const canPerformManualCheckIn = computed(() => {
  return manualCheckInForm.value.nr_startowy > 0 && 
         manualCheckInForm.value.powod !== '' &&
         previewZawodnik.value !== null &&
         !previewZawodnik.value.checked_in
})

// Watchers
watch(() => manualCheckInForm.value.nr_startowy, (newValue) => {
  if (previewTimeout) {
    clearTimeout(previewTimeout)
  }
  
  if (newValue && newValue > 0) {
    previewTimeout = setTimeout(() => {
      fetchZawodnikPreview(newValue)
    }, 500) // Debounce 500ms
  } else {
    previewZawodnik.value = null
  }
})

// Methods
const fetchDashboardData = async () => {
  try {
    loading.value = true
    const response = await axios.get('/api/qr/dashboard')
    
    if (response.data.success) {
      basicStats.value = response.data.basic_stats
      recentCheckpoints.value = response.data.recent_checkpoints
      deviceActivity.value = response.data.device_activity
      categoryStats.value = response.data.category_stats
      hourlyProgress.value = response.data.hourly_progress
      issues.value = response.data.issues
    }
  } catch (error) {
    console.error('Błąd podczas pobierania danych dashboard:', error)
  } finally {
    loading.value = false
  }
}

const refreshData = () => {
  fetchDashboardData()
}

const exportData = async () => {
  try {
    window.open('/api/qr/export', '_blank')
  } catch (error) {
    console.error('Błąd podczas eksportu:', error)
  }
}

const generateMissingQR = async () => {
  // TODO: Implement bulk QR generation
  alert('Funkcja w przygotowaniu')
}

const resetAllCheckIns = async () => {
  if (confirm('Czy na pewno chcesz zresetować wszystkie check-iny? Ta operacja jest nieodwracalna.')) {
    // TODO: Implement reset
    alert('Funkcja w przygotowaniu')
  }
}

const viewSystemLogs = () => {
  // TODO: Implement system logs viewer
  alert('Funkcja w przygotowaniu')
}

const formatTime = (timeString: string) => {
  const date = new Date(timeString)
  return date.toLocaleTimeString('pl-PL', { 
    hour: '2-digit', 
    minute: '2-digit',
    second: '2-digit'
  })
}

const formatHour = (hourString: string) => {
  const date = new Date(hourString)
  return date.toLocaleTimeString('pl-PL', { 
    hour: '2-digit', 
    minute: '2-digit'
  })
}

const formatCheckpointName = (name: string) => {
  const names: Record<string, string> = {
    'check-in': 'Zameldowanie',
    'finish': 'Meta',
    'verify': 'Weryfikacja'
  }
  return names[name] || name
}

const formatCheckInReason = (reason: string) => {
  const reasons: Record<string, string> = {
    'awaria_skanera': 'Awaria skanera QR',
    'brak_kodu': 'Brak/uszkodzony kod QR',
    'problem_techniczny': 'Problem techniczny',
    'decyzja_organizatora': 'Decyzja organizatora',
    'inne': 'Inne'
  }
  return reasons[reason] || reason
}

const fetchZawodnikPreview = async (nr_startowy: number) => {
  if (!nr_startowy || nr_startowy <= 0) {
    previewZawodnik.value = null
    return
  }

  try {
    previewLoading.value = true
    const response = await axios.get(`/api/zawodnicy/${nr_startowy}`)
    
    if (response.data.success) {
      previewZawodnik.value = response.data.zawodnik
    } else {
      previewZawodnik.value = null
    }
  } catch (error) {
    console.error('Błąd podczas pobierania podglądu zawodnika:', error)
    previewZawodnik.value = null
  } finally {
    previewLoading.value = false
  }
}

const performManualCheckIn = async () => {
  if (!canPerformManualCheckIn.value) {
    return
  }

  try {
    manualCheckInLoading.value = true
    
    const payload = {
      nr_startowy: manualCheckInForm.value.nr_startowy,
      device_id: 'manual-admin',
      manual: true,
      reason: manualCheckInForm.value.powod,
      description: manualCheckInForm.value.opis || null
    }

    const response = await axios.post('/api/qr/check-in', payload)
    
    if (response.data.success) {
      // Sukces - odśwież dane
      await fetchDashboardData()
      await fetchZawodnikPreview(manualCheckInForm.value.nr_startowy)
      
      // Dodaj do historii ręcznych zameldowań
      manualCheckIns.value.unshift({
        nr_startowy: manualCheckInForm.value.nr_startowy,
        imie: previewZawodnik.value?.imie || '',
        nazwisko: previewZawodnik.value?.nazwisko || '',
        kategoria: previewZawodnik.value?.kategoria || '',
        checked_in: true,
        check_in_time: new Date().toISOString(),
        qr_code: previewZawodnik.value?.qr_code || false,
        ma_wynik: previewZawodnik.value?.ma_wynik || false,
        klub: previewZawodnik.value?.klub || '',
        plec: previewZawodnik.value?.plec || '',
        powod: manualCheckInForm.value.powod,
        timestamp: new Date().toISOString()
      })
      
      // Reset formularza
      manualCheckInForm.value = {
        nr_startowy: 0,
        powod: '',
        opis: ''
      }
      
      alert(`✅ Zawodnik ${previewZawodnik.value?.imie} ${previewZawodnik.value?.nazwisko} został pomyślnie zameldowany ręcznie.`)
    } else {
      alert(`❌ Błąd podczas zameldowania: ${response.data.message}`)
    }
  } catch (error: any) {
    console.error('Błąd podczas ręcznego zameldowania:', error)
    const errorMsg = error.response?.data?.message || 'Nieznany błąd serwera'
    alert(`❌ Błąd podczas zameldowania: ${errorMsg}`)
  } finally {
    manualCheckInLoading.value = false
  }
}

const fetchManualCheckIns = async () => {
  try {
    const response = await axios.get('/api/qr/manual-checkins')
    if (response.data.success) {
      manualCheckIns.value = response.data.manual_checkins
    }
  } catch (error) {
    console.error('Błąd podczas pobierania ręcznych zameldowań:', error)
  }
}

// Lifecycle
onMounted(() => {
  fetchDashboardData()
  fetchManualCheckIns()
  // Auto refresh every 10 seconds
  refreshInterval = setInterval(fetchDashboardData, 10000)
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
  if (previewTimeout) {
    clearTimeout(previewTimeout)
  }
})
</script> 