from pydantic import BaseModel
from uuid import UUID


class ProjectFileLink(BaseModel):
    """
    Project File Link: ProjectStore and File Store mapping Schema
    """

    project_id: UUID
    file_id: UUID

    class Config:
        from_attributes = True
