from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class VideoCreate(BaseModel):
    version: float
    title: str
    duration: float
    status: str
    file_name: str

class Video(VideoCreate):
    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime | None
    updated_by: UUID | None
