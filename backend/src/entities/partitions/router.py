from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID


from .schemas import Partition, PartitionCreate
from src.users.schemas import User
from . import exceptions as partition_exceptions
from . import service as partition_service
from src.database.db_engine import engine
from src.authentification import service as auth_service
from src.authentification.dependencies import CustomSecurity

router = APIRouter(
    prefix="/partitions",
    tags=["Partitions"],
)


# Get all partitions
@router.get("")
def get_all_partitions(
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        response = partition_service.get_all_partitions(conn)
        return response


# Get partition by id
@router.get("/{partition_id}")
def get_partition_by_id(
    partition_id: UUID,
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        response = partition_service.get_partition_by_id(conn, partition_id)
        return response
    

# Create partition
@router.post("/partition")
def create_partition(
    new_partition: PartitionCreate, User: User = Depends(CustomSecurity())
):
    with engine.begin() as conn:
        new_partition = partition_service.create_partition(conn, new_partition)