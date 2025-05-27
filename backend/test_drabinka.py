#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

def test_drabinka_endpoint():
    """Test nowego endpointu drabinki"""
    
    print("🏆 Testowanie nowej logiki drabinki turniejowej...")
    
    try:
        # Wywołaj endpoint
        response = requests.get("http://localhost:5000/api/drabinka")
        
        if response.status_code != 200:
            print(f"❌ Błąd HTTP: {response.status_code}")
            return
        
        data = response.json()
        
        # Wyświetl podsumowanie
        if "podsumowanie" in data:
            podsumowanie = data["podsumowanie"]
            print(f"\n📊 PODSUMOWANIE:")
            print(f"  Kategorie: {', '.join(podsumowanie['wszystkie_kategorie'])}")
            print(f"  Łącznie zawodników: {podsumowanie['łączna_liczba_zawodników']}")
            print(f"  Mężczyźni: {podsumowanie['podział_płeć']['mężczyźni']}")
            print(f"  Kobiety: {podsumowanie['podział_płeć']['kobiety']}")
        
        # Wyświetl szczegóły dla każdej kategorii
        for kategoria in data:
            if kategoria == "podsumowanie":
                continue
                
            print(f"\n🏅 KATEGORIA: {kategoria}")
            
            for plec in data[kategoria]:
                drabinka = data[kategoria][plec]
                print(f"\n  👥 {plec}:")
                
                # Statystyki
                if "statystyki" in drabinka:
                    stats = drabinka["statystyki"]
                    print(f"    📈 Łącznie zawodników: {stats['łącznie_zawodników']}")
                    print(f"    📈 Grup ćwierćfinały: {stats['grup_ćwierćfinały']}")
                    print(f"    📈 Grup półfinały: {stats['grup_półfinały']}")
                    print(f"    📈 Grup finał: {stats['grup_finał']}")
                
                # Ćwierćfinały
                if "ćwierćfinały" in drabinka and drabinka["ćwierćfinały"]:
                    print(f"    🥉 ĆWIERĆFINAŁY:")
                    for grupa in drabinka["ćwierćfinały"]:
                        print(f"      Grupa {grupa['grupa']} (awansują: {grupa['awansują']}):")
                        for zawodnik in grupa["zawodnicy"]:
                            czas = zawodnik.get('czas_przejazdu_s', 'brak')
                            print(f"        {zawodnik['nr_startowy']}. {zawodnik['imie']} {zawodnik['nazwisko']} - {czas}s")
                
                # Półfinały
                if "półfinały" in drabinka and drabinka["półfinały"]:
                    print(f"    🥈 PÓŁFINAŁY:")
                    for grupa in drabinka["półfinały"]:
                        if grupa["zawodnicy"]:
                            print(f"      Grupa {grupa['grupa']} (awansują: {grupa['awansują']}):")
                            for zawodnik in grupa["zawodnicy"]:
                                print(f"        {zawodnik['nr_startowy']}. {zawodnik['imie']} {zawodnik['nazwisko']}")
                        else:
                            print(f"      Grupa {grupa['grupa']}: {grupa.get('info', 'Oczekuje na wyniki')}")
                
                # Finał
                if "finał" in drabinka and drabinka["finał"]:
                    print(f"    🥇 FINAŁ:")
                    for grupa in drabinka["finał"]:
                        if grupa["zawodnicy"]:
                            print(f"      Grupa {grupa['grupa']} (awansują: {grupa['awansują']}):")
                            for zawodnik in grupa["zawodnicy"]:
                                print(f"        {zawodnik['nr_startowy']}. {zawodnik['imie']} {zawodnik['nazwisko']}")
                        else:
                            print(f"      Grupa {grupa['grupa']}: {grupa.get('info', 'Oczekuje na wyniki')}")
                
                # Info o małej liczbie zawodników
                if "info" in drabinka:
                    print(f"    ℹ️  {drabinka['info']}")
        
        print(f"\n✅ Test zakończony pomyślnie!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Nie można połączyć się z backendem. Czy serwer działa na porcie 5000?")
    except Exception as e:
        print(f"❌ Błąd: {e}")

if __name__ == "__main__":
    test_drabinka_endpoint() 