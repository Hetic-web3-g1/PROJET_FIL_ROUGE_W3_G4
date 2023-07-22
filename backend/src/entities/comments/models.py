from datetime import datetime

from sqlalchemy import Table, Column, ForeignKey, Integer, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID

from src.database.db_engine import metadata


comment_table = Table(
    "comment",
    metadata,
    Column("id", Integer, primary_key=True, unique=True, nullable=False),
    Column("content", Text(), nullable=False),
    Column("created_at", DateTime(), default=datetime.utcnow, nullable=False),
    Column("updated_at", DateTime(), onupdate=datetime.utcnow, nullable=True),
    Column("created_by", UUID(as_uuid=True), ForeignKey("user.id"), nullable=False),
    Column("updated_by", UUID(as_uuid=True), ForeignKey("user.id"), nullable=True),
)
