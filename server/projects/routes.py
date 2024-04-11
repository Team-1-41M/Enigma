import datetime
import json
import os
from typing import Awaitable

from fastapi import APIRouter, Depends, WebSocket
from jose import jwt
from server.auth.models import User
from server.projects import content
from server.projects.models import Project
from server.projects.schemas import (
    ProjectCreateSchema,
    ProjectDBSchema,
    ProjectUpdateSchema,
    CredentialsSchema,
    TokenSchema,
)
from server.root.auth import get_current_user
from server.root.cache import get_clients_storage
from server.root.db import get_db
from server.root.settings import ALGORITHM, TOKEN_EXPIRE
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException
from starlette.websockets import WebSocketDisconnect

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post(
    "",
    response_model=ProjectDBSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create(
    data: ProjectCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Awaitable[Project]:
    """
    Create new project.

    Args:
        project: project data as ProjectCreateSchema.
        db: db async session.

    Returns:
        Project: created project data.

    Raises:
        HTTPException: 400 if some attribute from data
        doesn't exist in the constructed object.
    """

    data = data.model_dump()
    data["author_id"] = current_user.id
    data["content"] = "[]"

    try:
        project = await Project.create(data, db)
    except AttributeError as e:
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return project


@router.get("/{item_id}", response_model=ProjectDBSchema)
async def item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
) -> Awaitable[Project]:
    """
    Get project by id.

    Args:
        item_id: project id as integer.
        db: db async session.

    Returns:
        Project: project data.

    Raises:
        HTTPException: 404 if project with specified id not found.
    """

    project = await Project.by_id(item_id, db)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {item_id} doesn't exist.",
        )

    return project


@router.put("/{item_id}", response_model=ProjectDBSchema)
async def update(
    item_id: int,
    data: ProjectUpdateSchema,
    db: AsyncSession = Depends(get_db),
) -> Awaitable[Project]:
    """
    Update project.

    Args:
        item_id: project id as integer.
        data: project data as ProjectUpdateSchema.
        db: db async session.

    Returns:
        Project: updated project data.

    Raises:
        HTTPException: 404 if project with specified id not found.

        HTTPException: 400 if some attribute from data
        doesn't exist in the updated object.
    """

    project = await Project.by_id(item_id, db)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {item_id} doesn't exist.",
        )

    try:
        await project.update(data.model_dump(), db)
    except AttributeError as e:
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return project


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    item_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    """
    Delete project.

    Args:
        item_id: project id as integer.
        db: db async session.

    Raises:
        HTTPException: 404 if project with specified id not found.

    Returns:
        None
    """

    try:
        await Project.delete(item_id, db)
    except RuntimeError as e:
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_404_NOT_FOUND,
        )


def is_default(value) -> bool:
    """
    Checks if value is default.

    Args:
        value: value to check.

    Returns:
        bool: True if value is default, False otherwise.
    """

    if isinstance(value, int) or isinstance(value, float):
        return value == 0

    if isinstance(value, str):
        return value == ""

    return False


def remove_defaults(data: dict) -> dict:
    """
    Removes default values from data.

    Args:
        data: data to remove default values from.

    Returns:
        dict: data without default values.
    """

    undefaulted = {}

    for key, value in data.items():
        if value is not None and not is_default(value):
            undefaulted[key] = value

    return undefaulted


@router.post("/{item_id}/link", response_model=TokenSchema)
async def link(
    item_id: int,
    credentials: CredentialsSchema,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Awaitable[str]:
    project = await Project.by_id(item_id, db)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {item_id} doesn't exist.",
        )

    payload = {
        "id": str(item_id),
        "sub": str(current_user.id),
        "exp": datetime.datetime.now(datetime.UTC)
        + datetime.timedelta(minutes=TOKEN_EXPIRE),
        "credentials": credentials.value,
    }

    return {
        "token": jwt.encode(payload, os.getenv("SECRET"), algorithm=ALGORITHM)
    }


@router.websocket("/{identifier}/content")
async def manage(
    identifier: str,
    socket: WebSocket,
    db: AsyncSession = Depends(get_db),
    clients_storage=Depends(get_clients_storage),
) -> None:
    """
    Collects project content changes from the client
    and notifies other clients about this.

    Args:
        socket: client socket.

    Returns:
        None.
    """

    if identifier.isnumeric():
        item_id = int(identifier)
        credentials = "edit"
    else:
        payload = jwt.decode(identifier, os.getenv("SECRET"), algorithms=[ALGORITHM])

        item_id = int(payload["id"])
        credentials = payload["credentials"]

    project = await Project.by_id(item_id, db)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {item_id} doesn't exist.",
        )

    await socket.accept()

    clients = await clients_storage.get(project.id)
    if clients is None:
        clients = {socket}
    else:
        clients.add(socket)
    await clients_storage.set(project.id, clients)

    # TODO: make send json
    try:
        await socket.send_text(project.content)
    except WebSocketDisconnect:
        clients.remove(socket)
        await clients_storage.set(project.id, clients)

    content_list = json.loads(project.content)

    while True:
        try:
            message = await socket.receive_text()

            if credentials == "edit":
                command, data = message.split(" ", 1)

                element_data = json.loads(data)

                match command:
                    case "create":
                        content_list = content.create(content_list, element_data)
                    case "update":
                        content_list = content.update(content_list, element_data)
                    case "delete":
                        content_list = content.delete(content_list, element_data["id"])
                    case "put":
                        content_list = content.put(content_list, element_data)
                    case _:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid command.",
                        )

                await project.update({"content": json.dumps(content_list)}, db)

                for client in clients:
                    await client.send_text(message)
        except WebSocketDisconnect:
            clients.remove(socket)
            await clients_storage.set(project.id, clients)
            break
