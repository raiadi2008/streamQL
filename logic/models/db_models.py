from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from uuid import UUID, uuid4
from typing import List


class Base(DeclarativeBase):
    pass


class IDMixin:
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)


class ProjectStore(Base, IDMixin):
    __tablename__ = "project_store"

    project_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    project_description: Mapped[str] = mapped_column(nullable=True)
    project_db_name: Mapped[UUID] = mapped_column(nullable=False, unique=True)

    files: Mapped[List["ProjectFileLink"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )


class FileStore(Base, IDMixin):
    __tablename__ = "file_store"

    file_path: Mapped[str] = mapped_column(nullable=False, unique=True)
    file_name: Mapped[str] = mapped_column(nullable=False)

    projects: Mapped[List["ProjectFileLink"]] = relationship(
        back_populates="file", cascade="all, delete-orphan"
    )


class ProjectFileLink(Base):
    __tablename__ = "project_file_link"

    project_id: Mapped[UUID] = mapped_column(
        ForeignKey("project_store.id"), primary_key=True
    )
    file_id: Mapped[UUID] = mapped_column(ForeignKey("file_store.id"), primary_key=True)

    project: Mapped["ProjectStore"] = relationship(
        "ProjectStore", back_populates="files"
    )
    file: Mapped["FileStore"] = relationship("FileStore", back_populates="projects")
