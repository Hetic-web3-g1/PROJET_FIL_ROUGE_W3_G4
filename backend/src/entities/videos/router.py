from fastapi import APIRouter, Depends, File, Body, UploadFile

from src.database.db_engine import engine

from ..authentification.dependencies import CustomSecurity
from ..comments.schemas import CommentCreate
from ..users.schemas import User
from . import service as video_service

router = APIRouter(
    prefix="/videos",
    tags=["Videos"],
)


@router.post("/video")
def create_video(
    duration: int = Body(...),
    version: float = Body(...),
    public: bool = Body(...),
    file: UploadFile = File(...),
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        video_service.create_video(conn, user, duration, version, public, file)


# ---------------------------------------------------------------------------------------------------- #


@router.post("/video/comment/{video_id}")
def create_video_comment(
    comment: CommentCreate, video_id, user: User = Depends(CustomSecurity())
):
    with engine.begin() as conn:
        video_service.create_video_comment(conn, comment, video_id, user)
