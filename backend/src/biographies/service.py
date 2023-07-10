from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.engine import Connection


from src.database import db_srv
from src.database.db_engine import engine
from .schemas import Biography, BiographyCreate
from .models import biography_table
from src.users.models import user_table
from .exceptions import BiographyNotFound


def _parse_row(row: sa.Row):
    return Biography(**row._asdict())


def create_biography(conn: Connection, biography: BiographyCreate) -> Biography:
    """
    Create a biography.

    Args:
        biography (BiographyCreate): BiographyCreate object.

    Returns:
        Biography: The created Biography object.
    """
    create_biography = db_srv.create_object(conn, biography_table, biography.dict())
    return _parse_row(create_biography)


def get_all_biographies(conn: Connection):
    """
    Get all biographies.

    Returns:
        Biographies: Dict of Biography objects.
    """
    result = conn.execute(sa.select(biography_table)).fetchall()
    return [_parse_row(row) for row in result]


def get_biography_by_id(con: Connection, biography_id: UUID) -> Biography:
    """
    Get a biography by the given id.

    Args:
        biography_id (UUID): The id of the biography.

    Returns: The Biography object.

    Raises:
        BiographyNotFound: If the biography does not exist.

    """
    result = con.execute(
        sa.select(biography_table).where(biography_table.c.id == biography_id)
    ).first()
    if result is None:
        raise BiographyNotFound

    return _parse_row(result)