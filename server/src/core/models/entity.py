"""
23.02.2024
Alexander Tyamin.

Entity - base class for models
with some common fields
like id, created_at, updated_at etc.
"""

import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from server.src.core.models.base import Base


class Entity(Base):
    """Used as base class for all models
    with useful base fields.
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=None, onupdate=func.now(), nullable=True)
