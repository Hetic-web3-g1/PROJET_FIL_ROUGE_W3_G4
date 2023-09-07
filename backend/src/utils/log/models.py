from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Table, Text

from ...database.db_engine import metadata

log_table = Table(
    "log",
    metadata,
    Column("id", Integer, primary_key=True, unique=True, nullable=False),
    Column("level", String(), nullable=False),
    Column("message", Text(), nullable=False),
    Column("time", DateTime(), default=datetime.utcnow, nullable=False),
    schema="logging",
)
