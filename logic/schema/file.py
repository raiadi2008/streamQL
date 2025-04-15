from pydantic import BaseModel, Field
from uuid import UUID

from logic.schema.project_file_link import ProjectFileLink


class FileStore(BaseModel):
    """
    File Store Schema corresponding to sqlalchemy
    """

    id: UUID
    file_path: str
    file_name: str
    projects: list[ProjectFileLink] = Field(default_factory=list)

    class Config:
        from_attributes = True


class FileUploadRequest(BaseModel):
    """
    File upload request json schema
    """

    file_name: str
    file_path: str


class MultiFileUploadRequest(BaseModel):
    """
    Multiple file upload request json schema
    """

    files: list[FileUploadRequest] = Field(default_factory=list)


class FileDeleteRequest(BaseModel):
    """
    Delete file request json schema
    """

    file_ids: list[UUID]


class FileUpdateRequest(BaseModel):
    """
    File update request json schema
    """

    file_path: str
