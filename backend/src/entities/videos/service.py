import sqlalchemy as sa
from fastapi import UploadFile, File
from sqlalchemy.engine import Connection

from .models import video_table
from .schemas import VideoCreate, Video
from ..users.schemas import User
from ..s3_objects import service as s3_service
from ...database import service as db_service


def _parse_row(row: sa.Row):
    return Video(**row._asdict())


def create_video(
    conn: Connection,
    user: User,
    public: bool,
    duration: int,
    version: float,
    file: UploadFile = File(...),
) -> Video:
    """Create a video.

    Args:
        user (User): The user creating the partition.
        public (bool): Whether the partition file should be public or not.
        duration (int): The duration of the video.
        version (float): The version of the video.
        file (UploadFile): The file to upload.

    Returns:
        Video: The created video.
    """
    object = s3_service.upload(file, user, public)

    video = VideoCreate(
        filename=object.filename,
        duration=duration,
        status="uploaded",
        version=version,
        s3_object_id=object.id,
    )

    result = db_service.create_object(conn, video_table, video, user_id=user.id)
    return _parse_row(result)
