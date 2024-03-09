"""
28.02.2024
Daniil Stenyushkin.

Models for projects on platform.
"""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from server.shared.models import Entity


class Project(Entity):
    """
    Application interface layout/prototype 
    project created on the platform by the user.
    """

    __tablename__ = "projects"

    title: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
