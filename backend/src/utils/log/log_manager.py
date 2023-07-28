from typing import Literal

import sqlalchemy as sa
from sqlalchemy.engine import Connection

from ...database.db_engine import metadata, engine
from ...utils.log.log_table import log_table
from ...utils.log.log_schema import LogCreate


def create_log(conn: Connection, log: LogCreate):
    table = metadata.tables["log"]
    stmt = sa.insert(table).values(log.dict()).returning(table)
    return conn.execute(stmt).first()


def log(level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], message: str):
    with engine.begin() as conn:
        log_item = LogCreate(level=level, message=message)
        create_log(conn, log_item)
