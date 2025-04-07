from logic.models.db_models import ProjectStore
from sqlalchemy.orm import Session
from uuid import uuid4, UUID


class ProjectStoreDB:
    @staticmethod
    def create_project(
        session: Session,
        project_name: str,
        project_db_name,
        project_description: str = None,
    ):
        project = ProjectStore(
            id=uuid4(),
            project_name=project_name,
            project_description=project_description,
            project_db_name=project_db_name,
        )
        session.add(project)
        session.commit()
        return project

    @staticmethod
    def delete_project(session: Session, project_id):
        project = session.query(ProjectStore).filter_by(id=project_id).first()
        if project:
            session.delete(project)
            session.commit()
            return True
        return False

    @staticmethod
    def update_project(session: Session, project_id, **kwargs):
        project = session.query(ProjectStore).filter_by(id=project_id).first()
        if not project:
            return None
        for key, value in kwargs.items():
            setattr(project, key, value)
        session.commit()
        return project

    @staticmethod
    def get_project(project_id: UUID, session: Session):
        return session.query(ProjectStore).filter_by(id=project_id).first()

    @staticmethod
    def get_projects(session: Session):
        return session.query(ProjectStore).all()
