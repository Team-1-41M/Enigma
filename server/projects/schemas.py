from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field
from server.shared.schemas import EntityDBSchema


class ProjectBaseSchema(BaseModel):
    """Minimal information about the project."""

    title: str = Field(
        min_length=3,
        max_length=255,
    )

class ProjectCreateSchema(ProjectBaseSchema):
    """Information that the user must provide to create a project."""

    pass


class ProjectUpdateSchema(ProjectBaseSchema):
    """Information that the user must provide to update a project."""

    archived: bool


class ProjectDBSchema(EntityDBSchema, ProjectCreateSchema, ProjectUpdateSchema):
    """Project data in the database."""

    author_id: int
    content: str


class ProjectItemsSchema(BaseModel):
    """Details of requested projects with some additional information."""

    length: int
    data: list[ProjectDBSchema]


class ChangeDBSchema(EntityDBSchema):
    """Change data in the database."""

    project_id: int
    user_id: int
    content: str


class ChangeItemsSchema(BaseModel):
    """Details of requested changes with some additional information."""

    length: int
    data: list[ChangeDBSchema]


class JoinCreateSchema(BaseModel):
    """Information to join another user to a project."""

    user_id: int


class JoinDBSchema(JoinCreateSchema, EntityDBSchema):
    """Join data in the database"""

    project_id: int


class ProjectCommentCreateSchema(BaseModel):
    component_id: Optional[str]
    component_name: Optional[str]
    text: str
    parent_id: Optional[int]

class ProjectCommentDBSchema(ProjectCommentCreateSchema, EntityDBSchema):
    project_id: int
    user_id: int
    text: str


class AccessSchema(BaseModel):
    credential: Literal["read", "edit"]


class TokenSchema(BaseModel):
    token: str
