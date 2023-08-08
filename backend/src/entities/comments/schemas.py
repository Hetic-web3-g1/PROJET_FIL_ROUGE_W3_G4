from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class CommentCreate(BaseModel):
    content: str


class Comment(BaseModel):
    id: int
    created_by: UUID
    created_at: datetime
    updated_at: datetime | None
    updated_by: UUID | None


class BiographyComment(BaseModel):
    entity_id: UUID
    comment_id: int


class MasterclassComment(BaseModel):
    entity_id: UUID
    comment_id: int


class PartitionComment(BaseModel):
    entity_id: UUID
    comment_id: int


class SubtitleComment(BaseModel):
    entity_id: UUID
    comment_id: int


class VideoComment(BaseModel):
    entity_id: UUID
    comment_id: int


class WorkAnalysisComment(BaseModel):
    entity_id: UUID
    comment_id: int
