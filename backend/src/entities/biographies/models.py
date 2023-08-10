from datetime import datetime
from uuid import uuid4

from sqlalchemy import ARRAY, Column, DateTime, ForeignKey, Integer, String, Table, Text
from sqlalchemy.dialects.postgresql import UUID

from src.database.db_engine import metadata

biography_table = Table(
    "biography",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4),
    Column("first_name", String(), nullable=False),
    Column("last_name", String(), nullable=False),
    Column("instrument", ARRAY(String(), dimensions=1), nullable=True),
    Column("nationality", String(), nullable=True),
    Column("website", String(), nullable=True),
    Column("award", ARRAY(String(), dimensions=1), nullable=True),
    Column("content", Text(), nullable=True),
    Column("type", String(), nullable=False),
    Column("status", String(), nullable=False, default="created"),
    Column("image_id", UUID(as_uuid=True), ForeignKey("image.id"), nullable=True),
    Column("created_at", DateTime(), default=datetime.utcnow, nullable=False),
    Column("updated_at", DateTime(), onupdate=datetime.utcnow, nullable=True),
    Column("created_by", UUID(as_uuid=True), ForeignKey("user.id"), nullable=False),
    Column("updated_by", UUID(as_uuid=True), ForeignKey("user.id"), nullable=True),
)

biography_translation_table = Table(
    "biography_translation",
    metadata,
    Column("id", Integer, primary_key=True, unique=True, nullable=False),
    Column(
        "biography_id", UUID(as_uuid=True), ForeignKey("biography.id"), nullable=False
    ),
    Column("language", String(), nullable=False),
    Column("award", ARRAY(String(), dimensions=1), nullable=True),
    Column("content", Text(), nullable=True),
    Column("status", String(), nullable=False, default="created"),
    Column("created_at", DateTime(), default=datetime.utcnow, nullable=False),
    Column("updated_at", DateTime(), onupdate=datetime.utcnow, nullable=True),
    Column("created_by", UUID(as_uuid=True), ForeignKey("user.id"), nullable=False),
    Column("updated_by", UUID(as_uuid=True), ForeignKey("user.id"), nullable=True),
)

biography_comment_table = Table(
    "biography_comment",
    metadata,
    Column(
        "entity_id",
        UUID(as_uuid=True),
        ForeignKey("biography.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column(
        "comment_id",
        Integer,
        ForeignKey("comment.id", ondelete="CASCADE"),
        nullable=False,
    ),
)

biography_tag_table = Table(
    "biography_tag",
    metadata,
    Column(
        "entity_id",
        UUID(as_uuid=True),
        ForeignKey("biography.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("tag_id", Integer, ForeignKey("tag.id", ondelete="CASCADE"), nullable=False),
)

biography_meta_table = Table(
    "biography_meta",
    metadata,
    Column("id", Integer, primary_key=True, unique=True, nullable=False),
    Column(
        "biography_id", UUID(as_uuid=True), ForeignKey("biography.id"), nullable=False
    ),
    Column("meta_key", String(), nullable=False),
    Column("meta_value", String(), nullable=False),
)
