from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID

from .schemas import MasterclassCreate, MasterclassUserCreate
from ..users.schemas import User
from ..tags.schemas import TagCreate, MasterclassTag
from src.entities.masterclasses.models import masterclass_table, masterclass_tag_table
from . import exceptions as masterclass_exceptions
from ..users import exceptions as user_exceptions
from . import service as masterclass_service
from ..tags import service as tag_service
from src.database.db_engine import engine
from ..authentification.dependencies import CustomSecurity
from src.utils.sanitize import sanitize_string

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
        created_masterclass = masterclass_service.create_masterclass(
            conn, masterclass, user
        )
        tags = [masterclass.title]
        if masterclass.instrument:
            tags.extend(masterclass.instrument)

        for content in tags:
            tag = TagCreate(
                content=sanitize_string(content), tag_type=str(masterclass_table)
            )
            created_tag = tag_service.create_tag(conn, tag, user)
            masterclass_tag = MasterclassTag(
                masterclass_id=created_masterclass.id,
                tag_id=created_tag.id,
            )
            tag_service.create_link_table(
                conn, masterclass_tag, masterclass_tag_table, user
            )


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
