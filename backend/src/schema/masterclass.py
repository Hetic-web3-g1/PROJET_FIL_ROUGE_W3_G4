from pydantic import BaseModel
from typing import List
from uuid import UUID
from datetime import datetime

class MasterclassCreate(BaseModel):
    academy_id: UUID
    title: str
    description: str | None
    teacher_bio_id: UUID | None
    composer_bio_id: UUID | None
    work_analysis_id: UUID | None
    partition_id: UUID | None
    instrument: List[str] | None
    status: str = "created"
    created_by: UUID

class Masterclass(MasterclassCreate):
    id: UUID
    created_at: datetime

class MasterclassUpdate(BaseModel):
    academy_id: UUID | None
    title: str | None
    description: str | None
    teacher_bio_id: UUID | None
    composer_bio_id: UUID | None
    work_analysis_id: UUID | None
    partition_id: UUID | None
    instrument: List[str] | None
    status: str | None
    updated_at: datetime = datetime.now()
    updated_by: UUID