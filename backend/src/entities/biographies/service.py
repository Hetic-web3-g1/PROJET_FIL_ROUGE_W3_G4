from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.engine import Connection


from src.database import db_srv
from src.database.db_engine import engine
from .schemas import Biography, BiographyCreate
from ..users.schemas import User
from .models import biography_table
from ..users.models import user_table
from .exceptions import BiographyNotFound


def _parse_row(row: sa.Row):
    return Biography(**row._asdict())


def get_all_biographies(conn: Connection) -> list[Biography]:
    """
    Get all biographies.

    Returns:
        Biographies: Dict of Biography objects.
    """
    response = conn.execute(sa.select(biography_table)).fetchall()
    return [_parse_row(row) for row in response]


def get_biography_by_id(con: Connection, biography_id: UUID) -> Biography:
    """
    Get a biography by the given id.

    Args:
        biography_id (UUID): The id of the biography.

    Returns: The Biography object.

    Raises:
        BiographyNotFound: If the biography does not exist.

    """
    response = con.execute(
        sa.select(biography_table).where(biography_table.c.id == biography_id)
    ).first()
    if response is None:
        raise BiographyNotFound

    return _parse_row(response)


def create_biography(conn: Connection, biography: BiographyCreate, user: User) -> None:
    """
    Create a biography.

    Args:
        biography (BiographyCreate): BiographyCreate object.
        user (User): The user creating the biography.

    Returns:
        Biography: The created Biography object.
    """
    db_srv.create_object(conn, biography_table, biography.dict(), user_id=user.id)


def update_biography(conn: Connection, biography_id: UUID, biography: BiographyCreate, user: User) -> None:
    """
    Update a biography.

    Args:
        biography_id (UUID): The id of the biography.
        biography (Biography): The Biography object.
        user (User): The user updating the biography.

    Returns:
        Biography: The updated Biography object.

    Raises:
        BiographyNotFound: If the biography does not exist.
    """
    check = conn.execute(
        sa.select(biography_table).where(biography_table.c.id == biography_id)
    ).first()
    if check is None:
        raise BiographyNotFound
    
    db_srv.update_object(conn, biography_table, biography_id, biography.dict(), user_id=user.id)


def delete_biography(conn: Connection, biography_id: UUID) -> None:
    """ 
    Delete a biography.

    Args:
        biography_id (UUID): The id of the biography.

    Raises:
        BiographyNotFound: If the biography does not exist.
    """
    check = conn.execute(
        sa.select(biography_table).where(biography_table.c.id == biography_id)
    ).first()
    if check is None:
        raise BiographyNotFound
    
    db_srv.delete_object(conn, biography_table, biography_id)