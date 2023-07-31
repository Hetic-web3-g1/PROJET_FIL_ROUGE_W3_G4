from uuid import UUID

from pydantic import BaseModel


class TagCreate(BaseModel):
    content: str
    tag_type: str


class Tag(TagCreate):
    id: int


class BiographyTag(BaseModel):
    entity_id: UUID
    tag_id: int


class MasterclassTag(BaseModel):
    entity_id: UUID
    tag_id: int


class PartitionTag(BaseModel):
    entity_id: UUID
    tag_id: int


class SubtitleTag(BaseModel):
    entity_id: UUID
    tag_id: int


class UserTag(BaseModel):
    entity_id: UUID
    tag_id: int


class VideoTag(BaseModel):
    entity_id: UUID
    tag_id: int


class WorkAnalysisTag(BaseModel):
    entity_id: UUID
    tag_id: int
