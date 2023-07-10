from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class AcademyCreate(BaseModel):
    name: str


class Academy(AcademyCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime | None