from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.database.db_engine import engine

from .exceptions import (
    BiographyMetaNotFound,
    BiographyMetaKeyAlreadyExist,
)
from . import service as biography_service
from .schemas import BiographyMetaCreate

router = APIRouter(
    prefix="/biographies",
    tags=["Biographies"],
)


@router.get("")
def get_all_biographies():
    with engine.begin() as conn:
        response = biography_service.get_all_biographies(conn)
        return list(response)


@router.get("/biography/{biography_id}")
def get_biography_by_id(biography_id: UUID):
    with engine.begin() as conn:
        biography = biography_service.get_biography_by_id(conn, biography_id)
        return biography


# ---------------------------------------------------------------------------------------------------- #


@router.get("/biography/translation/{biography_translation_id}")
def get_biography_translation_by_id(biography_translation_id: int):
    with engine.begin() as conn:
        biography_translation = biography_service.get_biography_translation_by_id(
            conn, biography_translation_id
        )
        return biography_translation


@router.get("/biography/translation/biography/{biography_id}")
def get_biography_translation_biography(biography_id: UUID):
    with engine.begin() as conn:
        biography_translation = (
            biography_service.get_biography_translation_by_biography(conn, biography_id)
        )
        return biography_translation


# ---------------------------------------------------------------------------------------------------- #


@router.get("/biography/meta/{meta_id}")
def get_biography_meta_by_id(meta_id: int):
    try:
        with engine.begin() as conn:
            meta = biography_service.get_biography_meta_by_id(conn, meta_id)
            return meta

    except BiographyMetaNotFound:
        raise HTTPException(
            status_code=404,
            detail="Biography meta not found",
        )


@router.get("/biography/meta/biography/{biography_id}")
def get_biography_meta_by_biography_id(biography_id: UUID):
    with engine.begin() as conn:
        meta = biography_service.get_biography_meta_by_biography_id(conn, biography_id)
        return meta


@router.post("/biography/meta")
def create_biography_meta(meta: BiographyMetaCreate):
    try:
        with engine.begin() as conn:
            biography_service.create_biography_meta(conn, meta)

    except BiographyMetaKeyAlreadyExist:
        raise HTTPException(
            status_code=409,
            detail="Meta key already exists",
        )


@router.put("/biography/meta/{meta_id}")
def update_biography_meta(meta_id: int, meta: BiographyMetaCreate):
    try:
        with engine.begin() as conn:
            biography_service.update_biography_meta(conn, meta_id, meta)

    except BiographyMetaNotFound:
        raise HTTPException(
            status_code=404,
            detail="Biography meta not found",
        )


@router.delete("/biography/meta/{meta_id}")
def delete_biography_meta(meta_id: int):
    try:
        with engine.begin() as conn:
            biography_service.delete_biography_meta(conn, meta_id)

    except BiographyMetaNotFound:
        raise HTTPException(
            status_code=404,
            detail="Biography meta not found",
        )
