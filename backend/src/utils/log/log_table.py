from sqlalchemy import Table, Column, Integer, String, DateTime
from datetime import datetime

from src.database.db_engine_log import metadata_log, engine_log

log_table = Table(
    "log",
    metadata_log,
    Column("id", Integer, primary_key=True, unique=True, nullable=False),
    Column("level", String(), nullable=False),
    Column("message", String(), nullable=False),
    Column("timestamp", DateTime(), default=datetime.utcnow, nullable=False),
)
