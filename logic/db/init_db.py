from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from logic.models.db_models import Base
from logic.workspace_management.workspace import workspace
from logic.constants import WorkspaceFolders, STREAMQL_STORE


class SQLiteDB:
    def __init__(self):
        self._engine = None
        self._session_maker = None

    def init(self):
        """
        Lazily initialize DB — must be called **after** workspace is ready.
        """
        db_path = workspace.get_path(WorkspaceFolders.STORES)
        if db_path is None:
            raise RuntimeError("Workspace not initialized before DB init.")
        full_path = db_path / STREAMQL_STORE
        self._engine = create_engine(f"sqlite:///{full_path}")
        Base.metadata.create_all(self._engine)
        self._session_maker = sessionmaker(bind=self._engine)

    @contextmanager
    def get_db(self):
        if not self._session_maker:
            raise RuntimeError("Database not initialized. Call init() first.")

        session = self._session_maker()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


sqldb = SQLiteDB()
