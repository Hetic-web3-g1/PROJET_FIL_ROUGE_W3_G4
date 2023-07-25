from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.engine import Connection

from src.database import service as db_service
from .schemas import Image, ImageCreate
from ..users.schemas import User
from .models import image_table


def _parse_row(row: sa.Row):
    return Image(**row._asdict())


def create_image(conn: Connection, image: ImageCreate, user: User) -> Image:
    """
    Create a new image.

    Args:
        image (ImageCreate): The image to create.
        user (User): The user.

    Returns:
        Image: The created image.
    """
    result = db_service.create_object(conn, image_table, image.dict(), user_id=user.id)
    return _parse_row(result)
