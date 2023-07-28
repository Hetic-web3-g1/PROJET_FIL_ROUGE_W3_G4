from uuid import UUID

from typing import Callable, Optional, TypeVar, Type, Union, List, Any

import sqlalchemy as sa
from fastapi.encoders import jsonable_encoder
from pydantic import parse_obj_as
from pydantic.main import BaseModel
from sqlalchemy import Table
from sqlalchemy.engine import Connection

from .db_engine import metadata


T = TypeVar("T")


def parse_row(row, model: Type[T]) -> T:
    if "data" in row:
        return parse_obj_as(model, {**row.data, **row})
    else:
        return parse_obj_as(model, row)


def get_table_object(table_name: str):
    return metadata.tables[table_name]


def create_object(
    conn: Connection,
    table: Table,
    object_data: Any,
    object_id: Optional[Any] = None,
    user_id: Optional[UUID] = None,
    parser: Optional[Callable[[Any], T]] = None,
) -> T:
    if isinstance(object_data, BaseModel):
        object_data = object_data.dict()

    values = {}
    for column in table.columns:
        if column.name != "data" and column.name in object_data:
            values[column.name] = object_data.pop(column.name)

    if "data" in table.columns:
        values["data"] = jsonable_encoder(object_data)

    if object_id is not None:
        values["id"] = object_id

    if user_id is not None:
        values["created_by"] = user_id

    stmt = sa.insert(table).values(**values).returning(table)
    result = conn.execute(stmt).first()

    if parser is not None:
        return parser(result)
    else:
        return result


def update_object(
    conn: Connection,
    table: Table,
    object_id: Union[str, UUID, int],
    object_data: Any,
    user_id: Optional[UUID] = None,
    parser: Optional[Callable[[Any], T]] = None,
    id_key: str = "id",
) -> T:
    values = {}
    for column in table.columns:
        if column.name != "data" and column.name in object_data:
            values[column.name] = object_data.pop(column.name)

    if "data" in table.columns:
        values["data"] = jsonable_encoder(object_data)

    if user_id is not None:
        values["updated_by"] = user_id

    stmt = (
        sa.update(table)
        .values(**values)
        .where(table.c[id_key] == object_id)
        .returning(table)
    )

    result = conn.execute(stmt).first()

    if parser is not None:
        return parser(result)
    else:
        return result


def delete_object(
    conn: Connection,
    table: Table,
    object_id: Union[str, UUID, int],
    id_key: str = "id",
):
    # Check if object exists
    stmt = sa.select(table).where(table.c[id_key] == object_id)
    result = conn.execute(stmt).fetchone()
    if result is None:
        # Return a custom error response indicating that the object does not exist
        raise ValueError(f"Object with ID {object_id} does not exist")

    result = conn.execute(table.delete().where(table.c[id_key] == object_id))
    return result.rowcount


def delete_objects(
    conn: Connection,
    table: Table,
    object_ids: List[Union[str, UUID, int]],
):
    if not object_ids:
        # If the list of object_ids is empty, return immediately
        return 0

    # Check if objects exist
    stmt = sa.select(table).where(table.c.id.in_(object_ids))
    results = conn.execute(stmt).fetchall()
    existing_ids = {str(row[0]) for row in results}

    # Find IDs that don't exist in the table
    non_existing_ids = [
        str(obj_id) for obj_id in object_ids if str(obj_id) not in existing_ids
    ]

    if non_existing_ids:
        # Return a custom error response indicating the non-existing objects
        raise ValueError(f"Objects with IDs {non_existing_ids} do not exist")

    # Perform the deletion
    delete_stmt = table.delete().where(table.c.id.in_(object_ids))
    result = conn.execute(delete_stmt)

    return result.rowcount


def delete_object_column(
    conn: Connection, table: Table, object_key: str, object_id: Any
):
    conn.execute(table.delete(table.c[object_key] == object_id))


def clean_table(conn: Connection, table: Table):
    conn.execute(table.delete())
