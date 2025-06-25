# 🧹 SKATECROSS v36.1 - DATABASE CLEANUP BRANCH

## 🎯 **CEL GAŁĘZI**
Gałąź `v36.1-database-cleanup` ma na celu **uporządkowanie bazy danych** i **naprawę rozbieżności** wykrytych w dogłębnej analizie systemu SKATECROSS v36.0.

---

## 🔍 **WYKRYTE PROBLEMY**

### **1. 🚨 KRYTYCZNE: Chaos w SECTRO_SESSIONS**
- **15 aktywnych sesji jednocześnie** (powinno być max 1)
- **Duplikaty sesji** dla tych samych grup
- **Śmieciowe sesje** z testów (nazwy: "a", "e", "t", "y")
- **Stare sesje aktywne** z 8 czerwca nadal `active`

### **2. 🗑️ LEGACY CRUFT**
- `start_queue` (14 rekordów) - **nieużywane**
- `kolejki_startowe` (118 rekordów) - **legacy system**
- `unified_start_queue` (1 rekord) - **niedokończone**
- `aktywna_grupa_settings` (1 rekord) - **stary system**
- `v_current_queue` - **view na legacy tabele**

### **3. 🔄 ROZBIEŻNE SYSTEMY KOLEJEK**
3 różne systemy kolejek działające równolegle bez koordynacji

### **4. 📊 NIESPÓJNOŚCI API**
- Błędna logika `_get_sectro_info_for_group`
- Brak sprawdzania duplikatów przy aktywacji grup
- Nieużywane legacy endpoints

---

## 📋 **PLAN NAPRAW**

### **FAZA 1: 🧹 CLEANUP BAZY DANYCH**
- ✅ **Skrypt przygotowany**: `CLEANUP_DATABASE_SCRIPT.sql`
- 🔄 **Backup bazy** przed cleanup
- 🧹 **Anulowanie śmieciowych sesji**
- 🗑️ **Usunięcie legacy tabel**
- 🔧 **Zachowanie tylko najnowszych sesji**

### **FAZA 2: 🔧 NAPRAWY API**
- 🛠️ **Poprawa `unified_start_manager.py`**
- 🚫 **Usunięcie legacy endpoints**
- ✅ **Dodanie constraints bazy**
- 📊 **Nowa logika grup**

### **FAZA 3: 🧪 TESTY I WERYFIKACJA**
- 🔍 **Testy scenariuszy aktywacji**
- 📈 **Monitoring aktywnych sesji**
- ✅ **Weryfikacja API responses**

---

## 📁 **PLIKI W GAŁĘZI**

### **📋 Dokumentacja cleanup:**
- `CLEANUP_DATABASE_SCRIPT.sql` - **Główny skrypt czyszczenia**
- `DATABASE_FIXES_NEEDED.md` - **Plan napraw API**
- `README_v36.1_DATABASE_CLEANUP.md` - **Ten plik**

### **🔧 Naprawione już:**
- `unified_start_manager.py` - **Naprawiona logika `_get_sectro_info_for_group`**
- `StartGroupsCard.vue` - **Mapowanie `status` vs `is_active`**

---

## 🚀 **WORKFLOW DEVELOPMENT**

### **1. Backup Production Data**
```bash
# Uruchom przed jakimikolwiek zmianami
CREATE TABLE sectro_sessions_backup AS SELECT * FROM sectro_sessions;
CREATE TABLE sectro_results_backup AS SELECT * FROM sectro_results;
```

### **2. Uruchom Cleanup Script**
```bash
# W bezpiecznym środowisku testowym
psql < CLEANUP_DATABASE_SCRIPT.sql
```

### **3. Deploy API Fixes**
```bash
# Po cleanup bazy
git checkout v36.1-database-cleanup
# Test API endpoints
curl http://localhost:5001/api/unified/groups
```

### **4. Monitoring**
```bash
# Sprawdź aktywne sesje
SELECT COUNT(*) FROM sectro_sessions WHERE status = 'active';
# Powinno zwrócić 0-1
```

---

## ✅ **KRYTERIA SUKCESU**

### **📊 Baza Danych:**
- ✅ **0-1 aktywnych sesji SECTRO** jednocześnie
- ✅ **Brak legacy tabel** (start_queue, kolejki_startowe, etc.)
- ✅ **Czyste sesje** (bez śmieciowych nazw)
- ✅ **Spójne dane** API vs baza

### **🔧 API:**
- ✅ **Prawidłowa aktywacja grup** (tylko 1 na raz)
- ✅ **Poprawne statusy** WAITING/READY/ACTIVE/TIMING
- ✅ **Brak legacy endpoints**
- ✅ **Constraints bazy** zapobiegające duplikatom

### **🧪 Frontend:**
- ✅ **Przyciski aktywacji działają**
- ✅ **Statusy grup prawidłowe**
- ✅ **Real-time updates**
- ✅ **Brak błędów w console**

---

## 🔄 **MERGE STRATEGY**

1. **Ukończ wszystkie naprawy** na `v36.1-database-cleanup`
2. **Przetestuj thoroughly** w środowisku dev
3. **Create Pull Request** do `v36.0`
4. **Code review** i weryfikacja
5. **Merge do v36.0** po zatwierdzeniu
6. **Deploy na production** z backup planem

---

## 📞 **KONTAKT**

W przypadku pytań lub problemów z implementacją napraw:
- 🔧 **API Issues**: Sprawdź `DATABASE_FIXES_NEEDED.md`
- 🗄️ **Database Issues**: Użyj `CLEANUP_DATABASE_SCRIPT.sql`
- ⚠️ **Emergency**: Przywróć backup i wróć do v36.0

---

**🎯 Cel: System SKATECROSS z czystą bazą danych i stabilną logiką grup!** 