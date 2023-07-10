from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ImageCreate(BaseModel):
    title: str
    file_name: str
    created_by: UUID

class Image(ImageCreate):
    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime | None
    updated_by: UUID | None
