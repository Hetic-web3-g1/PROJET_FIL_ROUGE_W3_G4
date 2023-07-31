import sqlalchemy as sa
from sqlalchemy.engine import Connection

from .models import comment_table
from .schemas import Comment, CommentCreate
from ..users.schemas import User
from ...database import service as db_service


def _parse_row(row: sa.Row):  # type: ignore
    return Comment(**row._asdict())


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
