from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase

from uuid import UUID


class Base(DeclarativeBase):
    """
    Base class to create models from
    """

    id: Mapped[UUID] = mapped_column(primary_key=True)


class FileStore(Base):
    """
    Table Schema: Maps all the files copied in streamql workspace
    """

    __tablename__ = "file_store"

    file_path: Mapped[str] = mapped_column(nullable=False, unique=True)
    file_name: Mapped[str] = mapped_column(nullable=False)


class ProjectStore(Base):
    """
    Table Schema: Sotres all the projects of user
    """

    __tablename__ = "project_store"

    project_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    project_description: Mapped[str] = mapped_column(nullable=True)
    project_db_name: Mapped[UUID] = mapped_column(nullable=False, unique=True)
