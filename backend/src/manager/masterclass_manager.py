from sqlalchemy.engine import Connection
from sqlalchemy import select
from typing import Union, Generator
from uuid import uuid4

from database import db_srv
from schema.masterclass import Masterclass, MasterclassCreate, MasterclassUpdate
from database.tables.masterclass import masterclass_table

def get_all_masterclass(conn: Connection) -> Generator[Masterclass, None, None]:
    result = conn.execute(select(masterclass_table))
    if result is None:
        return
    else:
        for masterclass_row in result:
            masterclass_dict = masterclass_row._asdict()
            yield Masterclass(**masterclass_dict)

def get_masterclass_by_id(conn: Connection, masterclass_id: str) -> Union[Masterclass, None]:
    result = conn.execute(select(masterclass_table).where(masterclass_table.c.id == masterclass_id))
    masterclass_row = result.fetchone()
    if masterclass_row is None:
        return None
    else:
        masterclass_dict = masterclass_row._asdict()
        return Masterclass(**masterclass_dict)

def create_masterclass(conn: Connection, masterclass: MasterclassCreate):
    try:
        result = db_srv.create_object(conn, 'masterclass', masterclass, object_id=uuid4())
        return {"status": "success", "message": "Masterclass created successfully", "value": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def update_masterclass(conn: Connection, masterclass_id: str, masterclass: MasterclassUpdate):
    try:
        filtered_masterclass = {k: v for k, v in masterclass.dict().items() if v is not None}
        result = db_srv.update_object(conn, 'masterclass', masterclass_id, filtered_masterclass)
        return {"status": "success", "message": "Masterclass updated successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
def delete_masterclass(conn: Connection, masterclass_id: str):
    try:
        result = db_srv.delete_object(conn, 'masterclass', masterclass_id)
        return {"status": "success", "message": "Masterclass deleted successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}