from typing import Annotated

from fastapi import APIRouter, Query
from src.database.db_engine import engine

from . import service as search_service
from .schemas import Tag

router = APIRouter(
    prefix="/tags",
    tags=["Tags"],
)


@router.get("/search/{search}")
def get_all_tags_by_table(search: str, tables: Annotated[list[str], Query()] = []):
    with engine.begin() as conn:
        response = search_service.get_all_tags_by_table(conn, search, tables)
        return response


@router.get("/get_object_by_tag")
def get_object_by_tag(id: int, content: str, tag_type: str):
    tag = Tag(id=id, content=content, tag_type=tag_type)
    with engine.begin() as conn:
        response = search_service.get_object_by_tag(conn, tag)
        return response
