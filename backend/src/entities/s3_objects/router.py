from typing import Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Body

from ..users.schemas import User
from . import exceptions as s3_exceptions
from . import service as upload_service
from ..authentification.dependencies import CustomSecurity

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


@router.post("/upload/{file_type}")
def upload(
    file_type: str,
    file: UploadFile = File(...),
    user: User = Depends(CustomSecurity()),
    public: bool = Body(...),
    status: Optional[str] = Body(None),
    version: Optional[float] = Body(None),
    video_id: Optional[UUID] = Body(None),
    video_duration: Optional[int] = Body(None),
):
    try:
        upload_service.upload(
            file_type, file, user, public, status, version, video_id, video_duration
        )

    except s3_exceptions.s3Error:
        raise HTTPException(status_code=400, detail="Error during upload")
