"""
20.02.2024
Alexander Tyamin.

This file contains the FastAPI application instance.
"""

from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from server.root.db import engine
from server.shared.models import Base
from server.root.settings import CONFIG
from server.auth.routes import router as auth_router
from server.users.routes import router as users_router
from server.projects.routes import router as projects_router

from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent.parent.parent
MEDIA_PATH = BASE_PATH / "media"

app = FastAPI(debug=CONFIG["DEBUG"])

if CONFIG["DEBUG"]:
    app.mount("/media", StaticFiles(directory=MEDIA_PATH), name=MEDIA_PATH)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:3000",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_v1_router = APIRouter(prefix="/api/v1", tags=["API v1"])

api_v1_router.include_router(auth_router)
api_v1_router.include_router(users_router)
api_v1_router.include_router(projects_router)

app.include_router(api_v1_router)

@app.on_event("startup")
async def startup_event() -> None:
    """Creating models at application startup."""

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
