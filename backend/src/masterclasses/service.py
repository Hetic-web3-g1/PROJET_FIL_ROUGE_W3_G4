from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.engine import Connection

from src.database import db_srv
from src.database.db_engine import engine
from .schemas import Masterclass, MasterclassCreate
from .models import masterclass_table
from .exceptions import MasterclassNotFound


def _parse_row(row: sa.Row):
    return Masterclass(**row._asdict())


def create_masterclass(conn: Connection, masterclass: MasterclassCreate) -> Masterclass:
    create_masterclass = db_srv.create_object(conn, masterclass_table, masterclass.dict())
    return _parse_row(create_masterclass)


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