#!/usr/bin/env python3
"""
SECTRO Manual Timing Simulator
Pozwala ręcznie sterować startem i finiszem zawodników z kolejki.

Autor: Claude AI
Data: 2025
"""

import requests
import time
from datetime import datetime
import sys
import os

API_URL = "http://localhost:5000"
SESSION_ID = int(os.environ.get('SESSION_ID', '1'))  # ID sesji z env lub domyślnie 1

# Pomocnicze funkcje

def format_sectro_time(timestamp: float) -> str:
    hours = int(timestamp // 3600)
    minutes = int((timestamp % 3600) // 60)
    seconds = int(timestamp % 60)
    milliseconds = int((timestamp % 1) * 1000)
    return f"{hours:02d}{minutes:02d}{seconds:02d}{milliseconds:03d}"

def get_seconds_since_midnight() -> float:
    now = datetime.now()
    return now.hour * 3600 + now.minute * 60 + now.second + now.microsecond / 1_000_000

def generate_sectro_frame(input_number: int, timestamp: float) -> str:
    return f"CZL{input_number}{format_sectro_time(timestamp)}"

def send_measurement(session_id: int, nr_startowy: int, frame: str) -> bool:
    try:
        response = requests.post(
            f"{API_URL}/api/sectro/measurements",
            json={
                "session_id": session_id,
                "nr_startowy": nr_startowy,
                "raw_frame": frame
            }
        )
        if response.status_code != 200:
            print(f"❌ Błąd API: {response.status_code} {response.text}")
            return False
        return True
    except Exception as e:
        print(f"Błąd wysyłania pomiaru: {e}")
        return False

def main():
    print("\n=== SECTRO Manual Timing Simulator ===\n")
    # Pobierz kolejkę zawodników
    response = requests.get(f"{API_URL}/api/start-queue")
    if response.status_code != 200:
        print("❌ Nie można pobrać kolejki startowej")
        return
    data = response.json()
    queue = data.get('queue', [])
    if not queue:
        print("ℹ️ Kolejka pusta, nic do symulacji.")
        return
    # Wyświetl listę
    print("Lista zawodników:")
    for i, athlete in enumerate(queue):
        print(f"{i+1}. {athlete['nr_startowy']} - {athlete['imie']} {athlete['nazwisko']}")
    print("\nWpisz numer zawodnika do START (Enter = kolejny z listy, q = zakończ):")
    idx = 0
    while idx < len(queue):
        athlete = queue[idx]
        nr_startowy = athlete['nr_startowy']
        imie = athlete['imie']
        nazwisko = athlete['nazwisko']
        inp = input(f"START zawodnika [{nr_startowy} - {imie} {nazwisko}]: ")
        if inp.strip().lower() == 'q':
            print("Kończę symulację.")
            break
        if inp.strip().isdigit():
            # Szukaj zawodnika o podanym numerze
            found = False
            for j, a in enumerate(queue):
                if str(a['nr_startowy']) == inp.strip():
                    athlete = a
                    nr_startowy = athlete['nr_startowy']
                    imie = athlete['imie']
                    nazwisko = athlete['nazwisko']
                    idx = j
                    found = True
                    break
            if not found:
                print("Nie ma takiego zawodnika w kolejce!")
                continue
        # START
        start_time = get_seconds_since_midnight()
        start_frame = generate_sectro_frame(1, start_time)
        if send_measurement(SESSION_ID, nr_startowy, start_frame):
            print(f"START: {nr_startowy} ({imie} {nazwisko}) @ {start_time:.3f}s od północy")
        else:
            print(f"❌ Błąd wysyłania START dla {nr_startowy}")
            continue
        # STOP
        input(f"Naciśnij Enter aby wysłać FINISH dla {nr_startowy}...")
        finish_time = get_seconds_since_midnight()
        finish_frame = generate_sectro_frame(4, finish_time)
        if send_measurement(SESSION_ID, nr_startowy, finish_frame):
            print(f"FINISH: {nr_startowy} ({imie} {nazwisko}) @ {finish_time:.3f}s od północy (czas: {finish_time-start_time:.3f}s)")
        else:
            print(f"❌ Błąd wysyłania FINISH dla {nr_startowy}")
        idx += 1
    print("\n✅ Symulacja zakończona!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Przerwano ręcznie.")
        sys.exit(0) 