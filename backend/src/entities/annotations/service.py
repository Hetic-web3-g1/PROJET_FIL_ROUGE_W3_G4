from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.engine import Connection

from src.database import service as db_service

from ..users.schemas import User
from .models import annotation_table
from .exceptions import AnnotationNotFound
from .schemas import Annotation, AnnotationCreate


def _parse_row(row: sa.Row):
    return Annotation(**row._asdict())


def get_annotation_by_id(conn: Connection, annotation_id: int) -> Annotation:
    """
    Get a annotation by the given id.

    Args:
        annotation_id (int): The id of the annotation.

    Raises:
        AnnotationNotFound: If the annotation does not exist.

    Returns:
        The Annotation object.
    """
    result = conn.execute(
        sa.select(annotation_table).where(annotation_table.c.id == annotation_id)
    ).first()
    if result is None:
        raise AnnotationNotFound

    return _parse_row(result)


def get_annotations_by_partition_id(conn: Connection, partition_id) -> list[Annotation]:
    """
    Get all annotations for a given partition id.

    Args:
        partition_id: The id of the partition.

    Returns:
        A list of Annotation objects.
    """
    query = sa.select(annotation_table).where(
        annotation_table.c.partition_id == partition_id
    )

    result = conn.execute(query).fetchall()
    return [_parse_row(result) for result in result]


def create_annotation(
    conn: Connection, annotation: AnnotationCreate, user: User
) -> Annotation:
    """
    Create a annotation.

    Args:
        annotation (Annotation): Annotation object.
        user (User): The user creating the annotation.

    Returns:
        Annotation: The created Annotation object.
    """
    created_annotation = db_service.create_object(
        conn, annotation_table, annotation.dict(), user_id=user.id
    )
    return _parse_row(created_annotation)


def update_annotation(
    conn: Connection, annotation_id: int, annotation: AnnotationCreate, user: User
):
    """
    Update a annotation.

    Args:
        annotation_id (int): Id of annotation.
        annotation (AnnotationCreate): AnnotationCreate object.
        user (User): The user updating the annotation.

    Raises:
        AnnotationNotFound: If the annotation does not exist.

    Returns:
        The updated Annotation object.
    """
    check = conn.execute(
        sa.select(annotation_table).where(annotation_table.c.id == annotation_id)
    ).first()
    if check is None:
        raise AnnotationNotFound

    result = db_service.update_object(
        conn, annotation_table, annotation_id, annotation.dict(), user_id=user.id
    )

    return _parse_row(result)


def delete_annotation(conn: Connection, annotation_id: int):
    """
    Delete a annotation.

    Args:
        annotation_id (int): Id of annotation.

    Raises:
        AnnotationNotFound: If the annotation does not exist.
    """
    check = conn.execute(
        sa.select(annotation_table).where(annotation_table.c.id == annotation_id)
    ).first()
    if check is None:
        raise AnnotationNotFound

    db_service.delete_object(conn, annotation_table, annotation_id)
