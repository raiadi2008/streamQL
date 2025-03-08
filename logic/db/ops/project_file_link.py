from logic.models.db_models import ProjectFileLink
from sqlalchemy.orm import Session


class ProjectFileLinkDB:
    @staticmethod
    def link_file_to_project(session: Session, project_id, file_id):
        link = ProjectFileLink(project_id=project_id, file_id=file_id)
        session.add(link)
        session.commit()
        return link

    @staticmethod
    def unlink_file_from_project(session: Session, project_id, file_id):
        link = (
            session.query(ProjectFileLink)
            .filter_by(project_id=project_id, file_id=file_id)
            .first()
        )
        if link:
            session.delete(link)
            session.commit()
            return True
        return False
