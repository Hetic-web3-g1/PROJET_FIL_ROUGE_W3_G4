from sqlalchemy.engine import Connection
from sqlalchemy import select
from typing import Union, Generator
from uuid import uuid4

from database import db_srv
from schema.partition import Partition, PartitionCreate, PartitionUpdate
from database.tables.partition import partition_table

def get_all_partition(conn: Connection) -> Generator[Partition, None, None]:
    result = conn.execute(select(partition_table))
    if result is None:
        return
    else:
        for partition_row in result:
            partition_dict = partition_row._asdict()
            yield Partition(**partition_dict)

def get_partition_by_id(conn: Connection, partition_id: str) -> Union[Partition, None]:
    result = conn.execute(select(partition_table).where(partition_table.c.id == partition_id))
    partition_row = result.fetchone()
    if partition_row is None:
        return None
    else:
        partition_dict = partition_row._asdict()
        return Partition(**partition_dict)

def create_partition(conn: Connection, partition: PartitionCreate):
    try:
        result = db_srv.create_object(conn, 'partition', partition, object_id=uuid4())
        return {"status": "success", "message": "Partition created successfully", "value": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def update_partition(conn: Connection, partition_id: str, partition: PartitionUpdate):
    try:
        filtered_partition = {k: v for k, v in partition.dict().items() if v is not None}
        result = db_srv.update_object(conn, 'partition', partition_id, filtered_partition)
        return {"status": "success", "message": "Partition updated successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def delete_partition(conn: Connection, partition_id: str):
    try:
        result = db_srv.delete_object(conn, 'partition', partition_id)
        return {"status": "success", "message": "Partition deleted successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}