import os
from pathlib import Path

from fastapi import APIRouter, FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from server.auth.routes import router as auth_router
from server.projects.routes import router as projects_router
from server.root.db import engine, init_db
from server.shared.models import Base
from server.users.routes import router as users_router

debug = os.getenv("DEBUG") == "True"
app = FastAPI(debug=debug)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MEDIA_DIR = BASE_DIR / "media"
os.makedirs(MEDIA_DIR, exist_ok=True)

if debug:
    app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ALLOWED_ORIGINS").split(","),
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
    await init_db()
