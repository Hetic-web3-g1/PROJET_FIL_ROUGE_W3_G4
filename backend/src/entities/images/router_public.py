from uuid import UUID

from fastapi import APIRouter, HTTPException

from src.database.db_engine import engine

from .exceptions import ImageMetaNotFound, ImageMetaKeyAlreadyExist
from . import service as image_service
from .schemas import ImageMetaCreate

router = APIRouter(
    prefix="/images",
    tags=["Images"],
)


@router.get("/image/{image_id}")
def get_image_by_id(image_id: UUID):
    with engine.begin() as conn:
        image = image_service.get_image_by_id(conn, image_id)
        return image


# ---------------------------------------------------------------------------------------------------- #


@router.get("/image/meta/{meta_id}")
def get_image_meta_by_id(meta_id: int):
    try:
        with engine.begin() as conn:
            return image_service.get_image_meta_by_id(conn, meta_id)

    except ImageMetaNotFound:
        raise HTTPException(
            status_code=404,
            detail="Image meta not found",
        )


@router.get("/image/meta/image/{image_id}")
def get_image_meta_by_image_id(image_id: UUID):
    with engine.begin() as conn:
        return image_service.get_image_meta_by_image_id(conn, image_id)


@router.post("/image/meta")
def create_image_meta(meta: ImageMetaCreate):
    try:
        with engine.begin() as conn:
            image_service.create_image_meta(conn, meta)

    except ImageMetaKeyAlreadyExist:
        raise HTTPException(
            status_code=400,
            detail="Image meta key already exists",
        )


@router.put("/image/meta/{meta_id}")
def update_image_meta(meta_id: int, meta: ImageMetaCreate):
    try:
        with engine.begin() as conn:
            return image_service.update_image_meta(conn, meta_id, meta)

    except ImageMetaNotFound:
        raise HTTPException(
            status_code=404,
            detail="Image meta not found",
        )


@router.delete("/image/meta/{meta_id}")
def delete_image_meta(meta_id: int):
    try:
        with engine.begin() as conn:
            image_service.delete_image_meta(conn, meta_id)

    except ImageMetaNotFound:
        raise HTTPException(
            status_code=404,
            detail="Image meta not found",
        )
