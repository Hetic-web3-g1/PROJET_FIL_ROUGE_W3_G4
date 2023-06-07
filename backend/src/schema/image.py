from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ImageCreate(BaseModel):
    title: str
    file_name: str
    created_by: UUID

class Image(ImageCreate):
    id: UUID
    created_at: datetime

class ImageUpdate(BaseModel):
    title: str | None
    file_name: str | None
    updated_at: datetime = datetime.now()
    updated_by: UUID