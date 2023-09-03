from uuid import UUID

from pydantic import BaseModel


class TimecodeCreate(BaseModel):
    video_id: UUID
    hour: int
    minute: int
    second: int
    frame: int


class Timecode(BaseModel):
    id: int
