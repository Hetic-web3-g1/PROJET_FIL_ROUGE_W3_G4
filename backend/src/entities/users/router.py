from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID

from .schemas import User, UserCreate
from . import exceptions as user_exceptions
from . import service as user_service
from src.database.db_engine import engine
from ..authentification import service as auth_service
from ..authentification.dependencies import CustomSecurity

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/academy/{academy_id}")
def get_all_users_by_academy(
    academy_id: UUID,
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        users = user_service.get_all_users_by_academy(conn, academy_id)
        return list(users)


@router.get("/masterclass/{masterclass_id}")
def get_all_users_by_masterclass(
    masterclass_id: UUID,
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        users = user_service.get_all_users_by_masterclass(conn, masterclass_id)
        return list(users)


@router.get("/user/me")
def get_user_by_token(
    response: User = Depends(CustomSecurity()),
):
    return response


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
            new_user = user_service.create_user(conn, new_user, user)
            token = auth_service.create_reset_token(conn, new_user.id)
            auth_service.send_reset_password_email(new_user.email, token)
            return new_user

    except user_exceptions.EmailAlreadyExist:
        raise HTTPException(
            status_code=400,
            detail="Email already exist",
        )


@router.put("/user/{user_id}")
def update_academy_user(
    user_id: str, new_user: UserCreate, user: User = Depends(CustomSecurity())
):
    try:
        with engine.begin() as conn:
            return user_service.update_user(conn, UUID(user_id), new_user, user)

    except user_exceptions.UserNotFound:
        raise HTTPException(
            status_code=400,
            detail="User not found",
        )
