"""
23.02.2024
Alexander Tyamin.

Contains the base SQLAlchemy classes for all models.
"""

import datetime
from typing import Optional, AsyncIterator

from sqlalchemy import func, select
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column


class Base(DeclarativeBase, AsyncAttrs):
    """
    Base class to work with SQLAlchemy functionality.
    Primarily used for Entity class.
    """

    pass


class Entity(Base):
    """
    Used as base class for all models
    with useful base fields
    like id, created_at, updated_at etc.
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=None, onupdate=func.now(), nullable=True)

    @classmethod
    async def every(cls, session: AsyncSession) -> AsyncIterator:
        """
        Get all objects.
        
        :params:
            session: db async session

        :return: AsyncIterator
        """

        scalars = await session.stream_scalars(select(cls))
        async for scalar in scalars:
            yield scalar

    @classmethod
    async def by_id(
            cls,
            item_id: int,
            session: AsyncSession,
    ) -> Optional:
        """
        Get an object by id.
        return: optional object or None
        """

        return await session.scalar(select(cls).where(cls.id == item_id))

    @classmethod
    async def create(
            cls,
            data,
            session: AsyncSession,
    ) -> "Entity":
        """
        Creates a new object.

        :params:
            data: new object data
            session: db async session

        :return: new object
        """

        item = cls()
        for attribute, value in data.dict().items():
            if hasattr(item, attribute):
                setattr(item, attribute, value)
            else:
                raise AttributeError(f"The attribute ${attribute} does not exist in the ${cls}")

        session.add(item)
        await session.commit()
        await session.flush()

        return item

    async def update(
            self,
            data: dict,
            session: AsyncSession,
    ) -> None:
        """
        Update object with new data.

        :params:
            data: new data to update the object
            session: db async session

        :raises:
            AttributeError: if the attribute to update does not exist in the source object

        :return: None
        """

        for attribute, value in data.items():
            if hasattr(self, attribute):
                setattr(self, attribute, value)
            else:
                raise AttributeError("The attribute to update does not exist in the source object")

        await session.commit()
        await session.refresh(self)

    def dict(self) -> dict:
        """
        Model attributes excluding SQLAlchemy attributes.

        :return: dict without SQLAlchemy attributes.
        """

        return {k: v for (k, v) in self.__dict__.items() if '_sa_' != k[:4]}
