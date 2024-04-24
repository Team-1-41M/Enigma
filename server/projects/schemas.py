from datetime import datetime
from typing import Literal, Optional

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
    component_id: Optional[int]
    component_name: Optional[str]
    text: str
    parent_id: Optional[int]

class ProjectCommentSchema(BaseModel):
    id: int
    project_id: int
    component_id: Optional[int]
    component_name: Optional[str]
    user_id: int
    text: str
    parent_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class AccessSchema(BaseModel):
    credential: Literal["read", "edit"]


class TokenSchema(BaseModel):
    token: str
