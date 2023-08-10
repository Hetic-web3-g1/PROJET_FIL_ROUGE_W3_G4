import sqlalchemy as sa
from fastapi import File, UploadFile
from sqlalchemy.engine import Connection
from src.database import service as db_service

from ..s3_objects import service as s3_service
from ..users.schemas import User
from .exceptions import ImageNotFound
from .models import image_table
from .schemas import Image, ImageCreate


def _parse_row(row: sa.Row):
    return Image(**row._asdict())


def get_all_images(conn: Connection):
    """
    Get all images.

    Args:
        conn (Connection): The database connection.

    Returns:
        list[Image]: The list of images.
    """
    result = conn.execute(sa.select(image_table)).fetchall()
    for row in result:
        yield _parse_row(row)


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
    object = s3_service.upload(file, user, public, "image")

    image = ImageCreate(
        filename=object.filename,
        s3_object_id=object.id,
    )

    result = db_service.create_object(conn, image_table, image.dict(), user_id=user.id)
    return _parse_row(result)


def delete_image(conn: Connection, image_id: str):
    """
    Delete an image.

    Args:
        image_id (str): The id of the image.

    Raises:
        ImageNotFound: If the image does not exist.
    """
    check = conn.execute(
        sa.select(image_table).where(image_table.c.id == image_id)
    ).first()
    if check is None:
        raise ImageNotFound

    s3_object = s3_service.get_s3_object_by_id(conn, check.s3_object_id)  # type: ignore
    s3_service.delete_object(s3_object.object_key)
    db_service.delete_object(conn, image_table, image_id)
