from pydantic import BaseModel, Field
from uuid import UUID


class FileStore(BaseModel):
    """
    File Store Schema corresponding to sqlalchemy
    """

    id: UUID
    file_path: str
    file_name: str
    projects: list = Field(default_factory=list)

    class Config:
        from_attributes = True


class FilePathUploadRequest(BaseModel):
    file_path: str
    file_name: str


class FileUploadRequest(BaseModel):
    """
    File upload request json schema
    """

    file_paths: list[FilePathUploadRequest]
    project_id: UUID


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
    file_id: UUID
