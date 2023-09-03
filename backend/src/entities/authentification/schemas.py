from datetime import datetime

from pydantic import BaseModel


class ResetToken(BaseModel):
    token: str
    expires_at: datetime

