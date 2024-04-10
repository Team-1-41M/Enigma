import datetime
from typing import AsyncIterator, Awaitable, Optional

from server.root.models import Base
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column


class Entity(Base):
    """
    Used as base class for all models
    with useful base fields
    like id, created_at, updated_at etc.
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(),
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        server_default=None,
        onupdate=func.now(),
        nullable=True,
    )

    @classmethod
    async def every(cls, session: AsyncSession) -> AsyncIterator:
        """
        Get all objects.

        Args:
            session: db async session.

        Returns: AsyncIterator.
        """

        scalars = await session.stream_scalars(select(cls))
        async for scalar in scalars:
            yield scalar

    @classmethod
    async def by_id(
        cls,
        item_id: int,
        session: AsyncSession,
    ) -> Awaitable[Optional["Entity"]]:
        """
        Get an object by id.

        Args:
            item_id: object id.
            session: db async session.

        Returns:
            Optional[Entity]: object if found, None otherwise.
        """

        return await session.scalar(select(cls).where(cls.id == item_id))

    @classmethod
    async def create(
        cls,
        data: dict,
        session: AsyncSession,
    ) -> Awaitable["Entity"]:
        """
        Creates a new object.

        Args:
            data: new object data.
            session: db async session.

        Returns:
            Entity: new object.

        Raises:
            AttributeError: if some attribute
            does not exist in the constructed object.
        """

        cls._verify_attributes(**data)

        item = cls(**data)

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

        Args:
            data: new data to update the object.
            session: db async session.

        Returns:
            None.

        Raises:
            AttributeError: if the attribute to update
            does not exist in the source object.
        """

        self._verify_attributes(**data)

        for attribute, value in data.items():
            setattr(self, attribute, value)

        await session.commit()
        await session.refresh(self)

    @classmethod
    async def delete(
        cls,
        item_id: int,
        db: AsyncSession,
    ):
        """
        Deletes an object.

        Args:
            item_id: object id.

        Returns:
            None.

        Raises:
            RuntimeError: if the object with specified id not found.
        """

        item = await cls.by_id(item_id, db)
        if item is None:
            raise RuntimeError(f"Item with id {item_id} not found.")

        await db.delete(item)
        await db.commit()

    @classmethod
    def _verify_attributes(cls, **kwargs) -> bool:
        """
        Verify if the attributes exist in the constructed object.

        Args:
            kwargs: new object data.

        Returns:
            bool: True if the attributes
            exist in the constructed object, False otherwise.

        Raises:
            AttributeError: if the attribute
            does not exist in the constructed object.
        """

        for attribute, _ in kwargs.items():
            if not hasattr(cls, attribute):
                raise AttributeError(
                    f"Impossible create {cls}: \
                    non-existent attribute {attribute}."
                )
