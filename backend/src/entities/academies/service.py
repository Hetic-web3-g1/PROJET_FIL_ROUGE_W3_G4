from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.engine import Connection

from src.database import service as db_service

from .exceptions import AcademyNotFound
from .models import academy_table
from .schemas import Academy, AcademyCreate


def _parse_row(row: sa.Row):
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
    """
    Create a academy.

    Args:
        academy (AcademyCreate): AcademyCreate object.
        user (User): The user creating the academy.

    Returns:
        Academy: The created Academy object.
    """
    created_academy = db_service.create_object(conn, academy_table, academy.dict())
    return created_academy
