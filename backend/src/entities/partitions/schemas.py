from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class PartitionCreate(BaseModel):
    status: str = "created"
    file_name: str

class Partition(PartitionCreate):
    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime | None
    updated_by: UUID | None
