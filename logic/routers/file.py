from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from logic.controller.file import FileController
from logic.schema.file import FileUpdateRequest, FileDeleteRequest, FileUploadRequest
from logic.db.init_db import sqldb


router = APIRouter(tags=["Files"])


@router.post("/upload")
async def upload_file(fur: FileUploadRequest, db: Session = Depends(sqldb.get_db)):
    FileController.add_files(fur, db)


@router.delete("/")
async def delete_files(request: FileDeleteRequest):
    try:
        FileController.delete_files(request.file_ids)
        return {"status": "success", "message": "Files deleted"}
    except Warning as w:
        raise HTTPException(status_code=400, detail=str(w))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/update")
async def update_file(request: FileUpdateRequest):
    try:
        FileController.update_files(request.file_path, request.file_id)
        return {"status": "success", "message": "File updated in all linked projects"}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except IOError as ioe:
        raise HTTPException(status_code=500, detail=str(ioe))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
