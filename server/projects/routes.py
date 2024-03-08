"""
28.02.2024
Daniil Stenyushkin.
Alexander Tyamin.

Routes for projects management.
"""

from typing import Awaitable, Any

from starlette import status
from fastapi import APIRouter, Depends
from starlette.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from server.root.db import get_db
from server.projects.models import Project
from server.projects.schemas import ProjectCreateSchema, ProjectUpdateSchema, ProjectDBSchema, ProjectItemsSchema

router = APIRouter(prefix='/projects')


@router.get('/', response_model = ProjectItemsSchema)
async def items(db: AsyncSession = Depends(get_db)) -> Awaitable[dict[str, Any]]:
    """
    Get all projects.

    Args:
        db: db async session.

    Returns:
        dict[str, Any]: dict with data as a list of projects and length of the list.
    
    """

    data: list[Project] = [_ async for _ in Project.every(db)]
    return {
        "data": data,
        "length": len(data),
    }


@router.post('/', response_model = ProjectDBSchema, status_code = status.HTTP_201_CREATED)
async def create(
        project: ProjectCreateSchema,
        db: AsyncSession = Depends(get_db),
) -> Awaitable[Project]:
    """
    Create new project.

    Args:
        project: project data as ProjectCreateSchema.
        db: db async session.

    Returns:
        Project: created project data.
    """

    return await Project.create(project, db)


@router.get('/{item_id}/', response_model = ProjectDBSchema)
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


@router.put('/{item_id}/', response_model = ProjectDBSchema)
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
    """

    project = await Project.by_id(item_id, db)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {item_id} doesn't exist.",
        )

    await project.update(data.dict(), db)
    
    return project

@router.delete('/{item_id}/')
async def delete_project(
        item_id: int, 
        db: AsyncSession = Depends(get_db)
):
    try:
       await Project.delete(item_id, db)
    except HTTPException as e:
       raise e
    
    return {'detail': 'Project deleted'}
