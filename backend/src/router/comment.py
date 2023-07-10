from fastapi import APIRouter
from typing import List, Union

from src.database.db_engine import engine
from src.schema.response import ResponseModel
from src.utils.route_function import check_id, route_response, get_route_response
from src.comments.schemas import Comment, CommentCreate
from src.manager import comment_manager

router = APIRouter(
    prefix="/comment",
    tags=["Comment"],
)

# Get all comments
@router.get("", response_model=Union[List[Comment], None])
def get_all_comments():
    with engine.begin() as conn:
        response = list(comment_manager.get_all_comment(conn))
        return get_route_response(response, 200, 404, "No comments found")

# Get comment by id
@router.get("/{comment_id}", response_model=Union[Comment, None])
def get_comment_by_id(comment_id: str):
    check_id(comment_id)
    with engine.begin() as conn:
        response = comment_manager.get_comment_by_id(conn, comment_id)
        return get_route_response(response, 200, 404, "Comment not found")

# # Create comment
# @router.post("", response_model=ResponseModel)
# def create_comment(comment: CommentCreate):
#     with engine.begin() as conn:
#         response = comment_manager.create_comment(conn, comment)
#         return route_response(response, 200, 500)

# Update comment
@router.put("/{comment_id}", response_model=ResponseModel)
def update_comment(comment_id: str, comment: Comment):
    check_id(comment_id)
    with engine.begin() as conn:
        response = comment_manager.update_comment(conn, comment_id, comment)
        return route_response(response, 200, 500)

# Delete comment
@router.delete("/{comment_id}", response_model=ResponseModel)
def delete_comment(comment_id: str):
    check_id(comment_id)
    with engine.begin() as conn:
        response = comment_manager.delete_comment(conn, comment_id)
        return route_response(response, 200, 500)