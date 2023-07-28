from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.engine import Connection

from .exceptions import EmailAlreadyExist, UserNotFound
from .models import user_table
from .schemas import User, UserCreate
from ..masterclasses.models import masterclass_user_table
from ...database import service as db_service


def _parse_row(row: sa.Row): 
    return User(**row._asdict())


def get_all_users_by_academy(conn: Connection, academy_id: UUID):
    """
    Get all users by the given academy.

    Args:
        academy_id (UUID): The id of the academy.

    Returns:
        Users: Dict of User objects.
    """
    result = conn.execute(
        sa.select(user_table).where(user_table.c.academy_id == academy_id)
    ).fetchall()
    for row in result:
        yield _parse_row(row)


def get_all_users_by_masterclass(conn: Connection, masterclass_id: UUID):
    """
    Get all users by the given masterclass.

    Args:
        masterclass_id (UUID): The id of the masterclass.

    Returns:
        Users: Generator of User objects.
    """
    stmt = (
        sa.select(user_table)
        .select_from(
            sa.join(
                user_table,
                masterclass_user_table,
                user_table.c.id == masterclass_user_table.c.user_id,
            )
        )
        .where(masterclass_user_table.c.masterclass_id == masterclass_id)
    )

    result = conn.execute(stmt).fetchall()
    for row in result:
        yield _parse_row(row)


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


def create_user(conn: Connection, new_user: UserCreate, user: User) -> User:
    """
    Create a user.

    Args:
        new_user (UserCreate): UserCreate object.
        user (User): The user that is creating the user.

    Raises:
        EmailAlreadyExist: If the email already exist.

    Returns:
        User: The created User object.
    """
    check = conn.execute(
        sa.select(user_table).where(user_table.c.email == new_user.email)
    ).first()
    if check is not None:
        raise EmailAlreadyExist

    result = db_service.create_object(
        conn, user_table, new_user.dict(), user_id=user.id
    )
    return _parse_row(result)


def update_user(
    conn: Connection, user_id: UUID, new_user: UserCreate, user: User
) -> User:
    """
    Update a user.

    Args:
        user_id (UUID): The id of the user.
        new_user (UserCreate): UserCreate object.
        user (User): The user that is updating the user.

    Raises:
        UserNotFound: If the user does not exist.

    Returns:
        User: The updated User object.
    """
    check = conn.execute(
        sa.select(user_table).where(user_table.c.id == user_id)
    ).first()
    if check is None:
        raise UserNotFound

    result = db_srv.update_object(
        conn, user_table, user_id, new_user.dict(), user_id=user.id
    )
    return _parse_row(result)
