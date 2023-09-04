from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel


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


class Masterclass(MasterclassCreate):
    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime | None
    updated_by: UUID | None


class MasterclassUserCreate(BaseModel):
    user_id: UUID
    masterclass_id: UUID
    masterclass_role: str


class MasterclassUser(MasterclassUserCreate):
    id: int


class MasterclassMetaCreate(BaseModel):
    masterclass_id: UUID
    meta_key: str
    meta_value: str


class MasterclassMeta(MasterclassMetaCreate):
    id: int
