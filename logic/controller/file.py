from uuid import UUID, uuid4
import csv
import pandas as pd
from sqlalchemy.orm import Session

from logic.workspace_management.file_manager import file_manager
from logic.db.ops.file_store import FileStoreDB
from logic.db.ops.project_store import ProjectStoreDB
from logic.db.ops.project_file_link import ProjectFileLinkDB
from logic.schema.file import FileStore as FileStoreSchema, MultiFileUploadRequest
from logic.workspace_management.workspace import workspace
from logic.constants import WorkspaceFolders
from logic.controller.project import ProjectController
from logic.schema.file import FileUploadRequest
from logic.db.init_db import sqldb


class FileController:
    @staticmethod
    def validate_csv_file(source_file_path: str, sample_lines=10) -> bool:
        try:
            df = pd.read_csv(source_file_path, nrows=sample_lines)
            return not df.empty and len(df.columns) > 0
        except Exception:
            return False

    @staticmethod
    def get_files(
        session: Session, file_ids: list[UUID] = None, project_ids: list[UUID] = None
    ) -> list[FileStoreSchema]:
        result_files = set()

        if file_ids:
            # Get specific files by ID
            for file_id in file_ids:
                file_obj = FileStoreDB.get_file(session, file_id)
                if file_obj:
                    result_files.add(file_obj)

        elif project_ids:
            # Get files linked to specific projects
            for project_id in project_ids:
                links = (
                    session.query(ProjectFileLinkDB)
                    .filter_by(project_id=project_id)
                    .all()
                )
                for link in links:
                    file_obj = FileStoreDB.get_file(session, link.file_id)
                    if file_obj:
                        result_files.add(file_obj)

        else:
            # Get all files
            result_files = set(FileStoreDB.get_all_files(session))

        # Convert to Pydantic schemas
        return [FileStoreSchema.model_validate(file) for file in result_files]

    @staticmethod
    def add_files(mfur: MultiFileUploadRequest, project_id: UUID, session: Session):
        added_files = []

        for source_file in mfur.files:
            if not FileController.validate_csv_file(source_file.file_path):
                continue

            file_copy_result = file_manager.copy_file(source_file.file_path, project_id)

            if file_copy_result is None:
                continue

            file_obj = FileStoreDB.add_file(
                session=session,
                file_path=str(file_copy_result),
                file_name=source_file.file_name,
            )
            added_files.append(FileStoreSchema.model_validate(file_obj))
        ProjectController.add_files(added_files, project_id, db_session=session)
        return added_files

    @staticmethod
    def delete_files(file_ids: list[UUID]):
        session = workspace.get_db_session()
        for file_id in file_ids:
            # Check if file is linked to any project
            file_links = (
                session.query(ProjectFileLinkDB).filter_by(file_id=file_id).all()
            )
            if file_links:
                raise Warning(f"File {file_id} is linked to one or more projects.")
            FileStoreDB.delete_file(session=session, file_id=file_id)

    @staticmethod
    def update_files(source_file_path: str, file_id: UUID):
        session = workspace.get_db_session()

        # Get file and its links
        file_obj = FileStoreDB.get_file(session, file_id)
        links = session.query(ProjectFileLinkDB).filter_by(file_id=file_id).all()

        if not FileController.validate_csv_file(source_file_path):
            raise ValueError("Invalid CSV file")

        file_copy_result = file_manager.copy_file(source_file_path)
        if file_copy_result is None:
            raise IOError("Failed to copy file")

        FileStoreDB.update_file(
            session=session,
            file_id=file_id,
            file_path=str(file_copy_result),
            file_name=file_copy_result.name,
        )

        # Replace data in all linked project DBs
        for link in links:
            project = ProjectStoreDB.get_project(session, link.project_id)
            df = pd.read_csv(file_copy_result)
            ProjectController.delete_table(file_obj.file_name, project.project_db_name)
            ProjectController.create_table(
                project.project_db_name, file_obj.file_name, df
            )
