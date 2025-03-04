from pydantic import BaseModel
from uuid import UUID


class ProjectFileLink(BaseModel):
    """
    Project File Link: ProjectStore and File Store mapping Schema
    """

    id: UUID
    project_id: UUID
    file_id: UUID
