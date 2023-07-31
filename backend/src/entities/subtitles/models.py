from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.dialects.postgresql import UUID
from ...database.db_engine import metadata

subtitle_table = Table(
    "subtitle",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4),
    Column("filename", String(), nullable=False),
    Column("language", String(), nullable=False),
    Column("status", String(), nullable=False, default="created"),
    Column("video_id", UUID(as_uuid=True), ForeignKey("video.id"), nullable=False),
    Column(
        "s3_object_id",
        UUID(as_uuid=True),
        ForeignKey("s3_object.id"),
        nullable=False,
    ),
    Column("created_at", DateTime(), default=datetime.utcnow, nullable=False),
    Column("updated_at", DateTime(), onupdate=datetime.utcnow, nullable=True),
    Column("created_by", UUID(as_uuid=True), ForeignKey("user.id"), nullable=False),
    Column("updated_by", UUID(as_uuid=True), ForeignKey("user.id"), nullable=True),
)

subtitle_comment_table = Table(
    "subtitle_comment",
    metadata,
    Column(
        "subtitle_id", UUID(as_uuid=True), ForeignKey("subtitle.id"), nullable=False
    ),
    Column("comment_id", Integer, ForeignKey("comment.id"), nullable=False),
)

subtitle_tag_table = Table(
    "subtitle_tag",
    metadata,
    Column(
        "entity_id",
        UUID(as_uuid=True),
        ForeignKey("subtitle.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("tag_id", Integer, ForeignKey("tag.id", ondelete="CASCADE"), nullable=False),
)
