from datetime import datetime

from pydantic import BaseModel, Field

from app.models.enums import ProjectStatus, RepositoryPlatform
from app.schemas.common import ORMModel, TimestampedReadModel
from app.schemas.experiment_logs import ExperimentLogRead
from app.schemas.hardware_issues import HardwareIssueRead


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str = ""
    status: ProjectStatus = ProjectStatus.IDEA


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    description: str | None = None
    status: ProjectStatus | None = None


class ProjectStatusUpdate(BaseModel):
    status: ProjectStatus


class ProjectListItem(TimestampedReadModel):
    name: str
    description: str
    status: ProjectStatus


class ProjectRepositorySummary(ORMModel):
    id: int
    name: str
    owner: str
    platform: RepositoryPlatform
    url: str
    last_synced_at: datetime | None


class RepositoryCreate(BaseModel):
    platform: RepositoryPlatform
    name: str = Field(min_length=1, max_length=120)
    owner: str = Field(min_length=1, max_length=120)
    external_id: str | None = Field(default=None, max_length=120)
    url: str = Field(min_length=1, max_length=255)
    last_synced_at: datetime | None = None


class RepositoryRead(ProjectRepositorySummary):
    created_at: datetime
    updated_at: datetime
    project_id: int


class ProjectDetail(ProjectListItem):
    repositories: list[ProjectRepositorySummary] = []


class TimelineEvent(BaseModel):
    event_type: str
    occurred_at: datetime
    title: str
    description: str
    project_id: int
    source_id: int


class ProjectActivitySummary(BaseModel):
    project: ProjectDetail
    repositories: list[ProjectRepositorySummary]
    latest_experiment_logs: list[ExperimentLogRead]
    open_hardware_issues: list[HardwareIssueRead]
    repository_count: int
    experiment_log_count: int
    hardware_issue_count: int
