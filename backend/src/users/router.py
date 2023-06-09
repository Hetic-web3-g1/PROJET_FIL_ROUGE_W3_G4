from fastapi import APIRouter, HTTPException, Depends

from .schemas import User, UserCreate
from . import exceptions as user_exceptions
from . import service as user_service
from src.database.db_engine import engine
from src.authentification import service as auth_service
from src.authentification.dependencies import CustomSecurity

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/academy/{academy_id}/user")
def create_academy_user(
    academy_id: str, new_user: UserCreate, user: User = Depends(CustomSecurity())
):
    try:
        with engine.begin() as conn:
            new_user = user_service.create_user(conn, new_user)
            token = auth_service.create_reset_token(conn, new_user.id)
            auth_service.send_reset_password_email(new_user.email, token)

    except user_exceptions.EmailAlreadyExist:
        raise HTTPException(
            status_code=400,
            detail="Email already exist",
        )
