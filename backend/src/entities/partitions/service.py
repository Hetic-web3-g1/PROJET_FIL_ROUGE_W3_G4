from uuid import UUID

import sqlalchemy as sa
from fastapi import File, UploadFile
from sqlalchemy.engine import Connection

from src.database import service as db_service

from ..s3_objects import service as s3_service
from ..tags import service as tag_service
from ..tags.schemas import PartitionTag
from ..users.schemas import User
from .exceptions import PartitionNotFound
from .models import partition_table, partition_tag_table
from .schemas import Partition, PartitionCreate


def _parse_row(row: sa.Row):
    return Partition(**row._asdict())


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


def create_partition(
    conn: Connection,
    user: User,
    public: bool,
    file: UploadFile = File(...),
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
    object = s3_service.upload(file, user, public)

    partition = PartitionCreate(
        filename=object.filename,
        status="uploaded",
        s3_object_id=object.id,
    )

    result = db_service.create_object(
        conn, partition_table, partition.dict(), user_id=user.id
    )

    tag_service.create_tag_and_link_table(
        conn,
        partition.filename,
        partition_table,
        partition_tag_table,
        PartitionTag,
        result.id,
    )

    return _parse_row(result)


def update_partition(
    conn: Connection, partition_id: UUID, partition: PartitionCreate, user: User
) -> Partition:
    """
    Update a partition.

    Args:
        partition_id (UUID): The id of the partition to update.
        partition (PartitionCreate): PartitionCreate object.
        user (User): The user updating the partition.

    Raises:
        PartitionNotFound: If the partition does not exist.

    Returns:
        Partition: The updated Partition object.
    """
    check = conn.execute(
        sa.select(partition_table).where(partition_table.c.id == partition_id)
    ).first()
    if check is None:
        raise PartitionNotFound

    result = db_service.update_object(
        conn, partition_table, partition_id, partition.dict(), user_id=user.id
    )
    return _parse_row(result)


def delete_partition(conn: Connection, connection_id: UUID) -> None:
    """
    Delete a partition.

    Args:
        partition_id (UUID): The id of the partition.

    Raises:
        PartitionNotFound: If the partition does not exist.
    """
    check = conn.execute(
        sa.select(partition_table).where(partition_table.c.id == connection_id)
    ).first()
    if check is None:
        raise PartitionNotFound

    db_service.delete_object(conn, partition_table, connection_id)
