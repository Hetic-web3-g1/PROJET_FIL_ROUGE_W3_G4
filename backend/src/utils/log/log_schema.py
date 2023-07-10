from pydantic import BaseModel
from datetime import datetime
from typing import Any

class LogCreate(BaseModel):
    level: str
    message: Any

class Log(LogCreate):
    id: int
    time: datetime