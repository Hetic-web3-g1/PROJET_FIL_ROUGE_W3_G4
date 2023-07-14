from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.engine import Connection

from src.database import db_srv
from src.database.db_engine import engine
from .schemas import Masterclass, MasterclassCreate, MasterclassUserCreate, MasterclassUser
from ..users.schemas import User
from .models import masterclass_table, masterclass_user_table
from ..users.models import user_table
from .exceptions import MasterclassNotFound, MasterclassUserAlreadyExist, MasterclassUserNotFound


def _parse_row(row: sa.Row):
    return Masterclass(**row._asdict())


def _parse_row_masterclass_user(row: sa.Row):
    return MasterclassUser(**row._asdict())


def get_all_masterclasses(conn: Connection) -> list[Masterclass]:
    """
    Get all masterclasses.

    Returns:
        Masterclasses: Dict of Masterclass objects.
    """
    response = conn.execute(sa.select(masterclass_table)).fetchall()
    return [_parse_row(row) for row in response]


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
    response = conn.execute(
        sa.select(masterclass_table).where(masterclass_table.c.id == masterclass_id)
    ).first()
    if response is None:
        raise MasterclassNotFound

    return _parse_row(response)


def get_masterclasses_by_user(conn: Connection, user_id: UUID):
    """
    Get all masterclasses created by the given user.

    Args:
        user_id (UUID): The id of the user.

    Returns:
        Masterclasses: Dict of Masterclass objects.
    """
    response = conn.execute(
        sa.select(masterclass_table)
        .where(masterclass_table.c.created_by == user_id)
        .order_by(masterclass_table.c.created_at)
    ).fetchall()
    return [_parse_row(row) for row in response]


def create_masterclass(conn: Connection, masterclass: MasterclassCreate, user: User) -> None:
    """
    Create a masterclass.

    Args:
        masterclass (MasterclassCreate): MasterclassCreate object.
        user (User): The user who created the masterclass.

    Returns:
        Masterclass: The created Masterclass object.
    """
    db_srv.create_object(conn, masterclass_table, masterclass.dict(), user_id=user.id)


def update_masterclass(conn: Connection, masterclass_id: UUID, masterclass: MasterclassCreate) -> None:
    """
    Update a masterclass.

    Args:
        masterclass_id (UUID): The id of the masterclass.
        masterclass (MasterclassCreate): MasterclassCreate object.

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
    
    db_srv.update_object(conn, masterclass_table, masterclass_id, masterclass.dict())


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
    
    db_srv.delete_object(conn, masterclass_table, masterclass_id)


# ---------------------------------------------------------------------------------------------------- #


def get_user_by_id_and_masterclass_id_from_masterclass_user(conn: Connection, masterclass_user: MasterclassUserCreate) -> MasterclassUser | None:
    """
    Get a user by the given id and masterclass id.

    Args:
        masterclass_user (MasterclassUserCreate): MasterclassUserCreate object.
    
    Returns:
        MasterclassUser: The MasterclassUser object. | None
    """
    query = sa.select(masterclass_user_table).where(
        (masterclass_user_table.c.user_id == masterclass_user.user_id) &
        (masterclass_user_table.c.masterclass_id == masterclass_user.masterclass_id)
    )

    response = conn.execute(query).first()
    if response is None:
        return None
    return _parse_row_masterclass_user(response)


def update_user_masterclass(conn: Connection, masterclass_user: MasterclassUser):
    """
    Update a user masterclass.

    Args:
        masterclass_user (MasterclassUserCreate): MasterclassUserCreate object.

    Returns:
        MasterclassUser: The updated MasterclassUser object.
    """
    check = get_user_by_id_and_masterclass_id_from_masterclass_user(conn, masterclass_user)
    if check is None:
        raise MasterclassUserNotFound
    
    db_srv.update_object(conn, masterclass_user_table, masterclass_user.id, masterclass_user.dict())


def assigne_user_to_masterclass(conn: Connection, masterclass_user: MasterclassUserCreate):
    """
    Attribute a user to a masterclass.

    Args:
        masterclass_user (MasterclassUserCreate): MasterclassUserCreate object.

    Returns:
        MasterclassUser: The created MasterclassUser object.
    """
    check = get_user_by_id_and_masterclass_id_from_masterclass_user(conn, masterclass_user)
    if check:
        new_masterclass_user = MasterclassUser(
            user_id=check.user_id,
            masterclass_id=check.masterclass_id,
            masterclass_role=masterclass_user.masterclass_role,
            id=check.id
        )
        reponse = update_user_masterclass(conn, new_masterclass_user)
        return reponse
    else:
        response = db_srv.create_object(conn, masterclass_user_table, masterclass_user.dict())
        return _parse_row_masterclass_user(response)
    

def unassigne_user_from_masterclass(conn: Connection, masterclass_user: MasterclassUserCreate):
    """
    Delete a user from a masterclass.

    Args:
        masterclass_user (MasterclassUserCreate): MasterclassUserCreate object.
    
    Returns:
        MasterclassUser: The deleted MasterclassUser object.
    """
    check = get_user_by_id_and_masterclass_id_from_masterclass_user(conn, masterclass_user)
    if check is None:
        raise MasterclassUserNotFound
    
    db_srv.delete_object(conn, masterclass_user_table, check.id)