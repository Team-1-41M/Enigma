"""
23.02.2024
Alexander Tyamin.

Contains the base SQLAlchemy class for all models.
"""

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(DeclarativeBase, AsyncAttrs):
    """
    Base class for all models.
    Primarily used for Entity class.
    """

    pass
