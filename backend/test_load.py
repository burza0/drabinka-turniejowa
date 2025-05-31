import requests
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import statistics
import os
from dotenv import load_dotenv

load_dotenv()

# Użyj adresu z zmiennych środowiskowych lub domyślnego
BASE_URL = os.getenv("API_URL", "http://localhost:5000/api")

ENDPOINTS = [
    {"path": "/zawodnicy", "method": "GET"},
    {"path": "/kategorie", "method": "GET"},
    {"path": "/statystyki", "method": "GET"},
    {"path": "/drabinka", "method": "GET"},
    {"path": "/grupy-startowe", "method": "GET"},
    # Dodatkowe endpointy z różnymi metodami
    {"path": "/qr/stats", "method": "GET"},
    {"path": "/qr/live-feed", "method": "GET"},
    {"path": "/version", "method": "GET"}
]

class LoadTestResult:
    def __init__(self):
        self.successful_requests = 0
        self.failed_requests = 0
        self.response_times = []
        self.errors = []
        self.start_time = None
        self.end_time = None

    @property
    def total_requests(self):
        return self.successful_requests + self.failed_requests

    @property
    def success_rate(self):
        return (self.successful_requests / self.total_requests * 100) if self.total_requests > 0 else 0

    @property
    def avg_response_time(self):
        return statistics.mean(self.response_times) if self.response_times else 0

    @property
    def test_duration(self):
        return self.end_time - self.start_time if self.start_time and self.end_time else 0

def test_endpoint(endpoint, result):
    """Testuje pojedynczy endpoint"""
    try:
        start_time = time.time()
        if endpoint["method"] == "GET":
            response = requests.get(f"{BASE_URL}{endpoint['path']}")
        elif endpoint["method"] == "POST":
            response = requests.post(f"{BASE_URL}{endpoint['path']}")
        end_time = time.time()
        
        response_time = end_time - start_time
        
        if response.status_code == 200:
            result.successful_requests += 1
            result.response_times.append(response_time)
        else:
            result.failed_requests += 1
            result.errors.append(f"Status {response.status_code} for {endpoint['path']}")
            
    except Exception as e:
        result.failed_requests += 1
        result.errors.append(f"Error for {endpoint['path']}: {str(e)}")

def run_load_test(concurrent_users=10, requests_per_user=5, test_duration=60):
    """Wykonuje test obciążeniowy"""
    print(f"Rozpoczynam test obciążeniowy:")
    print(f"- Liczba równoczesnych użytkowników: {concurrent_users}")
    print(f"- Liczba zapytań na użytkownika: {requests_per_user}")
    print(f"- Maksymalny czas testu: {test_duration}s")
    print(f"- Adres API: {BASE_URL}")
    print("\nTestowane endpointy:")
    for endpoint in ENDPOINTS:
        print(f"- {endpoint['method']} {endpoint['path']}")
    
    result = LoadTestResult()
    result.start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
        futures = []
        while time.time() - result.start_time < test_duration:
            for _ in range(concurrent_users):
                for _ in range(requests_per_user):
                    for endpoint in ENDPOINTS:
                        futures.append(
                            executor.submit(test_endpoint, endpoint, result)
                        )
    
    result.end_time = time.time()
    
    # Wyświetl wyniki
    print("\nWyniki testu obciążeniowego:")
    print("=" * 50)
    print(f"Czas trwania testu: {result.test_duration:.2f}s")
    print(f"Całkowita liczba zapytań: {result.total_requests}")
    print(f"Udane zapytania: {result.successful_requests}")
    print(f"Nieudane zapytania: {result.failed_requests}")
    print(f"Współczynnik sukcesu: {result.success_rate:.1f}%")
    
    if result.response_times:
        print("\nCzasy odpowiedzi:")
        print(f"- Średni: {result.avg_response_time:.3f}s")
        print(f"- Minimalny: {min(result.response_times):.3f}s")
        print(f"- Maksymalny: {max(result.response_times):.3f}s")
        print(f"- Mediana: {statistics.median(result.response_times):.3f}s")
        if len(result.response_times) > 1:
            print(f"- Odchylenie standardowe: {statistics.stdev(result.response_times):.3f}s")
    
    if result.errors:
        print("\nBłędy podczas testu:")
        for error in result.errors[:10]:  # Pokaż tylko pierwsze 10 błędów
            print(f"- {error}")
        if len(result.errors) > 10:
            print(f"... i {len(result.errors) - 10} więcej błędów")
    
    # Oblicz przepustowość
    requests_per_second = result.total_requests / result.test_duration
    print(f"\nPrzepustowość: {requests_per_second:.1f} zapytań/sekundę")

if __name__ == "__main__":
    run_load_test(concurrent_users=10, requests_per_user=5, test_duration=60) 