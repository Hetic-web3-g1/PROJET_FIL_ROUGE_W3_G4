from datetime import datetime
from uuid import uuid4

from sqlalchemy import Table, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from ...database.db_engine import metadata

image_table = Table(
    "image",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4),
    Column("name", String(), nullable=False),
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

image_meta_table = Table(
    "image_meta",
    metadata,
    Column("id", Integer, primary_key=True, unique=True, nullable=False),
    Column("image_id", UUID(as_uuid=True), ForeignKey("image.id"), nullable=False),
    Column("meta_key", String(), nullable=False),
    Column("meta_value", String(), nullable=False),
)
