from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.engine import Connection

from src.database import service as db_service

from ..users.schemas import User
from ..partitions.models import partition_table, partition_annotation_table
from .models import annotation_table
from .exceptions import AnnotationNotFound
from .schemas import Annotation, AnnotationCreate, PartitionAnnotation


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
    query = (
        sa.select(annotation_table)
        .select_from(
            annotation_table.join(
                partition_annotation_table,
                annotation_table.c.id == partition_annotation_table.c.annotation_id,
            ).join(
                partition_table,
                partition_table.c.id == partition_annotation_table.c.partition_id,
            )
        )
        .where(partition_table.c.id == partition_id)
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


def create_link_table(conn: Connection, link_table):
    """
    Link Annotation to Partition.

    Args:
        link_table (Table): Table of link.

    Returns:
        The created link table.
    """
    result = db_service.create_object(
        conn, partition_annotation_table, link_table.dict()
    )
    return result


def create_annotation_and_link_table(
    conn: Connection,
    annotation: AnnotationCreate,
    partition_id,
    user,
):
    """
    Create a annotation and link it to a partition.

    Args:
        annotation (AnnotationCreate): AnnotationCreate object.
        partition_id (int): Id of partition.
        user (User): The user creating the annotation.
    """
    created_annotation = create_annotation(conn, annotation, user)

    entity_annotation = PartitionAnnotation(
        partition_id=partition_id, annotation_id=created_annotation.id
    )
    create_link_table(conn, entity_annotation)


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


def delete_annotations_by_partition_id(conn: Connection, partition_id: UUID):
    """
    Delete annotations by partition id.

    Args:
        partition_id (int): Id of partition.
    """
    result = get_annotations_by_partition_id(conn, partition_id)
    annotations_ids = [annotation.id for annotation in result]
    db_service.delete_objects(conn, annotation_table, annotations_ids)
