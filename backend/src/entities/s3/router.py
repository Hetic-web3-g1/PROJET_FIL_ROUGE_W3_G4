from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
import mimetypes

from . import service as upload_service
from ..users.schemas import User
from src.database.db_engine import engine
from ..authentification import service as auth_service
from ..authentification.dependencies import CustomSecurity

router = APIRouter(
    prefix="/s3",
    tags=["s3"],
)

from fastapi.responses import JSONResponse

# Upload file
@router.post("/upload")
async def upload(
    file: UploadFile = File(...),
    # user: User = Depends(CustomSecurity())
):
    response = upload_service.upload(file)
    if isinstance(response, dict) and "error" in response:
        return JSONResponse(content=response, status_code=400)
    return response

# Get file
@router.get("/get/{file_name}")
def get_file(file_name: str):
    response = upload_service.download_object(file_name)
    return response


# Get info
@router.get("/info")
def get_info():
    response = upload_service.info()
    return response