from fastapi import APIRouter, HTTPException, Depends, UploadFile, File

from ..users.schemas import User
from . import exceptions as s3_exception
from . import service as upload_service
from src.database.db_engine import engine
from ..authentification import service as auth_service
from ..authentification.dependencies import CustomSecurity

router = APIRouter(
    prefix="/s3_objects",
    tags=["S3_Objects"],
)

from fastapi.responses import JSONResponse


@router.post("/upload/{file_type}")
def upload(
    file_type: str,
    file: UploadFile = File(...),
    user: User = Depends(CustomSecurity()),
):
    try:
        response = upload_service.upload(file_type, file, user)

    except s3_exception.S3Error:
        raise HTTPException(status_code=400, detail="Error during upload")


@router.get("/presigned_url/{object_key}")
def get_presigned_url(object_key: str, user: User = Depends(CustomSecurity())):
    response = upload_service.get_presigned_url(object_key)
    return response


@router.get("/info")
def info(user: User = Depends(CustomSecurity())):
    response = upload_service.info()
    return response
