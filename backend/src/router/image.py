from fastapi import APIRouter
from typing import List, Union

from src.database.db_engine import engine
from src.schema.response import ResponseModel
from src.utils.route_function import check_id, route_response, get_route_response
from src.schema.image import Image, ImageCreate
from src.manager import image_manager

router = APIRouter(
    prefix="/image",
    tags=["Image"],
)

# Get all images
@router.get("", response_model=Union[List[Image], None])
def get_all_images():
    with engine.begin() as conn:
        response = list(image_manager.get_all_image(conn))
        return get_route_response(response, 200, 404, "No images found")

# Get image by id
@router.get("/{image_id}", response_model=Union[Image, None])
def get_image_by_id(image_id: str):
    check_id(image_id)
    with engine.begin() as conn:
        response = image_manager.get_image_by_id(conn, image_id)
        return get_route_response(response, 200, 404, "Image not found")

# Create image
@router.post("", response_model=ResponseModel)
def create_image(image: ImageCreate):
    with engine.begin() as conn:
        response = image_manager.create_image(conn, image)
        return route_response(response, 200, 500)

# Update image
@router.put("/{image_id}", response_model=ResponseModel)
def update_image(image_id: str, image: Image):
    check_id(image_id)
    with engine.begin() as conn:
        response = image_manager.update_image(conn, image_id, image)
        return route_response(response, 200, 500)

# Delete image
@router.delete("/{image_id}", response_model=ResponseModel)
def delete_image(image_id: str):
    check_id(image_id)
    with engine.begin() as conn:
        response = image_manager.delete_image(conn, image_id)
        return route_response(response, 200, 500)