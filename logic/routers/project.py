from fastapi import APIRouter

router = APIRouter(tags=["projects"])


@router.get("/")
async def get_projects():
    """
    Get all the projects created
    """
    pass


@router.post("/")
async def create_project():
    """
    create a project with unique id
    """
    pass


@router.delete("/{project_id}")
async def delete_project(project_id):
    """
    deletes a project with given project id
    Args:
        project_id: The id of the project to be deleted
    """
    pass


@router.put("/{project_id}")
async def update_project(project_id):
    """
    Update a project by either deleting a file, adding a file or replacing (updating) a file
    """
    pass
