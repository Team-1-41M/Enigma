"""
28.02.2024
Daniil Stenyushkin.
Alexander Tyamin.

Routes for projects management.
"""

from typing import Awaitable

from starlette import status
from fastapi import APIRouter, Depends
from starlette.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


from server.root.db import get_db
from server.auth.models import User
from server.projects.models import Project
from server.root.auth import get_current_user
from server.projects.schemas import ProjectCreateSchema, ProjectUpdateSchema, ProjectDBSchema

router = APIRouter(prefix='/projects')


@router.post('', response_model = ProjectDBSchema, status_code = status.HTTP_201_CREATED)
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
        HTTPException: 400 if some attribute from data doesn't exist in the constructed object.
    """

    data = data.dict()
    data['author_id'] = current_user.id
    data['content'] = '{"elements": []}'

    try:
        project = await Project.create(data, db)
    except AttributeError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    return project


@router.get('/{item_id}', response_model = ProjectDBSchema)
async def item(
        item_id: int,
        db: AsyncSession=Depends(get_db)
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


@router.put('/{item_id}', response_model = ProjectDBSchema)
async def update(
        item_id: int,
        data: ProjectUpdateSchema,
        db: AsyncSession=Depends(get_db)
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
        HTTPException: 400 if some attribute from data doesn't exist in the updated object.
    """

    project = await Project.by_id(item_id, db)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {item_id} doesn't exist.",
        )

    try:
        await project.update(data.dict(), db)
    except AttributeError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    return project

@router.delete('/{item_id}', status_code=status.HTTP_204_NO_CONTENT)
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
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
