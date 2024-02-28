from sqlalchemy.orm import Mapped

from server.shared.models import Entity


class Project(Entity):
    __tablename__ = "projects"

    title: Mapped[str]
