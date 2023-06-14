from fastapi import APIRouter
from typing import List, Union

from src.database.db_engine import engine
from src.schema.response import ResponseModel
from src.utils.route_function import check_id, route_response, get_route_response
from src.schema.tag import Tag, TagCreate
from src.manager import tag_manager

router = APIRouter(
    prefix="/tag",
    tags=["Tag"],
)

# Get all tags
@router.get("", response_model=Union[List[Tag], None])
def get_all_tags():
    with engine.begin() as conn:
        response = list(tag_manager.get_all_tag(conn))
        return get_route_response(response, 200, 404, "No tags found")

# Get tag by id
@router.get("/{tag_id}", response_model=Union[Tag, None])
def get_tag_by_id(tag_id: str):
    check_id(tag_id)
    with engine.begin() as conn:
        response = tag_manager.get_tag_by_id(conn, tag_id)
        return get_route_response(response, 200, 404, "Tag not found")

# Create tag
@router.post("", response_model=ResponseModel)
def create_tag(tag: TagCreate):
    with engine.begin() as conn:
        response = tag_manager.create_tag(conn, tag)
        return route_response(response, 200, 500)

# Update tag
@router.put("/{tag_id}", response_model=ResponseModel)
def update_tag(tag_id: str, tag: Tag):
    check_id(tag_id)
    with engine.begin() as conn:
        response = tag_manager.update_tag(conn, tag_id, tag)
        return route_response(response, 200, 500)

# Delete tag
@router.delete("/{tag_id}", response_model=ResponseModel)
def delete_tag(tag_id: str):
    check_id(tag_id)
    with engine.begin() as conn:
        response = tag_manager.delete_tag(conn, tag_id)
        return route_response(response, 200, 500)