from fastapi import APIRouter

from .schemas import User, UserCreate
from . import service as user_service
from src.database.db_engine import aysnc_engine

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/academy/{academy_id}/user")
async def create_academy_user(
    academy_id: str,
    user: UserCreate,
):
    async with aysnc_engine.begin() as conn:
        user_service.create_user(conn, user)
