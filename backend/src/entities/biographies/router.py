from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID

from .schemas import BiographyCreate
from ..users.schemas import User
from . import exceptions as biography_exceptions
from . import service as biography_service
from src.database.db_engine import engine
from ..authentification.dependencies import CustomSecurity

router = APIRouter(
    prefix="/biographies",
    tags=["Biographies"],
)


@router.get("")
def get_all_biographies(
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        response = biography_service.get_all_biographies(conn)
        return response


@router.get("/biography/{biography_id}")
def get_biography_by_id(
    biography_id: UUID,
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        biography = biography_service.get_biography_by_id(conn, biography_id)
        return biography


@router.post("/biography")
def create_biography(
    biography: BiographyCreate, user: User = Depends(CustomSecurity())
):
    with engine.begin() as conn:
        return biography_service.create_biography(conn, biography, user)


@router.put("/biography/{biography_id}")
def update_biography(
    biography_id: UUID,
    biography: BiographyCreate,
    user: User = Depends(CustomSecurity()),
):
    try:
        with engine.begin() as conn:
            return biography_service.update_biography(
                conn, biography_id, biography, user
            )

    except biography_exceptions.BiographyNotFound:
        raise HTTPException(
            status_code=404,
            detail="Biography not found",
        )


@router.delete("/biography/{biography_id}")
def delete_biography(
    biography_id: UUID,
    user: User = Depends(CustomSecurity()),
):
    try:
        with engine.begin() as conn:
            biography_service.delete_biography(conn, biography_id)

    except biography_exceptions.BiographyNotFound:
        raise HTTPException(
            status_code=404,
            detail="Biography not found",
        )
