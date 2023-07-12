from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.engine import Connection

from src.database import service as db_service
from .schemas import Comment, CommentCreate
from .models import comment_table


def _parse_row(row: sa.Row):
    return Comment(**row._asdict())


def create_comment(conn: Connection, comment: CommentCreate, user_id: UUID) -> Comment:
    created_comment = db_service.create_object(conn, comment_table, comment.dict(), user_id=user_id)
    return _parse_row(created_comment)