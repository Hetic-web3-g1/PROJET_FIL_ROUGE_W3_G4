from uuid import UUID

import sqlalchemy as sa
from fastapi import File, UploadFile
from sqlalchemy.engine import Connection
from src.database import service as db_service

from ..s3_objects import service as s3_service
from ..users.schemas import User
from .exceptions import ImageNotFound, ImageMetaNotFound, ImageMetaKeyAlreadyExist
from .models import image_table, image_meta_table
from .schemas import Image, ImageCreate, ImageMeta, ImageMetaCreate


def _parse_row(row: sa.Row):
    return Image(**row._asdict())


def _parse_meta_row(row: sa.Row):
    return ImageMeta(**row._asdict())


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


def get_image_by_id(conn: Connection, image_id: UUID) -> Image:
    """
    Get an image by the given id.

    Args:
        image_id (UUID): The id of the image.

    Raises:
        ImageNotFound: If the image does not exist.

    Returns:
        Image: The image object.
    """
    result = conn.execute(
        sa.select(image_table).where(image_table.c.id == image_id)
    ).first()
    if result is None:
        raise ImageNotFound

    return _parse_row(result)


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


# ---------------------------------------------------------------------------------------------------- #


def get_image_meta_by_id(conn: Connection, meta_id: int) -> ImageMeta:
    """
    Get a meta entry by the given id.

    Args:
        meta_id (int): The id of the meta entry.

    Raises:
        ImageMetaNotFound: If the meta entry does not exist.

    Returns:
        ImageMeta: The ImageMeta object.
    """
    result = conn.execute(
        sa.select(image_meta_table).where(image_meta_table.c.id == meta_id)
    ).first()
    if result is None:
        raise ImageMetaNotFound

    return _parse_meta_row(result)


def get_image_meta_by_image_id(conn: Connection, image_id: UUID) -> list[ImageMeta]:
    """
    Get all meta entries for an image.

    Args:
        image_id (UUID): The id of the image.

    Returns:
        list[ImageMeta]: The list of ImageMeta objects.
    """
    result = conn.execute(
        sa.select(image_meta_table).where(image_meta_table.c.image_id == image_id)
    ).fetchall()

    return [_parse_meta_row(row) for row in result]


def create_image_meta(conn: Connection, meta: ImageMetaCreate) -> ImageMeta:
    """
    Create a meta entry for an image.

    Args:
        meta (ImageMetaCreate): The ImageMetaCreate object.

    Raises:
        ImageMetaKeyAlreadyExist: If the meta entry already exists.

    Returns:
        ImageMeta: The created ImageMeta object.
    """
    check = conn.execute(
        sa.select(image_meta_table).where(
            image_meta_table.c.meta_key == meta.meta_key,
        )
    ).first()
    if check is not None:
        raise ImageMetaKeyAlreadyExist

    result = db_service.create_object(conn, image_meta_table, meta.dict())

    return _parse_meta_row(result)


def update_image_meta(
    conn: Connection, meta_id: int, meta: ImageMetaCreate
) -> ImageMeta:
    """
    Update a meta entry.

    Args:
        meta_id (int): The id of the meta entry.
        meta (ImageMetaCreate): The ImageMetaCreate object.

    Raises:
        ImageMetaKeyAlreadyExists: If the meta entry already exists.

    Returns:
        ImageMeta: The updated ImageMeta object.
    """
    check = conn.execute(
        sa.select(image_meta_table).where(image_meta_table.c.id == meta_id)
    ).first()
    if check is None:
        raise ImageMetaNotFound

    result = db_service.update_object(conn, image_meta_table, meta_id, meta.dict())

    return _parse_meta_row(result)


def delete_image_meta(conn: Connection, meta_id: int) -> None:
    """
    Delete a meta entry.

    Args:
        meta_id (int): The id of the meta entry.

    Raises:
        ImageMetaNotFound: If the meta entry does not exist.
    """
    check = conn.execute(
        sa.select(image_meta_table).where(image_meta_table.c.id == meta_id)
    ).first()
    if check is None:
        raise ImageMetaNotFound

    db_service.delete_object(conn, image_meta_table, meta_id)
