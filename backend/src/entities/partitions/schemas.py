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
