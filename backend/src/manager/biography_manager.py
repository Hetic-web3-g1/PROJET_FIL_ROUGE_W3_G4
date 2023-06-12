from sqlalchemy.engine import Connection
from sqlalchemy import select
from typing import Union, Generator
from uuid import uuid4

from src.database import db_srv
from src.schema.biography import Biography, BiographyCreate, BiographyUpdate
from src.database.tables.biography import biography_table

def get_all_biography(conn: Connection) -> Generator[Biography, None, None]:
    result = conn.execute(select(biography_table))
    if result is None:
        return
    else:
        for biography_row in result:
            biography_dict = biography_row._asdict()
            yield Biography(**biography_dict)

def get_biography_by_id(conn: Connection, biography_id: str) -> Union[Biography, None]:
    result = conn.execute(select(biography_table).where(biography_table.c.id == biography_id))
    biography_row = result.fetchone()
    if biography_row is None:
        return None
    else:
        biography_dict = biography_row._asdict()
        return Biography(**biography_dict)

def create_biography(conn: Connection, biography: BiographyCreate):
    try:
        result = db_srv.create_object(conn, 'biography', biography, object_id=uuid4())
        return {"status": "success", "message": "Biography created successfully", "value": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def update_biography(conn: Connection, biography_id: str, biography: BiographyUpdate):
    try:
        filtered_biography = {k: v for k, v in biography.dict().items() if v is not None}
        result = db_srv.update_object(conn, 'biography', biography_id, filtered_biography)
        return {"status": "success", "message": "Biography updated successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def delete_biography(conn: Connection, biography_id: str):
    try:
        result = db_srv.delete_object(conn, 'biography', biography_id)
        return {"status": "success", "message": "Biography deleted successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}