import asyncio

import pytest
import pytest_asyncio

from core.db.session import async_session_maker


@pytest_asyncio.fixture(scope="session")
async def db_session():
    async with async_session_maker() as session:
        yield session
