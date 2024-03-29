from uuid import UUID
from typing import List

import sqlalchemy as sa
from sqlalchemy.engine import Connection
from src.database import service as db_service


from ..comments import service as comment_service
from ..comments.schemas import CommentCreate, MasterclassComment
from ..tags import service as tag_service
from ..tags.schemas import MasterclassTag
from ..users.schemas import User
from .exceptions import (
    MasterclassNotFound,
    MasterclassUserNotFound,
    MasterclassMetaNotFound,
    MasterclassMetaKeyAlreadyExist,
)
from .models import (
    masterclass_table,
    masterclass_user_table,
    masterclass_comment_table,
    masterclass_tag_table,
    masterclass_meta_table,
)
from .schemas import (
    Masterclass,
    MasterclassCreate,
    MasterclassUser,
    MasterclassUserCreate,
    MasterclassMeta,
    MasterclassMetaCreate,
)


def _parse_row(row: sa.Row):
    return Masterclass(**row._asdict())


def _parse_row_masterclass_user(row: sa.Row):  # type: ignore
    return MasterclassUser(**row._asdict())


def _parse_meta_row(row: sa.Row):
    return MasterclassMeta(**row._asdict())


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


def create_masterclass_tags(conn: Connection, masterclass: Masterclass) -> None:
    """
    Create tags for a masterclass.

    Args:
        masterclass (MasterclassCreate): MasterclassCreate object.
        result (sa.Row): Result of masterclass creation.
    """
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
            masterclass.id,
        )


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

    masterclass = _parse_row(result)
    create_masterclass_tags(conn, masterclass)

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

    tag_service.delete_tags_by_object_id(
        conn, masterclass_id, masterclass_table, masterclass_tag_table
    )

    masterclass = _parse_row(result)
    create_masterclass_tags(conn, masterclass)

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

    tag_service.delete_tags_by_object_id(
        conn, masterclass_id, masterclass_table, masterclass_tag_table
    )
    comment_service.delete_comments_by_object_id(
        conn, masterclass_id, masterclass_table, masterclass_comment_table
    )
    db_service.delete_object(conn, masterclass_table, masterclass_id)


def remove_masterclass_foreign_key(
    conn: Connection,
    masterclass_ids: List[UUID],
    foreign_key: str,
) -> None:
    """
    Remove a foreign key from multiple masterclasses.

    Args:
        masterclass_ids (List[UUID]): A list of UUIDs for the masterclasses.
        foreign_id (UUID): The foreign id to remove.
        foreign_key (str): The foreign key to remove.

    Raises:
        MasterclassNotFound: If the masterclass does not exist.
    """
    for masterclass_id in masterclass_ids:
        check = conn.execute(
            sa.select(masterclass_table).where(masterclass_table.c.id == masterclass_id)
        ).first()
        if check is None:
            raise MasterclassNotFound

        conn.execute(
            sa.update(masterclass_table)
            .where(masterclass_table.c.id == masterclass_id)
            .values({foreign_key: None})
        )


# ---------------------------------------------------------------------------------------------------- #


def create_masterclass_comment(
    conn: Connection, comment: CommentCreate, masterclass_id: UUID, user: User
):
    """
    Create a comment and link it to a masterclass.

    Args:
        comment (CommentCreate): CommentCreate object.
        masterclass_id (UUID): Id of masterclass.
        user (User): The user creating the comment.

    """
    comment_service.create_comment_and_link_table(
        conn,
        comment,
        masterclass_comment_table,
        MasterclassComment,
        masterclass_id,
        user,
    )


# ---------------------------------------------------------------------------------------------------- #


def get_masterclass_meta_by_id(conn: Connection, meta_id: int) -> MasterclassMeta:
    """
    Get a masterclass meta by the given id.

    Args:
        meta_id (int): The id of the masterclass meta.

    Raises:
        MasterclassMetaNotFound: If the masterclass meta does not exist.

    Returns:
        MasterclassMeta: The MasterclassMeta object.
    """
    result = conn.execute(
        sa.select(masterclass_meta_table).where(masterclass_meta_table.c.id == meta_id)
    ).first()
    if result is None:
        raise MasterclassMetaNotFound

    return _parse_meta_row(result)


def get_masterclass_meta_by_masterclass_id(
    conn: Connection, masterclass_id: UUID
) -> list[MasterclassMeta]:
    """
    Get all meta entries for a masterclass.

    Args:
        masterclass_id (UUID): The id of the masterclass.

    Returns:
        list[MasterclassMeta]: List of MasterclassMeta objects.
    """
    result = conn.execute(
        sa.select(masterclass_meta_table).where(
            masterclass_meta_table.c.masterclass_id == masterclass_id
        )
    ).fetchall()

    return [_parse_meta_row(row) for row in result]


def create_masterclass_meta(
    conn: Connection,
    meta: MasterclassMetaCreate,
) -> MasterclassMeta:
    """
    Create a masterclass meta.

    Args:
        meta (MasterclassMetaCreate): MasterclassMetaCreate object.

    Raises:
        MasterclassMetaKeyAlreadyExist: If the masterclass meta key already exists.

    Returns:
        MasterclassMeta: The created MasterclassMeta object.
    """
    check = conn.execute(
        sa.select(masterclass_meta_table).where(
            masterclass_meta_table.c.meta_key == meta.meta_key,
        )
    ).first()
    if check is not None:
        raise MasterclassMetaKeyAlreadyExist

    result = db_service.create_object(conn, masterclass_meta_table, meta.dict())

    return _parse_meta_row(result)


def update_masterclass_meta(
    conn: Connection,
    meta_id: int,
    meta: MasterclassMetaCreate,
) -> MasterclassMeta:
    """
    Update a meta entry.

    Args:
        meta_id (int): The id of the meta entity.
        meta (MasterclassMetaCreate): MasterclassMetaCreate object.

    Raises:
        MasterclassMetaNotFound: If the masterclass meta does not exist.

    Returns:
        MasterclassMeta: The updated MasterclassMeta object.
    """
    check = conn.execute(
        sa.select(masterclass_meta_table).where(masterclass_meta_table.c.id == meta_id)
    ).first()
    if check is None:
        raise MasterclassMetaNotFound

    result = db_service.update_object(
        conn, masterclass_meta_table, meta_id, meta.dict()
    )

    return _parse_meta_row(result)


def delete_masterclass_meta(conn: Connection, meta_id: int) -> None:
    """
    Delete a meta entry.

    Args:
        meta_id (int): The id of the meta entity.

    Raises:
        MasterclassMetaNotFound: If the masterclass meta does not exist.
    """
    check = conn.execute(
        sa.select(masterclass_meta_table).where(masterclass_meta_table.c.id == meta_id)
    ).first()
    if check is None:
        raise MasterclassMetaNotFound

    db_service.delete_object(conn, masterclass_meta_table, meta_id)


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
