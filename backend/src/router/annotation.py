from fastapi import APIRouter
from typing import List, Union

from src.database.db_engine import engine
from src.schema.response import ResponseModel
from src.utils.route_function import check_id, route_response, get_route_response
from src.schema.annotation import Annotation, AnnotationCreate
from src.manager import annotation_manager

router = APIRouter(
    prefix="/annotation",
    tags=["Annotation"],
)

# Get all annotations
@router.get("", response_model=Union[List[Annotation], None])
def get_all_annotations():
    with engine.begin() as conn:
        response = list(annotation_manager.get_all_annotation(conn))
        return get_route_response(response, 200, 404, "No annotations found")

# Get annotation by id
@router.get("/{annotation_id}", response_model=Union[Annotation, None])
def get_annotation_by_id(annotation_id: str):
    check_id(annotation_id)
    with engine.begin() as conn:
        response = annotation_manager.get_annotation_by_id(conn, annotation_id)
        return get_route_response(response, 200, 404, "Annotation not found")

# Create annotation
@router.post("", response_model=ResponseModel)
def create_annotation(annotation: AnnotationCreate):
    with engine.begin() as conn:
        response = annotation_manager.create_annotation(conn, annotation)
        return route_response(response, 200, 500)

# Update annotation
@router.put("/{annotation_id}", response_model=ResponseModel)
def update_annotation(annotation_id: str, annotation: Annotation):
    check_id(annotation_id)
    with engine.begin() as conn:
        response = annotation_manager.update_annotation(conn, annotation_id, annotation)
        return route_response(response, 200, 500)

# Delete annotation
@router.delete("/{annotation_id}", response_model=ResponseModel)
def delete_annotation(annotation_id: str):
    check_id(annotation_id)
    with engine.begin() as conn:
        response = annotation_manager.delete_annotation(conn, annotation_id)
        return route_response(response, 200, 500)