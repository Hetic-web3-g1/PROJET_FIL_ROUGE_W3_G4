from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.engine import Connection

from src.database import db_srv
from src.database.db_engine import engine
from .schemas import Partition, PartitionCreate
from ..users.schemas import User
from .models import partition_table
from ..users.models import user_table
from .exceptions import PartitionNotFound


def _parse_row(row: sa.Row):
    return Partition(**row._asdict())


def get_all_partitions(conn: Connection) -> list[Partition]:
    """
    Get all partitions.

    Returns:
        Partitions: Dict of Partition objects.
    """
    result = conn.execute(sa.select(partition_table)).fetchall()
    return [_parse_row(row) for row in result]


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


def create_partition(conn: Connection, partition: PartitionCreate, user: User) -> Partition:
    """
    Create a partition.

    Args:
        partition (PartitionCreate): PartitionCreate object.
        user (User): The user creating the partition.

    Returns:
        Partition: The created Partition object.
    """
    result = db_srv.create_object(conn, partition_table, partition.dict(), user_id=user.id)
    return _parse_row(result)


def update_partition(conn: Connection, partition_id: UUID, partition: PartitionCreate, user: User) -> Partition:
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

    result = db_srv.update_object(conn, partition_table, partition_id, partition.dict(), user_id=user.id)
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

    db_srv.delete_object(conn, partition_table, connection_id)