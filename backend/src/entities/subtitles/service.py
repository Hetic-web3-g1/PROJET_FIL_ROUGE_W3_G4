from uuid import UUID

import sqlalchemy as sa
from fastapi import File, UploadFile
from sqlalchemy.engine import Connection
from src.database import service as db_service

from ..comments import service as comment_service
from ..comments.schemas import CommentCreate, SubtitleComment
from ..s3_objects import service as s3_service
from ..users.schemas import User
from .exceptions import SubtitleNotFound
from .models import subtitle_table, subtitle_comment_table
from .schemas import Subtitle, SubtitleCreate


def _parse_row(row: sa.Row):
    return Subtitle(**row._asdict())


def get_subtitle_by_id(conn: Connection, subtitle_id: UUID) -> Subtitle:
    """
    Get a subtitle by the given id.

    Args:
        subtitle_id (UUID): The id of the subtitle.

    Raises:
        SubtitleNotFound: If the subtitle does not exist.

    Returns:
        The Subtitle object.
    """
    result = conn.execute(
        sa.select(subtitle_table).where(subtitle_table.c.id == subtitle_id)
    ).first()
    if result is None:
        raise SubtitleNotFound

    return _parse_row(result)


def get_subtitles_by_video_id(conn: Connection, video_id: UUID) -> list[Subtitle]:
    query = sa.select(subtitle_table).where(subtitle_table.c.video_id == video_id)

    result = conn.execute(query).fetchall()
    return [_parse_row(result) for result in result]


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
    object = s3_service.upload(file, user, public, "subtitle")

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


def delete_subtitle(conn: Connection, subtitle_id: UUID):
    """
    Delete a subtitle.

    Args:
        subtitle_id (UUID): The id of the subtitle.

    Raises:
        SubtitleNotFound: If the subtitle does not exist.
    """
    check = conn.execute(
        sa.select(subtitle_table).where(subtitle_table.c.id == subtitle_id)
    ).first()
    if check is None:
        raise SubtitleNotFound

    s3_object = s3_service.get_s3_object_by_id(conn, check.s3_object_id)  # type: ignore
    s3_service.delete_object(s3_object.object_key)
    db_service.delete_object(conn, subtitle_table, subtitle_id)


# ---------------------------------------------------------------------------------------------------- #


def create_subtitle_comment(
    conn: Connection, comment: CommentCreate, subtitle_id: UUID, user: User
):
    """
    Create a comment and link it to a subtitle.

    Args:
        comment (CommentCreate): CommentCreate object.
        subtitle_id (UUID): Id of subtitle.
        user (User): The user creating the comment.
    """
    comment_service.create_comment_and_link_table(
        conn,
        comment,
        subtitle_comment_table,
        SubtitleComment,
        subtitle_id,
        user,
    )
