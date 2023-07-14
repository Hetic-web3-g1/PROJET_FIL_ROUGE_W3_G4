from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID


from .schemas import Partition, PartitionCreate
from ..users.schemas import User
from . import exceptions as partition_exceptions
from . import service as partition_service
from src.database.db_engine import engine
from ..authentification import service as auth_service
from ..authentification.dependencies import CustomSecurity

router = APIRouter(
    prefix="/partitions",
    tags=["Partitions"],
)


@router.get("")
def get_all_partitions(
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        response = partition_service.get_all_partitions(conn)
        return response


@router.get("/partition/{partition_id}")
def get_partition_by_id(
    partition_id: UUID,
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        response = partition_service.get_partition_by_id(conn, partition_id)
        return response
    

@router.post("/partition")
def create_partition(
    partition: PartitionCreate,
    user: User = Depends(CustomSecurity())
):
    with engine.begin() as conn:
        partition_service.create_partition(conn, partition, user)


@router.put("/partition/{partition_id}")
def update_partition(
    partition_id: UUID,
    partition: PartitionCreate,
    user: User = Depends(CustomSecurity())
):
    with engine.begin() as conn:
        partition_service.update_partition(conn, partition_id, partition, user)


@router.delete("/partition/{partition_id}")
def delete_partition(
    partition_id: UUID,
    user: User = Depends(CustomSecurity())
):
    try:
        with engine.begin() as conn:
            partition_service.delete_partition(conn, partition_id)

    except partition_exceptions.PartitionNotFound:
        raise HTTPException(
            status_code=404,
            detail="Partition not found",
        )