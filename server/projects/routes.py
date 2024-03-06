from starlette import status
from fastapi import APIRouter, Depends
from starlette.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from server.root.db import get_db
from server.projects.models import Project
from server.projects.schemas import ProjectCreate, ProjectUpdate, ProjectDB

router = APIRouter(prefix='/projects')


@router.get('/')
async def items(db: AsyncSession = Depends(get_db)) -> dict:
    return {
        "data": [_.dict() async for _ in Project.every(db)]
    }


@router.post('/', response_model = ProjectDB)
async def create_project(
        project: ProjectCreate,
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
        data: ProjectUpdate,
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