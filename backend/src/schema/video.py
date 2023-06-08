from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class VideoCreate(BaseModel):
    version: float
    title: str
    duration: float
    status: str
    file_name: str
    created_by: UUID

class Video(VideoCreate):
    id: UUID
    created_at: datetime

class VideoUpdate(BaseModel):
    title: str | None
    duration: float | None
    status: str | None
    file_name: str | None
    updated_at: datetime = datetime.now()
    updated_by: UUID