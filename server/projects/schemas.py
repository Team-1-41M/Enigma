from pydantic import BaseModel
from ..shared.schemas import EntityDBSchema

# Схема валидации типов для проекта
class ProjectBase(BaseModel):
    title: str

# Схема валидации типов для создания проекта
class ProjectCreate(ProjectBase):
    pass

#Схема валидации данных с сервера
class ProjectDB(EntityDBSchema, ProjectCreate):
    pass 