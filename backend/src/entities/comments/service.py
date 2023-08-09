import sqlalchemy as sa
from sqlalchemy.engine import Connection
from src.database import service as db_service

from ..users.schemas import User
from .exceptions import CommentNotFound
from .models import comment_table
from .schemas import Comment, CommentCreate


def _parse_row(row: sa.Row):
    return Comment(**row._asdict())


def get_comment_by_id(conn: Connection, comment_id: int) -> Comment:
    """
    Get comment by id.

    Args:
        comment_id (int): Id of comment.

    Raises:
        CommentNotFound: If the comment is not found.

    Returns:
        Comment: Comment object.
    """
    result = conn.execute(
        sa.select(comment_table).where(comment_table.c.id == comment_id)
    ).first()
    if result is None:
        raise CommentNotFound

    return _parse_row(result)


def get_comment_by_object_id(
    conn: Connection, object_id, object_table, object_comment_table
):
    """
    Get comment by object.

    Args:
        object_id (int): Id of object.
        object_table (Table): Table of object.
        object_tag_table (Table): Table linking tag to object.

    Returns:
        List[Comment]: List of Comment objects.
    """
    query = (
        sa.select(comment_table)
        .select_from(
            comment_table.join(
                object_comment_table,
                comment_table.c.id == object_comment_table.c.comment_id,
            ).join(object_table, object_table.c.id == object_comment_table.c.entity_id)
        )
        .where(object_table.c.id == object_id)
    )

    result = conn.execute(query).fetchall()
    return [_parse_row(row) for row in result]


def create_comment(conn: Connection, comment: CommentCreate, user: User) -> Comment:
    """
    Create a comment.

    Args:
        comment (CommentCreate): CommentCreate object.
        user_id (UUID): The id of the user creating the comment.

    Returns:
        Comment: The created Comment object.
    """
    created_comment = db_service.create_object(
        conn, comment_table, comment.dict(), user_id=user.id
    )
    return _parse_row(created_comment)


def create_link_table(conn: Connection, entity, entity_table):
    """
    Link Comment to entity.

    Args:
        entity (Entity): Entity object.
        entity_table (Table): Table of entity.

    Returns:
        Entity: The created Entity object.
    """
    result = db_service.create_object(conn, entity_table, entity.dict())
    return result


def create_comment_and_link_table(
    conn: Connection,
    comment,
    object,
    object_comment_table,
    object_id,
    user,
):
    """
    Create a comment and link it to an object.

    Args:
        content (str): Comment object.
        object (str): Object.
        object_tag_table (Table): Table of object_comment.
        object_id (int): Id of object.
    """
    comment = CommentCreate(content=comment.content)

    created_comment = create_comment(conn, comment, user)

    entity_comment = object_comment_table(
        entity_id=object_id, comment_id=created_comment.id
    )
    create_link_table(conn, entity_comment, object)


def update_comment(
    conn: Connection, comment_id: int, comment: CommentCreate, user: User
) -> Comment:
    """
    Update a comment.

    Args:
        comment_id (int): Id of comment.
        comment (CommentCreate): CommentCreate object.
        user_id (UUID): The id of the user updating the comment.

    Raises:
        CommentNotFound: If the comment is not found.

    Returns:
        Comment: The updated Comment object.
    """
    check = conn.execute(
        sa.select(comment_table).where(comment_table.c.id == comment_id)
    ).first()
    if check is None:
        raise CommentNotFound

    result = db_service.update_object(
        conn, comment_table, comment_id, comment.dict(), user_id=user.id
    )

    return _parse_row(result)


def delete_comment(conn: Connection, comment_id: int) -> None:
    """
    Delete comment.

    Args:
        comment_id (int): Id of comment.

    Raises:
        CommentNotFound: If the comment is not found.
    """
    check = conn.execute(
        sa.select(comment_table).where(comment_table.c.id == comment_id)
    ).first()
    if check is None:
        raise CommentNotFound

    db_service.delete_object(conn, comment_table, comment_id)


def delete_comments_by_object_id(
    conn: Connection, object_id, object_table, object_comment_table
):
    """
    Delete comments by object id.

    Args:
        object_id (int): Id of object.
        object_table (Table): Table of object.
        object_tag_table (Table): Table linking tag to object.
    """
    result = get_comment_by_object_id(
        conn, object_id, object_table, object_comment_table
    )
    comment_ids = [comment.id for comment in result]
    db_service.delete_objects(conn, comment_table, comment_ids)
