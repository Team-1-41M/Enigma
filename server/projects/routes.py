from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..root.db import get_db
from .schemas import ProjectCreate, ProjectDB
from .models import Project

router = APIRouter(prefix='/projects')

@router.post('/',response_model = ProjectDB)
async def create_project(
        project: ProjectCreate,
        db: AsyncSession = Depends(get_db)):
    return await Project.create(project,db)