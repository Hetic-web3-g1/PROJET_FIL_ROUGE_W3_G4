from typing import List

from fastapi import APIRouter, Body, Depends

from src.database.db_engine import engine

from ..authentification.dependencies import CustomSecurity
from ..users.schemas import User
from . import service as search_service
from .schemas import Tag

router = APIRouter(
    prefix="/tags",
    tags=["Tags"],
)


@router.get("/search/{search}&{tables}")
def get_all_tags_by_table(
    search: str,
    tables: str,
    user: User = Depends(CustomSecurity()),
):
    tables = tables.split(",")    
    with engine.begin() as conn:
        response = search_service.get_all_tags_by_table(conn, search, tables)
        return response


@router.get("/get_object_by_tag")
def get_object_by_tag(
    tag: Tag,
    user: User = Depends(CustomSecurity()),
):
    with engine.begin() as conn:
        response = search_service.get_object_by_tag(conn, tag)
        return response
