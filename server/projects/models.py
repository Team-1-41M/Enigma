from datetime import datetime
from typing import AsyncIterator

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

    archived: Mapped[bool] = mapped_column(default=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    content: Mapped[str]
    title: Mapped[str]

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


class Change(Entity):
    """Project history tracking."""

    __tablename__ = "changes"

    message: Mapped[str]
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    @staticmethod
    async def by_project(
        project_id: int,
        session: AsyncSession,
    ) -> AsyncIterator:
        scalars = await session.stream_scalars(
            select(Change).where(Change.project_id == project_id)
        )

        async for scalar in scalars:
            yield scalar


class Join(Entity):
    """Access information model."""

    __tablename__ = "joins"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))


class ProjectComment(Entity):
    """
    Model for user comments on project components.
    """

    __tablename__ = "project_comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    component_id: Mapped[int | None] = mapped_column(default=None)
    component_name: Mapped[str | None] = mapped_column(default=None)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    text: Mapped[str] = mapped_column(Text)
    parent_id: Mapped[int | None] = mapped_column(default=None)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    @staticmethod
    async def by_project(
        project_id: int,
        session: AsyncSession,
    ) -> AsyncIterator:
        scalars = await session.stream_scalars(
            select(ProjectComment).where(ProjectComment.project_id == project_id)
        )

        async for scalar in scalars:
            yield scalar
