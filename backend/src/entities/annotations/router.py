from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.database.db_engine import engine

from ..authentification.dependencies import CustomSecurity
from ..users.schemas import User
from . import exceptions as annotation_exceptions
from . import service as annotation_service
from .schemas import AnnotationCreate

router = APIRouter(
    prefix="/annotations",
    tags=["annotations"],
)


@router.get("/annotation/{partition_id}")
def get_annotations_by_partition_id(
    partition_id: UUID,
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        annotations = annotation_service.get_annotations_by_partition_id(
            conn, partition_id
        )
        return annotations


@router.post("/annotation")
def create_annotation(
    annotation: AnnotationCreate,
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        annotation_service.create_annotation(conn, annotation, user)


@router.put("/annotation/{annotation_id}")
def update_annotation(
    annotation_id: int,
    annotation: AnnotationCreate,
    user: User = Depends(CustomSecurity()),
):
    try:
        with engine.begin() as conn:
            annotation_service.update_annotation(conn, annotation_id, annotation, user)

    except annotation_exceptions.AnnotationNotFound:
        raise HTTPException(
            status_code=404,
            detail="Comment not found",
        )


@router.delete("/annotation/{annotation_id}")
def delete_annotation(
    annotation_id: int,
    user: User = Depends(CustomSecurity()),
):
    try:
        with engine.begin() as conn:
            annotation_service.delete_annotation(conn, annotation_id)

    except annotation_exceptions.AnnotationNotFound:
        raise HTTPException(
            status_code=404,
            detail="Comment not found",
        )
