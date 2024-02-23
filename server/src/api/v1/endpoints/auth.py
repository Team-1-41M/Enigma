import datetime
import uuid
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse

from server.src.api.v1.schemas.users import UserSignInSchema
from server.src.core.models.users import User
from server.src.core.settings import AUTH_ROUTER_PREFIX, SIGN_UP_URL, SIGN_IN_URL, SIGN_OUT_URL, ME_URL, SESSION_TTL
from server.src.core.utils.auth import authenticate_user
from server.src.core.utils.cache import get_cache_storage
from server.src.core.utils.db import get_db

router = APIRouter(prefix=AUTH_ROUTER_PREFIX)


@router.post(SIGN_UP_URL)
async def sign_up():
    pass


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
