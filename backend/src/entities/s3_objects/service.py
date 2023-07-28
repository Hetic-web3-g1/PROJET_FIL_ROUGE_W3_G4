import os
from typing import Optional
from uuid import uuid4, UUID

import sqlalchemy as sa
from fastapi import UploadFile
from sqlalchemy.engine import Connection

from . import dependencies as s3_dependencies
from .exceptions import s3Error, s3ObjectNotFound
from .models import s3_object_table
from .schemas import S3Object, S3ObjectCreate
from ..users.schemas import User
from ...database import service as db_service
from ...database.db_engine import engine
from ...database.s3_engine import s3_client
from config import settings


def _parse_row(row: sa.Row):
    return S3Object(**row._asdict())


def get_all_buckets_and_all_s3_objects():
    """
    Get all buckets and objects from S3.

    Returns:
        dict: The buckets and objects.
    """
    response_bucket = s3_client.list_buckets()
    response_object = s3_client.list_objects_v2(Bucket=settings.bucket_name)

    return response_bucket["Buckets"], response_object


def get_s3_object_by_id(conn: Connection, s3_object_id: UUID) -> S3Object:
    """
    Get a s3_object by its id.

    Args:
        s3_object_id (UUID): The s3_object id.

    Returns:
        S3Object: The s3_object.
    """
    result = conn.execute(
        sa.select(s3_object_table).where(s3_object_table.c.id == s3_object_id)
    ).first()
    if result is None:
        raise s3ObjectNotFound
    return _parse_row(result)


def get_s3_object_by_object_key(conn: Connection, object_key: str) -> S3Object:
    """
    Get a s3_object by its object_key.

    Args:
        object_key (str): The s3_object object_key.

    Returns:
        S3Object: The s3_object.
    """
    result = conn.execute(
        sa.select(s3_object_table).where(s3_object_table.c.object_key == object_key)
    ).first()
    if result is None:
        raise s3ObjectNotFound
    return _parse_row(result)


def get_url(s3_object: S3Object):
    """
    Get presigned url.

    Args:
        object_key (str): The object_key of the file.

    Returns:
        str: The presigned url.
    """
    with engine.begin() as conn:
        s3_object = get_s3_object_by_id(conn, s3_object.id)

    if s3_object.public is False:
        url = s3_dependencies.create_presigned_url(
            settings.bucket_name, s3_object.object_key
        )
        if os.getenv("CONFIG_NAME") == "development":
            url = str(url).replace("http://s3", "http://localhost")

    else:
        url = "http://{hostname}:{port}/{bucket}/{key}".format(
            hostname="localhost"
            if os.getenv("CONFIG_NAME") == "development"
            else settings.s3_hostname,
            port=settings.s3_port,
            bucket=settings.bucket_name,
            key=s3_object.object_key,
        )
    return url


def get_object_info(object_key: str):
    """
    Get object info.

    Args:
        object_key (str): The object_key of the file.

    Returns:
        dict: The object info.
    """
    response = s3_client.head_object(Bucket=settings.bucket_name, Key=object_key)
    return response


def get_url_and_object_info(s3_object_id: UUID):
    """
    Get presigned url and object info.

    Args:
        object_key (str): The object_key of the file.

    Returns:
        dict: The presigned url and object info.
    """
    with engine.begin() as conn:
        s3_object = get_s3_object_by_id(conn, s3_object_id)

    url = get_url(s3_object)
    object_info = get_object_info(s3_object.object_key)
    return {"url": url, "object_info": object_info}


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


def upload(
    file: UploadFile,
    user: User,
    public: bool,
    status: Optional[str] = None,
    version: Optional[float] = None,
    video_id: Optional[UUID] = None,
    video_duration: Optional[float] = None,
):
    """
    Upload a file to S3.

    Args:
        file (UploadFile): The file to upload.
        user (User): The user who uploaded the file.
        public (bool): If the file is public or not.
        status (str): The status of the file.
        version (float): The version of the file.
        video_id (UUID): The video id.
        video_duration (float): The duration of the video.

    Exceptions:
        s3Error: If the file is not valid.

    Returns:
        dict: The response from S3 and the created s3_object.
    """
    type = s3_dependencies.file_validation(file)

    s3_object = S3ObjectCreate(
        object_key=str(uuid4()),
        filename=file.filename,  # type: ignore
        bucket=settings.bucket_name,
        public=True,
        major_type=type[0],
        minor_type=type[1],
    )

    # metadata = {
    #     "filename": file.filename,
    #     "public": str(public),
    #     "major_type": type[0],
    #     "minor_type": type[1],
    # }

    if public is False:
        response = s3_client.upload_fileobj(
            file.file,
            settings.bucket_name,
            s3_object.object_key,
            ExtraArgs={
                "ContentDisposition": f'attachment; filename="{file.filename}"',
            },
        )
    else:
        response = s3_client.upload_fileobj(
            file.file,
            settings.bucket_name,
            s3_object.object_key,
            # ExtraArgs={"ACL": "public-read", "Metadata": metadata},
            ExtraArgs={
                "ACL": "public-read",
                "ContentDisposition": f'attachment; filename="{file.filename}"',
            },
        )
    result = create_s3_object(s3_object, user)

    if response is not None:
        raise s3Error
    print(result)
    return result
