from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class BiographyCreate(BaseModel):
    first_name: str
    last_name: str
    instrument: Optional[List[str]] = None
    nationality: Optional[str] = None
    website: Optional[str] = None
    award: Optional[List[str]] = None
    content: Optional[str] = None
    type: str
    status: str = "created"
    image_id: Optional[UUID] = None
    created_by: UUID

class Biography(BiographyCreate):
    id: UUID
    created_at: datetime

class BiographyUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    instrument: Optional[List[str]]
    nationality: Optional[str]
    website: Optional[str]
    award: Optional[List[str]]
    content: Optional[str]
    type: Optional[str]
    status: Optional[str]
    image_id: Optional[UUID]
    updated_at: datetime = datetime.now()
    updated_by: UUID