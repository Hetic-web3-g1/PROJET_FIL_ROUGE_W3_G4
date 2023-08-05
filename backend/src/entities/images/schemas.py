from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ImageCreate(BaseModel):
    filename: str
    s3_object_id: UUID


class Image(ImageCreate):
    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime | None
    updated_by: UUID | None
