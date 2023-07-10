from sqlalchemy.engine import Connection
from sqlalchemy import select
from typing import Union, Generator

from src.database import db_srv
from src.comments.schemas import Comment, CommentCreate
from src.comments.models import comment_table

def get_all_comment(conn: Connection) -> Generator[Comment, None, None]:
    result = conn.execute(select(comment_table))
    if result is None:
        return
    else:
        for comment_row in result:
            comment_dict = comment_row._asdict()
            yield Comment(**comment_dict)

def get_comment_by_id(conn: Connection, comment_id: str) -> Union[Comment, None]:
    result = conn.execute(select(comment_table).where(comment_table.c.id == comment_id))
    comment_row = result.fetchone()
    if comment_row is None:
        return None
    else:
        comment_dict = comment_row._asdict()
        return Comment(**comment_dict)

# def create_comment(conn: Connection, comment: CommentCreate):
#     try:
#         result = db_srv.create_object(conn, comment_table, comment)
#         return {"status": "success", "message": "Comment created successfully", "value": result}
#     except Exception as e:
#         return {"status": "error", "message": str(e)}

def update_comment(conn: Connection, comment_id: str, comment: Comment):
    try:
        filtered_comment = {k: v for k, v in comment.dict().items() if v is not None}
        result = db_srv.update_object(conn, 'comment', comment_id, filtered_comment)
        return {"status": "success", "message": "Comment updated successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def delete_comment(conn: Connection, comment_id: str):
    try:
        result = db_srv.delete_object(conn, 'comment', comment_id)
        return {"status": "success", "message": "Comment deleted successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}