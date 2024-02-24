"""
23.02.2024
Alexander Tyamin.

Helper functions for working for users identification.
"""

from typing import Optional

from starlette import status
from fastapi import Depends, Cookie
from passlib.context import CryptContext
from starlette.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .db import get_db
from ..auth.models import User
from .crypt import crypt_context
from .cache import get_cache_storage


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

    user = await User.by_name(name, db)
    if user and await verify_password(password, user.password, context):
        return user
    return None


async def get_current_user(
        session: str = Cookie(None),
        db: AsyncSession = Depends(get_db),
        cache_storage=Depends(get_cache_storage),
) -> Optional[User]:
    """
    Get current user by session value.

    :params:
        session: session id from cookie
        db: db async session
        cache_storage: key-value storage interface

    :raises:
        HTTPException: 401 if session is not provided or expired

    :return: optional user object or none
    """

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session ID not provided"
        )

    user_id = await cache_storage.get(session)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The session has expired. Please re-login"
        )

    return await User.by_id(int(user_id), db)
