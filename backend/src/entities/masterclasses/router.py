from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.database.db_engine import engine

from ..authentification.dependencies import CustomSecurity
from ..users import exceptions as user_exceptions
from ..users.schemas import User
from . import exceptions as masterclass_exceptions
from . import service as masterclass_service
from .schemas import MasterclassCreate, MasterclassUserCreate

router = APIRouter(
    prefix="/masterclasses",
    tags=["Masterclasses"],
)


@router.get("")
def get_all_masterclasses(
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        masterclasses = masterclass_service.get_all_masterclasses(conn)
        return list(masterclasses)


@router.get("/masterclass/{masterclass_id}")
def get_masterclass_by_id(
    masterclass_id: UUID,
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        masterclass = masterclass_service.get_masterclass_by_id(conn, masterclass_id)
        return masterclass


@router.get("/masterclass/user/{user_id}")
def get_masterclasses_by_user(
    user_id: UUID,
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        masterclasses = masterclass_service.get_masterclasses_by_user(conn, user_id)
        return list(masterclasses)


@router.post("/masterclass")
def create_masterclass(
    masterclass: MasterclassCreate, user: User = Depends(CustomSecurity())
):
    with engine.begin() as conn:
        masterclass_service.create_masterclass(conn, masterclass, user)


@router.put("/masterclass/{masterclass_id}")
def update_masterclass(
    masterclass_id: UUID,
    masterclass: MasterclassCreate,
    user: User = Depends(CustomSecurity()),
):
    try:
        with engine.begin() as conn:
            masterclass_service.update_masterclass(
                conn, masterclass_id, masterclass, user
            )

    except masterclass_exceptions.MasterclassNotFound:
        raise HTTPException(
            status_code=404,
            detail="Masterclass not found",
        )


@router.delete("/masterclass/{masterclass_id}")
def delete_masterclass(
    masterclass_id: UUID,
    user: User = Depends(CustomSecurity()),
):
    try:
        with engine.begin() as conn:
            masterclass_service.delete_masterclass(conn, masterclass_id)

    except masterclass_exceptions.MasterclassNotFound:
        raise HTTPException(
            status_code=404,
            detail="Masterclass not found",
        )


# ---------------------------------------------------------------------------------------------------- #


@router.post("/masterclass/assign_user")
def assign_user_to_masterclass(
    masterclass_user: MasterclassUserCreate,
    user: User = Depends(CustomSecurity()),
):
    try:
        with engine.begin() as conn:
            return masterclass_service.assign_user_to_masterclass(
                conn, masterclass_user
            )

    except masterclass_exceptions.MasterclassNotFound:
        raise HTTPException(
            status_code=404,
            detail="Masterclass not found",
        )

    except user_exceptions.UserNotFound:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    except masterclass_exceptions.MasterclassUserAlreadyExist:
        raise HTTPException(
            status_code=400,
            detail="User already assigned to this masterclass",
        )


@router.delete("/masterclass/unassign_user")
def unassign_user_from_masterclass(
    masterclass_user: MasterclassUserCreate,
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        masterclass_service.unassign_user_from_masterclass(conn, masterclass_user)
