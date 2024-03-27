import os
from pathlib import Path

from fastapi import APIRouter, FastAPI
from server.auth.routes import router as auth_router
from server.projects.routes import router as projects_router
from server.root.db import init_db
from server.users.routes import router as users_router
from starlette.staticfiles import StaticFiles

debug = os.getenv("DEBUG") == "True"
app = FastAPI(debug=debug)

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


@app.on_event("startup")
async def startup_event() -> None:
    """Run db initialization."""
    
    await init_db()
