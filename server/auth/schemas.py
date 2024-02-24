"""
23.02.2024
Alexander Tyamin.

API schemas for working with user accounts, including registration and login.
"""

import re
import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from ..shared.schemas import EntityDBSchema


class UserSignInSchema(BaseModel):
    """Data for user authentication."""

    name: str = Field(
        min_length=3,
        max_length=32,
        pattern=r"^[a-zA-Z0-9_]{3,32}$",
    )
    password: str = Field(
        min_length=12,
        max_length=64,
    )

    @field_validator("password")
    @classmethod
    def check_password_correct(cls, password: str) -> str:
        pattern: re.Pattern[str] = re.compile(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{12,}$")
        if not pattern.match(password):
            raise ValueError("Invalid password")
        return password


class UserSignUpSchema(UserSignInSchema):
    """Data for creating a user account."""

    email: EmailStr = Field(
        min_length=3,
        max_length=256,
    )


class UserDBSchema(EntityDBSchema, UserSignUpSchema):
    """User data in the database."""

    is_active: bool
    login_at: Optional[datetime.datetime]
