from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class PartitionCreate(BaseModel):
    filename: str
    status: str
    s3_object_id: UUID


class Partition(PartitionCreate):
    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime | None
    updated_by: UUID | None


class PartitionMetaCreate(BaseModel):
    partition_id: UUID
    meta_key: str
    meta_value: str


class PartitionMeta(PartitionMetaCreate):
    id: int
