import pytest
from httpx import AsyncClient

from tests.test_data import parties


@pytest.fixture(scope="session")
async def create_party(async_client: AsyncClient):
    await async_client.post(url="/api/v1/parties/", json=parties)
