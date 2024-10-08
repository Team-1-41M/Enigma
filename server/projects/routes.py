import datetime
import json
import os
from typing import Any, Awaitable, List

from fastapi import APIRouter, Depends, WebSocket
from jose import jwt
from server.auth.models import User
from server.projects import content
from server.projects.models import Change, Join, Project, ProjectComment
from server.projects.schemas import (
    AccessSchema,
    ChangeItemsSchema,
    JoinCreateSchema,
    JoinDBSchema,
    ProjectCommentCreateSchema,
    ProjectCommentDBSchema,
    ProjectCreateSchema,
    ProjectDBSchema,
    ProjectUpdateSchema,
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

    projects = [_ async for _ in Project.by_author(current_user.id, db)]
    if len(projects) >= 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can't create more than 3 projects for one user.",
        )

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


@router.post("/{item_id}/join", response_model=JoinDBSchema)
async def join(
        item_id: int,
        data: JoinCreateSchema,
        db: AsyncSession = Depends(get_db),
) -> Awaitable[Join]:
    """
    Join project.

    Args:
        project_id: project id.
        data: user id as ProjectJoinSchema.
        db: db async session.

    Returns:
        ProjectJoinSchema: created access data with id.

    Raises:
        HTTPException: 400 if some attribute from data
        doesn't exist in the constructed object.
    """
    project = await Project.by_id(item_id, db)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {item_id} doesn't exist.",
        )

    joined_user = await User.by_id(data.user_id, db)
    if joined_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {data.user_id} doesn't exist.",
        )

    try:
        join = await Join.create({"project_id": item_id, "user_id": data.user_id}, db)
    except AttributeError as e:
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return join

@router.post("/{project_id}/comments", response_model=ProjectCommentDBSchema)
async def create_project_comment(
    project_id: int,
    comment_data: ProjectCommentCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    project_comment = ProjectComment(
        project_id=project_id,
        component_id=comment_data.component_id,
        component_name=comment_data.component_name,
        user_id=current_user.id,
        text=comment_data.text,
        parent_id=comment_data.parent_id,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )
    db.add(project_comment)
    await db.commit()
    return project_comment

@router.get("/{project_id}/comments", response_model=List[ProjectCommentDBSchema])
async def get_project_comments(
    project_id: int,
    db: AsyncSession = Depends(get_db),
):
    comments = []
    async for comment in ProjectComment.by_project(project_id, db):
        comments.append(comment)
    return comments

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


@router.post("/{item_id}/link", response_model=TokenSchema)
async def link(
    item_id: int,
    access: AccessSchema,
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
        "credential": access.credential,
    }

    return {
        "token": jwt.encode(payload, os.getenv("SECRET"), algorithm=ALGORITHM)
    }


@router.get("/{item_id}/changes", response_model=ChangeItemsSchema)
async def changes(
    item_id: int,
    db: AsyncSession = Depends(get_db),
) -> Awaitable[dict[str, Any]]:
    data = [_ async for _ in Change.by_project(item_id, db)]
    return {
        "data": data,
        "length": len(data),
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
        credential = "edit"
    else:
        payload = jwt.decode(identifier, os.getenv("SECRET"), algorithms=[ALGORITHM])

        item_id = int(payload["id"])
        credential = payload["credential"]

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

            if credential == "edit":
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

                # # FIXME: need a real user's id here
                # await Change.create(
                #     ChangeDBSchema(
                #         project_id=project.id,
                #         user_id=1,
                #         content=message,
                #     ).model_dump(),
                #     db,
                # )

                for client in clients:
                    await client.send_text(message)
        except WebSocketDisconnect:
            clients.remove(socket)
            await clients_storage.set(project.id, clients)
            break
