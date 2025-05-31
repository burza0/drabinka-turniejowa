from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from threading import Lock

class SimpleCache:
    def __init__(self, default_ttl: int = 300):  # domyślnie 5 minut
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = Lock()
        self._default_ttl = default_ttl

    def get(self, key: str) -> Optional[Any]:
        """Pobiera wartość z cache jeśli istnieje i nie wygasła"""
        with self._lock:
            if key not in self._cache:
                return None
            
            cache_data = self._cache[key]
            if datetime.now() > cache_data['expires']:
                del self._cache[key]
                return None
                
            return cache_data['value']

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Zapisuje wartość w cache z określonym czasem życia"""
        ttl = ttl if ttl is not None else self._default_ttl
        with self._lock:
            self._cache[key] = {
                'value': value,
                'expires': datetime.now() + timedelta(seconds=ttl)
            }

    def delete(self, key: str) -> None:
        """Usuwa wartość z cache"""
        with self._lock:
            if key in self._cache:
                del self._cache[key]

    def clear(self) -> None:
        """Czyści cały cache"""
        with self._lock:
            self._cache.clear()

# Globalny obiekt cache
app_cache = SimpleCache() 