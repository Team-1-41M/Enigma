from datetime import datetime
from typing import AsyncIterator
<<<<<<< HEAD
=======
from datetime import datetime
>>>>>>> aae7a384c46b271010f45e92619e6520314cebbe

from server.shared.models import Entity
from sqlalchemy import DateTime, ForeignKey, Text, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


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
class Join(Entity):
    """Access information model."""

    __tablename__ = "joins"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))

class Comment(Entity):
    """
    Model for user comments on projects.
    """

    __tablename__ = "comments"

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    text: Mapped[str] = mapped_column(Text)