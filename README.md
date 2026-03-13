# APIClient

Универсальный клиент для работы с API с поддержкой:
- Таймаутов
- Автоматических повторов (retry)
- Сессий
- JSON-ответов
- Асинхронной версии

## Установка
```bash
pip install requests aiohttp
```

## Пример использование
```python
from apiclient import AsyncAPIClient

client = AsyncAPIClient(
    base_url="https://api.example.com",
    default_params={"api_key": "your_key"}
)

async def get_data():
    data = await client.get("/endpoint")
    print(data)
```
