import sqlalchemy as sa
from fastapi import UploadFile, File
from sqlalchemy.engine import Connection

from .models import image_table
from .schemas import Image, ImageCreate
from ..s3_objects import service as s3_service
from ..users.schemas import User
from ...database import service as db_service


def _parse_row(row: sa.Row):
    return Image(**row._asdict())


def create_image(
    conn: Connection,
    user: User,
    public: bool,
    file: UploadFile = File(...),
) -> Image:
    """
    Create a new image.

    Args:
        user (User): The user creating the partition.
        public (bool): Whether the partition file should be public or not.
        file (UploadFile): The file to upload.

    Returns:
        Image: The created image.
    """
    object = s3_service.upload(file, user, public)

    image = ImageCreate(
        filename=object.filename,
        s3_object_id=object.id,
    )

    result = db_service.create_object(conn, image_table, image.dict(), user_id=user.id)
    return _parse_row(result)
