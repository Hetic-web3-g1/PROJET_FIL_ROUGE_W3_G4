from uuid import uuid4
from datetime import datetime

from sqlalchemy.types import UUID
from sqlalchemy import Table, Column, String, DateTime

from src.database.db_engine import metadata


academy_table = Table(
    "academy",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, unique=True, default=uuid4),
    Column("name", String(), nullable=False),
    Column("created_at", DateTime(), default=datetime.utcnow, nullable=False),
    Column("updated_at", DateTime(), onupdate=datetime.utcnow, nullable=True),
)