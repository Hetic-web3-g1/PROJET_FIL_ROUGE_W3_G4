from sqlalchemy import Table, Column, Integer, String, DateTime
from datetime import datetime

from src.database.db_engine import metadata

log_table = Table(
    "log",
    metadata,
    Column("id", Integer, primary_key=True, unique=True, nullable=False),
    Column("level", String(), nullable=False),
    Column("message", String(), nullable=False),
    Column("time", DateTime(), default=datetime.utcnow, nullable=False),
)