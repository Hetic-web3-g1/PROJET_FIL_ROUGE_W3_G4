from fastapi import APIRouter
from typing import List, Union

from database.db_engine import engine
from schema.response import ResponseModel
from utils.route_function import check_id, route_response, get_route_response
from schema.user import User, UserCreate, UserUpdate
from manager import user_manager

router = APIRouter(
    prefix="/user",
    tags=["User"],
)

# Get all users
@router.get("", response_model=Union[List[User], None])
def get_all_users():
    with engine.begin() as conn:
        response = list(user_manager.get_all_user(conn))
        return get_route_response(response, 200, 404, "No users found")

# Get user by id
@router.get("/{user_id}", response_model=Union[User, None])
def get_user_by_id(user_id: str):
    check_id(user_id)
    with engine.begin() as conn:
        response = user_manager.get_user_by_id(conn, user_id)
        return get_route_response(response, 200, 404, "User not found")
    
# Create user
@router.post("", response_model=ResponseModel)
def create_user(user: UserCreate):
    with engine.begin() as conn:
        response = user_manager.create_user(conn, user)
        return route_response(response, 200, 500) # Dev
        return route_response(response, 200, 500, success_message="User created successfully." ,error_message="Failed to create user. Please check your request.")

# Update user
@router.put("/{user_id}", response_model=ResponseModel)
def update_user(user_id: str, user: UserUpdate):
    check_id(user_id)
    with engine.begin() as conn:
        response = user_manager.update_user(conn, user_id, user)
        return route_response(response, 200, 500) # Dev
        return route_response(response, 200, 500, success_message="User updated successfully.", error_message="Failed to update user. Please check your request.")

# Delete user
@router.delete("/{user_id}", response_model=ResponseModel)
def delete_user(user_id: str):
    check_id(user_id)
    with engine.begin() as conn:
        response = user_manager.delete_user(conn, user_id)
        return route_response(response, 200, 500) # Dev
        return route_response(response, 200, 500, success_message="User deleted successfully.", error_message="Failed to delete user. Please check your request.")