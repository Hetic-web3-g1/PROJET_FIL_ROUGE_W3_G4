from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class AnnotationCreate(BaseModel):
    measure: int
    content: str
    created_by: UUID

class Annotation(AnnotationCreate):
    id: UUID
    created_at: datetime

class AnnotationUpdate(BaseModel):
    measure: Optional[int]
    content: Optional[str]
    updated_at: datetime = datetime.now()
    updated_by: UUID