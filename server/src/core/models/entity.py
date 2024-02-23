"""
23.02.2024
Alexander Tyamin.

Entity - base class for models
with some common fields
like id, created_at, updated_at etc.
"""

import datetime
from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from server.src.core.models.base import Base


class Entity(Base):
    """
    Used as base class for all models
    with useful base fields.
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=None, onupdate=func.now(), nullable=True)

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

        # TODO: is it safety? Maybe need some validation
        item = cls(**data.dict())

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
        return await session.refresh(self)

    def dict(self) -> dict:
        """
        Model attributes excluding SQLAlchemy attributes.

        :return: dict without SQLAlchemy attributes.
        """

        return {k: v for (k, v) in self.__dict__.items() if '_sa_' != k[:4]}
