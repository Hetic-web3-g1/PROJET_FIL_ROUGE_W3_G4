from uuid import UUID

from fastapi import APIRouter

from . import service as upload_service

router = APIRouter(
    prefix="/s3_objects",
    tags=["S3_Objects"],
)


@router.get("/url_and_object_info/{s3_object_id}")
def get_presigned_url_and_object_info(s3_object_id: UUID):
    response = upload_service.get_url_and_object_info(s3_object_id)
    return response
