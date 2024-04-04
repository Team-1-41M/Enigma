from pydantic import BaseModel, Field
from typing import List, Any
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

    author_id: int
    content: str


class ProjectItemsSchema(BaseModel):
    """Details of requested projects with some additional information."""

    length: int
    data: list[ProjectDBSchema]


class ProjectJoinSchema(BaseModel):
    """Schema for joining a project."""
    user_id: int