from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.database.db_engine import engine

from .exceptions import (
    PartitionMetaNotFound,
    PartitionMetaKeyAlreadyExist,
)
from . import service as partition_service
from .schemas import PartitionMetaCreate

router = APIRouter(
    prefix="/partitions",
    tags=["Partitions"],
)


@router.get("")
def get_all_partitions():
    with engine.begin() as conn:
        partitions = partition_service.get_all_partitions(conn)
        return list(partitions)


@router.get("/partition/{partition_id}")
def get_partition_by_id(partition_id: UUID):
    with engine.begin() as conn:
        partition = partition_service.get_partition_by_id(conn, partition_id)
        return partition


# ---------------------------------------------------------------------------------------------------- #


@router.get("/partition/meta/{meta_id}")
def get_partition_meta_by_id(meta_id: int):
    try:
        with engine.begin() as conn:
            meta = partition_service.get_partition_meta_by_id(conn, meta_id)
            return meta

    except PartitionMetaNotFound:
        raise HTTPException(
            status_code=404,
            detail="Partition meta not found",
        )


@router.get("/partition/meta/partition/{partition_id}")
def get_partition_meta_by_partition_id(partition_id: UUID):
    with engine.begin() as conn:
        meta = partition_service.get_partition_meta_by_partition_id(conn, partition_id)
        return meta


@router.post("/partition/meta")
def create_partition_meta(meta: PartitionMetaCreate):
    try:
        with engine.begin() as conn:
            meta = partition_service.create_partition_meta(conn, meta)
            return meta

    except PartitionMetaKeyAlreadyExist:
        raise HTTPException(
            status_code=400,
            detail="Partition meta key already exist",
        )


@router.put("/partition/meta/{meta_id}")
def update_partition_meta(meta_id: int, meta: PartitionMetaCreate):
    try:
        with engine.begin() as conn:
            meta = partition_service.update_partition_meta(conn, meta_id, meta)
            return meta

    except PartitionMetaNotFound:
        raise HTTPException(
            status_code=404,
            detail="Partition meta not found",
        )


@router.delete("/partition/meta/{meta_id}")
def delete_partition_meta(meta_id: int):
    try:
        with engine.begin() as conn:
            partition_service.delete_partition_meta(conn, meta_id)

    except PartitionMetaNotFound:
        raise HTTPException(
            status_code=404,
            detail="Partition meta not found",
        )
