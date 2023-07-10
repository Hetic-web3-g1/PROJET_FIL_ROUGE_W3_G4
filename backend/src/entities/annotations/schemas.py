from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class AnnotationCreate(BaseModel):
    measure: int
    content: str

class Annotation(AnnotationCreate):
    id: int
    created_by: UUID
    created_at: datetime
    updated_at: datetime | None
    updated_by: UUID | None