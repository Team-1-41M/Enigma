"""
23.02.2024
Alexander Tyamin.

API schemas for working with user accounts, including registration and login.
"""

import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from server.src.api.v1.schemas.entity import EntityDBSchema


class UserSignInSchema(BaseModel):
    """Data for user authentication."""

    name: str = Field(
        min_length=3,
        max_length=32,
        pattern=r"^[a-zA-Z0-9_]{3,32}$",
    )
    password: str


class UserSignUpSchema(UserSignInSchema):
    """Data for creating a user account."""

    email: EmailStr


class UserDBSchema(EntityDBSchema, UserSignUpSchema):
    """User data in the database."""

    is_active: bool
    login_at: Optional[datetime.datetime]
