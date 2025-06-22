"""
SKATECROSS QR System - Database Utils (In-Memory Demo)
Zarządzanie danymi demo w pamięci
"""

from datetime import datetime

# Przykładowe dane zawodników (zamiast bazy danych)
zawodnicy_data = [
    {"nr_startowy": 1, "imie": "Jan", "nazwisko": "Kowalski", "kategoria": "Senior", "plec": "M", "klub": "KTH Krynica", "qr_code": None, "checked_in": False, "check_in_time": None},
    {"nr_startowy": 2, "imie": "Anna", "nazwisko": "Nowak", "kategoria": "Senior", "plec": "K", "klub": "UKS Boots", "qr_code": None, "checked_in": False, "check_in_time": None},
    {"nr_startowy": 3, "imie": "Piotr", "nazwisko": "Wiśniewski", "kategoria": "Junior", "plec": "M", "klub": "KTH Krynica", "qr_code": None, "checked_in": False, "check_in_time": None},
    {"nr_startowy": 4, "imie": "Maria", "nazwisko": "Wójcik", "kategoria": "Junior", "plec": "K", "klub": "UKS Boots", "qr_code": None, "checked_in": False, "check_in_time": None},
    {"nr_startowy": 5, "imie": "Tomasz", "nazwisko": "Kowalczyk", "kategoria": "Senior", "plec": "M", "klub": "SKL Zakopane", "qr_code": None, "checked_in": False, "check_in_time": None},
    {"nr_startowy": 6, "imie": "Katarzyna", "nazwisko": "Dąbrowska", "kategoria": "Junior", "plec": "K", "klub": "Roller Team", "qr_code": None, "checked_in": False, "check_in_time": None},
    {"nr_startowy": 7, "imie": "Michał", "nazwisko": "Lewandowski", "kategoria": "Senior", "plec": "M", "klub": "Speed Demons", "qr_code": None, "checked_in": False, "check_in_time": None},
    {"nr_startowy": 8, "imie": "Agnieszka", "nazwisko": "Zielińska", "kategoria": "Senior", "plec": "K", "klub": "Roller Team", "qr_code": None, "checked_in": False, "check_in_time": None},
]

# Grupy startowe
grupy_startowe_data = [
    {"kategoria": "Senior", "plec": "M", "numer_grupy": 1, "nazwa": "Senior Mężczyźni", "status": "WAITING"},
    {"kategoria": "Senior", "plec": "K", "numer_grupy": 2, "nazwa": "Senior Kobiety", "status": "WAITING"},
    {"kategoria": "Junior", "plec": "M", "numer_grupy": 3, "nazwa": "Junior Mężczyźni", "status": "WAITING"},
    {"kategoria": "Junior", "plec": "K", "numer_grupy": 4, "nazwa": "Junior Kobiety", "status": "WAITING"},
]

def find_zawodnik_by_nr(nr_startowy):
    """Znajdź zawodnika po numerze startowym"""
    for zawodnik in zawodnicy_data:
        if zawodnik["nr_startowy"] == nr_startowy:
            return zawodnik
    return None

def find_grupa_by_kategoria_plec(kategoria, plec):
    """Znajdź grupę po kategorii i płci"""
    for grupa in grupy_startowe_data:
        if grupa["kategoria"] == kategoria and grupa["plec"] == plec:
            return grupa
    return None

def get_zawodnicy_w_grupie(kategoria, plec):
    """Pobierz zawodników w danej grupie"""
    return [z for z in zawodnicy_data 
            if z["kategoria"] == kategoria and z["plec"] == plec]

def get_aktywna_grupa():
    """Pobierz aktywną grupę"""
    for grupa in grupy_startowe_data:
        if grupa["status"] == "ACTIVE":
            return grupa
    return None

def set_grupa_aktywna(kategoria, plec, active=True):
    """Ustaw grupę jako aktywną"""
    # Najpierw deaktywuj wszystkie grupy
    for grupa in grupy_startowe_data:
        grupa["status"] = "WAITING"
    
    # Potem aktywuj wybraną
    if active:
        grupa = find_grupa_by_kategoria_plec(kategoria, plec)
        if grupa:
            grupa["status"] = "ACTIVE"
            return grupa
    return None

def update_zawodnik_qr(nr_startowy, qr_code):
    """Zaktualizuj QR kod zawodnika"""
    zawodnik = find_zawodnik_by_nr(nr_startowy)
    if zawodnik:
        zawodnik["qr_code"] = qr_code
        return True
    return False

def checkin_zawodnik(nr_startowy):
    """Zamelduj zawodnika w kolejce"""
    zawodnik = find_zawodnik_by_nr(nr_startowy)
    if zawodnik:
        zawodnik["checked_in"] = True
        zawodnik["check_in_time"] = datetime.now().isoformat()
        return True
    return False

def get_qr_stats():
    """Pobierz statystyki QR kodów"""
    total = len(zawodnicy_data)
    z_qr = len([z for z in zawodnicy_data if z.get("qr_code")])
    bez_qr = total - z_qr
    
    return {
        "total_zawodnikow": total,
        "z_qr_kodami": z_qr,
        "bez_qr_kodow": bez_qr
    } 