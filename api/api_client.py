import requests
import json
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class AnimeAPIClient:
    def __init__(self, base_url: str = "https://api.jikan.moe/v4"):
        self.base_url = base_url
        self.cache: Dict[str, dict] = {}
        self.cache_ttl: Dict[str, float] = {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        })
        
    def _get_cache_key(self, endpoint: str, params: dict) -> str:
        return f"{endpoint}_{hash(frozenset(params.items()))}"
    
    def _is_cache_valid(self, cache_key: str, ttl: int = 300) -> bool:
        """Проверяет валидность кэша (по умолчанию 5 минут)"""
        if cache_key not in self.cache_ttl:
            return False
        return time.time() - self.cache_ttl[cache_key] < ttl
    
    def _cached_request(self, endpoint: str, params: dict = None, ttl: int = 300) -> dict:
        if params is None:
            params = {}
        
        cache_key = self._get_cache_key(endpoint, params)
        
        # Проверяем кэш
        if cache_key in self.cache and self._is_cache_valid(cache_key, ttl):
            return self.cache[cache_key]
        
        try:
            # Jikan API имеет лимит 1 запрос в секунду
            time.sleep(1)
            
            response = self.session.get(f"{self.base_url}/{endpoint}", params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Сохраняем в кэш
            self.cache[cache_key] = data
            self.cache_ttl[cache_key] = time.time()
            
            return data
        except requests.RequestException as e:
            print(f"API request error: {e}")
            return self._get_fallback_data(endpoint)
    
    def _get_fallback_data(self, endpoint: str) -> dict:
        """Возвращает фолбэк данные, если API недоступно"""
        fallback_data = {
            "recommendations": {
                "data": [{
                    "entry": [{
                        "mal_id": 1,
                        "title": "Доктор Стоун: Финальная битва",
                        "synopsis": "Эпический финал легендарного аниме. Сенку и его друзья вступают в последнюю битву за судьбу человечества.",
                        "images": {"jpg": {"image_url": "https://cdn.myanimelist.net/images/anime/1935/116875.jpg"}}
                    }]
                }]
            },
            "top": {
                "data": self._generate_fallback_anime_list()
            },
            "seasons": {
                "data": self._generate_fallback_anime_list()
            },
            "anime": {
                "data": self._generate_fallback_anime_list()
            }
        }
        
        if "recommendations" in endpoint:
            return fallback_data["recommendations"]
        elif "top" in endpoint:
            return fallback_data["top"]
        elif "season" in endpoint:
            return fallback_data["seasons"]
        else:
            return fallback_data["anime"]
    
    def _generate_fallback_anime_list(self) -> List[dict]:
        """Генерирует фолбэк список аниме"""
        fallback_anime = [
            {
                "mal_id": 1,
                "title": "Доктор Стоун: Финальная битва",
                "synopsis": "Эпический финал легендарного аниме.",
                "genres": [{"name": "Научное"}],
                "episodes": 65,
                "score": 9.2,
                "images": {"jpg": {"image_url": "https://cdn.myanimelist.net/images/anime/1935/116875.jpg"}}
            },
            {
                "mal_id": 2,
                "title": "Атака титанов",
                "synopsis": "Битва за выживание человечества.",
                "genres": [{"name": "Экшен"}, {"name": "Драма"}],
                "episodes": 75,
                "score": 9.0,
                "images": {"jpg": {"image_url": "https://cdn.myanimelist.net/images/anime/10/47347.jpg"}}
            },
            {
                "mal_id": 3,
                "title": "Моя геройская академия",
                "synopsis": "История о становлении героя.",
                "genres": [{"name": "Экшен"}, {"name": "Супергерои"}],
                "episodes": 113,
                "score": 8.5,
                "images": {"jpg": {"image_url": "https://cdn.myanimelist.net/images/anime/10/78745.jpg"}}
            }
        ]
        return fallback_anime
    
    def _format_anime_data(self, api_data: dict) -> dict:
        """Форматирует данные из API в наш формат"""
        return {
            "id": api_data.get("mal_id", 0),
            "title": api_data.get("title", "Неизвестно"),
            "genre": ", ".join([genre["name"] for genre in api_data.get("genres", [])]),
            "episodes": f"{api_data.get('episodes', '?')} эп.",
            "rating": api_data.get("score", 0),
            "description": api_data.get("synopsis", "Описание отсутствует.")[:200] + "...",
            "image_url": api_data.get("images", {}).get("jpg", {}).get("image_url", "")
        }
    
    def get_recommended(self) -> dict:
        """Получает рекомендованное аниме"""
        data = self._cached_request("recommendations/anime")
        
        # Проверяем структуру ответа
        if "data" in data and isinstance(data["data"], list) and len(data["data"]) > 0:
            # Jikan API возвращает список рекомендаций, каждая рекомендация имеет "entry" (список аниме)
            first_recommendation = data["data"][0]
            if "entry" in first_recommendation and isinstance(first_recommendation["entry"], list) and len(first_recommendation["entry"]) > 0:
                # Берем первое аниме из первой рекомендации
                anime_data = first_recommendation["entry"][0]
                return {
                    "title": anime_data.get("title", "Доктор Стоун: Финальная битва"),
                    "description": anime_data.get("synopsis", "Эпический финал легендарного аниме."),
                    "image_url": anime_data.get("images", {}).get("jpg", {}).get("image_url", "")
                }
        
        # Фолбэк данные
        return {
            "title": "Доктор Стоун: Финальная битва",
            "description": "Эпический финал легендарного аниме. Сенку и его друзья вступают в последнюю битву за судьбу человечества.",
            "image_url": "https://cdn.myanimelist.net/images/anime/1935/116875.jpg"
        }
    
    def get_top_anime(self, page: int = 1, limit: int = 20) -> dict:
        """Получает топ аниме"""
        params = {
            "page": page,
            "limit": limit
        }
        data = self._cached_request("top/anime", params)
        
        formatted_data = []
        if "data" in data and isinstance(data["data"], list):
            for anime in data["data"]:
                formatted_data.append(self._format_anime_data(anime))
        
        return {"data": formatted_data}
    
    def get_seasonal_anime(self, page: int = 1, limit: int = 20) -> dict:
        """Получает аниме текущего сезона"""
        current_year = datetime.now().year
        current_month = datetime.now().month
        
        # Определяем сезон
        if current_month in [1, 2, 3]:
            season = "winter"
        elif current_month in [4, 5, 6]:
            season = "spring"
        elif current_month in [7, 8, 9]:
            season = "summer"
        else:
            season = "fall"
        
        params = {
            "page": page,
            "limit": limit
        }
        data = self._cached_request(f"seasons/{current_year}/{season}", params)
        
        formatted_data = []
        if "data" in data and isinstance(data["data"], list):
            for anime in data["data"]:
                formatted_data.append(self._format_anime_data(anime))
        
        return {"data": formatted_data}
    
    def search_anime(self, query: str, page: int = 1, limit: int = 20) -> dict:
        """Поиск аниме"""
        params = {
            "q": query,
            "page": page,
            "limit": limit
        }
        data = self._cached_request("anime", params)
        
        formatted_data = []
        if "data" in data and isinstance(data["data"], list):
            for anime in data["data"]:
                formatted_data.append(self._format_anime_data(anime))
        
        return {"data": formatted_data}
    
    def get_anime_by_id(self, anime_id: int) -> dict:
        """Получает детальную информацию об аниме"""
        data = self._cached_request(f"anime/{anime_id}")
        
        if "data" in data:
            return self._format_anime_data(data["data"])
        
        return {}

# Создаем глобальный экземпляр API клиента
api_client = AnimeAPIClient()