from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    role: str = "User"
    academy_id: Optional[UUID]
    image_id: Optional[UUID]

class User(UserCreate):
    id: UUID
    created_by: UUID
    created_at: datetime
    updated_at: datetime | None
    updated_by: UUID | None