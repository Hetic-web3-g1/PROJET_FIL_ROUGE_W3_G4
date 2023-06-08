from enum import Enum
from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class ResetToken(BaseModel):
    token: str
    expires_at: datetime


class Service(Enum):
    ADMIN = "admin"

    # Add more ex:
    # VIDEO_EDITING = "video-editing"
    # TRADUCTION = "traduction"


class Right(Enum):
    EDITOR = "EDITOR"
    VIEWER = "VIEWER"


ServicesRights = dict[Service, Optional[Right]]
