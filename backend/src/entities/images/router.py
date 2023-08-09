from fastapi import APIRouter, Depends, File, Body, UploadFile

from src.database.db_engine import engine

from ..authentification.dependencies import CustomSecurity
from ..users.schemas import User
from . import service as image_service

router = APIRouter(
    prefix="/images",
    tags=["images"],
)


@router.post("/image")
def create_image(
    public: bool = Body(...),
    file: UploadFile = File(...),
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        return image_service.create_image(conn, user, public, file)
