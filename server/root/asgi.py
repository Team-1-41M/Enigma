import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

from fastapi import APIRouter, FastAPI
from server.auth.routes import router as auth_router
from server.projects.routes import router as projects_router
from server.root.db import init_db
from server.users.routes import router as users_router
from starlette.staticfiles import StaticFiles


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Run operations on application startup and shutdown."""
    
    await init_db()

    yield


debug = os.getenv("DEBUG") == "True"
app = FastAPI(
    debug=debug,
    title="Enigma",
    summary="An API for the best Figma clone ever.",
    description="This API primarily includes includes function for authentication and project management.",
    version="0.1.0",
    lifespan=lifespan,
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MEDIA_DIR = BASE_DIR / "media"
os.makedirs(MEDIA_DIR, exist_ok=True)

if debug:
    app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")

api_v1_router = APIRouter(prefix="/api/v1", tags=["API v1"])

api_v1_router.include_router(auth_router)
api_v1_router.include_router(users_router)
api_v1_router.include_router(projects_router)

app.include_router(api_v1_router)
