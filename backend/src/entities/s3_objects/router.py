from fastapi import APIRouter, Depends, UploadFile, File

from . import service as upload_service
from ..users.schemas import User
from src.database.db_engine import engine
from ..authentification import service as auth_service
from ..authentification.dependencies import CustomSecurity

router = APIRouter(
    prefix="/s3_objects",
    tags=["S3_Objects"],
)

from fastapi.responses import JSONResponse


@router.post("/upload")
async def upload(file: UploadFile = File(...), user: User = Depends(CustomSecurity())):
    response = upload_service.upload(file, user)
    if isinstance(response, dict) and "error" in response:
        return JSONResponse(content=response, status_code=400)
    return response


@router.get("/presigned_url/{file_name}")
def get_presigned_url(object_key: str, user: User = Depends(CustomSecurity())):
    response = upload_service.get_presigned_url(object_key)
    return response
