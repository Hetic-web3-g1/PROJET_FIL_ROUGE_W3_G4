from uuid import UUID

import sqlalchemy as sa
from fastapi import UploadFile
from sqlalchemy.engine import Connection
from src.database import service as db_service

from ..comments import service as comment_service
from ..comments.schemas import CommentCreate, PartitionComment
from ..s3_objects import service as s3_service
from ..tags import service as tag_service
from ..tags.schemas import PartitionTag
from ..users.schemas import User
from .exceptions import (
    PartitionNotFound,
    PartitionMetaNotFound,
    PartitionMetaKeyAlreadyExist,
)
from .models import (
    partition_table,
    partition_tag_table,
    partition_comment_table,
    partition_meta_table,
)
from .schemas import Partition, PartitionCreate, PartitionMeta, PartitionMetaCreate


def _parse_row(row: sa.Row):
    return Partition(**row._asdict())


def _parse_meta_row(row: sa.Row):
    return PartitionMeta(**row._asdict())


def get_all_partitions(conn: Connection):
    """
    Get all partitions.

    Returns:
        Partitions: Dict of Partition objects.
    """
    result = conn.execute(sa.select(partition_table)).fetchall()
    for row in result:
        yield _parse_row(row)


def get_partition_by_id(conn: Connection, partition_id: UUID) -> Partition:
    """
    Get a partition by the given id.

    Args:
        partition_id (UUID): The id of the partition.

    Returns:
        Partition: The Partition object.

    Raises:
        PartitionNotFound: If the partition does not exist.
    """
    result = conn.execute(
        sa.select(partition_table).where(partition_table.c.id == partition_id)
    ).first()
    if result is None:
        raise PartitionNotFound

    return _parse_row(result)


def create_partition_tags(conn: Connection, partition: Partition) -> None:
    """
    Create tags for a partition.

    Args:
        partition (PartitionCreate): PartitionCreate object.
        result (sa.Row): Result of partition creation.
    """
    tags = [partition.filename]

    for content in tags:
        tag_service.create_tag_and_link_table(
            conn,
            content,
            partition_table,
            partition_tag_table,
            PartitionTag,
            partition.id,
        )


def create_partition(
    conn: Connection,
    user: User,
    public: bool,
    file: UploadFile,
) -> Partition:
    """
    Create a partition.

    Args:
        user (User): The user creating the partition.
        public (bool): Whether the partition file should be public or not.
        file (UploadFile): The file to upload.

    Returns:
        Partition: The created Partition object.
    """
    object = s3_service.upload(file, user, public, "partition")

    partition = PartitionCreate(
        filename=object.filename,
        status="uploaded",
        s3_object_id=object.id,
    )

    result = db_service.create_object(
        conn, partition_table, partition.dict(), user_id=user.id
    )

    partition = _parse_row(result)
    create_partition_tags(conn, partition)

    return _parse_row(result)


def delete_partition(conn: Connection, partition_id: UUID) -> None:
    """
    Delete a partition.

    Args:
        partition_id (UUID): The id of the partition.

    Raises:
        PartitionNotFound: If the partition does not exist.
    """
    check = conn.execute(
        sa.select(partition_table).where(partition_table.c.id == partition_id)
    ).first()
    if check is None:
        raise PartitionNotFound

    s3_object = s3_service.get_s3_object_by_id(conn, check.s3_object_id)  # type: ignore
    s3_service.delete_object(s3_object.object_key)

    tag_service.delete_tags_by_object_id(
        conn, partition_id, partition_table, partition_tag_table
    )
    comment_service.delete_comments_by_object_id(
        conn, partition_id, partition_table, partition_comment_table
    )
    db_service.delete_object(conn, partition_table, partition_id)


# ---------------------------------------------------------------------------------------------------- #


def create_partition_comment(
    conn: Connection, comment: CommentCreate, partition_id: UUID, user: User
):
    """
    Create a comment and link it to a partition.

    Args:
        comment (CommentCreate): CommentCreate object.
        partition_id (UUID): Id of partition.
        user (User): The user creating the comment.
    """
    comment_service.create_comment_and_link_table(
        conn,
        comment,
        partition_comment_table,
        PartitionComment,
        partition_id,
        user,
    )


# ---------------------------------------------------------------------------------------------------- #


def get_partition_meta_by_id(conn: Connection, meta_id: int) -> PartitionMeta:
    """
    Get a partition meta by the given id.

    Args:
        meta_id (int): The id of the partition meta.

    Raises:
        PartitionMetaNotFound: If the partition meta does not exist.

    Returns:
        PartitionMeta: The PartitionMeta object.
    """
    result = conn.execute(
        sa.select(partition_meta_table).where(partition_meta_table.c.id == meta_id)
    ).first()
    if result is None:
        raise PartitionMetaNotFound

    return _parse_meta_row(result)


def get_partition_meta_by_partition_id(
    conn: Connection, partition_id: UUID
) -> list[PartitionMeta]:
    """
    Get all meta entries for a partition.

    Args:
        partition_id (UUID): The id of the partition.

    Returns:
        list[PartitionMeta]: List of PartitionMeta objects.
    """
    result = conn.execute(
        sa.select(partition_meta_table).where(
            partition_meta_table.c.partition_id == partition_id
        )
    ).fetchall()

    return [_parse_meta_row(row) for row in result]


def create_partition_meta(
    conn: Connection,
    meta: PartitionMetaCreate,
) -> PartitionMeta:
    """
    Create a meta entry for a partition.

    Args:
        meta (PartitionMetaCreate): PartitionMetaCreate object.

    Raises:
        PartitionMetaKeyAlreadyExist: If the meta key already exists.

    Returns:
        PartitionMeta: The created PartitionMeta object.
    """
    check = conn.execute(
        sa.select(partition_meta_table).where(
            partition_meta_table.c.meta_key == meta.meta_key,
        )
    ).first()
    if check is not None:
        raise PartitionMetaKeyAlreadyExist

    result = db_service.create_object(
        conn,
        partition_meta_table,
        meta.dict(),
    )

    return _parse_meta_row(result)


def update_partition_meta(
    conn: Connection,
    meta_id: int,
    meta: PartitionMetaCreate,
) -> PartitionMeta:
    """
    Update a meta entry.

    Args:
        meta_id (int): The id of the meta entry.
        meta (PartitionMetaCreate): The PartitionMetaCreate object.

    Raises:
        PartitionMetaNotFound: If the meta entry does not exist.

    Returns:
        PartitionMeta: The updated PartitionMeta object.
    """
    check = conn.execute(
        sa.select(partition_meta_table).where(partition_meta_table.c.id == meta_id)
    ).first()
    if check is None:
        raise PartitionMetaNotFound

    result = db_service.update_object(
        conn,
        partition_meta_table,
        meta_id,
        meta.dict(),
    )

    return _parse_meta_row(result)


def delete_partition_meta(conn: Connection, meta_id: int) -> None:
    """
    Delete a meta entry.

    Args:
        meta_id (int): The id of the meta entry.

    Raises:
        PartitionMetaNotFound: If the meta entry does not exist.
    """
    check = conn.execute(
        sa.select(partition_meta_table).where(partition_meta_table.c.id == meta_id)
    ).first()
    if check is None:
        raise PartitionMetaNotFound

    db_service.delete_object(conn, partition_meta_table, meta_id)
