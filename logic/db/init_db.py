from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from logic.models.db_models import Base, ProjectFileLink, FileStore, ProjectStore
from logic.workspace_management.workspace import workspace
from logic.constants import WorkspaceFolders, STREAMQL_STORE


class SQLiteDB:
    def __init__(self):
        self.db_path = workspace.get_path(WorkspaceFolders.STORES) / STREAMQL_STORE
        self.engine = create_engine(f"sqlite:///{self.db_path}")
        Base.metadata.create_all(self.engine)
        self.session_maker = sessionmaker(bind=self.engine)

    @contextmanager
    def get_db(self):
        session = self.session_maker()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
