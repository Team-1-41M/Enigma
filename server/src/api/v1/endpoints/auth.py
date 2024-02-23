import uuid
import datetime
from typing import Optional

from starlette import status
from fastapi import APIRouter, Depends
from passlib.context import CryptContext
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from server.src.core.utils.db import get_db
from server.src.core.models.users import User
from server.src.core.utils.crypt import crypt_context
from server.src.core.utils.auth import authenticate_user
from server.src.core.utils.cache import get_cache_storage
from server.src.api.v1.schemas.users import UserSignInSchema, UserSignUpSchema
from server.src.core.settings import AUTH_ROUTER_PREFIX, SIGN_UP_URL, SIGN_IN_URL, SIGN_OUT_URL, ME_URL, SESSION_TTL

router = APIRouter(prefix=AUTH_ROUTER_PREFIX)


@router.post(SIGN_UP_URL)
async def sign_up(
        data: UserSignUpSchema,
        db: AsyncSession = Depends(get_db),
        cache_storage=Depends(get_cache_storage),
        context: CryptContext = Depends(crypt_context),
):
    """
    User account creation.
    Login immediately.
    """

    same_email_user = await User.by_email(data.email, db)
    same_name_user = await User.by_name(data.account_name, db)

    if same_email_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with the same email address already exists"
        )

    if same_name_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with the same name already exists"
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
            account_name=data.account_name,
            password=data.password
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
    """User authentication into the system with setting the session valueю."""

    user: Optional[User] = await authenticate_user(data.name, data.password, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect name or password"
        )

    session_id = str(uuid.uuid4())
    await cache_storage.set(session_id, user.id)

    # TODO: later for Redis storage
    # await session_storage.expire(session_id, SESSION_TTL)

    response = JSONResponse({"detail": "Logged in successfully"})
    response.set_cookie("session", session_id, max_age=SESSION_TTL)

    updated_login_time = {
        "login_at": datetime.datetime.now()
    }
    await user.update(updated_login_time, db)

    return response


@router.post(SIGN_OUT_URL)
async def sign_out():
    pass


@router.get(ME_URL)
async def me():
    pass
