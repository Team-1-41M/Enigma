import os

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from server.auth.models import User
from server.auth.schemas import UserSignUpSchema
from server.root.crypt import crypt_context

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
                    password=crypt_context.hash(os.getenv("SUPERUSER_PASSWORD")),
                ).model_dump(),
                session,
            )
        finally:
            await session.close()
