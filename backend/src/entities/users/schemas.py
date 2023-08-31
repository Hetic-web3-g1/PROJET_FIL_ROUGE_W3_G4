from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserCreate(BaseModel):
    academy_id: UUID
    first_name: str
    last_name: str
    email: str
    primary_role: str = "User"
    secondary_role: list[str] | None = None
    image_id: UUID | None = None


class User(UserCreate):
    id: UUID
    created_by: UUID | None
    created_at: datetime
    updated_at: datetime | None
    updated_by: UUID | None
