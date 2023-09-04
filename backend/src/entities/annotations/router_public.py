from uuid import UUID

from fastapi import APIRouter

from src.database.db_engine import engine

from . import service as annotation_service

router = APIRouter(
    prefix="/annotations",
    tags=["annotations"],
)


@router.get("/annotation/partition/{partition_id}")
def get_annotations_by_partition_id(partition_id: UUID):
    with engine.begin() as conn:
        annotations = annotation_service.get_annotations_by_partition_id(
            conn, partition_id
        )
        return annotations
