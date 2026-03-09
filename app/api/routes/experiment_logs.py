from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.models import ExperimentLog, Project
from app.schemas import ExperimentLogCreate, ExperimentLogRead, ExperimentLogUpdate

router = APIRouter(prefix="/experiment-logs", tags=["experiment-logs"])


@router.get("", response_model=list[ExperimentLogRead])
def list_experiment_logs(
    project_id: int | None = Query(default=None),
    db: Session = Depends(get_db_session),
) -> list[ExperimentLog]:
    statement = select(ExperimentLog).order_by(ExperimentLog.recorded_at.desc())
    if project_id is not None:
        statement = statement.where(ExperimentLog.project_id == project_id)
    return list(db.scalars(statement))


@router.post("", response_model=ExperimentLogRead, status_code=status.HTTP_201_CREATED)
def create_experiment_log(
    payload: ExperimentLogCreate,
    db: Session = Depends(get_db_session),
) -> ExperimentLog:
    project = db.get(Project, payload.project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    experiment_log = ExperimentLog(**payload.model_dump())
    db.add(experiment_log)
    db.commit()
    db.refresh(experiment_log)
    return experiment_log


@router.get("/{log_id}", response_model=ExperimentLogRead)
def get_experiment_log(log_id: int, db: Session = Depends(get_db_session)) -> ExperimentLog:
    experiment_log = db.get(ExperimentLog, log_id)
    if experiment_log is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experiment log not found")
    return experiment_log


@router.patch("/{log_id}", response_model=ExperimentLogRead)
def update_experiment_log(
    log_id: int,
    payload: ExperimentLogUpdate,
    db: Session = Depends(get_db_session),
) -> ExperimentLog:
    experiment_log = db.get(ExperimentLog, log_id)
    if experiment_log is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experiment log not found")

    if payload.project_id is not None and db.get(Project, payload.project_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(experiment_log, key, value)

    db.commit()
    db.refresh(experiment_log)
    return experiment_log


@router.delete("/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_experiment_log(log_id: int, db: Session = Depends(get_db_session)) -> None:
    experiment_log = db.get(ExperimentLog, log_id)
    if experiment_log is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experiment log not found")

    db.delete(experiment_log)
    db.commit()
