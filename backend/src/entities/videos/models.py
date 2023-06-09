from sqlalchemy import Table, Column, ForeignKey, Integer, String, Float, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from datetime import datetime

from src.database.db_engine import metadata

video_table = Table(
    "video",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4),
    Column("version", Float(), nullable=False, default=1.0),
    Column("title", String(), nullable=False),
    Column("duration", Float(), nullable=True),
    Column("status", String(), nullable=False, default="created"),
    Column("file_name", String(), nullable=False),
    Column("created_at", DateTime(), default=datetime.utcnow, nullable=False),
    Column("updated_at", DateTime(), onupdate=datetime.utcnow, nullable=True),
    Column("created_by", UUID(as_uuid=True), ForeignKey("user.id"), nullable=False),
    Column("updated_by", UUID(as_uuid=True), ForeignKey("user.id"), nullable=True)
)

video_comment_table = Table(
    "video_comment",
    metadata,
    Column("video_id", UUID(as_uuid=True), ForeignKey("video.id"), nullable=False),
    Column("comment_id", Integer, ForeignKey("comment.id"), nullable=False)
)

video_tag_table = Table(
    "video_tag",
    metadata,
    Column("video_id", UUID(as_uuid=True), ForeignKey("video.id"), nullable=False),
    Column("tag_id", Integer, ForeignKey("tag.id"), nullable=False)
)

video_meta_table = Table(
    "video_meta",
    metadata,
    Column("id", Integer, primary_key=True, unique=True, nullable=False),
    Column("video_id", UUID(as_uuid=True), ForeignKey("video.id"), nullable=False),
    Column("meta_key", String(), nullable=False),
    Column("meta_value", String(), nullable=False)
)