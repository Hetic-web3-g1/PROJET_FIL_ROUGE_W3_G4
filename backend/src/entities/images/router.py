from uuid import UUID

from fastapi import APIRouter, Depends, File, Body, UploadFile, HTTPException

from src.database.db_engine import engine

from ..authentification.dependencies import CustomSecurity
from ..users.schemas import User
from .exceptions import ImageNotFound, ImageMetaNotFound, ImageMetaKeyAlreadyExist
from . import service as image_service
from .schemas import ImageMetaCreate

router = APIRouter(
    prefix="/images",
    tags=["Images"],
)


@router.post("/image")
def create_image(
    public: bool = Body(...),
    file: UploadFile = File(...),
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        return image_service.create_image(conn, user, public, file)


@router.delete("/image/{image_id}")
def delete_image(image_id: str, user: User = Depends(CustomSecurity())):
    try:
        with engine.begin() as conn:
            image_service.delete_image(conn, image_id)

    except ImageNotFound:
        raise HTTPException(
            status_code=404,
            detail="Image not found",
        )


# ---------------------------------------------------------------------------------------------------- #


@router.get("/image/meta/{meta_id}")
def get_image_meta_by_id(meta_id: int, user: User = Depends(CustomSecurity())):
    try:
        with engine.begin() as conn:
            return image_service.get_image_meta_by_id(conn, meta_id)

    except ImageMetaNotFound:
        raise HTTPException(
            status_code=404,
            detail="Image meta not found",
        )


@router.get("/image/meta/image/{image_id}")
def get_image_meta_by_image_id(image_id: UUID, user: User = Depends(CustomSecurity())):
    with engine.begin() as conn:
        return image_service.get_image_meta_by_image_id(conn, image_id)


@router.post("/image/meta")
def create_image_meta(meta: ImageMetaCreate, user: User = Depends(CustomSecurity())):
    try:
        with engine.begin() as conn:
            image_service.create_image_meta(conn, meta)

    except ImageMetaKeyAlreadyExist:
        raise HTTPException(
            status_code=400,
            detail="Image meta key already exists",
        )


@router.put("/image/meta/{meta_id}")
def update_image_meta(
    meta_id: int, meta: ImageMetaCreate, user: User = Depends(CustomSecurity())
):
    try:
        with engine.begin() as conn:
            return image_service.update_image_meta(conn, meta_id, meta)

    except ImageMetaNotFound:
        raise HTTPException(
            status_code=404,
            detail="Image meta not found",
        )


@router.delete("/image/meta/{meta_id}")
def delete_image_meta(meta_id: int, user: User = Depends(CustomSecurity())):
    try:
        with engine.begin() as conn:
            image_service.delete_image_meta(conn, meta_id)

    except ImageMetaNotFound:
        raise HTTPException(
            status_code=404,
            detail="Image meta not found",
        )
