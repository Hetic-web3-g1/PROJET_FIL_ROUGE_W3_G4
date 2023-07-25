from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class S3ObjectCreate(BaseModel):
    object_key: str
    filename: str
    bucket: str
    public: bool
    major_type: str
    minor_type: str


class S3Object(S3ObjectCreate):
    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime | None
    updated_by: UUID | None
