"""
23.02.2024
Alexander Tyamin.

API router with other concrete routers included.
"""

from fastapi import APIRouter

from server.src.core.settings import API_VERSION_1_PREFIX
from server.src.api.v1.endpoints.auth import router as auth_router

router = APIRouter(prefix=API_VERSION_1_PREFIX)

router.include_router(auth_router)
