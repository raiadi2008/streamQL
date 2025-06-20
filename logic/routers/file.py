from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from logic.controller.file import FileController
from logic.schema.file import (
    FileUpdateRequest,
    FileDeleteRequest,
    MultiFileUploadRequest,
)
from logic.db.init_db import sqldb


router = APIRouter(tags=["Files"])


@router.post("/upload/{project_id}")
async def upload_file(
    project_id: UUID, mfur: MultiFileUploadRequest, db: Session = Depends(sqldb.get_db)
):
    return FileController.add_files(mfur, project_id, db)


@router.get("/")
async def get_files(
    file_ids: list[UUID] = [],
    project_ids: list[UUID] = [],
    db: Session = Depends(sqldb.get_db),
):
    return FileController.get_files(
        file_ids=file_ids, project_ids=project_ids, session=db
    )


@router.delete("/")
async def delete_files(request: FileDeleteRequest):
    try:
        FileController.delete_files(request.file_ids)
        return {"status": "success", "message": "Files deleted"}
    except Warning as w:
        raise HTTPException(status_code=400, detail=str(w))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/update/{file_id}")
async def update_file(
    file_id: UUID, request: FileUpdateRequest, db: Session = Depends(sqldb.get_db)
):
    return FileController.update_files(request.file_path, file_id, db)
