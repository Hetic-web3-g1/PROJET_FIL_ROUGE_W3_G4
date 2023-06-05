from pydantic import BaseModel
from uuid import UUID

class TimecodeCreate(BaseModel):
    video_id: UUID
    hour: int
    minute: int
    second: int
    frame: int

class Timecode(BaseModel):
    id: int