from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.database.db_engine import engine

from ..authentification.dependencies import CustomSecurity
from ..users.schemas import User
from .exceptions import CommentNotFound
from . import service as comment_service
from .schemas import CommentCreate

router = APIRouter(
    prefix="/comments",
    tags=["Comments"],
)

from ..videos.models import video_table, video_comment_table


@router.get("/comment/{object_id}")
def get_comments_by_object_id(
    object_id: UUID,
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        comments = comment_service.get_comment_by_object_id(
            conn, object_id, video_table, video_comment_table
        )
        return comments


@router.put("/comment/{comment_id}")
def update_comment(
    comment_id: int,
    comment: CommentCreate,
    user: User = Depends(CustomSecurity()),
):
    try:
        with engine.begin() as conn:
            comment_service.update_comment(conn, comment_id, comment, user)

    except CommentNotFound:
        raise HTTPException(
            status_code=404,
            detail="Comment not found",
        )


@router.delete("/comment/{comment_id}")
def delete_comment(
    comment_id: int,
    user: User = Depends(CustomSecurity()),
):
    try:
        with engine.begin() as conn:
            comment_service.delete_comment(conn, comment_id)

    except CommentNotFound:
        raise HTTPException(
            status_code=404,
            detail="Comment not found",
        )
