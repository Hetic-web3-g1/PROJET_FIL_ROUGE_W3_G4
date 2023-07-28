from uuid import UUID

from pydantic import BaseModel


class TagCreate(BaseModel):
    content: str
    tag_type: str


class Tag(TagCreate):
    id: int


class BiographyTag(BaseModel):
    biography_id: UUID
    tag_id: int


class MasterclassTag(BaseModel):
    masterclass_id: UUID
    tag_id: int


class PartitionTag(BaseModel):
    partition_id: UUID
    tag_id: int


class SubtitleTag(BaseModel):
    subtitle_id: UUID
    tag_id: int


class UserTag(BaseModel):
    user_id: UUID
    tag_id: int


class VideoTag(BaseModel):
    video_id: UUID
    tag_id: int


class WorkAnalysisTag(BaseModel):
    work_analysis_id: UUID
    tag_id: int
