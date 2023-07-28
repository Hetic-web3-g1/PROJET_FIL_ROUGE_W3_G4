from uuid import UUID

import sqlalchemy as sa
from fastapi import File, UploadFile
from sqlalchemy.engine import Connection

from src.database import service as db_service

from ..s3_objects import service as s3_service
from ..users.schemas import User
from .models import subtitle_table
from .schemas import Subtitle, SubtitleCreate


def _parse_row(row: sa.Row):
    return Subtitle(**row._asdict())


def create_subtitle(
    conn: Connection,
    user: User,
    language: str,
    video_id: UUID,
    public: bool,
    file: UploadFile = File(...),
) -> Subtitle:
    """
    Create a new subtitle.

    Args:
        user (User): The user creating the partition.
        language (str): The language of the subtitle.
        video_id (UUID): The video id.
        public (bool): Whether the partition file should be public or not.
        file (UploadFile): The file to upload.

    Returns:
        Subtitle: The created subtitle.
    """
    object = s3_service.upload(file, user, public)

    subtitle = SubtitleCreate(
        filename=object.filename,
        language=language,
        status="uploaded",
        video_id=video_id,
        s3_object_id=object.id,
    )

    result = db_service.create_object(
        conn, subtitle_table, subtitle.dict(), user_id=user.id
    )
    return _parse_row(result)
