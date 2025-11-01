# api_client.py (исправленная версия)
import requests
import hashlib
import json
import time
from typing import Dict, List, Optional

class AnimeAPIClient:
    def __init__(self, base_url: str = "https://api.anime.com/v1"):
        self.base_url = base_url
        self.cache: Dict[str, dict] = {}
        self.cache_ttl: Dict[str, float] = {}
        self.session = requests.Session()
        
    def _get_cache_key(self, endpoint: str, params: dict) -> str:
        param_str = json.dumps(params, sort_keys=True)
        return hashlib.md5(f"{endpoint}{param_str}".encode()).hexdigest()
    
    def _is_cache_valid(self, cache_key: str, ttl: int = 3600) -> bool:
        if cache_key not in self.cache_ttl:
            return False
        return time.time() - self.cache_ttl[cache_key] < ttl
    
    def _cached_request(self, endpoint: str, params: dict, ttl: int = 3600) -> dict:
        cache_key = self._get_cache_key(endpoint, params)
        
        if cache_key in self.cache and self._is_cache_valid(cache_key, ttl):
            return self.cache[cache_key]
        
        try:
            response = self.session.get(f"{self.base_url}/{endpoint}", params=params)
            response.raise_for_status()
            data = response.json()
            
            self.cache[cache_key] = data
            self.cache_ttl[cache_key] = time.time()
            
            return data
        except requests.RequestException as e:
            return {"error": str(e), "data": []}
    
    def get_recommended(self) -> dict:
        data = self._cached_request("recommended", {})
        if "data" in data and isinstance(data["data"], list) and len(data["data"]) > 0:
            return data["data"][0]
        return {
            "title": "Доктор Стоун: Финальная битва",
            "description": "Эпический финал легендарного аниме. Сенку и его друзья вступают в последнюю битву за судьбу человечества."
        }
    
    def get_anime_list(self, category: str, page: int = 1, limit: int = 20) -> dict:
        params = {
            "category": category,
            "page": page,
            "limit": limit
        }
        return self._cached_request("anime", params)
    
    def get_trending(self, page: int = 1, limit: int = 20) -> dict:
        params = {
            "sort": "trending",
            "page": page,
            "limit": limit
        }
        return self._cached_request("anime", params)
    
    def get_new(self, page: int = 1, limit: int = 20) -> dict:
        params = {
            "sort": "new",
            "page": page,
            "limit": limit
        }
        return self._cached_request("anime", params)
    
    def get_popular(self, page: int = 1, limit: int = 20) -> dict:
        params = {
            "sort": "popular",
            "page": page,
            "limit": limit
        }
        return self._cached_request("anime", params)

api_client = AnimeAPIClient()