from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class Service(str, Enum):
    USER_MANAGEMENT = "user_management"
    MASTERCLASS = "masterclass"
    BIOGRAPHY = "biography"

class Right(Enum):
    EDITOR = "EDITOR"
    VIEWER = "VIEWER"


ServicesRights = dict[Service, Right | None]

class RoleCreate(BaseModel):
    name: str
    description: str
    service_rights: ServicesRights
    academy_id: UUID

class Role(BaseModel):
    id: int