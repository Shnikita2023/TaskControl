from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.config import settings


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)


DATABASE_URL: str = settings.db.database_url_asyncpg

engine: AsyncEngine = create_async_engine(DATABASE_URL)
async_session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(engine,
                                                                           class_=AsyncSession,
                                                                           expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
