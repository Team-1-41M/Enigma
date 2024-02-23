"""
23.02.2024
Alexander Tyamin.

Helper functions for working for users identification.
"""
from typing import Optional

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from server.src.core.models.users import User
from server.src.core.utils.crypt import crypt_context


async def verify_password(
        plain_password: str,
        hashed_password: str,
        context: CryptContext = crypt_context,
) -> bool:
    """
    Verify hashed password.

    params:
        plain_password: raw user password
        hashed_password: hashed password stored in the database
        context: helper with hashing algorithms

    :return bool: True if passwords match, False otherwise.
    """

    return context.verify(plain_password, hashed_password)


async def authenticate_user(
        name: str,
        password: str,
        db: AsyncSession,
        context: CryptContext = crypt_context,
) -> Optional[User]:
    """Trying to find a user with same name and password."""

    user = await User.by_email(name, db)
    if user and await verify_password(password, user.password, context):
        return user
    return None
