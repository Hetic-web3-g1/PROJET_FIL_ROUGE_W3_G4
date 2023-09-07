from datetime import datetime
from typing import Any

from pydantic import BaseModel


class LogCreate(BaseModel):
    level: str
    message: Any


class Log(LogCreate):
    id: int
    time: datetime
