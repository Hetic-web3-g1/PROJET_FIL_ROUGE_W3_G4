from fastapi import APIRouter
from typing import List, Union

from database.db_engine import engine
from schema.response import ResponseModel
from utils.route_function import check_id, route_response, get_route_response
from schema.user import User, UserCreate, UserUpdate
from manager import user_manager

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post("/academy/{academy_id}/user")
async def create_academy_user(
    academy_id: str,
    
)