from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    role: str = "User"
    academy_id: UUID | None
    image_id: UUID | None

class User(UserCreate):
    id: UUID
    created_at: datetime

class UserUpdate(BaseModel):
    id: UUID | None
    first_name: str | None
    last_name: str | None
    email: str | None
    password: str | None
    role: str | None
    academy_id: UUID | None
    image_id: UUID | None
    updated_at: datetime = datetime.now()   
    updated_by: UUID