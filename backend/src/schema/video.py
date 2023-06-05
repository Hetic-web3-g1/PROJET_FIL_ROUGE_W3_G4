from pydantic import BaseModel
from typing import Optional
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
    title: Optional[str]
    duration: Optional[float]
    status: Optional[str]
    file_name: Optional[str]
    updated_at: datetime = datetime.now()
    updated_by: UUID