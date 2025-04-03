from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID

from logic.controller.project import ProjectController
from logic.workspace_management.workspace import workspace
from logic.schema.project import (
    CreateProjectRequest,
    UpdateProjectRequest,
    FileOpsRequest,
)

router = APIRouter(tags=["Projects"])


def get_session():
    return workspace.get_db_session()


@router.get("/")
async def get_projects(session=Depends(get_session)):
    try:
        projects = ProjectController.get_projects(session)
        return {"projects": [p.__dict__ for p in projects]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/")
async def create_project(request: CreateProjectRequest):
    try:
        project = ProjectController.create(
            project_name=request.project_name, description=request.description
        )
        return {"status": "success", "project_id": project.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{project_id}")
async def delete_project(project_id: UUID):
    try:
        ProjectController.delete(project_id)
        return {"status": "success", "message": "Project deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{project_id}")
async def update_project(project_id: UUID, request: UpdateProjectRequest):
    try:
        ProjectController.update(
            files=request.files, project_id=project_id, description=request.description
        )
        return {"status": "success", "message": "Project updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{project_id}/add-files")
async def add_files_to_project(project_id: UUID, request: FileOpsRequest):
    try:
        ProjectController.add_files(request.files, project_id)
        return {"status": "success", "message": "Files added to project"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{project_id}/remove-files")
async def remove_files_from_project(project_id: UUID, request: FileOpsRequest):
    try:
        ProjectController.remove_files(request.files, project_id)
        return {"status": "success", "message": "Files removed from project"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
