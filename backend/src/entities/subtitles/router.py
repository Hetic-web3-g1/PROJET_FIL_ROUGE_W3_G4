from uuid import UUID

from fastapi import APIRouter, Depends, File, Body, UploadFile

from src.database.db_engine import engine

from ..authentification.dependencies import CustomSecurity
from ..comments.schemas import CommentCreate
from ..users.schemas import User
from . import service as subtitle_service

router = APIRouter(
    prefix="/subtitles",
    tags=["Subtitles"],
)


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


# ----------------------------------------------------------------------------------------------------


@router.post("/subtitle/comment/{subtitle_id}")
def create_subtitle_comment(
    comment: CommentCreate, subtitle_id, user: User = Depends(CustomSecurity())
):
    with engine.begin() as conn:
        subtitle_service.create_subtitle_comment(conn, comment, subtitle_id, user)
