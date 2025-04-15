from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlalchemy.orm import Session

from logic.controller.project import ProjectController
from logic.db.init_db import sqldb
from logic.schema.project import (
    CreateProjectRequest,
    ProjectSqlQuery,
    UpdateProjectRequest,
    FileOpsRequest,
)

router = APIRouter(tags=["Projects"])


@router.get("/")
async def get_projects(session=Depends(sqldb.get_db)):
    try:
        projects = ProjectController.get_all(session)
        return {"projects": [p.__dict__ for p in projects]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/")
async def create_project(
    request: CreateProjectRequest, db_session: Session = Depends(sqldb.get_db)
):
    return ProjectController.create(
        project_name=request.project_name,
        description=request.description,
        db=db_session,
    )


@router.get("/{project_id}")
async def get_project(project_id: UUID, db_session: Session = Depends(sqldb.get_db)):
    return ProjectController.get(project_id, db_session)


@router.delete("/{project_id}")
async def delete_project(project_id: UUID, db_session: Session = Depends(sqldb.get_db)):
    try:
        ProjectController.delete(project_id, db_session)
        return {"status": "success", "message": "Project deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{project_id}")
async def update_project(
    project_id: UUID, request: UpdateProjectRequest, db: Session = Depends(sqldb.get_db)
):
    return ProjectController.update(
        project_id=project_id,
        db_session=db,
        description=request.description,
    )


# @router.post("/{project_id}/add-files")
# async def add_files_to_project(
#     project_id: UUID,
#     request: FileOpsRequest,
#     db_session: Session = Depends(sqldb.get_db),
# ):
#     try:
#         ProjectController.add_files(request.files, project_id, db_session)
#         return {"status": "success", "message": "Files added to project"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


@router.post("/{project_id}/remove-files")
async def remove_files_from_project(
    project_id: UUID, request: FileOpsRequest, db: Session = Depends(sqldb.get_db)
):
    try:
        ProjectController.remove_files(request.files, project_id, db)
        return {"status": "success", "message": "Files removed from project"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{project_id}/execute-sql-query")
async def execute_sql_query(
    project_id: UUID, query: ProjectSqlQuery, db: Session = Depends(sqldb.get_db)
):
    return ProjectController.execute_sql_query(project_id, query.sql_query, db)
