"""
Async API Client — асинхронный HTTP-клиент с повторными попытками.

Пример:
    >>> from async_api_client import AsyncAPIClient
    >>> client = AsyncAPIClient("https://api.github.com")
    >>> data = await client.get("/users/octocat")
"""

from .client import AsyncAPIClient

__version__ = "0.1.0"
__all__ = ["AsyncAPIClient"]