from fastapi import UploadFile
from uuid import uuid4
import os

import sqlalchemy as sa
from sqlalchemy.engine.base import Connection

from config import settings
from src.database import service as db_service
from src.database.db_engine import engine
from src.utils.s3.s3_engine import s3_client
from .schemas import S3Object, S3ObjectCreate
from ..users.schemas import User
from .models import s3_object_table
from ..users.models import user_table
from . import dependencies as s3_dependencies


def _parse_row(row: sa.Row):
    return S3Object(**row._asdict())


def create_s3_object(conn: Connection, s3_object: S3ObjectCreate, user: User):
    """
    Create a new s3_object.

    Args:
        s3_object (S3ObjectCreate): The s3_object to create.
        user (User): The user who created the masterclass.

    Returns:
        S3Object: The created s3_object.
    """
    result = db_service.create_object(
        conn, s3_object_table, s3_object.dict(), user_id=user.id
    )
    return _parse_row(result)


def upload(file: UploadFile, user: User):
    """
    Upload a file to S3.

    Args:
        file (UploadFile): The file to upload.

    Returns:
        dict: The response from S3.
    """
    s3_dependencies.file_validation(file)
    file_type = s3_dependencies.check_mimetype(file)

    s3_object = S3ObjectCreate(
        object_key=str(uuid4()),
        original_filename=file.filename,
        bucket=settings.bucket_name,
        public=True,
        major_type=file_type[0],
        minor_type=file_type[1],
    )

    try:
        response = s3_client.upload_fileobj(
            file.file,
            settings.bucket_name,
            s3_object.object_key,
            ExtraArgs={"ACL": "public-read"},
        )
        create_s3_object(engine.connect(), s3_object, user)
        return response
    except Exception as e:
        return {"error": str(e)}


def get_presigned_url(object_key):
    """
    Get presigned url.

    Args:
        file (UploadFile): The file to upload.

    Returns:
        str: The presigned url.
    """
    config = os.getenv("CONFIG_NAME")

    if config == "development":
        url = "http://localhost:{port}/{bucket}/{key}".format(
            hostname=settings.s3_hostname,
            port=settings.s3_port,
            bucket=settings.bucket_name,
            key=object_key,
        )
    else:
        url = s3_dependencies.create_presigned_url(settings.bucket_name, object_key)
    return url


# def info():
#     response_bucket = s3_client.list_buckets()
#     response_object = get_bucket_objects()

#     return response_bucket["Buckets"], response_object


# def get_bucket_objects():
#     response = s3_client.list_objects_v2(Bucket=settings.bucket_name)

#     if "Contents" in response:
#         return response["Contents"]
#     else:
#         print("No objects found in the bucket")
