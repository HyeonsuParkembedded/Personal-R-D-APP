from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.models import Project, Repository
from app.schemas import RepositoryCreate, RepositoryRead

router = APIRouter(prefix="/projects/{project_id}/repositories", tags=["repositories"])


@router.get("", response_model=list[RepositoryRead])
def list_project_repositories(project_id: int, db: Session = Depends(get_db_session)) -> list[Repository]:
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    statement = (
        select(Repository)
        .where(Repository.project_id == project_id)
        .order_by(Repository.updated_at.desc())
    )
    return list(db.scalars(statement))


@router.post("", response_model=RepositoryRead, status_code=status.HTTP_201_CREATED)
def create_project_repository(
    project_id: int,
    payload: RepositoryCreate,
    db: Session = Depends(get_db_session),
) -> Repository:
    project = db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    repository = Repository(project_id=project_id, **payload.model_dump())
    db.add(repository)
    db.commit()
    db.refresh(repository)
    return repository


@router.delete("/{repository_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project_repository(
    project_id: int,
    repository_id: int,
    db: Session = Depends(get_db_session),
) -> None:
    repository = db.get(Repository, repository_id)
    if repository is None or repository.project_id != project_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Repository not found")

    db.delete(repository)
    db.commit()
