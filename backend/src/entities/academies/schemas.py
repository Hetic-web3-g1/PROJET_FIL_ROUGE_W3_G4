from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class AcademyCreate(BaseModel):
    name: str
    image_id: UUID | None = None


class Academy(AcademyCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime | None
    updated_by: UUID | None
