from sqlalchemy import String
from sqlalchemy.orm import Mapped
from ..shared.models import Entity

# Определение модели данных для проекта
class Project(Entity):
    __tablename__ = "projects"

    title: Mapped[str]
