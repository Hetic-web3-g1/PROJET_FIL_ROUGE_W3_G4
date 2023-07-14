from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID

from .schemas import Masterclass, MasterclassCreate, MasterclassUser, MasterclassUserCreate
from ..users.schemas import User
from . import exceptions as masterclass_exceptions
from . exceptions import MasterclassNotFound, MasterclassUserAlreadyExist
from ..users import exceptions as user_exceptions
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
@router.get("/masterclass/{masterclass_id}")
def get_masterclass_by_id(
    masterclass_id: UUID,
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        response = masterclass_service.get_masterclass_by_id(conn, masterclass_id)
        return response


# Get masterclasses by user
@router.get("/masterclass/user/{user_id}")
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
    masterclass: MasterclassCreate,
    user: User = Depends(CustomSecurity())
):
    with engine.begin() as conn:
        masterclass_service.create_masterclass(conn, masterclass, user)


# Update masterclass
@router.put("/masterclass/{masterclass_id}")
def update_masterclass(
    masterclass_id: UUID,
    masterclass: MasterclassCreate,
    user: User = Depends(CustomSecurity()),
):
    try:
        with engine.begin() as conn:
            masterclass_service.update_masterclass(conn, masterclass_id, masterclass, user)

    except masterclass_exceptions.MasterclassNotFound:
        raise HTTPException(
            status_code=404,
            detail="Masterclass not found",
        )


# Delete masterclass
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


# Assign user to masterclass and update role if already assigned
@router.post("/masterclass/assign_user")
def assigne_user_to_masterclass(
    masterclass_user: MasterclassUserCreate,
    user: User = Depends(CustomSecurity()),
):
    try:
        with engine.begin() as conn:
            masterclass_service.assigne_user_to_masterclass(conn, masterclass_user)
    
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


# Unassign user from masterclass
@router.delete("/masterclass/unassign_user")
def unassigne_user_from_masterclass(
    masterclass_user: MasterclassUserCreate,
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        masterclass_service.unassigne_user_from_masterclass(conn, masterclass_user)