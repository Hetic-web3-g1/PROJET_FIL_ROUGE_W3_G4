from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserCreate(BaseModel):
    academy_id: UUID
    first_name: str
    last_name: str
    email: str
    role_id: int
    image_id: UUID | None = None


class User(UserCreate):
    id: UUID
    created_by: UUID | None
    created_at: datetime
    updated_at: datetime | None
    updated_by: UUID | None
