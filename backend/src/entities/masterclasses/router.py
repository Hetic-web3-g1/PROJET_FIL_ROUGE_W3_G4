from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID

from .schemas import Masterclass, MasterclassCreate, MasterclassUser, MasterclassUserCreate
from ..users.schemas import User
from . import exceptions as masterclass_exceptions
from . import service as masterclass_service
from src.database.db_engine import engine
from ..authentification import service as auth_service
from ..authentification.dependencies import CustomSecurity

router = APIRouter(
    prefix="/masterclasses",
    tags=["Masterclasses"],
)


# Get all masterclasses
@router.get("")
def get_all_masterclasses(
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        response = masterclass_service.get_all_masterclasses(conn)
        return response
    

# Get masterclass by id
@router.get("/{masterclass_id}")
def get_masterclass_by_id(
    masterclass_id: UUID,
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        response = masterclass_service.get_masterclass_by_id(conn, masterclass_id)
        return response


# Get masterclasses by user
@router.get("/user/{user_id}")
def get_masterclasses_by_user(
    user_id: UUID,
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        response = masterclass_service.get_masterclasses_by_user(conn, user_id)
        return response


# Create masterclass
@router.post("/masterclass")
def create_masterclass(
    new_masterclass: MasterclassCreate, User: User = Depends(CustomSecurity())
):
    with engine.begin() as conn:
        masterclass_service.create_masterclass(conn, new_masterclass)


# Update masterclass
@router.put("/{masterclass_id}")
def update_masterclass(
    masterclass_id: UUID,
    updated_masterclass: MasterclassCreate,
    user: User = Depends(CustomSecurity()),
):
    try:
        with engine.begin() as conn:
            masterclass_service.update_masterclass(conn, masterclass_id, updated_masterclass)

    except masterclass_exceptions.MasterclassNotFound:
        raise HTTPException(
            status_code=404,
            detail="Masterclass not found",
        )