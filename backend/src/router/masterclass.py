from fastapi import APIRouter
from typing import List, Union

from database.db_engine import engine
from schema.response import ResponseModel
from utils.route_function import check_id, route_response, get_route_response
from schema.masterclass import Masterclass, MasterclassCreate, MasterclassUpdate
from manager import masterclass_manager

router = APIRouter(
    prefix="/masterclass",
    tags=["Masterclass"],
)

# Get all masterclasses
@router.get("", response_model=Union[List[Masterclass], None])
def get_all_masterclasses():
    with engine.begin() as conn:
        response = list(masterclass_manager.get_all_masterclass(conn))
        return get_route_response(response, 200, 404, "No masterclasses found")

# Get masterclass by id
@router.get("/{masterclass_id}", response_model=Union[Masterclass, None])
def get_masterclass_by_id(masterclass_id: str):
    check_id(masterclass_id)
    with engine.begin() as conn:
        response = masterclass_manager.get_masterclass_by_id(conn, masterclass_id)
        return get_route_response(response, 200, 404, "Masterclass not found")

# Create masterclass
@router.post("", response_model=ResponseModel)
def create_masterclass(masterclass: MasterclassCreate):
    with engine.begin() as conn:
        response = masterclass_manager.create_masterclass(conn, masterclass)
        return route_response(response, 200, 500)

# Update masterclass
@router.put("/{masterclass_id}", response_model=ResponseModel)
def update_masterclass(masterclass_id: str, masterclass: MasterclassUpdate):
    check_id(masterclass_id)
    with engine.begin() as conn:
        response = masterclass_manager.update_masterclass(conn, masterclass_id, masterclass)
        return route_response(response, 200, 500)

# Delete masterclass
@router.delete("/{masterclass_id}", response_model=ResponseModel)
def delete_masterclass(masterclass_id: str):
    check_id(masterclass_id)
    with engine.begin() as conn:
        response = masterclass_manager.delete_masterclass(conn, masterclass_id)
        return route_response(response, 200, 500)