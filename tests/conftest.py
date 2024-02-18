import asyncio
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from app.config import settings
from app.db.database import Base, async_session_maker, get_async_session
from app.main import app

# DATABASE
DATABASE_URL_TEST: str = settings.db.database_test_url_asyncpg

engine_test: AsyncEngine = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker_test: async_sessionmaker[AsyncSession] = async_sessionmaker(
    engine_test, class_=AsyncSession, expire_on_commit=False
)
Base.metadata.bind = engine_test


async def get_async_session_test() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker_test() as session:
        yield session


app.dependency_overrides[async_session_maker] = async_session_maker_test
app.dependency_overrides[get_async_session] = get_async_session_test


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    """Фикстура на создание и удаление таблицы"""
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(autouse=True, scope="session")
def event_loop(request):
    """Фикстура для создания экземпляра цикла событий"""
    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client: TestClient = TestClient(app)  # Создание синхронного клиента


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Фикстура для создания асинхронного клиента"""
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        yield async_client
