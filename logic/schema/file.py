from pydantic import BaseModel, Field
from uuid import UUID


class FileStore(BaseModel):
    """
    File Store Schema
    """

    id: UUID
    file_path: str
    file_name: str
    projects: list = Field(default_factory=list)
