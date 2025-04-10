from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID

from logic.schema.file import FileStore as FileStoreSchema


class ProjectStore(BaseModel):
    """
    Project Store Schema corresponding to sql alchemy
    """

    id: UUID
    project_name: str
    project_description: Optional[str] = Field(default=None)
    project_db_name: UUID
    files: list = Field(default_factory=list)

    class Config:
        orm_mode = True


class CreateProjectRequest(BaseModel):
    project_name: str
    description: Optional[str] = None


class UpdateProjectRequest(BaseModel):
    files: Optional[list[FileStoreSchema]] = Field(default_factory=list)
    description: Optional[str] = None


class FileOpsRequest(BaseModel):
    files: list[FileStoreSchema]
