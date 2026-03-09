from sqlalchemy import Enum, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.models.enums import ProjectStatus


class Project(TimestampMixin, Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus, native_enum=False),
        nullable=False,
        default=ProjectStatus.IDEA,
    )

    repositories = relationship(
        "Repository",
        back_populates="project",
        cascade="all, delete-orphan",
    )
    experiment_logs = relationship(
        "ExperimentLog",
        back_populates="project",
        cascade="all, delete-orphan",
    )
    hardware_issues = relationship(
        "HardwareIssue",
        back_populates="project",
        cascade="all, delete-orphan",
    )
