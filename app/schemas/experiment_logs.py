from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.attachments import AttachmentRead
from app.schemas.common import TimestampedReadModel


class ExperimentLogCreate(BaseModel):
    project_id: int
    title: str = Field(min_length=1, max_length=200)
    recorded_at: datetime
    objective: str
    board_firmware_version: str = Field(min_length=1, max_length=120)
    conditions: str
    result: str
    issues: str
    next_action: str
    related_git_reference: str | None = None


class ExperimentLogUpdate(BaseModel):
    project_id: int | None = None
    title: str | None = Field(default=None, min_length=1, max_length=200)
    recorded_at: datetime | None = None
    objective: str | None = None
    board_firmware_version: str | None = Field(default=None, min_length=1, max_length=120)
    conditions: str | None = None
    result: str | None = None
    issues: str | None = None
    next_action: str | None = None
    related_git_reference: str | None = None


class ExperimentLogRead(TimestampedReadModel):
    project_id: int
    title: str
    recorded_at: datetime
    objective: str
    board_firmware_version: str
    conditions: str
    result: str
    issues: str
    next_action: str
    related_git_reference: str | None
    attachments: list[AttachmentRead] = []
