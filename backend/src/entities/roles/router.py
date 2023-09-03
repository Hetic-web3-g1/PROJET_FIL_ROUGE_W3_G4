from fastapi import APIRouter, Depends

from src.database.db_engine import engine

from ..authentification.dependencies import CustomSecurity
from ..users.schemas import User
from . import service as role_service

router = APIRouter(
    prefix="/roles",
    tags=["Roles and Permissions"],
)

@router.get("")
def get_academy_roles(
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        return list(role_service.get_academy_roles(conn, academy_id=user.academy_id))