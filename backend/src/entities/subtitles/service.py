from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.engine import Connection

from src.database import service as db_service
from src.database.db_engine import engine
from .schemas import Subtitle, SubtitleCreate
from ..users.schemas import User
from .models import subtitle_table


def _parse_row(row: sa.Row):
    return Subtitle(**row._asdict())


def create_subtitle(conn: Connection, subtitle: SubtitleCreate, user: User) -> Subtitle:
    """
    Create a new subtitle.

    Args:
        subtitle (SubtitleCreate): The subtitle to create.
        user (User): The user.

    Returns:
        Subtitle: The created subtitle.
    """
    result = db_service.create_object(
        conn, subtitle_table, subtitle.dict(), user_id=user.id
    )
    return _parse_row(result)
