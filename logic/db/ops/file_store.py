from logic.models.db_models import FileStore
from sqlalchemy.orm import Session
from uuid import uuid4


class FileStoreDB:
    @staticmethod
    def add_file(session: Session, file_path: str, file_name: str):
        file = FileStore(id=uuid4(), file_path=file_path, file_name=file_name)
        session.add(file)
        session.commit()
        return file

    @staticmethod
    def delete_file(session: Session, file_id):
        file = session.query(FileStore).filter_by(id=file_id).first()
        if file:
            session.delete(file)
            session.commit()
            return True
        return False

    @staticmethod
    def update_file(session: Session, file_id, **kwargs):
        file = session.query(FileStore).filter_by(id=file_id).first()
        if not file:
            return None
        for key, value in kwargs.items():
            setattr(file, key, value)
        session.commit()
        return file

    @staticmethod
    def get_file(session: Session, file_id):
        return session.query(FileStore).filter_by(id=file_id).first()
