from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID

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


@router.get("/user/me")
def get_user_by_token(
    user: User = Depends(CustomSecurity()),
):
    return user
    

# Get user by id
@router.get("/{user_id}")
def get_user_by_id(
    user_id: UUID,
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        response = user_service.get_user_by_id(conn, user_id)
        return response


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


