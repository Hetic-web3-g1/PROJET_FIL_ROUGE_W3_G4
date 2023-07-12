from fastapi import HTTPException, UploadFile
from sqlalchemy.engine import Connection
import os, mimetypes, io
from uuid import uuid4

from config import settings
from src.database import service as db_service
from src.database.db_engine import engine
from ..users.models import user_table
# from src.utils.s3 import service as s3_service
from src.utils.s3.s3_engine import s3_client



def file_validation(file: UploadFile) -> None:
    KB = 1000
    MB = KB * KB

    supported_file_types = {
        "image": ["jpg", "jpeg", "png", "svg"],
        "application": ["pdf"]
    }

    if not file:
        raise HTTPException(status_code=400, detail="No file provided")

    if file.file is None:
        raise HTTPException(status_code=400, detail="Invalid file object")

    if file.file.tell() != 0:
        raise HTTPException(status_code=400, detail="File cursor position must be at the start of the file")

    size = file.file.seek(0, 2)  # Get the size of the file using seek()
    file.file.seek(0)  # Reset the file cursor to the start of the file

    if size == 0:
        raise HTTPException(status_code=400, detail="File is empty")

    if size > 10 * MB:
        raise HTTPException(status_code=400, detail=f"File too large, max size is 10MB, this file weight {size} bytes")

    mime_type, _ = mimetypes.guess_type(file.filename)
    if mime_type is None:
        raise HTTPException(status_code=400, detail="File type not supported")

    major_type, minor_type = mime_type.split("/")

    if major_type not in supported_file_types:
        raise HTTPException(status_code=400, detail="File type not supported")

    if minor_type not in supported_file_types[major_type]:
        raise HTTPException(status_code=400, detail="File type not supported")


def upload(file: UploadFile):
    file_validation(file)
    try:

        response = s3_client.upload_fileobj(file.file, settings.bucket_name, file.filename, ExtraArgs={'ACL': 'public-read'})
        object_info = {
            "object_key": file.filename,
            "object": file,
            "object_url": f"https://{settings.bucket_name}.s3.fr-par.scw.cloud/{file.filename}"
        }
        return response
    except Exception as e:
        print(e)
        return {
            "error": str(e)
        }


# def download_object(object_key):
#     try:
#         directory = '/tmp/s3/'
#         os.makedirs(directory, exist_ok=True)  # Create the directory if it doesn't exist

#         file_path = os.path.join(directory, object_key)
#         with open(file_path, 'wb') as file:
#             response = s3_client.download_fileobj(settings.bucket_name, object_key, file)
#         return response
#     except Exception as e:
#         return e

# import io
# import base64

# def download_object(object_key):
#     try:
#         file_obj = io.BytesIO()  # Create an in-memory file-like object

#         # Download the file directly to the file-like object
#         s3_client.download_fileobj(settings.bucket_name, object_key, file_obj)

#         # Set the file-like object's position to the beginning
#         file_obj.seek(0)

#         # Retrieve the contents of the file as bytes
#         file_data = file_obj.read()

#         # Encode the file data as base64
#         encoded_data = base64.b64encode(file_data)

#         return encoded_data
#     except Exception as e:
#         return str(e)

def info():
    response_bucket = s3_client.list_buckets()
    response_object = get_bucket_objects()
    
    return response_bucket['Buckets'], response_object

def get_bucket_objects():
    response = s3_client.list_objects_v2(Bucket=settings.bucket_name)

    if 'Contents' in response:
        return response['Contents']
    else:
        print("No objects found in the bucket")
