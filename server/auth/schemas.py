"""
23.02.2024
Alexander Tyamin.

API schemas for working with user accounts, including registration and login.
"""

import re
import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from server.shared.schemas import EntityDBSchema


class UserSignInSchema(BaseModel):
    """
    Data for user authentication.

    Name must be between 3 and 32 characters
    long and contain only letters (a-zA-Z), numbers and underscores.

    Password must meet the following requirements:
        contain at least one capital letter (A-Z),
        contain at least one lowercase letter (a-z),
        contain at least one digit (0-9),
        contain at least one special character from the #?!@$%^&*- ,
        be 12 characters to 64 characters long.
    """

    name: str = Field(
        min_length=3,
        max_length=32,
        pattern=r"^[a-zA-Z0-9_]{3,32}$",
    )
    password: str = Field(
        min_length=12,
        max_length=64,
    )

    @classmethod
    @field_validator("password")
    def check_password(cls, password: str) -> str:
        """
        Password validation.

        Raises:
            ValueError: if password doesn't meet the requirements.
        """

        pattern: re.Pattern[str] = re.compile(
            "^\
                (?=.*?[A-Z])\
                (?=.*?[a-z])\
                (?=.*?[0-9])\
                (?=.*?[#?!@$%^&*-])\
                .{12,64}\
            $"
        )
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
