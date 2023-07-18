from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class PartitionCreate(BaseModel):
    name: str | None
    status: str | None
    s3_object_id: UUID


class Partition(PartitionCreate):
    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime | None
    updated_by: UUID | None
