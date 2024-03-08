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


@router.get('/', response_model=ProjectItemsSchema)
async def items(db: AsyncSession = Depends(get_db)) -> Awaitable[dict[str, Any]]:
    data = [_ async for _ in Project.every(db)]
    return {
        "data": data,
        "length": len(data),
    }


@router.post('/', response_model = ProjectDBSchema)
async def create_project(
        project: ProjectCreateSchema,
        db: AsyncSession = Depends(get_db)):
    return await Project.create(project,db)


@router.get('/{item_id}/')
async def item(
        item_id: int,
        db: AsyncSession=Depends(get_db)
):
    return await Project.by_id(item_id, db)


@router.put('/{item_id}/')
async def update(
        item_id: int,
        data: ProjectUpdateSchema,
        db: AsyncSession=Depends(get_db)
):
    project = await Project.by_id(item_id, db)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ERROR: can't find a project with id {item_id}"
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
