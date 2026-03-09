from pydantic import BaseModel, Field

from app.models.enums import HardwareIssueCategory, HardwareIssueSeverity, HardwareIssueStatus
from app.schemas.attachments import AttachmentRead
from app.schemas.common import TimestampedReadModel


class HardwareIssueCreate(BaseModel):
    project_id: int
    title: str = Field(min_length=1, max_length=200)
    category: HardwareIssueCategory
    severity: HardwareIssueSeverity
    symptoms: str
    reproduction_conditions: str
    suspected_cause: str
    attempted_fixes: str
    status: HardwareIssueStatus = HardwareIssueStatus.OPEN
    related_git_issue: str | None = None


class HardwareIssueUpdate(BaseModel):
    project_id: int | None = None
    title: str | None = Field(default=None, min_length=1, max_length=200)
    category: HardwareIssueCategory | None = None
    severity: HardwareIssueSeverity | None = None
    symptoms: str | None = None
    reproduction_conditions: str | None = None
    suspected_cause: str | None = None
    attempted_fixes: str | None = None
    status: HardwareIssueStatus | None = None
    related_git_issue: str | None = None


class HardwareIssueRead(TimestampedReadModel):
    project_id: int
    title: str
    category: HardwareIssueCategory
    severity: HardwareIssueSeverity
    symptoms: str
    reproduction_conditions: str
    suspected_cause: str
    attempted_fixes: str
    status: HardwareIssueStatus
    related_git_issue: str | None
    attachments: list[AttachmentRead] = []
