import os

from server.auth.models import User
from server.auth.schemas import UserSignUpSchema
from server.root.crypt import crypt_context
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


def build_url(data: dict) -> str:
    """
    Builds url for database connection.

    Args:
        data: database connection data.

    Returns:
        str: url for database connection.
    """

    engine = data.get("engine")
    name = data.get("name")
    user = data.get("user")
    password = data.get("password")
    host = data.get("host")
    port = data.get("port")

    AUTH: str = f"{user}:{password}" if user and password else user if user else ""
    LOCATION: str = f"{host}:{port}" if host and port else host if host else ""
    CREDENTIALS: str = f"{AUTH}@{LOCATION}" if AUTH and LOCATION else LOCATION if LOCATION else ""

    return f"{engine}://{CREDENTIALS}/{name}"


DB_URL = build_url(
    {
        "engine": os.getenv("DB_ENGINE"),
        "name": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
    }
)

engine: AsyncEngine = create_async_engine(DB_URL)
session_maker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db() -> AsyncSession:
    """
    Provides a database session.

    Returns:
        AsyncSession: database session
    """

    async with session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db() -> None:
    async with session_maker() as session:
        try:
            if await User.by_email(os.getenv("SUPERUSER_EMAIL"), session):
                return

            await User.create(
                UserSignUpSchema(
                    name=os.getenv("SUPERUSER_NAME"),
                    email=os.getenv("SUPERUSER_EMAIL"),
                    password=crypt_context.hash(
                        os.getenv("SUPERUSER_PASSWORD")
                    ),
                ).model_dump(),
                session,
            )
        finally:
            await session.close()
