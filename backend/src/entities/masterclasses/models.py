from sqlalchemy import Table, Column, ForeignKey, Integer, String, DateTime, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from datetime import datetime

from src.database.db_engine import metadata

masterclass_table = Table(
    "masterclass",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4),
    Column("academy_id", UUID(as_uuid=True), ForeignKey("academy.id"), nullable=False),
    Column("title", String(), nullable=False),
    Column("description", String(), nullable=True),
    Column(
        "teacher_bio_id", UUID(as_uuid=True), ForeignKey("biography.id"), nullable=True
    ),
    Column(
        "composer_bio_id", UUID(as_uuid=True), ForeignKey("biography.id"), nullable=True
    ),
    Column(
        "work_analysis_id",
        UUID(as_uuid=True),
        ForeignKey("work_analysis.id"),
        nullable=True,
    ),
    Column(
        "partition_id", UUID(as_uuid=True), ForeignKey("partition.id"), nullable=True
    ),
    Column("instrument", ARRAY(String()), nullable=True),
    Column("status", String(), nullable=False, default="created"),
    Column("created_at", DateTime(), default=datetime.utcnow, nullable=False),
    Column("updated_at", DateTime(), onupdate=datetime.utcnow, nullable=True),
    Column("created_by", UUID(as_uuid=True), ForeignKey("user.id"), nullable=False),
    Column("updated_by", UUID(as_uuid=True), ForeignKey("user.id"), nullable=True),
)

masterclass_user_table = Table(
    "masterclass_user",
    metadata,
    Column("id", Integer, primary_key=True, unique=True, nullable=False),
    Column("user_id", UUID(as_uuid=True), ForeignKey("user.id"), nullable=False),
    Column(
        "masterclass_id",
        UUID(as_uuid=True),
        ForeignKey("masterclass.id"),
        nullable=False,
    ),
    Column("masterclass_role", String(), nullable=False),
)

masterclass_video_table = Table(
    "masterclass_video",
    metadata,
    Column(
        "masterclass_id",
        UUID(as_uuid=True),
        ForeignKey("masterclass.id"),
        nullable=False,
    ),
    Column("video_id", UUID(as_uuid=True), ForeignKey("video.id"), nullable=False),
)

masterclass_image_table = Table(
    "masterclass_image",
    metadata,
    Column(
        "masterclass_id",
        UUID(as_uuid=True),
        ForeignKey("masterclass.id"),
        nullable=False,
    ),
    Column("image_id", UUID(as_uuid=True), ForeignKey("image.id"), nullable=False),
)

masterclass_comment_table = Table(
    "masterclass_comment",
    metadata,
    Column(
        "masterclass_id",
        UUID(as_uuid=True),
        ForeignKey("masterclass.id"),
        nullable=False,
    ),
    Column("comment_id", Integer, ForeignKey("comment.id"), nullable=False),
)

masterclass_tag_table = Table(
    "masterclass_tag",
    metadata,
    Column(
        "masterclass_id",
        UUID(as_uuid=True),
        ForeignKey("masterclass.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("tag_id", Integer, ForeignKey("tag.id", ondelete="CASCADE"), nullable=False),
)
