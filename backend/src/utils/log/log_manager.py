import sqlalchemy as sa
from sqlalchemy.engine import Connection
from utils.log import log_table 

from database.db_engine_log import metadata_log, engine_log
from utils.log.log_schema import LogCreate

def create_log(conn: Connection, log: LogCreate):
    table = metadata_log.tables['log']
    stmt = sa.insert(table).values(log.dict()).returning(table)
    return conn.execute(stmt).first()

def log(level, message):
    authorized_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    level = level.upper()
    if level not in authorized_levels:
        log("WARNING", f"Invalid log level: {level}")
        return
    
    with engine_log.begin() as conn:
        log_item = LogCreate(level=level, message=message)
        create_log(conn, log_item)