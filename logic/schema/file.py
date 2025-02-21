from pydantic import BaseModel
from uuid import UUID


class File(BaseModel):
    """
    manages the workspace in which file is being used
    """

    workspace_file_id: UUID
    workspace_file_path: str
