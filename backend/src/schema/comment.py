from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class CommentCreate(BaseModel):
    content: str
    created_by: UUID

class Comment(CommentCreate):
    id: int
    created_at: datetime

class CommentUpdate(BaseModel):
    updated_at: datetime = datetime.now()
    updated_by: UUID
    