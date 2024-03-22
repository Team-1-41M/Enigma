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

ENGINE = os.getenv("DB_ENGINE")
NAME = os.getenv("DB_NAME")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")

AUTH: str = f"{USER}:{PASSWORD}" if USER and PASSWORD else ""
LOCATION: str = f"{HOST}:{PORT}" if HOST and PORT else ""
CREDENTIALS: str = f"{AUTH}@{LOCATION}" if AUTH and LOCATION else ""
    
DB_URL = f"{ENGINE}://{CREDENTIALS}/{NAME}"

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
