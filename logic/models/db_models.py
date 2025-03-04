from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from uuid import UUID
from typing import List


class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(primary_key=True)


class ProjectFileLink(Base):
    """
    Sqlalchemy ORM model to store relation between Project and File
    """

    __tablename__ = "project_file_link"

    project_id: Mapped[UUID] = mapped_column(
        ForeignKey("project_store.id"), primary_key=True
    )
    file_id: Mapped[UUID] = mapped_column(ForeignKey("file_store.id"), primary_key=True)


class FileStore(Base):
    """
    Sqlalchemy ORM model for user files
    """

    __tablename__ = "file_store"

    file_path: Mapped[str] = mapped_column(nullable=False, unique=True)
    file_name: Mapped[str] = mapped_column(nullable=False)

    projects: Mapped[List["ProjectFileLink"]] = relationship(
        back_populates="file", cascade="all, delete-orphan"
    )


class ProjectStore(Base):
    """
    Sqlalchemy ORM model for project
    """

    __tablename__ = "project_store"

    project_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    project_description: Mapped[str] = mapped_column(nullable=True)
    project_db_name: Mapped[UUID] = mapped_column(nullable=False, unique=True)

    files: Mapped[List["ProjectFileLink"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )


# Backrefs on the association model
ProjectFileLink.project: Mapped[ProjectStore] = relationship(back_populates="files")
ProjectFileLink.file: Mapped[FileStore] = relationship(back_populates="projects")
