"""
20.02.2024
Alexander Tyamin.

This file contains the FastAPI application instance.
"""

from fastapi import FastAPI, WebSocket, APIRouter
from starlette.middleware.cors import CORSMiddleware

from .db import engine
# TODO: why server.* works?
from server.shared.models import Base
from server.auth.routes import router as auth_router

app = FastAPI()

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

app.include_router(api_v1_router)


@app.on_event("startup")
async def startup_event() -> None:
    """Creating models at application startup."""

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get('/api/v1/projects')
async def items():
    return {
        "data": [
            {
                "id": 1,
                "title": "Project 1",
            },
            {
                "id": 2,
                "title": "Project 2",
            }
        ]
    }


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
