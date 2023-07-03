from typing import Literal

import sqlalchemy as sa
from sqlalchemy.engine import Connection

from src.database.db_engine_log import metadata_log, engine_log
from src.utils.log.log_schema import LogCreate


def create_log(conn: Connection, log: LogCreate):
    table = metadata_log.tables["log"]
    stmt = sa.insert(table).values(log.dict()).returning(table)
    return conn.execute(stmt).first()


def log(level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], message: str):
    with engine_log.begin() as conn:
        log_item = LogCreate(level=level, message=message)
        create_log(conn, log_item)
