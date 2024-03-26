from typing import AsyncIterator

from server.shared.models import Entity
from sqlalchemy import ForeignKey, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column


class Project(Entity):
    """
    Application interface layout/prototype
    project created on the platform by the user.
    """

    __tablename__ = "projects"

    title: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    content: Mapped[str]

    @staticmethod
    async def by_author(
        author_id: int,
        session: AsyncSession,
    ) -> AsyncIterator:
        scalars = await session.stream_scalars(
            select(Project).where(Project.author_id == author_id)
        )

        async for scalar in scalars:
            yield scalar
