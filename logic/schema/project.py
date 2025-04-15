from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


from logic.schema.project_file_link import ProjectFileLink
from logic.schema.file import FileStore as FileStoreSchema


class ProjectStore(BaseModel):
    """
    Project Store Schema corresponding to sql alchemy
    """

    id: UUID
    project_name: str
    project_description: Optional[str] = Field(default=None)
    project_db_name: UUID
    files: Optional[list[ProjectFileLink]] = Field(default_factory=list)

    class Config:
        from_attributes = True


class CreateProjectRequest(BaseModel):
    project_name: str
    description: Optional[str] = None


class UpdateProjectRequest(BaseModel):
    description: Optional[str] = None


class FileOpsRequest(BaseModel):
    files: list[FileStoreSchema]


class ProjectSqlQuery(BaseModel):
    sql_query: str
