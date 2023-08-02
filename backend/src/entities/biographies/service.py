from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.engine import Connection

from .exceptions import BiographyNotFound
from .models import biography_table, biography_tag_table
from .schemas import Biography, BiographyCreate
from ..tags import service as tag_service
from ..tags.schemas import BiographyTag
from ..users.schemas import User
from ...database import service as db_service


def _parse_row(row: sa.Row):  # type: ignore
    return Biography(**row._asdict())


def get_all_biographies(conn: Connection):
    """
    Get all biographies.

    Returns:
        Biographies: Dict of Biography objects.
    """
    result = conn.execute(sa.select(biography_table)).fetchall()
    for row in result:
        yield _parse_row(row)


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


def create_biography(
    conn: Connection, biography: BiographyCreate, user: User
) -> Biography:
    """
    Create a biography.

    Args:
        biography (BiographyCreate): BiographyCreate object.
        user (User): The user creating the biography.

    Returns:
        Biography: The created Biography object.
    """
    result = db_service.create_object(
        conn, biography_table, biography.dict(), user_id=user.id
    )

    tags = [biography.first_name, biography.last_name]
    if biography.instrument:
        tags.extend(biography.instrument)

    for content in tags:
        tag_service.create_tag_and_link_table(
            conn,
            content,
            biography_table,
            biography_tag_table,
            BiographyTag,
            result.id,
        )

    return _parse_row(result)


def update_biography(
    conn: Connection, biography_id: UUID, biography: BiographyCreate, user: User
) -> Biography:
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

    result = db_service.update_object(
        conn, biography_table, biography_id, biography.dict(), user_id=user.id
    )
    return _parse_row(result)


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

    db_service.delete_object(conn, biography_table, biography_id)
    tag_service.delete_orphaned_tags(conn, biography_tag_table, biography_table)
