"""
07.03.2024
Alexander Tyamin.

Routes for users management.
"""

from typing import Optional, Awaitable, Any

from starlette import status
from fastapi import APIRouter, Depends
from starlette.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from server.root.db import get_db
from server.auth.models import User
from server.projects.models import Project
from server.auth.schemas import UserDBSchema
from server.root.auth import get_current_user
from server.projects.schemas import ProjectItemsSchema

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserDBSchema)
async def me(current_user: User = Depends(get_current_user)) -> Optional[User]:
    """
    Current user data based on session value from cookie.

    Args:
        current_user: current user object.

    Returns:
        Optional[User]: current user object or None if user is not found.
    """

    return current_user


@router.get("/me/projects", response_model=ProjectItemsSchema)
async def created_projects(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Awaitable[dict[str, Any]]:
    """
    Get all projects created by current user.

    Args:
        current_user: current user object.
        db: db async session.

    Returns:
        dict[str, Any]: dict with data as a list of projects and length of the list.

    """

    data: list[Project] = [_ async for _ in Project.by_author(current_user.id, db)]
    return {
        "data": data,
        "length": len(data),
    }


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    item_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    """
    Delete user.

    Args:
        item_id: user id as integer.
        db: db async session.

    Raises:
        HTTPException: 404 if user with specified id not found.

    Returns:
        None
    """

    try:
        await Project.delete(item_id, db)
    except RuntimeError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
