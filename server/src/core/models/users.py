"""23.02.2024
Alexander Tyamin.

User model.
"""

import datetime

from sqlalchemy.orm import Mapped, mapped_column

from server.src.core.models.entity import Entity


class User(Entity):
    """User information model."""

    __tablename__ = "users"

    name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    is_active: Mapped[bool]
    login_at: Mapped[datetime.datetime] = mapped_column(server_default=None, nullable=True)
