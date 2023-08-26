from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.engine import Connection

from src.database import service as db_service

from ..comments import service as comment_service
from ..comments.schemas import CommentCreate, BiographyComment
from ..tags import service as tag_service
from ..tags.schemas import BiographyTag
from ..users.schemas import User
from .exceptions import (
    BiographyNotFound,
    BiographyTranslationNotFound,
    BiographyTranslationAlreadyExist,
    BiographyMetaNotFound,
    BiographyMetaKeyAlreadyExist,
)
from .models import (
    biography_table,
    biography_translation_table,
    biography_tag_table,
    biography_comment_table,
    biography_meta_table,
)
from .schemas import (
    Biography,
    BiographyCreate,
    BiographyTranslationCreate,
    BiographyTranslation,
    BiographyMeta,
    BiographyMetaCreate,
)

def _parse_row(row: sa.Row):
    return Biography(**row._asdict())


def _parse_translation_row(row: sa.Row):
    return BiographyTranslation(**row._asdict())
  
  
def _parse_meta_row(row: sa.Row):
    return BiographyMeta(**row._asdict())
  

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


def create_biography_tag(conn: Connection, biography: Biography) -> None:
    """
    Create tags for a biography.

    Args:
        biography (BiographyCreate): BiographyCreate object.
        result (sa.Row): Result of masterclass creation.

    Returns:
        BiographyTag: The created BiographyTag object.
    """
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
            biography.id,
        )


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

    biography = _parse_row(result)
    create_biography_tag(conn, biography)

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

    tag_service.delete_tags_by_object_id(
        conn, biography_id, biography_table, biography_tag_table
    )

    biography = _parse_row(result)
    create_biography_tag(conn, biography)

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

    tag_service.delete_tags_by_object_id(
        conn, biography_id, biography_table, biography_tag_table
    )
    comment_service.delete_comments_by_object_id(
        conn, biography_id, biography_table, biography_comment_table
    )
    db_service.delete_object(conn, biography_table, biography_id)


# ---------------------------------------------------------------------------------------------------- #


def get_biography_translation_by_id(
    conn: Connection, biography_translation_id: int
) -> BiographyTranslation:
    """
    Get a biography translation by the given id.

    Args:
        biography_translation_id (int): The id of the biography translation.

    Raises:
        BiographyTranslationNotFound: If the biography translation does not exist.

    Returns: The BiographyTranslation object.
    """
    result = conn.execute(
        sa.select(biography_translation_table).where(
            biography_translation_table.c.id == biography_translation_id
        )
    ).first()
    if result is None:
        raise BiographyTranslationNotFound

    return _parse_translation_row(result)


def get_biography_translation_by_biography(
    conn: Connection, biography_id: UUID
) -> BiographyTranslation | None:
    """
    Get a biography translation by the given biography id.

    Args:
        biography_id (UUID): The id of the biography.

    Returns:
        The BiographyTranslation object.
    """
    query = sa.select(biography_translation_table).where(
        biography_translation_table.c.biography_id == biography_id
    )

    result = conn.execute(query).first()
    if result is None:
        return None

    return _parse_translation_row(result)


def create_biography_translation(
    conn: Connection, biography_translation: BiographyTranslationCreate, user: User
) -> BiographyTranslation:
    """
    Create a biography translation.

    Args:
        biography_translation (BiographyTranslationCreate): BiographyTranslationCreate object.
        user (User): The user creating the biography translation.

    Raises:
        BiographyTranslationAlreadyExist: If the biography translation already exists.

    Returns:
        BiographyTranslation: The created BiographyTranslation object.
    """
    check = get_biography_translation_by_biography(
        conn, biography_translation.biography_id
    )
    if check is not None:
        raise BiographyTranslationAlreadyExist

    result = db_service.create_object(
        conn,
        biography_translation_table,
        biography_translation.dict(),
        user_id=user.id,
    )

    return _parse_translation_row(result)


def update_biography_translation(
    conn: Connection,
    biography_translation_id: int,
    biography_translation: BiographyTranslationCreate,
    user: User,
) -> BiographyTranslation:
    """
    Update a biography translation.

    Args:
        biography_translation_id (int): The id of the biography translation.
        biography_translation (BiographyTranslationCreate): The BiographyTranslationCreate object.
        user (User): The user updating the biography translation.

    Raises:
        BiographyTranslationNotFound: If the biography translation does not exist.

    Returns:
        BiographyTranslation: The updated BiographyTranslation object.
    """
    check = conn.execute(
        sa.select(biography_translation_table).where(
            biography_translation_table.c.id == biography_translation_id
        )
    ).first()
    if check is None:
        raise BiographyTranslationNotFound

    result = db_service.update_object(
        conn,
        biography_translation_table,
        biography_translation_id,
        biography_translation.dict(),
        user_id=user.id,
    )

    return _parse_translation_row(result)


