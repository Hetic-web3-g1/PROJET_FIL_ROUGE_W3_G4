from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    LargeBinary,
    String,
    Table,
)
from sqlalchemy.types import UUID

from src.database.db_engine import metadata

user_table = Table(
    "user",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4),
    Column("first_name", String(), nullable=False),
    Column("last_name", String(), nullable=False),
    Column("email", String(), unique=True, nullable=False),
    Column("password_hash", LargeBinary(), nullable=True),
    Column("salt", LargeBinary(), nullable=True),
    Column("role_id", Integer(), ForeignKey("role.id"), nullable=False),
    Column("academy_id", UUID(as_uuid=True), ForeignKey("academy.id"), nullable=False),
    Column("image_id", UUID(as_uuid=True), nullable=True),
    Column("created_at", DateTime(), default=datetime.utcnow, nullable=False),
    Column("updated_at", DateTime(), onupdate=datetime.utcnow, nullable=True),
    Column("created_by", UUID(as_uuid=True), ForeignKey("user.id"), nullable=True),
    Column("updated_by", UUID(as_uuid=True), ForeignKey("user.id"), nullable=True),
)

user_tag_table = Table(
    "user_tag",
    metadata,
    Column(
        "entity_id",
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("tag_id", Integer, ForeignKey("tag.id", ondelete="CASCADE"), nullable=False),
)
