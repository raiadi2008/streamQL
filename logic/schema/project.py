from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class ProjectStore(BaseModel):
    """
    Project Store Schema
    """

    id: UUID
    project_name: str
    project_description: Optional[str] = Field(default=None)
    project_db_name: UUID
    files: list = Field(default_factory=list)
