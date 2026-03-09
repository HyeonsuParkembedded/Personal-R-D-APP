from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.models.enums import HardwareIssueCategory, HardwareIssueSeverity, HardwareIssueStatus


class HardwareIssue(TimestampMixin, Base):
    __tablename__ = "hardware_issues"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    category: Mapped[HardwareIssueCategory] = mapped_column(
        Enum(HardwareIssueCategory, native_enum=False),
        nullable=False,
    )
    severity: Mapped[HardwareIssueSeverity] = mapped_column(
        Enum(HardwareIssueSeverity, native_enum=False),
        nullable=False,
    )
    symptoms: Mapped[str] = mapped_column(Text, nullable=False)
    reproduction_conditions: Mapped[str] = mapped_column(Text, nullable=False)
    suspected_cause: Mapped[str] = mapped_column(Text, nullable=False)
    attempted_fixes: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[HardwareIssueStatus] = mapped_column(
        Enum(HardwareIssueStatus, native_enum=False),
        nullable=False,
        default=HardwareIssueStatus.OPEN,
    )
    related_git_issue: Mapped[str | None] = mapped_column(String(255), nullable=True)

    project = relationship("Project", back_populates="hardware_issues")
    attachments = relationship(
        "Attachment",
        back_populates="hardware_issue",
        cascade="all, delete-orphan",
    )
