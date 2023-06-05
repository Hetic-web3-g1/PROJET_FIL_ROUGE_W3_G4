from pydantic import BaseModel
from typing import Optional
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
    status: Optional[str]
    updated_at: datetime = datetime.now()
    updated_by: UUID