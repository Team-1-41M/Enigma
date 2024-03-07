"""
20.02.2024
Alexander Tyamin.

This file contains the FastAPI application instance.
"""

from fastapi import FastAPI, WebSocket, APIRouter
from starlette.middleware.cors import CORSMiddleware

from server.root.db import engine
from server.shared.models import Base
from server.root.settings import CONFIG
from server.auth.routes import router as auth_router
from server.users.routes import router as users_router
from server.projects.routes import router as projects_router

app = FastAPI(debug=CONFIG["DEBUG"])

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

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(auth_router)
api_v1_router.include_router(users_router)
api_v1_router.include_router(projects_router)

app.include_router(api_v1_router)


@app.on_event("startup")
async def startup_event() -> None:
    """Creating models at application startup."""

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


project = '''{ "elements":[ { "id":1, "attributes":{ "name":"Element 1", "x":0, "y":0, "width":100, "height":100 } }, { "id":1, "attributes":{ "name":"Element 1", "x":0, "y":0, "width":100, "height":100 } } ] }'''

clients = set()


@app.websocket("/project")
async def process(socket: WebSocket) -> None:
    """
    Collects project status changes from the client
    and notifies other clients about this.

    :param socket: a WebSocket object from FastAPI.
    :return: None.
    """
    global project

    await socket.accept()
    clients.add(socket)

    await socket.send_text(project)

    while True:
        project = await socket.receive_text()

        for client in clients:
            if client != socket:
                await client.send_text(project)
