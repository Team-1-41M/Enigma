import datetime
from typing import Awaitable, Optional

from sqlalchemy import DateTime, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from server.shared.models import Entity


class User(Entity):
    """User information model."""

    __tablename__ = "users"

    name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    login_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=None,
        nullable=True,
    )

    @staticmethod
    async def by_email(
        email: str,
        session: AsyncSession,
    ) -> Awaitable[Optional["User"]]:
        """Finds a user by email."""

        return await session.scalar(select(User).where(User.email == email))

    @staticmethod
    async def by_name(
        name: str,
        session: AsyncSession,
    ) -> Awaitable[Optional["User"]]:
        """Finds a user by name."""

        return await session.scalar(select(User).where(User.name == name))
