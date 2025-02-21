from fastapi import APIRouter

router = APIRouter(tags=["Files"])


@router.post("/upload")
async def upload_file(file_path: str, project_id: str):
    """
    Adds a file to the project
    Args:
        file_path: Path of the source file to be uploaded
        project_id: Id of the project in which the file should be uploaded
    """
    pass


@router.delete("/{file_id}")
async def delete_file(file_path: str):
    """
    Deletes a file if its not being used in any project
    Args:
        file_id: Id of the file to be deleted
    """
    pass
