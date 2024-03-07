"""
07.03.2024
Alexander Tyamin.

Routes for users management.
"""

from typing import Optional

from fastapi import APIRouter, Depends

from server.auth.models import User
from server.auth.schemas import UserDBSchema
from server.root.auth import get_current_user

router = APIRouter(prefix='/users')


@router.get('/me', response_model=UserDBSchema)
async def me(current_user: User = Depends(get_current_user)) -> Optional[User]:
    """
    Current user data based on session value from cookie.

    Args:
        current_user: current user object.
    
    Returns:
        Optional[User]: current user object or None if user is not found.
    """

    return current_user
