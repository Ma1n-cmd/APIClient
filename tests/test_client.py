import pytest
from async_api_client import AsyncAPIClient


pytestmark = pytest.mark.asyncio

async def test_get_request():
    client = AsyncAPIClient("https://jsonplaceholder.typicode.com")
    
    data = await client.get("/posts/1")
    
    assert data["id"] == 1
    assert "title" in data
    assert "body" in data

async def test_post_request():
    client = AsyncAPIClient("https://jsonplaceholder.typicode.com")
    
    new_post = {
        "title": "foo",
        "body": "bar",
        "userId": 1
    }
    
    data = await client.post("/posts", json=new_post)
    
    assert data["title"] == "foo"
    assert "id" in data

async def test_default_params():
    client = AsyncAPIClient(
        "https://jsonplaceholder.typicode.com",
        default_params={"api_key": "test123"}
    )
    
    data = await client.get("/posts/1")
    assert data["id"] == 1

async def test_retry_on_failure():
    client = AsyncAPIClient(
        "https://не-существует.пример",
        max_retries=2,
        retry_delay=0.1
    )
    
    with pytest.raises(Exception):
        await client.get("/test")

async def test_invalid_endpoint():
    """Тест обработки несуществующего эндпоинта."""
    client = AsyncAPIClient("https://jsonplaceholder.typicode.com")
    
    with pytest.raises(Exception) as excinfo:
        await client.get("/not-exist-endpoint-12345")

    assert "404" in str(excinfo.value) or "Not Found" in str(excinfo.value)