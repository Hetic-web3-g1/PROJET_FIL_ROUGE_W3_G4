from fastapi import APIRouter
from typing import List, Union

from database.db_engine import engine
from schema.response import ResponseModel
from utils.route_function import check_id, route_response, get_route_response
from schema.academy import Academy, AcademyCreate, AcademyUpdate
from manager import academy_manager

router = APIRouter(
    prefix="/academy",
    tags=["Academy"],
)

# Get all academies
@router.get("", response_model=Union[List[Academy], None])
def get_all_academies():
    with engine.begin() as conn:
        response = list(academy_manager.get_all_academy(conn))
        return get_route_response(response, 200, 404, "No academies found")

# Get academy by id
@router.get("/{academy_id}", response_model=Union[Academy, None])
def get_academy_by_id(academy_id: str):
    check_id(academy_id)
    with engine.begin() as conn:
        response = academy_manager.get_academy_by_id(conn, academy_id)
        return get_route_response(response, 200, 404, "Academy not found")

# Create academy
@router.post("", response_model=ResponseModel)
def create_academy(academy: AcademyCreate):
    with engine.begin() as conn:
        response = academy_manager.create_academy(conn, academy)
        return route_response(response, 200, 500)

# Update academy
@router.put("/{academy_id}", response_model=ResponseModel)
def update_academy(academy_id: str, academy: AcademyUpdate):
    check_id(academy_id)
    with engine.begin() as conn:
        response = academy_manager.update_academy(conn, academy_id, academy)
        return route_response(response, 200, 500)

# Delete academy
@router.delete("/{academy_id}", response_model=ResponseModel)
def delete_academy(academy_id: str):
    check_id(academy_id)
    with engine.begin() as conn:
        response = academy_manager.delete_academy(conn, academy_id)
        return route_response(response, 200, 500)
