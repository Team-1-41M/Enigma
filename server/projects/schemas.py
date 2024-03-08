"""
28.02.2024
Daniil Stenyushkin.

API schemas for projects.
"""

from pydantic import BaseModel

from server.shared.schemas import EntityDBSchema


class ProjectBaseSchema(BaseModel):
    title: str

      
class ProjectCreateSchema(ProjectBaseSchema):
    pass


class ProjectUpdateSchema(ProjectBaseSchema):
    pass


class ProjectDBSchema(EntityDBSchema, ProjectCreateSchema):
    pass
