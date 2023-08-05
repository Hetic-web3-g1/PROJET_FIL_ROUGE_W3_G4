from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.engine import Connection

from src.database import service as db_service

from ..tags import service as tag_service
from ..tags.schemas import MasterclassTag
from ..users.schemas import User
from .exceptions import MasterclassNotFound, MasterclassUserNotFound
from .models import masterclass_table, masterclass_tag_table, masterclass_user_table
from .schemas import (
    Masterclass,
    MasterclassCreate,
    MasterclassUser,
    MasterclassUserCreate,
)


def _parse_row(row: sa.Row):  # type: ignore
    return Masterclass(**row._asdict())


def _parse_row_masterclass_user(row: sa.Row):  # type: ignore
    return MasterclassUser(**row._asdict())


def get_all_masterclasses(conn: Connection):
    """
    Get all masterclasses.

    Returns:
        Masterclasses: Dict of Masterclass objects.
    """
    result = conn.execute(sa.select(masterclass_table)).fetchall()
    for row in result:
        yield _parse_row(row)


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


def get_masterclasses_by_user(conn: Connection, user_id: UUID):
    """
    Get all masterclasses created by the given user.

    Args:
        user_id (UUID): The id of the user.

    Returns:
        Masterclasses: Dict of Masterclass objects.
    """
    result = conn.execute(
        sa.select(masterclass_table)
        .where(masterclass_table.c.created_by == user_id)
        .order_by(masterclass_table.c.created_at)
    ).fetchall()
    for row in result:
        yield _parse_row(row)


def create_masterclass(
    conn: Connection, masterclass: MasterclassCreate, user: User
) -> Masterclass:
    """
    Create a masterclass.

    Args:
        masterclass (MasterclassCreate): MasterclassCreate object.
        user (User): The user who created the masterclass.

    Returns:
        Masterclass: The created Masterclass object.
    """
    result = db_service.create_object(
        conn, masterclass_table, masterclass.dict(), user_id=user.id
    )

    tags = [masterclass.title]
    if masterclass.instrument:
        tags.extend(masterclass.instrument)

    for content in tags:
        tag_service.create_tag_and_link_table(
            conn,
            content,
            masterclass_table,
            masterclass_tag_table,
            MasterclassTag,
            result.id,
        )

    return _parse_row(result)


def update_masterclass(
    conn: Connection, masterclass_id: UUID, masterclass: MasterclassCreate, user: User
) -> Masterclass:
    """
    Update a masterclass.

    Args:
        masterclass_id (UUID): The id of the masterclass.
        masterclass (MasterclassCreate): MasterclassCreate object.
        user (User): The user who updated the masterclass.

    Raises:
        MasterclassNotFound: If the masterclass does not exist.

    Returns:
        Masterclass: The updated Masterclass object.
    """
    check = conn.execute(
        sa.select(masterclass_table).where(masterclass_table.c.id == masterclass_id)
    ).first()
    if check is None:
        raise MasterclassNotFound

    result = db_service.update_object(
        conn, masterclass_table, masterclass_id, masterclass.dict(), user_id=user.id
    )
    return _parse_row(result)


def delete_masterclass(conn: Connection, masterclass_id: UUID) -> None:
    """
    Delete a masterclass.

    Args:
        masterclass_id (UUID): The id of the masterclass.

    Raises:
        MasterclassNotFound: If the masterclass does not exist.
    """
    check = conn.execute(
        sa.select(masterclass_table).where(masterclass_table.c.id == masterclass_id)
    ).first()
    if check is None:
        raise MasterclassNotFound

    db_service.delete_object(conn, masterclass_table, masterclass_id)
    tag_service.delete_orphaned_tags(conn, masterclass_tag_table, masterclass_table)


# ---------------------------------------------------------------------------------------------------- #


def get_user_by_id_and_masterclass_id_from_masterclass_user(
    conn: Connection, masterclass_user: MasterclassUserCreate
) -> MasterclassUser | None:
    """
    Get a user by the given id and masterclass id.

    Args:
        masterclass_user (MasterclassUserCreate): MasterclassUserCreate object.

    Returns:
        MasterclassUser: The MasterclassUser object. | None
    """
    query = sa.select(masterclass_user_table).where(
        (masterclass_user_table.c.user_id == masterclass_user.user_id)
        & (masterclass_user_table.c.masterclass_id == masterclass_user.masterclass_id)
    )

    result = conn.execute(query).first()
    if result is None:
        return None
    return _parse_row_masterclass_user(result)


def update_user_masterclass(conn: Connection, masterclass_user: MasterclassUser):
    """
    Update a user masterclass.

    Args:
        masterclass_user (MasterclassUserCreate): MasterclassUserCreate object.

    Returns:
        MasterclassUser: The updated MasterclassUser object.
    """
    check = get_user_by_id_and_masterclass_id_from_masterclass_user(
        conn, masterclass_user
    )
    if check is None:
        raise MasterclassUserNotFound

    db_service.update_object(
        conn, masterclass_user_table, masterclass_user.id, masterclass_user.dict()
    )


def assign_user_to_masterclass(
    conn: Connection, masterclass_user: MasterclassUserCreate
):
    """
    Attribute a user to a masterclass.

    Args:
        masterclass_user (MasterclassUserCreate): MasterclassUserCreate object.

    Returns:
        MasterclassUser: The created MasterclassUser object.
    """
    check = get_user_by_id_and_masterclass_id_from_masterclass_user(
        conn, masterclass_user
    )
    if check:
        new_masterclass_user = MasterclassUser(
            user_id=check.user_id,
            masterclass_id=check.masterclass_id,
            masterclass_role=masterclass_user.masterclass_role,
            id=check.id,
        )
        result = update_user_masterclass(conn, new_masterclass_user)
        return result
    else:
        result = db_service.create_object(
            conn, masterclass_user_table, masterclass_user.dict()
        )
        return _parse_row_masterclass_user(result)


def unassign_user_from_masterclass(
    conn: Connection, masterclass_user: MasterclassUserCreate
):
    """
    Delete a user from a masterclass.

    Args:
        masterclass_user (MasterclassUserCreate): MasterclassUserCreate object.

    Returns:
        MasterclassUser: The deleted MasterclassUser object.
    """
    check = get_user_by_id_and_masterclass_id_from_masterclass_user(
        conn, masterclass_user
    )
    if check is None:
        raise MasterclassUserNotFound

    db_service.delete_object(conn, masterclass_user_table, check.id)
