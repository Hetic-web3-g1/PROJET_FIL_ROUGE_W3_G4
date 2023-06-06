from fastapi import APIRouter
from typing import List, Union

from database.db_engine import engine
from schema.response import ResponseModel
from utils.route_function import check_id, route_response, get_route_response
from schema.biography import Biography, BiographyCreate, BiographyUpdate
from manager import biography_manager

router = APIRouter(
    prefix="/biography",
    tags=["Biography"],
)

# Get all biographies
@router.get("", response_model=Union[List[Biography], None])
def get_all_biographies():
    with engine.begin() as conn:
        response = list(biography_manager.get_all_biography(conn))
        return get_route_response(response, 200, 404, "No biographies found")

# Get biography by id
@router.get("/{biography_id}", response_model=Union[Biography, None])
def get_biography_by_id(biography_id: str):
    check_id(biography_id)
    with engine.begin() as conn:
        response = biography_manager.get_biography_by_id(conn, biography_id)
        return get_route_response(response, 200, 404, "Biography not found")

# Create biography
@router.post("", response_model=ResponseModel)
def create_biography(biography: BiographyCreate):
    with engine.begin() as conn:
        response = biography_manager.create_biography(conn, biography)
        return route_response(response, 200, 500)

# Update biography
@router.put("/{biography_id}", response_model=ResponseModel)
def update_biography(biography_id: str, biography: BiographyUpdate):
    check_id(biography_id)
    with engine.begin() as conn:
        response = biography_manager.update_biography(conn, biography_id, biography)
        return route_response(response, 200, 500)

# Delete biography
@router.delete("/{biography_id}", response_model=ResponseModel)
def delete_biography(biography_id: str):
    check_id(biography_id)
    with engine.begin() as conn:
        response = biography_manager.delete_biography(conn, biography_id)
        return route_response(response, 200, 500)