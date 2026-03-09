from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import settings


def initialize_storage() -> None:
    Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)


def save_upload(file: UploadFile, group: str, owner_id: int) -> str:
    target_dir = Path(settings.upload_dir) / group / str(owner_id)
    target_dir.mkdir(parents=True, exist_ok=True)

    original_name = Path(file.filename or "upload.bin").name
    target_path = target_dir / f"{uuid4().hex}_{original_name}"

    with target_path.open("wb") as output:
        output.write(file.file.read())

    file.file.close()
    return str(target_path)
