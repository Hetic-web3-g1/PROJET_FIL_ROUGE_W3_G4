from pydantic import BaseModel
from typing import Optional

class TagCreate(BaseModel):
    content: str

class Tag(TagCreate):
    id: int

class TagUpdate(BaseModel):
    id: Optional[int]
    content: str