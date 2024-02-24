"""
23.02.2024
Alexander Tyamin.

Connecting to a database and providing a DB instance.
"""

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine

from .settings import DB_URL

engine: AsyncEngine = create_async_engine(DB_URL)


async def get_db() -> AsyncSession:
    """
    Provides a database session.
    :return: AsyncSession
    """

    session_maker = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=False
    )

    async with session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
