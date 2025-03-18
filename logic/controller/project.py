from uuid import UUID, uuid4
from logic.schema.file import FileStore as FileStoreSchema
from logic.db.ops.project_store import ProjectStoreDB
from logic.db.ops.file_store import FileStoreDB
from logic.db.ops.project_file_link import ProjectFileLinkDB
from logic.models.db_models import ProjectStore
from engine.db import EngineDB
from logic.workspace_management.workspace import workspace
from logic.constants import WorkspaceFolders
import pandas as pd


class ProjectController:
    @staticmethod
    def delete_table(table_name: str, db_name: UUID):
        db_file = f"{db_name}.db"
        EngineDB.execute_query(
            sql_query=f"DROP TABLE IF EXISTS '{table_name}'",
            db_name=db_file,
            workspace_path=str(workspace.get_path(WorkspaceFolders.USER_FILES)),
            fetch=False,
        )

    @staticmethod
    def create_table(db_id: UUID, table_name: str, table_data: pd.DataFrame):
        db_file = f"{db_id}.db"
        db_path = workspace.get_path(WorkspaceFolders.USER_FILES) / db_file
        conn = EngineDB.create_db(
            db_file, str(workspace.get_path(WorkspaceFolders.USER_FILES))
        )
        table_data.to_sql(table_name, conn, index=False, if_exists="replace")
        conn.close()

    @staticmethod
    def create(project_name: str, description: str = None):
        db_uuid = uuid4()
        project = ProjectStoreDB.create_project(
            session=workspace.get_db_session(),
            project_name=project_name,
            project_db_name=db_uuid,
            project_description=description,
        )
        EngineDB.create_db(
            f"{db_uuid}.db", str(workspace.get_path(WorkspaceFolders.USER_FILES))
        )
        return project

    @staticmethod
    def add_files(files: list[FileStoreSchema], project_id: UUID):
        session = workspace.get_db_session()
        project = ProjectStoreDB.get_project(session, project_id)
        db_file = f"{project.project_db_name}.db"
        db_path = str(workspace.get_path(WorkspaceFolders.USER_FILES))

        for file in files:
            df = pd.read_csv(file.file_path)
            ProjectController.create_table(project.project_db_name, file.file_name, df)
            ProjectFileLinkDB.link_file_to_project(session, project_id, file.id)

    @staticmethod
    def remove_files(files: list[FileStoreSchema], project_id: UUID):
        session = workspace.get_db_session()
        project = ProjectStoreDB.get_project(session, project_id)

        for file in files:
            ProjectController.delete_table(file.file_name, project.project_db_name)
            ProjectFileLinkDB.unlink_file_from_project(session, project_id, file.id)

    @staticmethod
    def update(files: list[FileStoreSchema], project_id: UUID, description: str = None):
        session = workspace.get_db_session()
        project = ProjectStoreDB.get_project(session, project_id)

        if files:
            for file in files:
                ProjectController.delete_table(file.file_name, project.project_db_name)
                df = pd.read_csv(file.file_path)
                ProjectController.create_table(
                    project.project_db_name, file.file_name, df
                )

        if description:
            ProjectStoreDB.update_project(
                session, project_id, project_description=description
            )

    @staticmethod
    def delete(project_id: UUID):
        session = workspace.get_db_session()
        project = ProjectStoreDB.get_project(session, project_id)

        EngineDB.delete_db(
            f"{project.project_db_name}.db",
            str(workspace.get_path(WorkspaceFolders.USER_FILES)),
        )
        ProjectStoreDB.delete_project(session, project_id)
