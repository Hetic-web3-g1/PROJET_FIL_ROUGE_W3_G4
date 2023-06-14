from uuid import UUID

import sqlalchemy as sa

from .schemas import User
from src.masterclasses.models import masterclass_user_table


def is_admin(user: User):
    """
    Check if the user is an admin.

    Args:
        user (User, optional): The user to check.

    Returns:
        bool: True if the user is an admin, False otherwise.
    """
    if user.role != 'admin':
        return False
    return True


def has_masterclass_role(conn, role_to_check: str, user_id: UUID, masterclass_id: UUID):
    """
    Check if the user has a masterclass role.

    Args:
        role_to_check (str): The role to check.
        user_id (UUID): The id of the user.
        masterclass_id (UUID): The id of the masterclass.
    Returns:
        bool: True if the user has a masterclass role, False otherwise.
    """
    result = conn.execute(
        sa.select(masterclass_user_table.c.role)
        .where(masterclass_user_table.c.masterclass_id == masterclass_id)
        .where(masterclass_user_table.c.user_id == user_id)
    ).first()

    if result is None or result[0] != role_to_check:
        return False
    return True