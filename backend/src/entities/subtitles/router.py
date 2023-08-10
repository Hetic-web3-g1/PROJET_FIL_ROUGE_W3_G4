from uuid import UUID

from fastapi import APIRouter, Depends, File, Body, UploadFile, HTTPException

from src.database.db_engine import engine

from ..authentification.dependencies import CustomSecurity
from ..comments.schemas import CommentCreate
from ..users.schemas import User
from .exceptions import SubtitleNotFound
from . import service as subtitle_service

router = APIRouter(
    prefix="/subtitles",
    tags=["Subtitles"],
)


@router.get("/subtitle/{subtitle_id}")
def get_subtitle_by_id(subtitle_id: UUID, user: User = Depends(CustomSecurity())):
    with engine.begin() as conn:
        subtitles = subtitle_service.get_subtitle_by_id(conn, subtitle_id)
        return subtitles


@router.get("/subtitle/video/{video_id}")
def get_subtitles_by_video_id(video_id: UUID, user: User = Depends(CustomSecurity())):
    with engine.begin() as conn:
        subtitles = subtitle_service.get_subtitles_by_video_id(conn, video_id)
        return subtitles


@router.post("/subtitle")
def create_subtitle(
    language: str = Body(...),
    video_id: UUID = Body(...),
    file: UploadFile = File(...),
    public: bool = True,
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        subtitle_service.create_subtitle(conn, user, language, video_id, public, file)


@router.delete("/subtitle/{subtitle_id}")
def delete_subtitle(subtitle_id: UUID, user: User = Depends(CustomSecurity())):
    try:
        with engine.begin() as conn:
            subtitle_service.delete_subtitle(conn, subtitle_id)

    except SubtitleNotFound:
        raise HTTPException(
            status_code=404,
            detail="Subtitle not found",
        )


# ----------------------------------------------------------------------------------------------------


@router.post("/subtitle/comment/{subtitle_id}")
def create_subtitle_comment(
    comment: CommentCreate, subtitle_id, user: User = Depends(CustomSecurity())
):
    with engine.begin() as conn:
        subtitle_service.create_subtitle_comment(conn, comment, subtitle_id, user)
