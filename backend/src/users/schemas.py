from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    role: str = "test"
    academy_id: UUID
    image_id: UUID | None


class User(UserCreate):
    id: UUID
    created_by: UUID | None
    created_at: datetime
    updated_at: datetime | None
    updated_by: UUID | None
