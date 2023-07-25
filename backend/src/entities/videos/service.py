from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.engine import Connection

from src.database import service as db_service
from .schemas import VideoCreate, Video
from ..users.schemas import User
from .models import video_table


def _parse_row(row: sa.Row):
    return Video(**row._asdict())


def create_video(conn: Connection, video: VideoCreate, user: User) -> Video:
    """Create a video.

    Args:
        video (VideoCreate): The video to create.
        user (User): The user.

    Returns:
        Video: The created video.
    """
    result = db_service.create_object(conn, video_table, video, user_id=user.id)
    print(result)
    return _parse_row(result)
