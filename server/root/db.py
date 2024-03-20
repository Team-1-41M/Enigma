"""
23.02.2024
Alexander Tyamin.

Connecting to a database and providing a DB instance.
"""

import os

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
)

if os.getenv("DEBUG") == "True":
    DB_URL = f"{os.getenv("DB_ENGINE")}:///{os.getenv('DB_NAME')}"
else:
    DB_URL = f"{os.getenv("DB_ENGINE")}://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

engine: AsyncEngine = create_async_engine(DB_URL)


async def get_db() -> AsyncSession:
    """
    Provides a database session.

    Returns:
        AsyncSession: database session
    """

    session_maker = async_sessionmaker(
        bind=engine, expire_on_commit=False, autoflush=False
    )

    async with session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
