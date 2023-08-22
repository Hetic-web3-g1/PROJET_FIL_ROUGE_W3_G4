from fastapi import APIRouter, Depends, File, Body, UploadFile, HTTPException

from src.database.db_engine import engine

from ..authentification.dependencies import CustomSecurity
from ..users.schemas import User
from .exceptions import ImageNotFound
from . import service as image_service

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
