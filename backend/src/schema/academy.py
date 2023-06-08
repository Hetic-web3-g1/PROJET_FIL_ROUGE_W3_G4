from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class AcademyCreate(BaseModel):
    name: str

class Academy(AcademyCreate):
    id: UUID
    created_at: datetime

class AcademyUpdate(BaseModel):
    name: str | None
    updated_at: datetime = datetime.now()