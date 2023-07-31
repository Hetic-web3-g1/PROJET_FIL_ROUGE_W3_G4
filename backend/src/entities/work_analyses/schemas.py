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
