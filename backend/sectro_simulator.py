#!/usr/bin/env python3
"""
SECTRO Live Timing Simulator
Symuluje pomiary czasu z urządzenia SECTRO dla celów testowych

Autor: Claude AI
Data: 2025
"""

import requests
import time
import random
from datetime import datetime, time as dtime
import json
import sys
from typing import List, Dict, Optional
import threading

# Konfiguracja
API_URL = "http://localhost:5000"
SESSION_ID = 1  # ID sesji SECTRO
MIN_RACE_TIME = 15.0  # Minimalny czas przejazdu (sekundy)
MAX_RACE_TIME = 20.0  # Maksymalny czas przejazdu (sekundy)
MIN_DELAY = 2.0  # Minimalne opóźnienie między zawodnikami (sekundy)
MAX_DELAY = 3.0  # Maksymalne opóźnienie między zawodnikami (sekundy)

def format_sectro_time(timestamp: float) -> str:
    """Formatuje czas w formacie SECTRO (HHMMSSMMM)"""
    hours = int(timestamp // 3600)
    minutes = int((timestamp % 3600) // 60)
    seconds = int(timestamp % 60)
    milliseconds = int((timestamp % 1) * 1000)
    return f"{hours:02d}{minutes:02d}{seconds:02d}{milliseconds:03d}"

def generate_sectro_frame(input_number: int, timestamp: float) -> str:
    """Generuje ramkę SECTRO w formacie CZLxtimestamp"""
    return f"CZL{input_number}{format_sectro_time(timestamp)}"

def send_measurement(session_id: int, nr_startowy: int, frame: str) -> bool:
    """Wysyła pomiar do API i zwraca True/False"""
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

def get_seconds_since_midnight() -> float:
    now = datetime.now()
    return now.hour * 3600 + now.minute * 60 + now.second + now.microsecond / 1_000_000

def simulate_race_async(session_id: int, nr_startowy: int, race_time: float, start_time: float):
    """Symuluje przejazd zawodnika w osobnym wątku (wysyła FINISH po czasie)"""
    # Wyślij START
    start_frame = generate_sectro_frame(1, start_time)
    if send_measurement(session_id, nr_startowy, start_frame):
        print(f"START: {nr_startowy} @ {start_time:.3f}s od północy")
    else:
        print(f"❌ Błąd wysyłania START dla {nr_startowy}")
        return
    # Poczekaj na czas przejazdu, potem wyślij FINISH
    def finish_thread():
        time.sleep(race_time)
        finish_time = start_time + race_time
        finish_frame = generate_sectro_frame(4, finish_time)
        if send_measurement(session_id, nr_startowy, finish_frame):
            print(f"FINISH: {nr_startowy} @ {finish_time:.3f}s od północy (czas: {race_time:.3f}s)")
        else:
            print(f"❌ Błąd wysyłania FINISH dla {nr_startowy}")
    threading.Thread(target=finish_thread, daemon=True).start()

def send_empty_start(session_id: int, nr_startowy: int) -> bool:
    """Wysyła pusty pomiar START (czas 0.0) aby zawodnik pojawił się w wynikach"""
    frame = generate_sectro_frame(1, 0.0)
    return send_measurement(session_id, nr_startowy, frame)

def main():
    print(f"🚀 SECTRO Live Timing Simulator (starty co 2-3s, biegi 15-20s)")
    print(f"📊 Sesja: {SESSION_ID}")
    print(f"⏱️  Czasy: {MIN_RACE_TIME}-{MAX_RACE_TIME}s")
    print(f"⏳ Odstęp między startami: {MIN_DELAY}-{MAX_DELAY}s")
    print("=" * 50)
    try:
        # Pobierz listę zawodników z kolejki
        response = requests.get(f"{API_URL}/api/start-queue")
        if response.status_code != 200:
            print("❌ Nie można pobrać kolejki startowej")
            return
        data = response.json()
        queue = data.get('queue', [])
        if not queue:
            print("ℹ️ Kolejka pusta, nic do symulacji.")
            return
        # Krok 1: Wyślij puste STARTy dla wszystkich zawodników
        print("\n🔄 Dodaję zawodników do sesji SECTRO (puste STARTy)...")
        for athlete in queue:
            nr_startowy = athlete['nr_startowy']
            send_empty_start(SESSION_ID, nr_startowy)
        print("✅ Wszyscy zawodnicy dodani do sesji!\n")
        # Krok 2: Symuluj przejazdy
        start_time = get_seconds_since_midnight()
        for i, athlete in enumerate(queue):
            nr_startowy = athlete['nr_startowy']
            race_time = random.uniform(MIN_RACE_TIME, MAX_RACE_TIME)
            planned_start = start_time + (i * random.uniform(MIN_DELAY, MAX_DELAY))
            delay = max(0, planned_start - get_seconds_since_midnight())
            if delay > 0:
                print(f"⏳ Czekam {delay:.1f}s do startu zawodnika {nr_startowy}...")
                time.sleep(delay)
            print(f"\n🎯 Zawodnik: {nr_startowy} ({athlete['imie']} {athlete['nazwisko']})")
            simulate_race_async(SESSION_ID, nr_startowy, race_time, get_seconds_since_midnight())
        print("\n✅ Wszystkie starty wysłane! Czekam na zakończenie biegów...")
        time.sleep(MAX_RACE_TIME + 5)
        print("\n✅ Symulacja zakończona!")
    except KeyboardInterrupt:
        print("\n\n👋 Zatrzymuję symulator...")
        sys.exit(0)

if __name__ == "__main__":
    main() 