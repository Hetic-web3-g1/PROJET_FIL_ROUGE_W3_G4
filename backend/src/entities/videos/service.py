from uuid import UUID

import sqlalchemy as sa
from fastapi import UploadFile
from sqlalchemy.engine import Connection
from src.database import service as db_service

from ..comments import service as comment_service
from ..comments.schemas import CommentCreate, VideoComment
from ..s3_objects import service as s3_service
from ..users.schemas import User
from .exceptions import VideoNotFound, VideoMetaNotFound, VideoMetaKeyAlreadyExist
from .models import video_table, video_comment_table, video_meta_table
from .schemas import Video, VideoCreate, VideoMeta, VideoMetaCreate


def _parse_row(row: sa.Row):
    return Video(**row._asdict())


def _parse_meta_row(row: sa.Row):
    return VideoMeta(**row._asdict())


def get_video_by_id(conn: Connection, video_id: UUID) -> Video:
    """
    Get a video by its id.

    Args:
        video_id (UUID): The id of the video.

    Raises:
        VideoNotFound: If the video does not exist.

    Returns:
        Video: The video.
    """
    result = conn.execute(
        sa.select(video_table).where(video_table.c.id == video_id)
    ).first()
    if result is None:
        raise VideoNotFound

    return _parse_row(result)


def get_videos_by_masterclass_id(conn: Connection, masterclass_id: UUID) -> list[Video]:
    """
    Get all videos of a masterclass.

    Args:
        masterclass_id (UUID): The id of the masterclass.

    Returns:
        list[Video]: The videos.
    """
    result = conn.execute(
        sa.select(video_table)
        .where(video_table.c.masterclass_id == masterclass_id)
        .order_by(video_table.c.version)
    ).fetchall()
    return [_parse_row(row) for row in result]


def create_video(
    conn: Connection,
    user: User,
    masterclass_id: UUID,
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
    object = s3_service.upload(file, user, public, "video")

    video = VideoCreate(
        filename=object.filename,
        masterclass_id=masterclass_id,
        duration=duration,
        status="uploaded",
        version=version,
        s3_object_id=object.id,
    )

    result = db_service.create_object(conn, video_table, video.dict(), user_id=user.id)
    return _parse_row(result)


def delete_video(conn: Connection, video_id: UUID):
    """
    Delete a video.

    Args:
        video_id (UUID): The id of the video.

    Raises:
        VideoNotFound: If the video does not exist.
    """
    check = conn.execute(
        sa.select(video_table).where(video_table.c.id == video_id)
    ).first()
    if check is None:
        raise VideoNotFound

    s3_object = s3_service.get_s3_object_by_id(conn, check.s3_object_id)  # type: ignore
    s3_service.delete_object(s3_object.object_key)

    comment_service.delete_comments_by_object_id(
        conn, video_id, video_table, video_comment_table
    )
    db_service.delete_object(conn, video_table, video_id)


# ---------------------------------------------------------------------------------------------------- #


def create_video_comment(
    conn: Connection, comment: CommentCreate, video_id: UUID, user: User
):
    """
    Create a comment and link it to a video.

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


# ---------------------------------------------------------------------------------------------------- #


def get_video_meta_by_id(conn: Connection, meta_id: int) -> VideoMeta:
    """
    Get a video meta by the given id.

    Args:
        meta_id (int): The id of the meta entry.

    Raises:
        VideoMetaNotFound: If the meta entry does not exist.

    Returns:
        VideoMeta: The video meta.
    """
    result = conn.execute(
        sa.select(video_meta_table).where(video_meta_table.c.id == meta_id)
    ).first()
    if result is None:
        raise VideoMetaNotFound

    return _parse_meta_row(result)


def get_video_meta_by_video_id(conn: Connection, video_id: UUID) -> list[VideoMeta]:
    """
    Get all meta entries of a video.

    Args:
        video_id (UUID): The id of the video.

    Returns:
        list[VideoMeta]: The video meta entries.
    """
    result = conn.execute(
        sa.select(video_meta_table).where(video_meta_table.c.video_id == video_id)
    ).fetchall()

    return [_parse_meta_row(row) for row in result]


def create_video_meta(conn: Connection, meta: VideoMetaCreate) -> VideoMeta:
    """
    Create a meta entry for a video.

    Args:
        meta (VideoMetaCreate): The meta entry to create.

    Raises:
        VideoMetaKeyAlreadyExist: If the meta key already exists.

    Returns:
        VideoMeta: The created video meta.
    """
    check = conn.execute(
        sa.select(video_meta_table).where(
            video_meta_table.c.meta_key == meta.meta_key,
        )
    ).first()
    if check is not None:
        raise VideoMetaKeyAlreadyExist

    result = db_service.create_object(conn, video_meta_table, meta.dict())

    return _parse_meta_row(result)


def update_video_meta(
    conn: Connection, meta_id: int, meta: VideoMetaCreate
) -> VideoMeta:
    """
    Update a video meta entry.

    Args:
        meta_id (int): The id of the meta entry.
        meta (VideoMetaCreate): The new meta entry.

    Raises:
        VideoMetaNotFound: If the meta entry does not exist.

    Returns:
        VideoMeta: The updated video meta.
    """
    check = conn.execute(
        sa.select(video_meta_table).where(video_meta_table.c.id == meta_id)
    ).first()
    if check is None:
        raise VideoMetaNotFound

    result = db_service.update_object(conn, video_meta_table, meta_id, meta.dict())

    return _parse_meta_row(result)


def delete_video_meta(conn: Connection, meta_id: int):
    """
    Delete a video meta entry.

    Args:
        meta_id (int): The id of the meta entry.

    Raises:
        VideoMetaNotFound: If the meta entry does not exist.
    """
    check = conn.execute(
        sa.select(video_meta_table).where(video_meta_table.c.id == meta_id)
    ).first()
    if check is None:
        raise VideoMetaNotFound

    db_service.delete_object(conn, video_meta_table, meta_id)
