from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.engine import Connection

from src.database import db_srv
from .schemas import Comment, CommentCreate
from .models import comment_table


def _parse_row(row: sa.Row):
    return Comment(**row._asdict())


def create_comment(conn: Connection, comment: CommentCreate, user_id: UUID) -> Comment:
    created_comment = db_srv.create_object(conn, comment_table, comment.dict(), user_id=user_id)
    return _parse_row(created_comment)