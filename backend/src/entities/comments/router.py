from uuid import UUID

from fastapi import APIRouter, Depends

from src.database.db_engine import engine

from ..authentification.dependencies import CustomSecurity
from ..users.schemas import User
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
    print("hello")
    with engine.begin() as conn:
        comments = comment_service.get_comment_by_object_id(
            conn, object_id, video_table, video_comment_table
        )
        return comments
