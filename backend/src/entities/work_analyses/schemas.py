from pydantic import BaseModel
from typing import List
from uuid import UUID
from datetime import datetime

class WorkAnalysisCreate(BaseModel):
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
