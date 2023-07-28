from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class CommentCreate(BaseModel):
    content: str


class Comment(CommentCreate):
    id: int
    created_by: UUID
    created_at: datetime
    updated_at: datetime | None
    updated_by: UUID | None
