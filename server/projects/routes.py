"""
28.02.2024
Daniil Stenyushkin.
Alexander Tyamin.

Routes for projects management.
"""

import json

from typing import Awaitable

from starlette import status
from starlette.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, WebSocket

from server.root.db import get_db
from server.auth.models import User
from server.projects.models import Project
from server.root.auth import get_current_user
from server.projects.schemas import (
    ProjectDBSchema,
    ProjectCreateSchema,
    ProjectUpdateSchema,
)

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


# TODO: Where to put it?
clients = set()


@router.websocket("/{item_id}/content")
async def process(
    item_id: int,
    socket: WebSocket,
    db: AsyncSession = Depends(get_db),
) -> None:
    """
    Collects project content changes from the client
    and notifies other clients about this.

    Args:
        socket: client socket.

    Returns:
        None.
    """

    project = await Project.by_id(item_id, db)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {item_id} doesn't exist.",
        )

    await socket.accept()
    clients.add(socket)

    await socket.send_text(project.content)

    content_list = json.loads(project.content)

    while True:
        message = await socket.receive_text()

        try:
            command, data = message.split(" ", 1)

            element_data = json.loads(data)

            if command == "create":
                id = element_data["id"]
                if any(e["id"] == id for e in content_list):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Element with this id already exists.",
                    )
                content_list.append(element_data)

            elif command == "update":
                for i, element in enumerate(content_list):
                    if element["id"] == element_data["id"]:
                        content_list[i] = element_data
                        break
                else:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Element with this id not found.",
                    )

            elif command == "delete":
                for i, element in enumerate(content_list):
                    if element["id"] == element_data["id"]:
                        del content_list[i]
                        break
                else:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Element with this id not found.",
                    )

            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid command.",
                )

            await project.update({"content": json.dumps(content_list)}, db)

            for client in clients:
                await client.send_text(message)
        except AttributeError as e:
            raise HTTPException(
                detail=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
