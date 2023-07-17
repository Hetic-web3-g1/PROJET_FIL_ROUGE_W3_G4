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
from . import exceptions as s3_exceptions
from ..users.schemas import User
from .models import s3_object_table
from . import dependencies as s3_dependencies
from .exceptions import s3Error


def _parse_row(row: sa.Row):
    return S3Object(**row._asdict())


def create_s3_object(s3_object: S3ObjectCreate, user: User):
    """
    Create a new s3_object.

    Args:
        s3_object (S3ObjectCreate): The s3_object to create.
        user (User): The user who created the masterclass.

    Returns:
        S3Object: The created s3_object.
    """
    with engine.begin() as conn:
        result = db_service.create_object(
            conn, s3_object_table, s3_object.dict(), user_id=user.id
        )
    return _parse_row(result)


def upload(file_type, file: UploadFile, user: User):
    """
    Upload a file to S3.

    Args:
        file_type (str): The type of the file to upload: image, video, partition.
        file (UploadFile): The file to upload.
        user (User): The user who uploaded the file.

    Exceptions:
        s3Error: If the file is not valid.

    Returns:
        dict: The response from S3 and the created s3_object.
    """
    type = s3_dependencies.file_validation(file)

    s3_object = S3ObjectCreate(
        object_key=str(uuid4()),
        filename=file.filename,
        bucket=settings.bucket_name,
        public=True,
        major_type=type[0],
        minor_type=type[1],
    )

    response = s3_client.upload_fileobj(
        file.file,
        settings.bucket_name,
        s3_object.object_key,
        ExtraArgs={"ACL": "public-read"},
    )
    result = create_s3_object(s3_object, user)

    match file_type:
        case "image":
            pass
        case "video":
            pass
        case "partition":
            pass
        case "subtitle":
            pass
        case _:
            return "No corresponding file type was provided."

    if response is not None:
        raise s3Error

    return response, result


def get_presigned_url(object_key):
    """
    Get presigned url.

    Args:
        file (UploadFile): The file to upload.

    Returns:
        str: The presigned url.
    """
    config = os.getenv("CONFIG_NAME")

    # Todo: Change is not using presigned url
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


def info():
    response_bucket = s3_client.list_buckets()
    response_object = s3_client.list_objects_v2(Bucket=settings.bucket_name)

    if "Contents" in response_object:
        return response_object["Contents"]
    else:
        print("No objects found in the bucket")

    return response_bucket["Buckets"], response_object
