from sqlalchemy.engine import Connection
from sqlalchemy import select
from typing import Union, Generator

from src.database import db_srv
from src.schema.tag import Tag, TagCreate
from src.database.tables.tag import tag_table

def get_all_tag(conn: Connection) -> Generator[Tag, None, None]:
    result = conn.execute(select(tag_table))
    if result is None:
        return
    else:
        for tag_row in result:
            tag_dict = tag_row._asdict()
            yield Tag(**tag_dict)

def get_tag_by_id(conn: Connection, tag_id: str) -> Union[Tag, None]:
    result = conn.execute(select(tag_table).where(tag_table.c.id == tag_id))
    tag_row = result.fetchone()
    if tag_row is None:
        return None
    else:
        tag_dict = tag_row._asdict()
        return Tag(**tag_dict)

def create_tag(conn: Connection, tag: TagCreate):
    try:
        result = db_srv.create_object(conn, tag_table, tag)
        return {"status": "success", "message": "Tag created successfully", "value": "result", "value": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def update_tag(conn: Connection, tag_id: str, tag: Tag):
    try:
        filtered_tag = {k: v for k, v in tag.dict().items() if v is not None}
        result = db_srv.update_object(conn, 'tag', tag_id, filtered_tag)
        return {"status": "success", "message": "Tag updated successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def delete_tag(conn: Connection, tag_id: str):
    try:
        result = db_srv.delete_object(conn, 'tag', tag_id)
        return {"status": "success", "message": "Tag deleted successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
