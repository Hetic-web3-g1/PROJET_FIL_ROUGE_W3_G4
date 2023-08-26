from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    primary_role: str = "User"
    secondary_role: list[str] | None
    academy_id: UUID
    image_id: UUID | None


class User(UserCreate):
    id: UUID
    created_by: UUID | None
    created_at: datetime
    updated_at: datetime | None
    updated_by: UUID | None
