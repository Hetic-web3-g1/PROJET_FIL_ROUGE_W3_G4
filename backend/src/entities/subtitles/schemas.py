from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class SubtitleCreate(BaseModel):
    video_id: UUID
    language: str
    status: str = "created"
    s3_object_id: UUID


class Subtitle(SubtitleCreate):
    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime | None
    updated_by: UUID | None
