#!/usr/bin/env python3
"""
SKATECROSS UNIFIED START CONTROL - Test Integration
Test całej ścieżki: QR Scanner → Grupy → Aktywacja → SECTRO → Wyniki
"""

import requests
import json
import time
from datetime import datetime

# Konfiguracja
BACKEND_URL = "http://localhost:5001"
TEST_DATA = {
    "test_zawodnik_id": 1,  # ID testowego zawodnika
    "test_kategoria": "Junior B",
    "test_plec": "M"
}

def test_step_1_qr_scanner():
    """Test 1: QR Scanner - meldowanie zawodnika"""
    print("🔍 TEST 1: QR Scanner - meldowanie zawodnika")
    
    url = f"{BACKEND_URL}/api/unified/register-athlete"
    payload = {
        "identifier": TEST_DATA["test_zawodnik_id"],
        "action": "checkin"
    }
    
    response = requests.post(url, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 200
    assert response.json()["success"] == True
    print("✅ QR Scanner działa!\n")

def test_step_2_groups():
    """Test 2: Grupy startowe - automatyczne grupowanie"""
    print("🎯 TEST 2: Grupy startowe")
    
    url = f"{BACKEND_URL}/api/unified/groups"
    response = requests.get(url)
    
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Liczba grup: {len(data.get('data', []))}")
    
    # Znajdź grupę testową
    test_group = None
    for group in data.get('data', []):
        if (group['kategoria'] == TEST_DATA["test_kategoria"] and 
            group['plec'] == TEST_DATA["test_plec"]):
            test_group = group
            break
    
    assert test_group is not None
    print(f"✅ Grupa znaleziona: {test_group['kategoria']}-{test_group['plec']}")
    print(f"   Zawodnicy w grupie: {len(test_group['zawodnicy'])}\n")
    
    return test_group

def test_step_3_activation(group):
    """Test 3: Aktywacja grupy → tworzy sesję SECTRO"""
    print("🚀 TEST 3: Aktywacja grupy")
    
    url = f"{BACKEND_URL}/api/unified/activate-group"
    payload = {
        "kategoria": group["kategoria"],
        "plec": group["plec"]
    }
    
    response = requests.post(url, json=payload)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {data}")
    
    assert response.status_code == 200
    assert data["success"] == True
    print("✅ Grupa aktywowana!\n")
    
    return data.get("session_id")

def test_step_4_sectro_timing(session_id):
    """Test 4: SECTRO Live Timing"""
    print("⏱️ TEST 4: SECTRO Live Timing")
    
    # Symuluj pomiar SECTRO
    url = f"{BACKEND_URL}/api/unified/record-measurement"
    test_frame = f"CZL1{TEST_DATA['test_zawodnik_id']:09d}"
    
    payload = {
        "raw_frame": test_frame,
        "session_id": session_id
    }
    
    response = requests.post(url, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 200
    print("✅ SECTRO timing działa!\n")

def test_step_5_results():
    """Test 5: Wyniki live"""
    print("🏆 TEST 5: Wyniki live")
    
    url = f"{BACKEND_URL}/api/unified/stats"
    response = requests.get(url)
    
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Status response: {data.get('success', False)}")
    
    if data.get('success'):
        print("Unified stats:")
        print(json.dumps(data.get('data', {}), indent=2, ensure_ascii=False))
    
    assert response.status_code == 200
    print("✅ Wyniki live działają!\n")

def main():
    """Główny test integracyjny"""
    print("=" * 60)
    print("🧪 SKATECROSS UNIFIED START CONTROL - TEST INTEGRACJI")
    print("=" * 60)
    
    try:
        # Sprawdź czy backend działa
        response = requests.get(f"{BACKEND_URL}/api/unified/health")
        if response.status_code != 200:
            print("❌ Backend nie odpowiada!")
            return
        
        print("✅ Backend dostępny\n")
        
        # Przeprowadź testy
        test_step_1_qr_scanner()
        group = test_step_2_groups()
        session_id = test_step_3_activation(group)
        
        # Daj czas na aktywację
        time.sleep(2)
        
        test_step_4_sectro_timing(session_id)
        test_step_5_results()
        
        print("=" * 60)
        print("🎉 WSZYSTKIE TESTY PRZESZŁY POMYŚLNIE!")
        print("✅ System unified jest gotowy do użycia")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        print("🔧 Sprawdź logi backend i popraw błędy")

if __name__ == "__main__":
    main() 