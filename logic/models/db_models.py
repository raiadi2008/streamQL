from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from uuid import UUID
from typing import List
from datetime import datetime


class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(primary_key=True)


class ProjectFileLink(Base):
    __tablename__ = "project_file_link"

    project_id: Mapped[UUID] = mapped_column(
        ForeignKey("project_store.id"), primary_key=True
    )
    file_id: Mapped[UUID] = mapped_column(ForeignKey("file_store.id"), primary_key=True)

    # Future fields — optional for now
    added_on: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    role: Mapped[str] = mapped_column(nullable=True)  # e.g., "main", "auxiliary"


class FileStore(Base):
    __tablename__ = "file_store"

    file_path: Mapped[str] = mapped_column(nullable=False, unique=True)
    file_name: Mapped[str] = mapped_column(nullable=False)

    projects: Mapped[List["ProjectFileLink"]] = relationship(
        back_populates="file", cascade="all, delete-orphan"
    )


class ProjectStore(Base):
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
