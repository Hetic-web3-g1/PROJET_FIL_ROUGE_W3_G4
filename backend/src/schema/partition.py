from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class PartitionCreate(BaseModel):
    status: str = "created"
    file_name: str
    created_by: UUID

class Partition(PartitionCreate):
    id: UUID
    created_at: datetime

class PartitionUpdate(BaseModel):
    status: str | None
    updated_at: datetime = datetime.now()
    updated_by: UUID