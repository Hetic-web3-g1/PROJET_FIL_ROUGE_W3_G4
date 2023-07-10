from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID

from .schemas import Academy, AcademyCreate
from src.users.schemas import User
from . import exceptions as academy_exceptions
from . import service as academy_service
from src.database.db_engine import engine
from src.authentification import service as auth_service
from src.authentification.dependencies import CustomSecurity

router = APIRouter(
    prefix="/academies",
    tags=["Academies"],
)


# Get academy by id
@router.get("/{academy_id}")
def get_academy_by_id(
    academy_id: UUID,
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        response = academy_service.get_academy_by_id(conn, academy_id)
        return response