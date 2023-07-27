from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class VideoCreate(BaseModel):
    name: str | None
    duration: float | None
    status: str | None
    version: float | None
    s3_object_id: UUID


class Video(VideoCreate):
    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime | None
    updated_by: UUID | None
