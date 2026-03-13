import asyncio
import aiohttp

class AsyncAPIClient:
    def __init__(self, base_url, default_params=None, timeout=10, max_retries=3, retry_delay=1):
        self.base_url = base_url.rstrip('/')
        self.default_params = default_params or {}
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    async def _request(self, method, endpoint, **kwargs):
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
                    await asyncio.sleep(self.retry_delay * (attempt + 1))

    async def get(self, endpoint, **kwargs):
        return await self._request("GET", endpoint, **kwargs)
    
    async def post(self, endpoint, **kwargs):
        return await self._request("POST", endpoint, **kwargs)
    
    async def delete(self, endpoint, **kwargs):
        return await self._request("DELETE", endpoint, **kwargs)
    
    async def put(self, endpoint, **kwargs):
        return await self._request("PUT", endpoint, **kwargs)