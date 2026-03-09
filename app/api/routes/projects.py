from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.models import Project
from app.models.enums import HardwareIssueStatus
from app.schemas import (
    ProjectActivitySummary,
    ProjectCreate,
    ProjectDetail,
    ProjectListItem,
    ProjectRepositorySummary,
    ProjectStatusUpdate,
    ProjectUpdate,
    TimelineEvent,
)

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=list[ProjectListItem])
def list_projects(db: Session = Depends(get_db_session)) -> list[Project]:
    statement = select(Project).order_by(Project.updated_at.desc())
    return list(db.scalars(statement))


@router.post("", response_model=ProjectDetail, status_code=status.HTTP_201_CREATED)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db_session)) -> Project:
    project = Project(**payload.model_dump())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.get("/{project_id}", response_model=ProjectDetail)
def get_project(project_id: int, db: Session = Depends(get_db_session)) -> Project:
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.patch("/{project_id}", response_model=ProjectDetail)
def update_project(
    project_id: int,
    payload: ProjectUpdate,
    db: Session = Depends(get_db_session),
) -> Project:
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)
    return project


@router.patch("/{project_id}/status", response_model=ProjectDetail)
def update_project_status(
    project_id: int,
    payload: ProjectStatusUpdate,
    db: Session = Depends(get_db_session),
) -> Project:
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    project.status = payload.status
    db.commit()
    db.refresh(project)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db_session)) -> None:
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    db.delete(project)
    db.commit()


@router.get("/{project_id}/summary", response_model=ProjectActivitySummary)
def get_project_summary(project_id: int, db: Session = Depends(get_db_session)) -> ProjectActivitySummary:
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    repositories = [
        ProjectRepositorySummary.model_validate(repository)
        for repository in project.repositories
    ]
    latest_experiment_logs = sorted(
        project.experiment_logs,
        key=lambda item: item.recorded_at,
        reverse=True,
    )[:5]
    open_hardware_issues = [
        issue for issue in project.hardware_issues if issue.status != HardwareIssueStatus.FIXED
    ][:5]

    return ProjectActivitySummary(
        project=ProjectDetail.model_validate(project),
        repositories=repositories,
        latest_experiment_logs=latest_experiment_logs,
        open_hardware_issues=open_hardware_issues,
        repository_count=len(project.repositories),
        experiment_log_count=len(project.experiment_logs),
        hardware_issue_count=len(project.hardware_issues),
    )


@router.get("/{project_id}/timeline", response_model=list[TimelineEvent])
def get_project_timeline(
    project_id: int,
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db_session),
) -> list[TimelineEvent]:
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    events: list[TimelineEvent] = []

    for log in project.experiment_logs:
        events.append(
            TimelineEvent(
                event_type="experiment_log",
                occurred_at=log.recorded_at,
                title=log.title,
                description=log.result,
                project_id=project.id,
                source_id=log.id,
            )
        )

    for issue in project.hardware_issues:
        events.append(
            TimelineEvent(
                event_type="hardware_issue",
                occurred_at=issue.updated_at,
                title=issue.title,
                description=f"{issue.status}: {issue.symptoms}",
                project_id=project.id,
                source_id=issue.id,
            )
        )

    for repository in project.repositories:
        if repository.last_synced_at is None:
            continue
        events.append(
            TimelineEvent(
                event_type=f"{repository.platform}_repository",
                occurred_at=repository.last_synced_at,
                title=repository.name,
                description="Repository linked",
                project_id=project.id,
                source_id=repository.id,
            )
        )

    events.sort(key=lambda item: item.occurred_at, reverse=True)
    return events[:limit]