def delete_biography_translation(
    conn: Connection, biography_translation_id: int
) -> None:
    """
    Delete a biography translation.

    Args:
        biography_translation_id (int): The id of the biography translation.

    Raises:
        BiographyTranslationNotFound: If the biography translation does not exist.
    """
    check = conn.execute(
        sa.select(biography_translation_table).where(
            biography_translation_table.c.id == biography_translation_id
        )
    ).first()
    if check is None:
        raise BiographyTranslationNotFound

    db_service.delete_object(
        conn, biography_translation_table, biography_translation_id
    )


# ---------------------------------------------------------------------------------------------------- #


def create_biography_comment(
    conn: Connection, comment: CommentCreate, biography_id: UUID, user: User
):
    """
    Create a comment and link it to a biography.

    Args:
        comment (CommentCreate): CommentCreate object.
        biography_id (UUID): Id of biography.
        user (User): The user creating the comment.
    """
    comment_service.create_comment_and_link_table(
        conn,
        comment,
        biography_comment_table,
        BiographyComment,
        biography_id,
        user,
    )


# ---------------------------------------------------------------------------------------------------- #


def get_biography_meta_by_id(conn: Connection, meta_id: int) -> BiographyMeta:
    """
    Get a meta entry by the given id.

    Args:
        meta_id (int): The id of the meta entry.

    Raises:
        BiographyMetaNotFound: If the meta entry does not exist.

    Returns:
        BiographyMeta: The BiographyMeta object.
    """
    result = conn.execute(
        sa.select(biography_meta_table).where(biography_meta_table.c.id == meta_id)
    ).first()
    if result is None:
        raise BiographyMetaNotFound

    return _parse_meta_row(result)


def get_biography_meta_by_biography_id(
    conn: Connection, biography_id: UUID
) -> list[BiographyMeta]:
    """
    Get all meta entries for a biography.

    Args:
        biography_id (UUID): The id of the biography.

    Returns:
        list[BiographyMeta]: List of BiographyMeta objects.
    """
    result = conn.execute(
        sa.select(biography_meta_table).where(
            biography_meta_table.c.biography_id == biography_id
        )
    ).fetchall()

    return [_parse_meta_row(row) for row in result]


def create_biography_meta(conn: Connection, meta: BiographyMetaCreate) -> BiographyMeta:
    """
    Create a meta entry for a biography.

    Args:
        meta (BiographyMetaCreate): BiographyMetaCreate object.

    Raises:
        BiographyMetaKeyAlreadyExist: If the meta entry already exists.

    Returns:
        BiographyMeta: The created BiographyMeta object.
    """
    check = conn.execute(
        sa.select(biography_meta_table).where(
            biography_meta_table.c.meta_key == meta.meta_key,
        )
    ).first()
    if check is not None:
        raise BiographyMetaKeyAlreadyExist

    result = db_service.create_object(
        conn,
        biography_meta_table,
        meta.dict(),
    )

    return _parse_meta_row(result)


def update_biography_meta(
    conn: Connection, meta_id: int, meta: BiographyMetaCreate
) -> BiographyMeta:
    """
    Update a meta entry.

    Args:
        meta_id (int): The id of the meta entry.
        meta (BiographyMetaCreate): The BiographyMetaCreate object.

    Raises:
        BiographyMetaNotFound: If the meta entry does not exist.

    Returns:
        BiographyMeta: The updated BiographyMeta object.
    """
    check = conn.execute(
        sa.select(biography_meta_table).where(biography_meta_table.c.id == meta_id)
    ).first()
    if check is None:
        raise BiographyMetaNotFound

    result = db_service.update_object(
        conn,
        biography_meta_table,
        meta_id,
        meta.dict(),
    )

    return _parse_meta_row(result)


def delete_biography_meta(conn: Connection, meta_id: int) -> None:
    """
    Delete a meta entry.

    Args:
        meta_id (int): The id of the meta entry.

    Raises:
        BiographyMetaNotFound: If the meta entry does not exist.
    """
    check = conn.execute(
        sa.select(biography_meta_table).where(biography_meta_table.c.id == meta_id)
    ).first()
    if check is None:
        raise BiographyMetaNotFound

    db_service.delete_object(conn, biography_meta_table, meta_id)
