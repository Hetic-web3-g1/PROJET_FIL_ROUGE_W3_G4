from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel


class BiographyCreate(BaseModel):
    first_name: str
    last_name: str
    instrument: List[str] | None
    nationality: str | None
    website: str | None
    award: List[str] | None
    content: str | None
    type: str
    status: str = "created"
    image_id: UUID | None


class Biography(BiographyCreate):
    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime | None
    updated_by: UUID | None


class BiographyTranslationCreate(BaseModel):
    biography_id: UUID
    language: str
    award: List[str] | None
    content: str | None
    status: str = "created"


class BiographyTranslation(BiographyTranslationCreate):
    id: int
    created_by: UUID
    created_at: datetime
    updated_at: datetime | None
    updated_by: UUID | None

      
class BiographyMetaCreate(BaseModel):
    biography_id: UUID
    meta_key: str
    meta_value: str


class BiographyMeta(BiographyMetaCreate):
    id: int