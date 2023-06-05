from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class WorkAnalysisCreate(BaseModel):
    about: Optional[str]
    learning: Optional[List[str]]
    content: Optional[str]
    status: str = "created"
    created_by: UUID

class WorkAnalysis(WorkAnalysisCreate):
    id: UUID
    created_at: datetime

class WorkAnalysisUpdate(BaseModel):
    about: Optional[str]
    learning: Optional[List[str]]
    content: Optional[str]
    status: Optional[str]
    updated_at: datetime = datetime.now()
    updated_by: UUID