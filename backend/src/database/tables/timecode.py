from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.dialects.postgresql import UUID

from src.database.db_engine import metadata

timecode_table = Table(
    "timecode",
    metadata,
    Column("id", Integer, primary_key=True, unique=True, nullable=False),
    Column("video_id", UUID(as_uuid=True), ForeignKey("video.id"), nullable=False),
    Column("hour", Integer, nullable=True),
    Column("minute", Integer, nullable=True),
    Column("second", Integer, nullable=True),
    Column("frame", Integer, nullable=True),
)
