from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.models import HardwareIssue, Project
from app.schemas import HardwareIssueCreate, HardwareIssueRead, HardwareIssueUpdate

router = APIRouter(prefix="/hardware-issues", tags=["hardware-issues"])


@router.get("", response_model=list[HardwareIssueRead])
def list_hardware_issues(
    project_id: int | None = Query(default=None),
    severity: str | None = Query(default=None),
    db: Session = Depends(get_db_session),
) -> list[HardwareIssue]:
    statement = select(HardwareIssue).order_by(HardwareIssue.updated_at.desc())
    if project_id is not None:
        statement = statement.where(HardwareIssue.project_id == project_id)
    if severity is not None:
        statement = statement.where(HardwareIssue.severity == severity)
    return list(db.scalars(statement))


@router.post("", response_model=HardwareIssueRead, status_code=status.HTTP_201_CREATED)
def create_hardware_issue(
    payload: HardwareIssueCreate,
    db: Session = Depends(get_db_session),
) -> HardwareIssue:
    project = db.get(Project, payload.project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    hardware_issue = HardwareIssue(**payload.model_dump())
    db.add(hardware_issue)
    db.commit()
    db.refresh(hardware_issue)
    return hardware_issue


@router.get("/{issue_id}", response_model=HardwareIssueRead)
def get_hardware_issue(issue_id: int, db: Session = Depends(get_db_session)) -> HardwareIssue:
    hardware_issue = db.get(HardwareIssue, issue_id)
    if hardware_issue is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hardware issue not found")
    return hardware_issue


@router.patch("/{issue_id}", response_model=HardwareIssueRead)
def update_hardware_issue(
    issue_id: int,
    payload: HardwareIssueUpdate,
    db: Session = Depends(get_db_session),
) -> HardwareIssue:
    hardware_issue = db.get(HardwareIssue, issue_id)
    if hardware_issue is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hardware issue not found")

    if payload.project_id is not None and db.get(Project, payload.project_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(hardware_issue, key, value)

    db.commit()
    db.refresh(hardware_issue)
    return hardware_issue


@router.delete("/{issue_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hardware_issue(issue_id: int, db: Session = Depends(get_db_session)) -> None:
    hardware_issue = db.get(HardwareIssue, issue_id)
    if hardware_issue is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hardware issue not found")

    db.delete(hardware_issue)
    db.commit()
