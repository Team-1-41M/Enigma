"""
28.02.2024
Daniil Stenyushkin.

Models for projects on platform.
"""

from sqlalchemy.orm import Mapped

from server.shared.models import Entity


class Project(Entity):
    """
    Application interface layout/prototype 
    project created on the platform by the user.
    """

    __tablename__ = "projects"

    title: Mapped[str]
