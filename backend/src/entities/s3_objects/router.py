from typing import Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Body

from ..users.schemas import User
from . import exceptions as s3_exceptions
from . import service as upload_service
from src.database.db_engine import engine
from ..authentification import service as auth_service
from ..authentification.dependencies import CustomSecurity

router = APIRouter(
    prefix="/s3_objects",
    tags=["S3_Objects"],
)


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


@router.get("/url/{s3_object_id}")
def get_presigned_url(s3_object_id: UUID, user: User = Depends(CustomSecurity())):
    response = upload_service.get_url(s3_object_id)
    return response


@router.get("/info")
def info(user: User = Depends(CustomSecurity())):
    response = upload_service.info()
    return response


@router.get("/info/{s3_object_id}")
def info_object(s3_object_id: str, user: User = Depends(CustomSecurity())):
    response = upload_service.info_object(s3_object_id)
    return response
