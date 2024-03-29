from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SubtitleCreate(BaseModel):
    filename: str | None
    language: str
    status: str | None
    masterclass_id: UUID | None
    s3_object_id: UUID


class Subtitle(SubtitleCreate):
    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime | None
    updated_by: UUID | None
