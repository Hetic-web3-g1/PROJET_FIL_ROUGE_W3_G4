from pydantic import BaseModel

class TagCreate(BaseModel):
    content: str

class Tag(TagCreate):
    id: int