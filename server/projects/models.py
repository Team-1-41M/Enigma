"""
28.02.2024
Daniil Stenyushkin.

Models for projects on platform.
"""

from sqlalchemy.orm import Mapped

from server.shared.models import Entity


class Project(Entity):
    __tablename__ = "projects"

    title: Mapped[str]
