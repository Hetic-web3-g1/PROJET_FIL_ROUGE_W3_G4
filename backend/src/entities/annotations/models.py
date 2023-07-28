from datetime import datetime

from sqlalchemy import Table, Column, Integer, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID

from ...database.db_engine import metadata

annotation_table = Table(
    "annotation",
    metadata,
    Column("id", Integer, primary_key=True, unique=True, nullable=False),
    Column("measure", Integer, nullable=False),
    Column("content", Text(), nullable=False),
    Column("created_at", DateTime(), default=datetime.utcnow, nullable=False),
    Column("updated_at", DateTime(), onupdate=datetime.utcnow, nullable=True),
    Column("created_by", UUID(as_uuid=True), ForeignKey("user.id"), nullable=False),
    Column("updated_by", UUID(as_uuid=True), ForeignKey("user.id"), nullable=True),
)
