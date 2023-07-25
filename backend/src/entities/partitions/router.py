from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID

from .schemas import PartitionCreate
from ..users.schemas import User
from ..tags.schemas import TagCreate, PartitionTag
from src.entities.partitions.models import partition_table, partition_tag_table
from . import exceptions as partition_exceptions
from . import service as partition_service
from ..tags import service as tag_service
from src.database.db_engine import engine
from ..authentification.dependencies import CustomSecurity
from src.utils.sanitize import sanitize_string

router = APIRouter(
    prefix="/partitions",
    tags=["Partitions"],
)


@router.get("")
def get_all_partitions(
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        partitions = partition_service.get_all_partitions(conn)
        return list(partitions)


@router.get("/partition/{partition_id}")
def get_partition_by_id(
    partition_id: UUID,
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        partition = partition_service.get_partition_by_id(conn, partition_id)
        return partition


@router.post("/partition")
def create_partition(
    partition: PartitionCreate, user: User = Depends(CustomSecurity())
):
    with engine.begin() as conn:
        created_partition = partition_service.create_partition(conn, partition, user)
        tag = TagCreate(
            content=sanitize_string(partition.file_name), tag_type=str(partition_table)
        )
        created_tag = tag_service.create_tag(conn, tag, user)
        partition_tag = PartitionTag(
            partition_id=created_partition.id,
            tag_id=created_tag.id,
        )
        tag_service.create_link_table(conn, partition_tag, partition_tag_table, user)


@router.put("/partition/{partition_id}")
def update_partition(
    partition_id: UUID,
    partition: PartitionCreate,
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        partition_service.update_partition(conn, partition_id, partition, user)


@router.delete("/partition/{partition_id}")
def delete_partition(partition_id: UUID, user: User = Depends(CustomSecurity())):
    try:
        with engine.begin() as conn:
            partition_service.delete_partition(conn, partition_id)

    except partition_exceptions.PartitionNotFound:
        raise HTTPException(
            status_code=404,
            detail="Partition not found",
        )
