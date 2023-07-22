from sqlalchemy import Table, Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from src.database.db_engine import metadata

tag_table = Table(
    "tag",
    metadata,
    Column("id", Integer, primary_key=True, unique=True, nullable=False),
    Column("content", String(), nullable=False),
    Column("tag_type", String(), nullable=False),
)
