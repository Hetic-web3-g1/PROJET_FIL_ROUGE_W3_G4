from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, Body

from src.database.db_engine import engine

from ..authentification.dependencies import CustomSecurity
from ..comments.schemas import CommentCreate
from ..users.schemas import User
from .exceptions import (
    PartitionNotFound,
    PartitionMetaNotFound,
    PartitionMetaKeyAlreadyExist,
)
from . import service as partition_service
from .schemas import PartitionCreate, PartitionMetaCreate

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
    public: bool = Body(...),
    file: UploadFile = File(...),
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        partition_service.create_partition(conn, user, public, file)


@router.delete("/partition/{partition_id}")
def delete_partition(partition_id: UUID, user: User = Depends(CustomSecurity())):
    try:
        with engine.begin() as conn:
            partition_service.delete_partition(conn, partition_id)

    except PartitionNotFound:
        raise HTTPException(
            status_code=404,
            detail="Partition not found",
        )


# ---------------------------------------------------------------------------------------------------- #


@router.post("/partition/comment/{partition_id}")
def create_partition_comment(
    comment: CommentCreate, partition_id, user: User = Depends(CustomSecurity())
):
    with engine.begin() as conn:
        partition_service.create_partition_comment(conn, comment, partition_id, user)


# ---------------------------------------------------------------------------------------------------- #


@router.get("/partition/meta/{meta_id}")
def get_partition_meta_by_id(
    meta_id: int,
    user: User = Depends(CustomSecurity()),
):
    try:
        with engine.begin() as conn:
            meta = partition_service.get_partition_meta_by_id(conn, meta_id)
            return meta

    except PartitionMetaNotFound:
        raise HTTPException(
            status_code=404,
            detail="Partition not found",
        )


@router.get("/partition/meta/partition/{partition_id}")
def get_partition_meta_by_partition_id(
    partition_id: UUID,
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        meta = partition_service.get_partition_meta_by_partition_id(conn, partition_id)
        return meta


@router.post("/partition/meta")
def create_partition_meta(
    meta: PartitionMetaCreate,
    user: User = Depends(CustomSecurity()),
):
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
def update_partition_meta(
    meta_id: int,
    meta: PartitionMetaCreate,
    user: User = Depends(CustomSecurity()),
):
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
def delete_partition_meta(
    meta_id: int,
    user: User = Depends(CustomSecurity()),
):
    try:
        with engine.begin() as conn:
            partition_service.delete_partition_meta(conn, meta_id)

    except PartitionMetaNotFound:
        raise HTTPException(
            status_code=404,
            detail="Partition meta not found",
        )
