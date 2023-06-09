from sqlalchemy.engine import Connection
from sqlalchemy import select
from typing import Union, Generator
from uuid import uuid4

from src.database import db_srv
from src.schema.academy import Academy, AcademyCreate, AcademyUpdate
from src.database.tables.academy import academy_table

def get_all_academy(conn: Connection) -> Generator[Academy, None, None]:
    result = conn.execute(select(academy_table))
    if result is None:
        return
    else:
        for academy_row in result:
            academy_dict = academy_row._asdict()
            yield Academy(**academy_dict)

def get_academy_by_id(conn: Connection, academy_id: str) -> Union[Academy, None]:
    result = conn.execute(select(academy_table).where(academy_table.c.id == academy_id))
    academy_row = result.fetchone()
    if academy_row is None:
        return None
    else:
        academy_dict = academy_row._asdict()
        return Academy(**academy_dict)

def create_academy(conn: Connection, academy: AcademyCreate):
    try:
        result = db_srv.create_object(conn, 'academy', academy, object_id=uuid4())
        return {"status": "success", "message": "Academy created successfully", "value": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def update_academy(conn: Connection, academy_id: str, academy: AcademyUpdate):
    try:
        filtered_academy = {k: v for k, v in academy.dict().items() if v is not None}
        result = db_srv.update_object(conn, 'academy', academy_id, filtered_academy)
        return {"status": "success", "message": "Academy updated successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def delete_academy(conn: Connection, academy_id: str):
    try:
        result = db_srv.delete_object(conn, 'academy', academy_id)
        return {"status": "success", "message": "Academy deleted successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}