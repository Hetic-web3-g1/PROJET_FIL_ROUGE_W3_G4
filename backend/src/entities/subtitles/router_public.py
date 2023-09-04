from uuid import UUID

from fastapi import APIRouter

from src.database.db_engine import engine

from . import service as subtitle_service

router = APIRouter(
    prefix="/subtitles",
    tags=["Subtitles"],
)


@router.get("/subtitle/{subtitle_id}")
def get_subtitle_by_id(subtitle_id: UUID):
    with engine.begin() as conn:
        subtitles = subtitle_service.get_subtitle_by_id(conn, subtitle_id)
        return subtitles


@router.get("/subtitle/masterclass/{masterclass_id}")
def get_subtitles_by_masterclass_id(masterclass_id: UUID):
    with engine.begin() as conn:
        subtitles = subtitle_service.get_subtitles_by_masterclass_id(
            conn, masterclass_id
        )
        return subtitles
