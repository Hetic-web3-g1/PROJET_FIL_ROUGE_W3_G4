from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class SubtitleCreate(BaseModel):
    video_id: UUID
    language: str
    status: str = "created"
    file_name: str
    created_by: UUID

class Subtitle(SubtitleCreate):
    id: UUID
    created_at: datetime

class SubtitleUpdate(BaseModel):
    status: str | None
    updated_at: datetime = datetime.now()
    updated_by: UUID
