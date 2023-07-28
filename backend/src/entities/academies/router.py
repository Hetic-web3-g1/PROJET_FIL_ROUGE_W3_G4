from uuid import UUID

from fastapi import APIRouter, Depends

from . import service as academy_service
from ..authentification.dependencies import CustomSecurity
from ..users.schemas import User
from ...database.db_engine import engine

router = APIRouter(
    prefix="/academies",
    tags=["Academies"],
)


@router.get("/{academy_id}")
def get_academy_by_id(
    academy_id: UUID,
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        academy = academy_service.get_academy_by_id(conn, academy_id)
        return academy
