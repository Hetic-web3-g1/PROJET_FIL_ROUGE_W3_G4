from sqlalchemy.types import UUID

from uuid import uuid4
from sqlalchemy import Table, Column, ForeignKey, Integer, String, DateTime, LargeBinary
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from datetime import datetime

import sqlalchemy as sa

from src.database.db_engine import metadata

reset_token = sa.Table(
    "reset_token",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4),
    Column("user_id", UUID(as_uuid=True), ForeignKey("user.id"), nullable=False),
    Column("hash", LargeBinary(), nullable=False),
    Column("expires_at", DateTime(), nullable=False),
)
