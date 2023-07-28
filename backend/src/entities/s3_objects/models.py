from datetime import datetime
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Table
from sqlalchemy.dialects.postgresql import UUID

from ...database.db_engine import metadata

s3_object_table = Table(
    "s3_object",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("object_key", String, nullable=False),
    Column("filename", String, nullable=False),
    Column("bucket", String, nullable=False),
    Column("public", Boolean, nullable=False),
    Column("major_type", String, nullable=False),
    Column("minor_type", String, nullable=False),
    Column("created_at", DateTime(), default=datetime.utcnow, nullable=False),
    Column("updated_at", DateTime(), onupdate=datetime.utcnow, nullable=True),
    Column("created_by", UUID(as_uuid=True), ForeignKey("user.id"), nullable=False),
    Column("updated_by", UUID(as_uuid=True), ForeignKey("user.id"), nullable=True),
)
