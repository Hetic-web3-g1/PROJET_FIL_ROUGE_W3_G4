from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File

from . import exceptions as partition_exceptions
from . import service as partition_service
from .schemas import PartitionCreate
from ..authentification.dependencies import CustomSecurity
from ..users.schemas import User
from ...database.db_engine import engine

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
    file: UploadFile = File(...),
    public: bool = True,
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        partition_service.create_partition(conn, user, public, file)


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
