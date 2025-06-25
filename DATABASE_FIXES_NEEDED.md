# 🔧 NAPRAWY POTRZEBNE W KODZIE API

## 1. 🚨 UNIFIED_START_MANAGER.PY

### Problem 1: Błędna logika `_get_sectro_info_for_group`
```python
# OBECNE (BŁĘDNE):
session = get_one("""
    SELECT id, nazwa, status FROM sectro_sessions 
    WHERE kategoria = %s AND plec = %s 
    AND status IN ('active', 'timing')  # To jest OK teraz po naprawie
    ORDER BY created_at DESC LIMIT 1
""", (kategoria, plec))

# PROBLEM: Może być wiele aktywnych sesji dla jednej grupy!
# POTRZEBA: Dodać UNIQUE constraint lub lepszą logikę
```

### Problem 2: `activate_group_unified` nie sprawdza duplikatów
```python
# DODAJ SPRAWDZENIE:
existing_active = get_all("""
    SELECT COUNT(*) as count FROM sectro_sessions 
    WHERE status IN ('active', 'timing')
""")[0]['count']

if existing_active > 0:
    # Dezaktywuj poprzednie lub wykaż błąd
```

### Problem 3: Brak cleanup przy deaktywacji
```python
# W deactivate_group_unified DODAJ:
# - Cleanup sectro_results dla sesji
# - Cleanup unified queue entries  
# - Reset group settings
```

## 2. 🗑️ USUNIĘCIE LEGACY ENDPOINTS

### Endpoints do usunięcia z api_server.py:
- `/api/grupy-startowe` (stary system grup)
- `/api/scan-qr` (stary QR system)  
- `/api/grupa-aktywna` (legacy active group)
- `/api/start-queue` (stary queue system)

### Komponenty frontend do usunięcia:
- CentrumStartuV2.vue ✅ (już usunięte)
- StartLineScanner.vue ✅ (już usunięte)
- Wszelkie referencje do starych API

## 3. 📊 NOWA LOGIKA GRUP

### Potrzebna zmiana w get_groups_with_status():
```python
# OBECNIE: Sprawdza wszystkie zameldowanych
# PROBLEM: Nie uwzględnia że grupa może być aktywna bez sesji

# NOWA LOGIKA:
def get_groups_with_status(self):
    # 1. Pobierz wszystkie grupy z zameldowanymi
    # 2. Sprawdź aktywne sesje SECTRO  
    # 3. Mapuj status WAITING/READY/ACTIVE/TIMING/COMPLETED
    # 4. Uwzględnij że może być tylko 1 aktywna grupa jednocześnie
```

## 4. 🔄 UNIFIED QUEUE SYSTEM

### Problem: 3 systemy kolejek
```sql
-- DO USUNIĘCIA:
- start_queue (legacy)
- unified_start_queue (nie używane)
- kolejki_startowe (legacy)
- v_current_queue (view na legacy)

-- ZOSTAJE:
- Tylko logika w get_unified_queue() z zawodnicy + sectro_results
```

## 5. 🏁 CONSTRAINTS BAZY DANYCH

### Dodać constraints:
```sql
-- Tylko jedna aktywna sesja jednocześnie
CREATE UNIQUE INDEX idx_one_active_session 
ON sectro_sessions (status) 
WHERE status = 'active';

-- Unikalne grupy w sesji
ALTER TABLE sectro_sessions 
ADD CONSTRAINT unique_active_group 
UNIQUE (kategoria, plec, status) 
WHERE status IN ('active', 'timing');
```

## 6. 📈 MONITORING I LOGI

### Dodać monitoring:
- Log przy aktywacji/deaktywacji grup
- Alert przy wielu aktywnych sesjach  
- Cleanup job dla starych sesji
- Backup przed każdą operacją cleanup

## 7. 🧪 TESTY

### Scenariusze testowe:
1. Aktywacja grupy gdy inna już aktywna
2. Deaktywacja i ponowna aktywacja tej samej grupy
3. System z 0 zameldowanych zawodników
4. Restart systemu z aktywnymi sesjami
5. Cleanup bazy po testach

## 8. 📋 MIGRATION SCRIPT

### Potrzebny migration dla produkcji:
1. Backup wszystkich danych
2. Cleanup według CLEANUP_DATABASE_SCRIPT.sql
3. Deploy nowego kodu API
4. Weryfikacja działania
5. Monitoring przez 24h

## PRIORYTETY:

🔥 **KRYTYCZNE** (do zrobienia natychmiast):
- Uruchomić CLEANUP_DATABASE_SCRIPT.sql
- Naprawić _get_sectro_info_for_group logic
- Dodać UNIQUE constraint dla aktywnych sesji

⚡ **WAŻNE** (w tym tygodniu):  
- Usunąć legacy endpoints
- Napisać testy dla grup
- Monitoring aktywnych sesji

✅ **NICE TO HAVE** (kiedy będzie czas):
- Automated cleanup job
- Advanced monitoring dashboard
- Performance optimization 