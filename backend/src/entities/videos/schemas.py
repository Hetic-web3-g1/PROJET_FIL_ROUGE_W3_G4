from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class VideoCreate(BaseModel):
    masterclass_id: UUID
    filename: str
    duration: float
    status: str
    version: float
    s3_object_id: UUID


class Video(VideoCreate):
    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime | None
    updated_by: UUID | None
