from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from server.root.db import get_db
from server.projects.models import Project
from server.projects.schemas import ProjectCreate, ProjectDB

router = APIRouter(prefix='/projects')


@router.get('/')
async def items(db: AsyncSession = Depends(get_db)) -> dict:
    return {
        "data": [_.dict() async for _ in Project.every(db)]
    }


@router.get('/')
async def items(db: AsyncSession = Depends(get_db)) -> dict:
    return {
        "data": [_.dict() async for _ in Project.every(db)]
    }


@router.get('/{item_id}/')
async def item(
        item_id: int,
        db: AsyncSession=Depends(get_db)
):
    return await Project.by_id(item_id, db)


@router.post('/', response_model = ProjectDB)
async def create_project(
        project: ProjectCreate,
        db: AsyncSession = Depends(get_db)):
    return await Project.create(project,db)
