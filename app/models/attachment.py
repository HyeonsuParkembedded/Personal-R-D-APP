from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Attachment(TimestampMixin, Base):
    __tablename__ = "attachments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(120), nullable=False)
    storage_path: Mapped[str] = mapped_column(String(255), nullable=False)
    experiment_log_id: Mapped[int | None] = mapped_column(
        ForeignKey("experiment_logs.id", ondelete="CASCADE"),
        nullable=True,
    )
    hardware_issue_id: Mapped[int | None] = mapped_column(
        ForeignKey("hardware_issues.id", ondelete="CASCADE"),
        nullable=True,
    )

    experiment_log = relationship("ExperimentLog", back_populates="attachments")
    hardware_issue = relationship("HardwareIssue", back_populates="attachments")
