from typing import List

from fastapi import APIRouter, Depends, Body

from . import service as search_service
from .schemas import Tag
from ..authentification.dependencies import CustomSecurity
from ..users.schemas import User
from ...database.db_engine import engine

router = APIRouter(
    prefix="/tags",
    tags=["Tags"],
)


@router.get("/search/{search}")
def search_by_table(
    search: str,
    tables: List[str] = Body(...),
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        response = search_service.search_by_table(conn, search, tables)
        return response


@router.get("/search_object_by_tag")
def search_object_by_tag(
    tag: Tag,
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        response = search_service.search_object_by_tag(conn, tag)
        return response
