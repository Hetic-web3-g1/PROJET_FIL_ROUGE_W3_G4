from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel


class WorkAnalysisCreate(BaseModel):
    title: str
    about: str | None
    learning: List[str]
    content: str | None
    status: str = "created"


class WorkAnalysis(WorkAnalysisCreate):
    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime | None
    updated_by: UUID | None


class WorkAnalysisTranslationCreate(WorkAnalysisCreate):
    work_analysis_id: UUID
    language: str


class WorkAnalysisTranslation(WorkAnalysisTranslationCreate):
    id: int
    created_by: UUID
    created_at: datetime
    updated_at: datetime | None
    updated_by: UUID | None

      
class WorkAnalysisMetaCreate(BaseModel):
    work_analysis_id: UUID
    meta_key: str
    meta_value: str


class WorkAnalysisMeta(WorkAnalysisMetaCreate):
    id: int

