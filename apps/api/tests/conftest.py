import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from main import app

# Force session scope event loop to avoid asyncpg "different loop" error
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test", follow_redirects=True) as client:
        yield client
