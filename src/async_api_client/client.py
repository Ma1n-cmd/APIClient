import asyncio
import aiohttp
from typing import Optional, Dict, Any, Union

class AsyncAPIClient:
    """
    Асинхронный HTTP-клиент с повторными попытками и таймаутами.
    
    Пример использования:
        client = AsyncAPIClient("https://api.example.com")
        data = await client.get("/users")
    """
    
    def __init__(
        self,
        base_url: str,
        default_params: Optional[Dict[str, Any]] = None,
        timeout: int = 10,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        """
        Инициализация клиента.
        
        Args:
            base_url: Базовый URL API (например, "https://api.example.com/v1")
            default_params: Параметры запроса, которые будут добавляться к каждому запросу
            timeout: Таймаут запроса в секундах
            max_retries: Максимальное количество повторных попыток
            retry_delay: Начальная задержка между попытками (удваивается с каждой)
        """
        self.base_url = base_url.rstrip('/')
        self.default_params = default_params or {}
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    async def _request(self, method: str, endpoint: str, **kwargs) -> Union[Dict, str]:
        """
        Внутренний метод для выполнения HTTP-запросов с повторными попытками.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        params = {**self.default_params, **kwargs.get('params', {})}
        kwargs['params'] = params
        kwargs['timeout'] = aiohttp.ClientTimeout(total=self.timeout)

        async with aiohttp.ClientSession() as session:
            for attempt in range(self.max_retries):
                try:
                    async with session.request(method, url, **kwargs) as response:
                        response.raise_for_status()
                        try:
                            return await response.json()
                        except:
                            return await response.text()
                            
                except Exception as e:
                    if attempt == self.max_retries - 1:
                        raise
                    # Экспоненциальная задержка: 1с, 2с, 4с...
                    await asyncio.sleep(self.retry_delay * (2 ** attempt))

    async def get(self, endpoint: str, **kwargs) -> Union[Dict, str]:
        """Выполнить GET-запрос."""
        return await self._request("GET", endpoint, **kwargs)
    
    async def post(self, endpoint: str, **kwargs) -> Union[Dict, str]:
        """Выполнить POST-запрос."""
        return await self._request("POST", endpoint, **kwargs)
    
    async def put(self, endpoint: str, **kwargs) -> Union[Dict, str]:
        """Выполнить PUT-запрос."""
        return await self._request("PUT", endpoint, **kwargs)
    
    async def delete(self, endpoint: str, **kwargs) -> Union[Dict, str]:
        """Выполнить DELETE-запрос."""
        return await self._request("DELETE", endpoint, **kwargs)
    
    async def patch(self, endpoint: str, **kwargs) -> Union[Dict, str]:
        """Выполнить PATCH-запрос."""
        return await self._request("PATCH", endpoint, **kwargs)