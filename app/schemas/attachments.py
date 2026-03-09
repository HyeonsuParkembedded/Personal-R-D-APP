from app.schemas.common import TimestampedReadModel


class AttachmentRead(TimestampedReadModel):
    file_name: str
    content_type: str
    storage_path: str
    experiment_log_id: int | None
    hardware_issue_id: int | None
