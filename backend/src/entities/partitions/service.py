from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.engine import Connection

from src.database import db_srv
from src.database.db_engine import engine
from .schemas import Partition, PartitionCreate
from .models import partition_table
from ..users.models import user_table
from .exceptions import PartitionNotFound


def _parse_row(row: sa.Row):
    return Partition(**row._asdict())


def get_all_partitions(conn: Connection):
    """
    Get all partitions.

    Returns:
        Partitions: Dict of Partition objects.
    """
    response = conn.execute(sa.select(partition_table)).fetchall()
    return [_parse_row(row) for row in response]


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
    response = conn.execute(
        sa.select(partition_table).where(partition_table.c.id == partition_id)
    ).first()
    if response is None:
        raise PartitionNotFound

    return _parse_row(response)


def create_partition(conn: Connection, partition: PartitionCreate) -> None:
    """
    Create a partition.

    Args:
        partition (PartitionCreate): PartitionCreate object.

    Returns:
        Partition: The created Partition object.
    """
    db_srv.create_object(conn, partition_table, partition.dict())