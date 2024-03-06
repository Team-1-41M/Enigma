from pydantic import BaseModel

from server.shared.schemas import EntityDBSchema


class ProjectBase(BaseModel):
    title: str

      
class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    pass


class ProjectDB(EntityDBSchema, ProjectCreate):
    pass
