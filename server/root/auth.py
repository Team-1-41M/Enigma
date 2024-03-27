from typing import Awaitable, Optional

from fastapi import Cookie, Depends
from passlib.context import CryptContext
from server.auth.models import User
from server.root.cache import get_cache_storage
from server.root.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException


async def verify_password(
    plain_password: str,
    hashed_password: str,
    context: CryptContext,
) -> Awaitable[bool]:
    """
    Verify hashed password.

    Args:
        plain_password: raw user password.
        hashed_password: hashed password stored in the database.
        context: helper with hashing algorithms.

    Returns:
        bool: True if passwords match, False otherwise.
    """

    return context.verify(plain_password, hashed_password)


async def authenticate_user(
    name: str,
    password: str,
    db: AsyncSession,
    context: CryptContext,
) -> Awaitable[Optional[User]]:
    """
    Trying to find a user with same name and password.

    Args:
        name: user name.
        password: raw user password.
        db: db async session.
        context: helper with hashing algorithms.

    Returns:
        Optional[User]: user object if found, None otherwise.
    """

    user = await User.by_name(name, db)
    if user and await verify_password(password, user.password, context):
        return user
    return None


async def get_current_user(
    session: str = Cookie(None),
    db: AsyncSession = Depends(get_db),
    cache_storage=Depends(get_cache_storage),
) -> Awaitable[Optional[User]]:
    """
    Get current user by session value.

    Args:
        session: session id from cookie.
        db: db async session.
        cache_storage: key-value storage interface.

    Returns:
        Optional[User]: user object if found, None otherwise.

    Raises:
        HTTPException: 401 if session is not provided or expired.
    """

    if session is None:
        raise HTTPException(
            detail="Session ID not provided",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    user_id = await cache_storage.get(session)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The session has expired. Please re-login",
        )

    return await User.by_id(int(user_id), db)
