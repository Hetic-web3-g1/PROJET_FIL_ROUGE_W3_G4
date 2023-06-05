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
    created_at: datetime

class UserUpdate(BaseModel):
    id: Optional[UUID]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    role: Optional[str]
    academy_id: Optional[UUID]
    image_id: Optional[UUID]
    updated_at: datetime = datetime.now()   
    updated_by: UUID