from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.models import Attachment, ExperimentLog, HardwareIssue
from app.schemas import AttachmentRead
from app.services.storage import save_upload

router = APIRouter(tags=["attachments"])


@router.post(
    "/experiment-logs/{log_id}/attachments",
    response_model=AttachmentRead,
    status_code=status.HTTP_201_CREATED,
)
def upload_experiment_log_attachment(
    log_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db_session),
) -> Attachment:
    experiment_log = db.get(ExperimentLog, log_id)
    if experiment_log is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experiment log not found")

    storage_path = save_upload(file, "experiment_logs", log_id)
    attachment = Attachment(
        file_name=file.filename or "upload.bin",
        content_type=file.content_type or "application/octet-stream",
        storage_path=storage_path,
        experiment_log_id=log_id,
    )
    db.add(attachment)
    db.commit()
    db.refresh(attachment)
    return attachment


@router.post(
    "/hardware-issues/{issue_id}/attachments",
    response_model=AttachmentRead,
    status_code=status.HTTP_201_CREATED,
)
def upload_hardware_issue_attachment(
    issue_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db_session),
) -> Attachment:
    hardware_issue = db.get(HardwareIssue, issue_id)
    if hardware_issue is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hardware issue not found")

    storage_path = save_upload(file, "hardware_issues", issue_id)
    attachment = Attachment(
        file_name=file.filename or "upload.bin",
        content_type=file.content_type or "application/octet-stream",
        storage_path=storage_path,
        hardware_issue_id=issue_id,
    )
    db.add(attachment)
    db.commit()
    db.refresh(attachment)
    return attachment
