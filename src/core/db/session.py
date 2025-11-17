from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from core.config import settings

engine = create_async_engine(
    url=settings.db.url,
    echo=True,
    future=True,
)

async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Получить сессию для работы с БД"""
    async with async_session_maker() as session:
        yield session
