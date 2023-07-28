from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy import Column, ForeignKey, DateTime, LargeBinary
from sqlalchemy.dialects.postgresql import UUID

from src.database.db_engine import metadata


reset_token = sa.Table(
    "reset_token",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4),
    Column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
    ),
    Column("hash", LargeBinary(), nullable=False),
    Column("expires_at", DateTime(), nullable=False),
)
