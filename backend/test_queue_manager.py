from queue_manager import QueueManager
import json

print('🧪 TESTOWANIE NOWEGO QUEUE MANAGER')
print('=' * 50)

qm = QueueManager()

# Test 1: Pobierz aktualną kolejkę
print('\n📊 TEST 1: Aktualna kolejka')
queue = qm.get_current_queue()
print(f'  Zawodników w kolejce: {len(queue)}')
for athlete in queue[:3]:  # Pokaż pierwszych 3
    print(f'  #{athlete["nr_startowy"]}: {athlete["imie"]} {athlete["nazwisko"]} | {athlete["source_type"]} | pos:{athlete["queue_position"]}')

# Test 2: Statystyki kolejki
print('\n📈 TEST 2: Statystyki kolejki')
stats = qm.get_queue_stats()
for key, value in stats.items():
    print(f'  {key}: {value}')

# Test 3: Informacje o konkretnym zawodniku
print('\n🔍 TEST 3: Info o zawodniku #1')
athlete_info = qm.get_athlete_queue_info(1)
if athlete_info:
    print(f'  Status: {athlete_info["status"]}')
    print(f'  Źródło: {athlete_info["source_type"]}')
    print(f'  Pozycja: {athlete_info["queue_position"]}')
    print(f'  Dodany: {athlete_info["added_at"]}')
else:
    print('  Zawodnik nie jest w kolejce')

# Test 4: Przetestuj usuwanie (tymczasowe)
print('\n❌ TEST 4: Usuwanie zawodnika #1 (tymczasowe)')
if athlete_info and athlete_info["status"] == "waiting":
    result = qm.remove_athlete(1, permanent=False)
    print(f'  Rezultat: {result["message"]}')
    print(f'  Typ: {result["type"]}')
    
    # Sprawdź statystyki po usunięciu
    stats_after = qm.get_queue_stats()
    print(f'  Ukrytych po usunięciu: {stats_after["hidden"]}')
    print(f'  Oczekujących po usunięciu: {stats_after["waiting"]}')
else:
    print('  Zawodnik nie jest w statusie waiting')

# Test 5: Przywrócenie zawodnika
print('\n🔄 TEST 5: Przywrócenie zawodnika #1')
unhide_result = qm.unhide_athlete(1)
if unhide_result['success']:
    print(f'  Rezultat: {unhide_result["message"]}')
    print(f'  Nowa pozycja: {unhide_result["position"]}')
else:
    print(f'  Błąd: {unhide_result["error"]}')

print('\n✅ TESTY ZAKOŃCZONE') 