from fastapi import APIRouter
from typing import List, Union

from src.database.db_engine import engine
from src.schema.response import ResponseModel
from src.utils.route_function import check_id, route_response, get_route_response
from src.schema.partition import Partition, PartitionCreate
from src.manager import partition_manager

router = APIRouter(
    prefix="/partition",
    tags=["Partition"],
)

# Get all partitions
@router.get("", response_model=Union[List[Partition], None])
def get_all_partitions():
    with engine.begin() as conn:
        response = list(partition_manager.get_all_partition(conn))
        return get_route_response(response, 200, 404, "No partitions found")

# Get partition by id
@router.get("/{partition_id}", response_model=Union[Partition, None])
def get_partition_by_id(partition_id: str):
    check_id(partition_id)
    with engine.begin() as conn:
        response = partition_manager.get_partition_by_id(conn, partition_id)
        return get_route_response(response, 200, 404, "Partition not found")

# Create partition
@router.post("", response_model=ResponseModel)
def create_partition(partition: PartitionCreate):
    with engine.begin() as conn:
        response = partition_manager.create_partition(conn, partition)
        return route_response(response, 200, 500)

# Update partition
@router.put("/{partition_id}", response_model=ResponseModel)
def update_partition(partition_id: str, partition: Partition):
    check_id(partition_id)
    with engine.begin() as conn:
        response = partition_manager.update_partition(conn, partition_id, partition)
        return route_response(response, 200, 500)

# Delete partition
@router.delete("/{partition_id}", response_model=ResponseModel)
def delete_partition(partition_id: str):
    check_id(partition_id)
    with engine.begin() as conn:
        response = partition_manager.delete_partition(conn, partition_id)
        return route_response(response, 200, 500)