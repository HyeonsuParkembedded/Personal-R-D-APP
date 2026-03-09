from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class ExperimentLog(TimestampMixin, Base):
    __tablename__ = "experiment_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    objective: Mapped[str] = mapped_column(Text, nullable=False)
    board_firmware_version: Mapped[str] = mapped_column(String(120), nullable=False)
    conditions: Mapped[str] = mapped_column(Text, nullable=False)
    result: Mapped[str] = mapped_column(Text, nullable=False)
    issues: Mapped[str] = mapped_column(Text, nullable=False)
    next_action: Mapped[str] = mapped_column(Text, nullable=False)
    related_git_reference: Mapped[str | None] = mapped_column(String(255), nullable=True)

    project = relationship("Project", back_populates="experiment_logs")
    attachments = relationship(
        "Attachment",
        back_populates="experiment_log",
        cascade="all, delete-orphan",
    )
