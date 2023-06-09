from pydantic import BaseModel
from typing import List
from uuid import UUID
from datetime import datetime

class BiographyCreate(BaseModel):
    first_name: str
    last_name: str
    instrument: List[str] | None
    nationality: str | None
    website: str | None
    award: List[str] | None
    content: str | None
    type: str
    status: str = "created"
    image_id: UUID | None
    created_by: UUID

class Biography(BiographyCreate):
    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime | None
    updated_by: UUID | None