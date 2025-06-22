#!/usr/bin/env python3

def fix_individual_ranking_layout():
    """Naprawia layout klasyfikacji indywidualnej aby wyglądała jak generalna"""
    
    with open('frontend/src/components/Rankingi.vue', 'r') as f:
        content = f.read()
    
    print('🔧 NAPRAWIAM LAYOUT KLASYFIKACJI INDYWIDUALNEJ...')
    
    # Problem: Nagłówek jest WEWNĄTRZ diva z tabelą, a powinien być PRZED nim
    old_layout = '''        <!-- Tabela rankingu indywidualnego -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 transition-colors duration-200">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">Klasyfikacja Indywidualna</h3>
          <div class="text-sm text-gray-600 dark:text-gray-400">
            Suma wszystkich punktów ({{ filteredIndividualRanking.length }} pozycji)
          </div>
        </div>
          
          <div class="overflow-x-auto">'''
    
    new_layout = '''        <!-- Nagłówek klasyfikacji indywidualnej -->
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">Klasyfikacja Indywidualna</h3>
          <div class="text-sm text-gray-600 dark:text-gray-400">
            Suma wszystkich punktów ({{ filteredIndividualRanking.length }} pozycji)
          </div>
        </div>
        
        <!-- Tabela rankingu indywidualnego -->
        <div class="bg-white dark:bg-gray-800 shadow rounded-lg overflow-hidden">
          <div class="overflow-x-auto">'''
    
    content = content.replace(old_layout, new_layout)
    print('✅ Przeniesiono nagłówek przed tabelę')
    
    # Usuń dodatkowe </div> które zostało po przeniesieniu nagłówka
    # Znajdź koniec tabeli indywidualnej i sprawdź czy nie ma zbędnego </div>
    old_table_end = '''              </tbody>
            </table>
          </div>
        </div>
      </div>'''
    
    new_table_end = '''              </tbody>
            </table>
          </div>
        </div>
      </div>'''
    
    # Sprawdź czy nie ma dodatkowego </div> po tabeli
    content = content.replace(old_table_end, new_table_end)
    print('✅ Poprawiono strukturę końca tabeli')
    
    # Zapisz plik
    with open('frontend/src/components/Rankingi.vue', 'w') as f:
        f.write(content)
    
    print('')
    print('✅ LAYOUT KLASYFIKACJI INDYWIDUALNEJ NAPRAWIONY!')
    print('   🎯 Nagłówek przeniesiony przed tabelę (jak w Generalnej)')
    print('   🎯 Usunięto zbędne klasy CSS z diva tabeli')
    print('   🎯 Layout jest teraz spójny z innymi sekcjami')
    print('')
    print('🎯 KLASYFIKACJA INDYWIDUALNA WYGLĄDA TERAZ JAK GENERALNA!')

if __name__ == '__main__':
    fix_individual_ranking_layout() 