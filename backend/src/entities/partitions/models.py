from sqlalchemy import Table, Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from datetime import datetime

from src.database.db_engine import metadata

partition_table = Table(
    "partition",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4),
    Column("name", String(), nullable=False),
    Column("status", String(), nullable=False, default="created"),
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

partition_annotation_table = Table(
    "partition_annotation",
    metadata,
    Column(
        "partition_id", UUID(as_uuid=True), ForeignKey("partition.id"), nullable=False
    ),
    Column("annotation_id", Integer, ForeignKey("annotation.id"), nullable=False),
)

partition_comment_table = Table(
    "partition_comment",
    metadata,
    Column(
        "partition_id", UUID(as_uuid=True), ForeignKey("partition.id"), nullable=False
    ),
    Column("comment_id", Integer, ForeignKey("comment.id"), nullable=False),
)

partition_tag_table = Table(
    "partition_tag",
    metadata,
    Column(
        "partition_id", UUID(as_uuid=True), ForeignKey("partition.id"), nullable=False
    ),
    Column("tag_id", Integer, ForeignKey("tag.id"), nullable=False),
)

partition_meta_table = Table(
    "partition_meta",
    metadata,
    Column("id", Integer, primary_key=True, unique=True, nullable=False),
    Column(
        "partition_id", UUID(as_uuid=True), ForeignKey("partition.id"), nullable=False
    ),
    Column("meta_key", String(), nullable=False),
    Column("meta_value", String(), nullable=False),
)
