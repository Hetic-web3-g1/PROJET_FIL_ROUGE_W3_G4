from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.engine import Connection

from database import db_srv
from .schemas import User, UserCreate
from .models import user_table
from .exceptions import EmailAlreadyExist


def create_user(conn: Connection, user: UserCreate) -> User:
    result = conn.execute(
        sa.select([user_table]).where(user_table.c.email == user.email)
    ).first()
    if result is not None:
        raise EmailAlreadyExist

    created_user = db_srv.create_object(conn, user_table, user.dict())
    return User(**created_user)


async def get_user_by_id(conn, user_id: UUID) -> User:
    """
    Get a user by the given id.

    Args:
        user_id (UUID): The id of the user.

    Returns:
        User: The User object.

    Raises:
        UserNotFound: If the user does not exist.
    """
