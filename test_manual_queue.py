#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SKATECROSS QR - Manual Testing Script
Testowanie kolejki startowej i funkcji aktywacji grup
"""

import requests
import json
import sys
import os

# Dodaj backend do path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

BASE_URL = "http://localhost:5001/api"

def test_queue():
    """Test kolejki startowej"""
    print("📋 SPRAWDZANIE KOLEJKI STARTOWEJ:")
    try:
        response = requests.get(f"{BASE_URL}/unified/queue")
        data = response.json()
        
        if data.get('success'):
            queue = data.get('data', [])
            print(f"   ✅ Kolejka: {len(queue)} zawodników")
            for i, athlete in enumerate(queue, 1):
                print(f"   {i}. #{athlete['nr_startowy']} {athlete['imie']} {athlete['nazwisko']} - {athlete['kategoria']} {athlete['plec']}")
        else:
            print(f"   ❌ Błąd: {data.get('error', 'Unknown')}")
    except Exception as e:
        print(f"   ❌ Błąd połączenia: {e}")

def test_groups():
    """Test statusu grup"""
    print("\n🏁 SPRAWDZANIE STATUSU GRUP:")
    try:
        response = requests.get(f"{BASE_URL}/unified/groups")
        data = response.json()
        
        if data.get('success'):
            groups = data.get('data', [])
            print(f"   ✅ Znaleziono {len(groups)} grup")
            for group in groups:
                status = "🟢 AKTYWNA" if group.get('is_active') else "⚪ NIEAKTYWNA"
                print(f"   {status} {group['kategoria']} {group['plec']} - {group.get('checked_in_count', 0)} zameldowanych")
        else:
            print(f"   ❌ Błąd: {data.get('error', 'Unknown')}")
    except Exception as e:
        print(f"   ❌ Błąd połączenia: {e}")

def test_activate_group(kategoria, plec):
    """Test aktywacji grupy"""
    print(f"\n🔛 AKTYWACJA GRUPY {kategoria} {plec}:")
    try:
        payload = {"kategoria": kategoria, "plec": plec}
        response = requests.post(f"{BASE_URL}/unified/activate-group", 
                               json=payload)
        data = response.json()
        
        if data.get('success'):
            action = data.get('action', 'unknown')
            session = data.get('session', {})
            athletes_added = data.get('athletes_added', 0)
            print(f"   ✅ Sukces: {action}")
            print(f"   📊 Session #{session.get('id')} - Status: {session.get('status')}")
            print(f"   👥 Dodano zawodników: {athletes_added}")
        else:
            print(f"   ❌ Błąd: {data.get('error', 'Unknown')}")
    except Exception as e:
        print(f"   ❌ Błąd połączenia: {e}")

def test_deactivate_group(kategoria, plec):
    """Test dezaktywacji grupy"""
    print(f"\n🔛 DEZAKTYWACJA GRUPY {kategoria} {plec}:")
    try:
        payload = {"kategoria": kategoria, "plec": plec}
        response = requests.post(f"{BASE_URL}/unified/deactivate-group", 
                               json=payload)
        data = response.json()
        
        if data.get('success'):
            print(f"   ✅ Sukces: {data.get('message', 'Grupa dezaktywowana')}")
        else:
            print(f"   ❌ Błąd: {data.get('error', 'Unknown')}")
    except Exception as e:
        print(f"   ❌ Błąd połączenia: {e}")

def test_register_athlete(nr_startowy, action="checkin"):
    """Test meldunku zawodnika"""
    print(f"\n👤 MELDUNEK ZAWODNIKA #{nr_startowy} ({action}):")
    try:
        payload = {"identifier": nr_startowy, "action": action}
        response = requests.post(f"{BASE_URL}/unified/register", 
                               json=payload)
        data = response.json()
        
        if data.get('success'):
            athlete = data.get('athlete', {})
            print(f"   ✅ Sukces: #{athlete.get('nr_startowy')} {athlete.get('imie')} {athlete.get('nazwisko')}")
            print(f"   📊 Status: {action}ed")
        else:
            print(f"   ❌ Błąd: {data.get('error', 'Unknown')}")
    except Exception as e:
        print(f"   ❌ Błąd połączenia: {e}")

def main():
    """Główna funkcja testująca"""
    print("🧪 SKATECROSS QR - MANUAL TESTING")
    print("=" * 50)
    
    # Test 1: Stan początkowy
    test_queue()
    test_groups()
    
    # Test 2: Aktywacja grupy Junior A M
    test_activate_group("Junior A", "M")
    test_queue()  # Sprawdź kolejkę po aktywacji
    
    # Test 3: Dezaktywacja grupy Junior B M
    test_deactivate_group("Junior B", "M")
    test_queue()  # Sprawdź kolejkę po dezaktywacji
    
    # Test 4: Reaktywacja grupy Junior B M
    test_activate_group("Junior B", "M")
    test_queue()  # Sprawdź kolejkę po reaktywacji
    
    # Test 5: Status końcowy
    print("\n" + "=" * 50)
    print("🎯 STATUS KOŃCOWY:")
    test_groups()
    test_queue()

if __name__ == "__main__":
    main()
