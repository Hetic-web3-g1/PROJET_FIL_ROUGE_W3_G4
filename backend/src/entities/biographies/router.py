from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.database.db_engine import engine

from ..authentification.dependencies import CustomSecurity
from ..comments.schemas import CommentCreate
from ..users.schemas import User
from .exceptions import (
    BiographyNotFound,
    BiographyTranslationNotFound,
    BiographyTranslationAlreadyExist,
    BiographyMetaNotFound,
    BiographyMetaKeyAlreadyExist,
)
from . import service as biography_service
from .schemas import BiographyCreate, BiographyTranslationCreate, BiographyMetaCreate

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
        return list(response)


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
        biography_service.create_biography(conn, biography, user)


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

    except BiographyNotFound:
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

    except BiographyNotFound:
        raise HTTPException(
            status_code=404,
            detail="Biography not found",
        )


# ---------------------------------------------------------------------------------------------------- #


@router.get("/biography/translation/{biography_translation_id}")
def get_biography_translation_by_id(
    biography_translation_id: int,
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        biography_translation = biography_service.get_biography_translation_by_id(
            conn, biography_translation_id
        )
        return biography_translation


@router.get("/biography/translation/biography/{biography_id}")
def get_biography_translation_biography(
    biography_id: UUID, user: User = Depends(CustomSecurity())
):
    with engine.begin() as conn:
        biography_translation = (
            biography_service.get_biography_translation_by_biography(conn, biography_id)
        )
        return biography_translation


@router.post("/biography/translation")
def create_biography_translation(
    biography_translation: BiographyTranslationCreate,
    user: User = Depends(CustomSecurity()),
):
    try:
        with engine.begin() as conn:
            return biography_service.create_biography_translation(
                conn, biography_translation, user
            )

    except BiographyTranslationAlreadyExist:
        raise HTTPException(
            status_code=409,
            detail="Biography translation already exist",
        )


@router.put("/biography/translation/{biography_translation_id}")
def update_biography_translation(
    biography_translation_id: int,
    biography_translation: BiographyTranslationCreate,
    user: User = Depends(CustomSecurity()),
):
    try:
        with engine.begin() as conn:
            return biography_service.update_biography_translation(
                conn, biography_translation_id, biography_translation, user
            )

    except BiographyTranslationNotFound:
        raise HTTPException(
            status_code=404,
            detail="Biography translation not found",
        )


@router.delete("/biography/translation/{biography_translation_id}")
def delete_biography_translation(
    biography_translation_id: int,
    user: User = Depends(CustomSecurity()),
):
    try:
        with engine.begin() as conn:
            biography_service.delete_biography_translation(
                conn, biography_translation_id
            )

    except BiographyTranslationNotFound:
        raise HTTPException(
            status_code=404,
            detail="Biography translation not found",
        )


# ---------------------------------------------------------------------------------------------------- #


@router.post("/biography/comment/{biography_id}")
def create_biography_comment(
    comment: CommentCreate, biography_id, user: User = Depends(CustomSecurity())
):
    with engine.begin() as conn:
        biography_service.create_biography_comment(conn, comment, biography_id, user)


# ---------------------------------------------------------------------------------------------------- #


@router.get("/biography/meta/{meta_id}")
def get_biography_meta_by_id(
    meta_id: int,
    user: User = Depends(CustomSecurity()),
):
    try:
        with engine.begin() as conn:
            meta = biography_service.get_biography_meta_by_id(conn, meta_id)
            return meta

    except BiographyMetaNotFound:
        raise HTTPException(
            status_code=404,
            detail="Biography not found",
        )


@router.get("/biography/meta/biography/{biography_id}")
def get_biography_meta_by_biography_id(
    biography_id: UUID,
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        meta = biography_service.get_biography_meta_by_biography_id(conn, biography_id)
        return meta


@router.post("/biography/meta")
def create_biography_meta(
    meta: BiographyMetaCreate,
    user: User = Depends(CustomSecurity()),
):
    try:
        with engine.begin() as conn:
            biography_service.create_biography_meta(conn, meta)

    except BiographyMetaKeyAlreadyExist:
        raise HTTPException(
            status_code=409,
            detail="Meta key already exists",
        )


@router.put("/biography/meta/{meta_id}")
def update_biography_meta(
    meta_id: int,
    meta: BiographyMetaCreate,
    user: User = Depends(CustomSecurity()),
):
    try:
        with engine.begin() as conn:
            biography_service.update_biography_meta(conn, meta_id, meta)

    except BiographyMetaNotFound:
        raise HTTPException(
            status_code=404,
            detail="Biography not found",
        )


@router.delete("/biography/meta/{meta_id}")
def delete_biography_meta(
    meta_id: int,
    user: User = Depends(CustomSecurity()),
):
    try:
        with engine.begin() as conn:
            biography_service.delete_biography_meta(conn, meta_id)

    except BiographyMetaNotFound:
        raise HTTPException(
            status_code=404,
            detail="Biography not found",
        )
