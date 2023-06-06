from sqlalchemy import Table, Column, Integer, String
from database.db_engine import metadata

tag_table = Table(
    "tag",
    metadata,
    Column("id", Integer, primary_key=True, unique=True, nullable=False),
    Column("content", String(), nullable=False)
)