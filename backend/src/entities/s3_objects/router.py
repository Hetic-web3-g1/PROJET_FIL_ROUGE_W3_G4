from uuid import UUID

from fastapi import APIRouter, Depends

from . import service as upload_service
from ..authentification.dependencies import CustomSecurity
from ..users.schemas import User

router = APIRouter(
    prefix="/s3_objects",
    tags=["S3_Objects"],
)


@router.get("/buckets_and_s3_objects")
def info(user: User = Depends(CustomSecurity())):
    response = upload_service.get_all_buckets_and_all_s3_objects()
    return response


@router.get("/url_and_object_info/{s3_object_id}")
def get_presigned_url_and_object_info(
    s3_object_id: UUID, user: User = Depends(CustomSecurity())
):
    response = upload_service.get_url_and_object_info(s3_object_id)
    return response
