"""
23.02.2024
Alexander Tyamin.

Routes for user authentication.
"""

import uuid
import datetime
from typing import Optional

from starlette import status
from fastapi import APIRouter, Depends, Cookie
from passlib.context import CryptContext
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from server.src.core.utils.db import get_db
from server.src.core.models.users import User
from server.src.core.utils.crypt import get_crypt_context
from server.src.core.utils.cache import get_cache_storage
from server.src.core.utils.auth import authenticate_user, get_current_user
from server.src.api.v1.schemas.users import UserSignInSchema, UserSignUpSchema, UserDBSchema
from server.src.core.settings import AUTH_ROUTER_PREFIX, SIGN_UP_URL, SIGN_IN_URL, SIGN_OUT_URL, ME_URL, SESSION_TTL

router = APIRouter(prefix=AUTH_ROUTER_PREFIX)


@router.post(SIGN_UP_URL)
async def sign_up(
        data: UserSignUpSchema,
        db: AsyncSession = Depends(get_db),
        cache_storage=Depends(get_cache_storage),
        context: CryptContext = Depends(get_crypt_context),
):
    """
    User account creation.
    Login immediately.
    """

    same_name_user = await User.by_name(data.name, db)
    if same_name_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with the same name already exists"
        )

    same_email_user = await User.by_email(data.email, db)
    if same_email_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with the same email address already exists"
        )

    user = User(
        name=data.name,
        email=data.email,
        password=context.hash(data.password),
        is_active=True,
    )

    _ = await User.create(user, db)

    return await sign_in(
        UserSignInSchema(
            name=data.name,
            password=data.password,
        ),
        db,
        cache_storage
    )


@router.post(SIGN_IN_URL)
async def sign_in(
        data: UserSignInSchema,
        db: AsyncSession = Depends(get_db),
        cache_storage=Depends(get_cache_storage),
) -> JSONResponse:
    """User authentication into the system with setting the session value."""

    user: Optional[User] = await authenticate_user(data.name, data.password, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect name or password"
        )

    session_id = str(uuid.uuid4())
    await cache_storage.set(session_id, user.id)

    await cache_storage.expire(session_id, SESSION_TTL)

    response = JSONResponse({"detail": "Logged in successfully"})
    response.set_cookie("session", session_id, max_age=SESSION_TTL)

    updated_login_time = {
        "login_at": datetime.datetime.now(datetime.UTC),
    }
    await user.update(updated_login_time, db)

    return response


@router.post(SIGN_OUT_URL)
async def sign_out(
        session: str = Cookie(),
        cache_storage=Depends(get_cache_storage),
) -> JSONResponse:
    """
    Deletes a user session.

    raises: HTTPException if session not found in cookie

    return: JSONResponse with message that session was successfully removed
    """

    if await cache_storage.get(session):
        await cache_storage.delete(session)

        response = JSONResponse({"detail": f"Session {session} was removed"})
        response.delete_cookie('session')

        return response
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session {session} not found"
        )


@router.get(ME_URL, response_model=UserDBSchema)
async def me(current_user: User = Depends(get_current_user)) -> Optional[User]:
    """Current user data based on session value from cookie."""

    return current_user
