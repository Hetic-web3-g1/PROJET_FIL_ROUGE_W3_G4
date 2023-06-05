from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class MasterclassCreate(BaseModel):
    academy_id: UUID
    title: str
    description: Optional[str]
    teacher_bio_id: Optional[UUID]
    composer_bio_id: Optional[UUID]
    work_analysis_id: Optional[UUID]
    partition_id: Optional[UUID]
    instrument: Optional[List[str]]
    status: str = "created"
    created_by: UUID

class Masterclass(MasterclassCreate):
    id: UUID
    created_at: datetime

class MasterclassUpdate(BaseModel):
    academy_id: Optional[UUID]
    title: Optional[str]
    description: Optional[str]
    teacher_bio_id: Optional[UUID]
    composer_bio_id: Optional[UUID]
    work_analysis_id: Optional[UUID]
    partition_id: Optional[UUID]
    instrument: Optional[List[str]]
    status: Optional[str]
    updated_at: datetime = datetime.now()
    updated_by: UUID