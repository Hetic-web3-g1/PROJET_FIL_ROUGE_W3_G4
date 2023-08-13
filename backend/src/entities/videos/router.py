from uuid import UUID

from fastapi import APIRouter, Depends, File, Body, UploadFile, HTTPException

from src.database.db_engine import engine

from ..authentification.dependencies import CustomSecurity
from ..comments.schemas import CommentCreate
from ..users.schemas import User
from .exceptions import VideoNotFound
from . import service as video_service

router = APIRouter(
    prefix="/videos",
    tags=["Videos"],
)


@router.get("/video/{video_id}")
def get_video_by_id(video_id: UUID, user: User = Depends(CustomSecurity())):
    with engine.begin() as conn:
        video = video_service.get_video_by_id(conn, video_id)
        return video


@router.get("/video/masterclass/{masterclass_id}")
def get_videos_by_masterclass_id(
    masterclass_id: UUID, user: User = Depends(CustomSecurity())
):
    with engine.begin() as conn:
        videos = video_service.get_videos_by_masterclass_id(conn, masterclass_id)
        return list(videos)


@router.post("/video")
def create_video(
    masterclass_id: UUID = Body(...),
    duration: int = Body(...),
    version: float = Body(...),
    public: bool = Body(...),
    file: UploadFile = File(...),
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        video_service.create_video(
            conn, user, masterclass_id, duration, version, public, file
        )


@router.delete("/video/{video_id}")
def delete_video(video_id: UUID, user: User = Depends(CustomSecurity())):
    try:
        with engine.begin() as conn:
            video_service.delete_video(conn, video_id)

    except VideoNotFound:
        raise HTTPException(status_code=404, detail="Video not found")


# ---------------------------------------------------------------------------------------------------- #


@router.post("/video/comment/{video_id}")
def create_video_comment(
    comment: CommentCreate, video_id, user: User = Depends(CustomSecurity())
):
    with engine.begin() as conn:
        video_service.create_video_comment(conn, comment, video_id, user)
