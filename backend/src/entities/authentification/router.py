from fastapi import APIRouter, Body, HTTPException

from src.database.db_engine import engine

from ..users import exceptions as user_exceptions
from ..users import service as user_service
from .exceptions import InvalidToken, ExpiredToken, InvalidCredentials
from . import service as auth_service

router = APIRouter(
    prefix="/auth",
    tags=["Authentification"],
)


@router.get("/forgot-password")
def send_email_reset_password(
    email: str,
):
    try:
        with engine.begin() as conn:
            user = user_service.get_user_by_email(conn, email)
            token = auth_service.create_reset_token(conn, user.id)
            # auth_service.send_email_reset_password(user.email, token)
        return token
    except user_exceptions.UserNotFound:
        pass


@router.post("/reset-password")
def reset_password(
    token: str = Body(...),
    password: str = Body(...),
):
    try:
        with engine.begin() as conn:
            user_id = auth_service.verify_reset_token(conn, token)
            auth_service.reset_password(conn, user_id, password)
    except InvalidToken:
        raise HTTPException(
            status_code=403,
            detail="Invalid token",
        )
    except ExpiredToken:
        raise HTTPException(
            status_code=403,
            detail="Expired token",
        )


@router.post("/login")
def login(
    email: str = Body(...),
    password: str = Body(...),
):
    try:
        with engine.begin() as conn:
            password_hash, salt = auth_service.get_user_password_hash(conn, email)
            if not auth_service.verify_password(password_hash, salt, password):
                raise InvalidCredentials

            user = user_service.get_user_by_email(conn, email)
            return auth_service.generate_jwt_token(user)

    except InvalidCredentials:
        raise HTTPException(
            status_code=403,
            detail="Invalid Credentials",
        )


@router.post("/refresh-token")
def refresh_auth_token(
    refresh_token: str = Body(...),
):
    # TODO: Implement refresh token
    pass
