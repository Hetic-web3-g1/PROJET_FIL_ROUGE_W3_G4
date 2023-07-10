from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.engine import Connection

from src.database import db_srv
from src.database.db_engine import engine
from .schemas import Academy, AcademyCreate
from .models import academy_table
from ..users.models import user_table
from .exceptions import AcademyNotFound


def _parse_row(row):
    return Academy(**row._asdict())


def get_academy_by_id(conn: Connection, academy_id: UUID) -> Academy:
    """
    Get a academy by the given id.

    Args:
        academy_id (UUID): The id of the academy.

    Returns: The Academy object.

    Raises:
        AcademyNotFound: If the academy does not exist.
    """
    result = conn.execute(
        sa.select(academy_table).where(academy_table.c.id == academy_id)
    ).first()
    if result is None:
        raise AcademyNotFound

    return _parse_row(result)


def create_academy(conn: Connection, academy: AcademyCreate) -> Academy:
    created_academy = db_srv.create_object(conn, academy_table, academy.dict())
    return created_academy