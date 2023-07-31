from uuid import uuid4
from datetime import datetime

from sqlalchemy import Table, Column, ForeignKey, Integer, String, Text, DateTime, ARRAY
from sqlalchemy.dialects.postgresql import UUID

from ...database.db_engine import metadata

work_analysis_table = Table(
    "work_analysis",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4),
    Column("title", String(), nullable=False),
    Column("about", Text(), nullable=True),
    Column("learning", ARRAY(String(), dimensions=1), nullable=True),
    Column("content", Text(), nullable=False),
    Column("status", String(), nullable=False, default="created"),
    Column("created_at", DateTime(), default=datetime.utcnow, nullable=False),
    Column("updated_at", DateTime(), onupdate=datetime.utcnow, nullable=True),
    Column("created_by", UUID(as_uuid=True), ForeignKey("user.id"), nullable=False),
    Column("updated_by", UUID(as_uuid=True), ForeignKey("user.id"), nullable=True),
)

work_analysis_translation_table = Table(
    "work_analysis_translation",
    metadata,
    Column("id", Integer, primary_key=True, unique=True, nullable=False),
    Column(
        "work_analysis_id",
        UUID(as_uuid=True),
        ForeignKey("work_analysis.id"),
        nullable=False,
    ),
    Column("language", String(), nullable=False),
    Column("about", Text(), nullable=True),
    Column("learning", ARRAY(String(), dimensions=1), nullable=True),
    Column("content", Text(), nullable=False),
    Column("status", String(), nullable=False, default="created"),
    Column("created_at", DateTime(), default=datetime.utcnow, nullable=False),
    Column("updated_at", DateTime(), onupdate=datetime.utcnow, nullable=True),
    Column("created_by", UUID(as_uuid=True), ForeignKey("user.id"), nullable=False),
    Column("updated_by", UUID(as_uuid=True), ForeignKey("user.id"), nullable=True),
)

work_analysis_comment_table = Table(
    "work_analysis_comment",
    metadata,
    Column(
        "work_analysis_id",
        UUID(as_uuid=True),
        ForeignKey("work_analysis.id"),
        nullable=False,
    ),
    Column("comment_id", Integer, ForeignKey("comment.id"), nullable=False),
)

work_analysis_tag_table = Table(
    "work_analysis_tag",
    metadata,
    Column(
        "entity_id",
        UUID(as_uuid=True),
        ForeignKey("work_analysis.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("tag_id", Integer, ForeignKey("tag.id", ondelete="CASCADE"), nullable=False),
)

work_analysis_meta_table = Table(
    "work_analysis_meta",
    metadata,
    Column("id", Integer, primary_key=True, unique=True, nullable=False),
    Column(
        "work_analysis_id",
        UUID(as_uuid=True),
        ForeignKey("work_analysis.id"),
        nullable=False,
    ),
    Column("meta_key", String(), nullable=False),
    Column("meta_value", String(), nullable=False),
)
