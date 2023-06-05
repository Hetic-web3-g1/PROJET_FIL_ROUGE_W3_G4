from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class ImageCreate(BaseModel):
    title: str
    file_name: str
    created_by: UUID

class Image:
    id: UUID
    created_at: datetime

class ImageUpdate(BaseModel):
    title: Optional[str]
    file_name: Optional[str]
    updated_at: datetime = datetime.now()
    updated_by: UUID