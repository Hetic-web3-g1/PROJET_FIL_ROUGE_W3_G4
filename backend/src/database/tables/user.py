from sqlalchemy import Table, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from datetime import datetime

from database.db_engine import metadata

user_table = Table(
    "user",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4),
    Column("first_name", String(), nullable=False),
    Column("last_name", String(), nullable=False),
    Column("email", String(), unique=True, nullable=False),
    Column("password", String(), nullable=False),
    Column("role", String(), nullable=False),
    Column("academy_id", UUID(as_uuid=True), ForeignKey("academy.id"), nullable=False),
    Column("image_id", UUID(as_uuid=True), nullable=True),
    Column("created_at", DateTime(), default=datetime.utcnow, nullable=False),
    Column("updated_at", DateTime(), nullable=True),
    Column("updated_by", UUID(as_uuid=True), ForeignKey("user.id"), nullable=True)
)

user_tag_table = Table(
    "user_tag",
    metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("user.id"), nullable=False),
    Column("tag_id", Integer, ForeignKey("tag.id"), nullable=False)
)