import sqlalchemy as sa
from fastapi import UploadFile
from sqlalchemy.engine import Connection
from src.database import service as db_service

from ..comments import service as comment_service
from ..comments.schemas import VideoComment
from ..s3_objects import service as s3_service
from ..users.schemas import User
from .exceptions import VideoNotFound
from .models import video_table, video_comment_table
from .schemas import Video, VideoCreate


def _parse_row(row: sa.Row):
    return Video(**row._asdict())


def create_video(
    conn: Connection,
    user: User,
    duration: int,
    version: float,
    public: bool,
    file: UploadFile,
) -> Video:
    """
    Create a video.

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

    result = db_service.create_object(conn, video_table, video.dict(), user_id=user.id)
    return _parse_row(result)


def delete_video(conn: Connection, video_id: str):
    """
    Delete a video.

    Args:
        video_id (str): The id of the video.

    Raises:
        VideoNotFound: If the video does not exist.
    """
    check = conn.execute(
        sa.select(video_table).where(video_table.c.id == video_id)
    ).first()
    if check is None:
        raise VideoNotFound

    comment_service.delete_comments_by_object_id(
        conn, video_id, video_table, video_comment_table
    )
    db_service.delete_object(conn, video_table, video_id)


# ---------------------------------------------------------------------------------------------------- #


def create_video_comment(conn: Connection, comment, video_id, user: User):
    """
    Create a comment for a video.

    Args:
        comment (CommentCreate): The comment to create.
        video_id (UUID): The id of the video.
        user (User): The user creating the comment.
    """
    comment_service.create_comment_and_link_table(
        conn,
        comment,
        video_comment_table,
        VideoComment,
        video_id,
        user,
    )
