from typing import Literal

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

    archived: bool


class ProjectDBSchema(EntityDBSchema, ProjectCreateSchema):
    """Project data in the database."""

    author_id: int
    content: str


class ProjectItemsSchema(BaseModel):
    """Details of requested projects with some additional information."""

    length: int
    data: list[ProjectDBSchema]


class AccessSchema(BaseModel):
    credential: Literal["read", "edit"]


class TokenSchema(BaseModel):
    token: str
