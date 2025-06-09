from queue_manager import QueueManager

print('🔍 SZCZEGÓŁOWY DEBUG unhide_athlete')

qm = QueueManager()

# Symulacja unhide_athlete krok po kroku
nr_startowy = 1

with qm.get_connection() as conn:
    cur = conn.cursor()
    
    print(f'1. Sprawdzanie zawodnika #{nr_startowy}')
    cur.execute("SELECT status FROM start_queue WHERE nr_startowy = %s", (nr_startowy,))
    result = cur.fetchone()
    
    print(f'   result: {result}')
    print(f'   type(result): {type(result)}')
    
    if result:
        print(f'   result["status"]: "{result["status"]}"')
        print(f'   result["status"] == "hidden": {result["status"] == "hidden"}')
        print(f'   result["status"] != "hidden": {result["status"] != "hidden"}')
    
    condition1 = not result
    condition2 = result and result['status'] != 'hidden'
    overall_condition = condition1 or condition2
    
    print(f'2. Warunki:')
    print(f'   not result: {condition1}')
    print(f'   result["status"] != "hidden": {condition2}')
    print(f'   overall (should return error): {overall_condition}')
    
    if overall_condition:
        print('3. ❌ Zwracam błąd: "Zawodnik nie jest ukryty"')
    else:
        print('3. ✅ Przechodzę dalej - zawodnik jest ukryty')
        
        # Sprawdź następną pozycję - POPRAWIONA SKŁADNIA
        cur.execute("SELECT COALESCE(MAX(queue_position), 0) + 1 as next_position FROM start_queue WHERE status = 'waiting'")
        next_position_result = cur.fetchone()
        next_position = next_position_result['next_position'] if next_position_result else 1
        print(f'   Następna pozycja: {next_position}')
        
        # Symulacja UPDATE (bez commitu)
        print(f'   Wykonuję UPDATE na zawodniku #{nr_startowy}')
        # cur.execute("""
        #     UPDATE start_queue 
        #     SET status = 'waiting', queue_position = %s 
        #     WHERE nr_startowy = %s
        # """, (next_position, nr_startowy))
        # conn.commit()
        print('   UPDATE wykonany pomyślnie (symulacja)')

print('\n🧪 Teraz wywołuję prawdziwą funkcję unhide_athlete:')
result = qm.unhide_athlete(1)
print(f'Rezultat: {result}') 