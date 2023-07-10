from sqlalchemy.engine import Connection
from sqlalchemy import select
from typing import Union, Generator

from src.database import db_srv
from src.schema.annotation import Annotation, AnnotationCreate
from src.database.tables.annotation import annotation_table

def get_all_annotation(conn: Connection) -> Generator[Annotation, None, None]:
    result = conn.execute(select(annotation_table))
    if result is None:
        return
    else:
        for annotation_row in result:
            annotation_dict = annotation_row._asdict()
            yield Annotation(**annotation_dict)

def get_annotation_by_id(conn: Connection, annotation_id: str) -> Union[Annotation, None]:
    result = conn.execute(select(annotation_table).where(annotation_table.c.id == annotation_id))
    annotation_row = result.fetchone()
    if annotation_row is None:
        return None
    else:
        annotation_dict = annotation_row._asdict()
        return Annotation(**annotation_dict)

def create_annotation(conn: Connection, annotation: AnnotationCreate):
    try:
        result = db_srv.create_object(conn, annotation_table, annotation)
        return {"status": "success", "message": "Annotation created successfully", "value": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def update_annotation(conn: Connection, annotation_id: str, annotation: Annotation):
    try:
        # Filter out None values from the annotation object
        filtered_annotation = {k: v for k, v in annotation.dict().items() if v is not None}
        result = db_srv.update_object(conn, 'annotation', annotation_id, filtered_annotation)
        return {"status": "success", "message": "Annotation updated successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def delete_annotation(conn: Connection, annotation_id: str):
    try:
        result = db_srv.delete_object(conn, 'annotation', annotation_id)
        return {"status": "success", "message": "Annotation deleted successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}