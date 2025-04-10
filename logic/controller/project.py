from uuid import UUID, uuid4
import pandas as pd
from sqlalchemy.orm import Session

from logic.schema.file import FileStore as FileStoreSchema
from logic.db.ops.project_store import ProjectStoreDB
from logic.db.ops.file_store import FileStoreDB
from logic.db.ops.project_file_link import ProjectFileLinkDB
from logic.models.db_models import ProjectStore
from engine.db import EngineDB
from logic.workspace_management.workspace import workspace
from logic.constants import WorkspaceFolders


class ProjectController:
    @staticmethod
    def delete_table(table_name: str, db_id: UUID):
        """
        Deletes a table inside a db with give db_id
        Args:
            table_name: name of the table to be deleted
            db_id: id of the database to be deleted
        """
        db_file = f"{db_id}.db"
        EngineDB.execute_query(
            sql_query=f"DROP TABLE IF EXISTS '{table_name}'",
            db_name=db_file,
            workspace_path=str(workspace.get_path(WorkspaceFolders.USER_FILES)),
            fetch=False,
        )

    @staticmethod
    def create_table(db_id: UUID, table_name: str, table_data: pd.DataFrame):
        """
        Creates a table inside the given db
        Args:
            db_id: Id of the database
            table_name: name of the table to be created
            table_data: Data to be inseted in the newly created table
        """
        db_file = f"{db_id}.db"
        db_path = workspace.get_path(WorkspaceFolders.USER_FILES) / db_file
        conn = EngineDB.create_db(
            db_file, str(workspace.get_path(WorkspaceFolders.USER_FILES))
        )
        table_data.to_sql(table_name, conn, index=False, if_exists="replace")
        conn.close()

    @staticmethod
    def create(
        project_name: str,
        db: Session,
        description: str = None,
    ):
        """
        Create a new project
        Args:
            project_name: name of the new project
            db: Database Session
            descripion (optional): description of the project
        """
        db_uuid = uuid4()
        project = ProjectStoreDB.create_project(
            db,
            project_name=project_name,
            project_db_name=db_uuid,
            project_description=description,
        )
        EngineDB.create_db(
            f"{db_uuid}.db", str(workspace.get_path(WorkspaceFolders.PROJECTS))
        )
        return project

    @staticmethod
    def add_files(files: list[FileStoreSchema], project_id: UUID, db_session: Session):
        """
        Add files to the project
        Args:
            files: list of files to be added to the project
            project_id: Id of the project in which files are being added
            db_session: DB session
        """
        project = ProjectStoreDB.get_project(db_session, project_id)
        db_file = f"{project.project_db_name}.db"
        db_path = str(workspace.get_path(WorkspaceFolders.USER_FILES))

        for file in files:
            df = pd.read_csv(file.file_path)
            ProjectController.create_table(project.project_db_name, file.file_name, df)
            ProjectFileLinkDB.link_file_to_project(db_session, project_id, file.id)

    @staticmethod
    def remove_files(
        files: list[FileStoreSchema], project_id: UUID, db_session: Session
    ):
        """
        Removes list of files from the project
        Args:
            files: List of files to be removed from the project
            project_id: Id of the project from which files are to be deleted
            db_session: DB Session
        """
        project = ProjectStoreDB.get_project(db_session, project_id)

        for file in files:
            ProjectController.delete_table(file.file_name, project.project_db_name)
            ProjectFileLinkDB.unlink_file_from_project(db_session, project_id, file.id)

    @staticmethod
    def update(
        files: list[FileStoreSchema],
        project_id: UUID,
        db_session: Session,
        description: str = None,
    ):
        """
        Update a project
        Args:
            files: list of files that can be added to the project while updating it
            project_id: UUID of the project in which the files will be added
            db_session: Session of the database
            description (Optional): Description of the project
        """
        project = ProjectStoreDB.get_project(db_session, project_id)

        if files:
            for file in files:
                ProjectController.delete_table(file.file_name, project.project_db_name)
                df = pd.read_csv(file.file_path)
                ProjectController.create_table(
                    project.project_db_name, file.file_name, df
                )

        if description:
            ProjectStoreDB.update_project(
                db_session, project_id, project_description=description
            )

    @staticmethod
    def delete(project_id: UUID, db_session: Session):
        """
        Delete a project
        Args:
            project_id: ID of the project to be deleted
            db_session: Session of the database
        """
        project = ProjectStoreDB.get_project(db_session, project_id)

        EngineDB.delete_db(
            f"{project.project_db_name}.db",
            str(workspace.get_path(WorkspaceFolders.USER_FILES)),
        )
        ProjectStoreDB.delete_project(db_session, project_id)

    @staticmethod
    def get_all(db: Session):
        """
        Get all the projects
        Args:
            db: DB Session

        Returns:
            List of all ProjectStore instances
        """
        return ProjectStoreDB.get_projects(db)

    @staticmethod
    def get(project_id: UUID, db: Session):
        """
        Get info of a project
        Args:
            project_id: ID of the project to be retrieved
            db: DB Session

        Returns:
            A single ProjectStore instance or None
        """
        return ProjectStoreDB.get_project(project_id, db)
