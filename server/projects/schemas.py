"""
28.02.2024
Daniil Stenyushkin.

API schemas for projects.
"""

from pydantic import BaseModel

from server.shared.schemas import EntityDBSchema


class ProjectBaseSchema(BaseModel):
    """Minimal information about the project."""

    title: str

      
class ProjectCreateSchema(ProjectBaseSchema):
    """Information that the user must provide to create a project."""

    pass


class ProjectUpdateSchema(ProjectBaseSchema):
    """Information that the user must provide to update a project."""

    pass


class ProjectDBSchema(EntityDBSchema, ProjectCreateSchema):
    """Project data in the database."""

    pass
