from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.engine import Connection

from src.database import service as db_service
from src.database.db_engine import engine
from .schemas import Masterclass, MasterclassCreate, MasterclassUserCreate, MasterclassUser
from .models import masterclass_table, masterclass_user_table
from ..users.models import user_table
from .exceptions import MasterclassNotFound


def _parse_row(row: sa.Row):
    return Masterclass(**row._asdict())

def _parse_row_masterclass_user(row: sa.Row):
    return MasterclassUser(**row._asdict())

def get_all_masterclasses(conn: Connection):
    """
    Get all masterclasses.

    Returns:
        Masterclasses: Dict of Masterclass objects.
    """
    result = conn.execute(sa.select(masterclass_table)).fetchall()
    return [_parse_row(row) for row in result]


def get_masterclass_by_id(conn: Connection, masterclass_id: UUID) -> Masterclass:
    """
    Get a masterclass by the given id.

    Args:
        masterclass_id (UUID): The id of the masterclass.

    Returns:
        Masterclass: The Masterclass object.

    Raises:
        MasterclassNotFound: If the masterclass does not exist.
    """
    result = conn.execute(
        sa.select(masterclass_table).where(masterclass_table.c.id == masterclass_id)
    ).first()
    if result is None:
        raise MasterclassNotFound

    return _parse_row(result)


def get_masterclasses_by_user(conn: Connection, user_id: UUID):
    """
    Get all masterclasses created by the given user.

    Args:
        user_id (UUID): The id of the user.

    Returns:
        Masterclasses: Dict of Masterclass objects.
    """
    result = conn.execute(
        sa.select(masterclass_table)
        .where(masterclass_table.c.created_by == user_id)
        .order_by(masterclass_table.c.created_at)
    ).fetchall()
    return [_parse_row(row) for row in result]


def create_masterclass(conn: Connection, masterclass: MasterclassCreate) -> Masterclass:
    """
    Create a masterclass.

    Args:
        masterclass (MasterclassCreate): MasterclassCreate object.

    Returns:
        Masterclass: The created Masterclass object.
    """
    result = db_service.create_object(conn, masterclass_table, masterclass.dict())
    return _parse_row(result)


def attribute_user_to_masterclass(conn: Connection, masterclass_user: MasterclassUserCreate):
    """
    Attribute a user to a masterclass.

    Args:
        masterclass_user (MasterclassUserCreate): MasterclassUserCreate object.

    Returns:
        MasterclassUser: The created MasterclassUser object.
    """
    result = db_service.create_object(conn, masterclass_user_table, masterclass_user.dict())
    return _parse_row_masterclass_user(result)