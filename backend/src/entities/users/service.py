from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.engine import Connection

from src.database import db_srv
from .schemas import User, UserCreate
from .models import user_table
from .exceptions import EmailAlreadyExist, UserNotFound

def _parse_row(row: sa.Row):
    return User(**row._asdict())


def get_user_by_id(conn: Connection, user_id: UUID) -> User:
    """
    Get a user by the given id.

    Args:
        user_id (UUID): The id of the user.

    Returns:
        User: The User object.

    Raises:
        UserNotFound: If the user does not exist.
    """
    result = conn.execute(
        sa.select(user_table).where(user_table.c.id == user_id)
    ).first()
    if result is None:
        raise UserNotFound

    return _parse_row(result)


def get_user_by_email(conn: Connection, email: str) -> User:
    """
    Get a user by the given email.

    Args:
        email (str): The email of the user.

    Returns:
        User: The User object.

    Raises:
        UserNotFound: If the user does not exist.
    """
    result = conn.execute(
        sa.select(user_table).where(user_table.c.email == email)
    ).first()
    if result is None:
        raise UserNotFound

    return _parse_row(result)


def create_user(conn: Connection, user: UserCreate) -> User:
    """
    Create a user.

    Args:
        user (UserCreate): UserCreate object.

    Raises:
        EmailAlreadyExist: If the email already exist.

    Returns:
        User: The created User object.
    """
    result = conn.execute(
        sa.select(user_table).where(user_table.c.email == user.email)
    ).first()
    if result is not None:
        raise EmailAlreadyExist

    created_user = db_srv.create_object(conn, user_table, user.dict())
    return _parse_row(created_user)


def update_user(conn: Connection, user_id: UUID, user: UserCreate) -> User:
    """
    Update a user.

    Args:
        user_id (UUID): The id of the user.
        user (UserCreate): UserCreate object.

    Raises:
        UserNotFound: If the user does not exist.

    Returns:
        User: The updated User object.
    """
    result = conn.execute(
        sa.select(user_table).where(user_table.c.id == user_id)
    ).first()
    if result is None:
        raise UserNotFound

    updated_user = db_srv.update_object(conn, user_table, user_id, user.dict())
    return updated_user


def delete_user(conn: Connection, user_id: UUID) -> None:
    """
    Delete a user.

    Args:
        user_id (UUID): The id of the user.

    Raises:
        UserNotFound: If the user does not exist.
    """
    result = conn.execute(
        sa.select(user_table).where(user_table.c.id == user_id)
    ).first()
    if result is None:
        raise UserNotFound

    db_srv.delete_object(conn, user_table, user_id)